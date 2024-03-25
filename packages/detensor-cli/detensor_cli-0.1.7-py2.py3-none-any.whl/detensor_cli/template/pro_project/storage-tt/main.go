package main

import (
	"embed"
	"fmt"
	"io/fs"
	"net/http"
	"os"
	"strings"
	"time"

	"buaa.edu.cn/storage/chain"
	"buaa.edu.cn/storage/chain/chainmaker"
	"buaa.edu.cn/storage/controller/core"
	ginzap "github.com/gin-contrib/zap"
	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
	"go.uber.org/zap"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

//go:embed swagger/*
var swaggerContent embed.FS

const DB_WAIT_TIME_DURATION = 5
const DB_CONNECT_TIMES = 30

const CHAIN_WAIT_TIME_DURATION = 5
const CHAIN_CONNECT_TIMES = 5

func buildIChain(logger *zap.Logger) chain.IChain {
	configPath := viper.GetString("chain.chainmaker.sdk_config")
	contractName := viper.GetString("chain.chainmaker.contract_name")
	if contractName == "" {
		panic("can't find chain.chainmaker.contract_name")
	}
	logger.Info("chain config",
		zap.String("sdk_config_path", configPath),
		zap.String("contract_name", contractName),
	)
	times := CHAIN_CONNECT_TIMES
	for times > 0 {
		ret, err := chainmaker.NewChainMakerModel(contractName, configPath)
		if err != nil {
			logger.Error("build blockchain model failed: ", zap.String("msg", err.Error()))
			logger.Info("build blockchain model failed, sleep and retry")
			time.Sleep(time.Second * CHAIN_WAIT_TIME_DURATION)
			times -= 1
			continue
		}
		return ret
	}
	logger.Fatal("build blockchain model failed, time out")
	return nil
}

func getDB(logger *zap.Logger) (db *gorm.DB, err error) {

	addr := viper.GetString("db.addr")
	port := viper.GetInt("db.port")
	name := viper.GetString("db.database")
	user := viper.GetString("db.user")
	password := viper.GetString("db.password")
	logger.Info("[init] db init",
		zap.String("addr", addr),
		zap.Int("port", port),
		zap.String("user", user),
		zap.String("database", name),
	)

	dsn := fmt.Sprintf(
		"%s:%s@tcp(%s:%d)/%s?charset=utf8mb4&parseTime=True&loc=Local",
		user,
		password,
		addr,
		port,
		name,
	)

	Db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
	errCount := 0
	for err != nil {
		errCount += 1
		logger.Error("open failed in GetDB", zap.String("error", err.Error()))
		time.Sleep(time.Duration(DB_WAIT_TIME_DURATION) * time.Second)
		Db, err = gorm.Open(mysql.Open(dsn), &gorm.Config{})
		if errCount == DB_CONNECT_TIMES {
			return Db, err
		}

	}
	return Db, err
}

func setupViper(configPath string) error {
	viper.SetConfigFile(configPath)
	viper.SetEnvPrefix("STORAGE")
	viper.SetEnvKeyReplacer(strings.NewReplacer(".", "__"))
	viper.AutomaticEnv()

	viper.SetDefault("addr", "127.0.0.1:8080")
	viper.SetDefault("chain.chainmaker.sdk_config", "./sdk_config.yml")

	return viper.ReadInConfig()
}

// @title storage API
// @version 0.1
// @description storage API是储存层的对象储存API

// @contact.name bravomikekilo
// @contact.email bravomikekilo@buaa.edu.cn
// @BasePath /api
func main() {
	println("hello world")

	logger, err := zap.NewDevelopment()
	if err != nil {
		panic("init logger failed")
	}

	configPath := os.Getenv("STORAGE_CONFIG_PATH")
	if configPath == "" {
		configPath = "./config.yaml"
	}

	if err := setupViper(configPath); err != nil {
		panic("init viper failed: " + err.Error())
	}

	addr := viper.GetString("addr")
	fmt.Printf("listen on addr %s\n", addr)

	r := gin.New()
	r.Use(ginzap.Ginzap(logger, time.RFC3339, true))
	r.SetTrustedProxies(nil)

	coreV1Group := r.Group("/api/core/v1")
	execV1Group := r.Group("/api/exec/v1")

	chain := buildIChain(logger)
	db, err := getDB(logger)
	if err != nil {
		panic("get db failed: " + err.Error())
	}

	err = core.RegisterCoreControllerV1(coreV1Group, logger, chain, db)

	if err != nil {
		panic("core v1 controller init failed: " + err.Error())
	}

	err = core.RegisterExecControllerV1(execV1Group, logger, chain, db)
	if err != nil {
		panic("exec v1 controller init failed: " + err.Error())
	}

	staticGroup := r.Group("/swagger")

	swaggerFS, _ := fs.Sub(swaggerContent, "swagger")
	staticGroup.StaticFS("/", http.FS(swaggerFS))

	r.Run(addr)
}
