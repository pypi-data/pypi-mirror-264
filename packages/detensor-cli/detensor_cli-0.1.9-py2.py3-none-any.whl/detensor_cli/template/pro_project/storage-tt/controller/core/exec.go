package core

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os/exec"
	"strings"
	"time"

	"buaa.edu.cn/storage/chain"
	"github.com/gin-gonic/gin"
	"github.com/golang/groupcache/lru"
	"github.com/spf13/viper"
	"go.uber.org/zap"
	"golang.org/x/sync/singleflight"
	"gorm.io/gorm"
)

type ExecControllV1 struct {
	logger       *zap.Logger
	chain        chain.IChain
	db           *gorm.DB
	compilerCmds []string
	cache        *lru.Cache
	single       *singleflight.Group
}

type ExecReq struct {
	ContractUid uint64   `json:"uid"`
	Orgs        []string `json:"orgs"`
	Compile     bool     `json:"compile,omitempty"`
}

type ExecRes struct {
	ByteCode  *string           `json:"bytecode,omitempty"`
	Data      map[string]string `json:"data"`
	Functions map[string]string `json:"functions"`
}

func RegisterExecControllerV1(g *gin.RouterGroup, logger *zap.Logger, chain chain.IChain, db *gorm.DB) error {

	cmds := viper.GetViper().GetStringSlice("compiler.cmds")
	logger.Info(
		"Exec Controller, compiler cmds",
		zap.Strings("commands", cmds),
	)

	ctl := &ExecControllV1{
		logger:       logger,
		chain:        chain,
		db:           db,
		compilerCmds: cmds,
		cache:        lru.New(20),
		single:       &singleflight.Group{},
	}

	g.POST("/", ctl.GetExec)
	g.POST("/contract", ctl.GetContract)

	return nil
}

func (ctl *ExecControllV1) GetContract(c *gin.Context) {
	req := &ExecReq{}
	if err := c.ShouldBind(&req); err != nil {
		c.JSON(http.StatusBadRequest, "parse request failed: "+err.Error())
		return
	}

	obj, err := ctl.chain.GetContract(req.ContractUid)
	if err != nil {
		c.JSON(http.StatusInternalServerError, "find contract by uid failed: "+err.Error())
		return
	}

	c.JSON(http.StatusOK, obj)
}

type DataResult struct {
	Uid     uint64
	Content string
}

func (ctl *ExecControllV1) FindData(contractID uint64, declares map[string]uint64) (map[string]string, error) {
	dataUids := []uint64{}
	ret := map[string]string{}
	for _, v := range declares {
		dataUids = append(dataUids, v)
	}

	SQL := `SELECT binding.data_declare_uid as uid, model.content as content
		FROM data_binding_models as binding
		INNER JOIN data_models as model
		ON binding.data_uid = model.id
		WHERE binding.contract_uid = ?
		AND binding.data_declare_uid IN ? 
		AND model.available is TRUE 
		AND binding.available is TRUE
	`
	results := []DataResult{}
	err := ctl.db.Raw(SQL, contractID, dataUids).Scan(&results).Error
	if err != nil {
		return nil, err
	}

	for k, uid := range declares {
		for _, v := range results {
			if v.Uid == uid {
				var value int64
				var key string
				_, err := fmt.Sscanf(v.Content, "%s %d", &key, &value)
				if err != nil {
					panic(err)
				}
				data := map[string]interface{}{
					"V": map[string]interface{}{
						key: value,
					},
				}
				result, _ := json.Marshal(data)

				ret[k] = string(result)
			}
		}
	}

	return ret, nil
}

type FunctionResult struct {
	Uid     uint64
	Content string
}

func (ctl *ExecControllV1) FindFunction(contractID uint64, declares map[string]uint64) (map[string]string, error) {
	funcUids := []uint64{}
	ret := map[string]string{}
	for _, v := range declares {
		funcUids = append(funcUids, v)
	}

	SQL := `SELECT binding.function_declare_uid as uid, model.content as content
		FROM function_binding_models as binding
		INNER JOIN function_models as model
		ON binding.function_uid = model.id
		WHERE binding.contract_uid = ?
		AND binding.function_declare_uid IN ?
		AND model.available IS TRUE 
		AND binding.available IS TRUE
	`
	results := []FunctionResult{}
	err := ctl.db.Raw(SQL, contractID, funcUids).Scan(&results).Error
	if err != nil {
		return nil, err
	}

	for k, uid := range declares {
		for _, v := range results {
			if v.Uid == uid {
				ret[k] = v.Content
			}
		}
	}
	return ret, nil
}

func (ctl *ExecControllV1) Compile(uid uint64, content string) ([]byte, error) {
	stderr := new(bytes.Buffer)
	stdout := new(bytes.Buffer)

	var cmd *exec.Cmd = nil
	if len(ctl.compilerCmds) == 1 {
		cmd = exec.Command(ctl.compilerCmds[0])
	} else {
		cmd = exec.Command(ctl.compilerCmds[0], ctl.compilerCmds[1:]...)
	}

	cmd.Stdin = strings.NewReader(content)
	cmd.Stderr = stderr
	cmd.Stdout = stdout
	timer := time.NewTimer(time.Second * 10)

	cpChan := make(chan error)
	go func() {
		cpChan <- cmd.Run()
	}()

	fail := false
	select {
	case <-timer.C:
		cmd.Process.Kill()
		ctl.logger.Info("compile timeout, contract",
			zap.Uint64("uid", uid),
		)
		fail = true
	case <-cpChan:
		ctl.logger.Info("compile success, contract ",
			zap.Uint64("uid", uid),
		)
		fail = cmd.ProcessState.ExitCode() != 0
	}

	if fail {
		out, err := ioutil.ReadAll(stderr)
		if err != nil {
			return nil, fmt.Errorf("read compiler error failed: %w", err)
		}
		return nil, fmt.Errorf("compile error: " + string(out))
	}

	out, err := ioutil.ReadAll(stdout)
	if err != nil {
		return nil, fmt.Errorf("read compiler output failed: " + err.Error())
	}

	return out, nil
}

func (ctl *ExecControllV1) GetExec(c *gin.Context) {
	req := &ExecReq{}

	if err := c.ShouldBind(&req); err != nil {
		c.JSON(http.StatusBadRequest, "parse request failed: "+err.Error())
		return
	}

	obj, err := ctl.chain.GetContract(req.ContractUid)
	if err != nil {
		ctl.logger.Error("find contract by uid failed", zap.Error(err))
		c.JSON(http.StatusInternalServerError, "find contract by uid failed: "+err.Error())
		return
	}

	if obj == nil {
		c.JSON(http.StatusNotFound, "contract not found")
		return
	}

	found := false
	for _, pattern := range obj.Spec.ExecPatterns {
		if len(pattern) != len(req.Orgs) {
			continue
		}
		for i, r := range req.Orgs {
			if pattern[i] != r {
				continue
			}
		}
		found = true
		break
	}

	if !found {
		c.JSON(http.StatusUnauthorized, "invalid exec pattern")
		return
	}

	// var bytecode *string = nil

	// if req.Compile {
	// 	var cache interface{} = nil
	// 	cache, ok := ctl.cache.Get(req.ContractUid)
	// 	if !ok {

	// 		key := strconv.Itoa(int(req.ContractUid))
	// 		cache, err, _ = ctl.single.Do(key, func() (interface{}, error) {
	// 			// out, err := ctl.Compile(req.ContractUid, obj.Spec.Content)
	// 			// if err == nil {
	// 			// 	ctl.cache.Add(req.ContractUid, out)
	// 			// }
	// 			out := obj.Spec.Content
	// 			ctl.cache.Add(req.ContractUid, out)
	// 			return out, err
	// 		})
	// 	}
	// 	out, ok := cache.([]byte)
	// 	if !ok {
	// 		panic("logic error")
	// 	}
	// 	if err != nil {
	// 		c.JSON(http.StatusInternalServerError, "compile contract failed: "+err.Error())
	// 		return
	// 	}
	// 	base64bytecode := base64.RawStdEncoding.EncodeToString(out)
	// 	bytecode = &base64bytecode
	// }

	data, err := ctl.FindData(req.ContractUid, obj.Data)
	if err != nil {
		c.JSON(http.StatusInternalServerError, "query data failed")
		return
	}

	functions, err := ctl.FindFunction(req.ContractUid, obj.Function)
	if err != nil {
		c.JSON(http.StatusInternalServerError, "query function failed")
		return
	}

	res := &ExecRes{
		ByteCode:  &obj.Spec.Content,
		Data:      data,
		Functions: functions,
	}

	c.JSON(http.StatusOK, res)
}
