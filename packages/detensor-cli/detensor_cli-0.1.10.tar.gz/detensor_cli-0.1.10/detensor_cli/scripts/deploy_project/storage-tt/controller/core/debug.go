//go:build debug

// 这个文件放置 core/v1 控制器调试功能的相关代码
package core

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// reInitDB 初始化数据库状态
func (ctl *CoreControllerV1) reInitDB() error {
	return nil
}

// reInitChain 初始化区块链状态
func (ctl *CoreControllerV1) reInitChain() error {
	err := ctl.chain.ReInit()
	if err != nil {
		return err
	}
	return nil
}

// 设置CoreV1 控制器的Debug功能.
// 这是测试版本的代码, 所以这个函数具有实际功能
func SetupDebug(g *gin.RouterGroup, ctl *CoreControllerV1) {
	ctl.logger.Info("setup debug interface")
	g.DELETE("/debug", ctl.ReInit)
	g.DELETE("/debug/chain", ctl.ReInitChain)
	g.DELETE("/debug/db", ctl.ReInitDB)
	g.GET("/debug/nextuid", ctl.NextUid)
}

// ReInitChain 初始化区块链状态, 用于调试
func (ctl *CoreControllerV1) ReInitChain(c *gin.Context) {
	ctl.logger.Info("ReInit system state, debug only!!")
	err := ctl.reInitChain()
	if err != nil {
		c.String(http.StatusInternalServerError, "reinit chain failed %s", err.Error())
		return
	}
	c.String(http.StatusOK, "ok")
	return
}

func (ctl *CoreControllerV1) ReInitDB(c *gin.Context) {
	ctl.logger.Info("ReInit database state, debug only!!")
	err := ctl.reInitDB()
	if err != nil {
		c.String(http.StatusInternalServerError, "reinit database failed %s", err.Error())
		return
	}
	c.String(http.StatusOK, "ok")
	return
}

// ReInit 初始化系统状态接口, 用于调试
func (ctl *CoreControllerV1) ReInit(c *gin.Context) {
	ctl.logger.Info("ReInit system state, debug only!!")
	err := ctl.reInitChain()
	if err != nil {
		c.String(http.StatusInternalServerError, "reinit chain failed %s", err.Error())
		return
	}

	err = ctl.reInitDB()
	if err != nil {
		c.String(http.StatusInternalServerError, "reinit db failed %s", err.Error())
		return
	}

	c.String(http.StatusOK, "ok")
	return
}

// NextUid 查询链上下一个Uid, 用于调试
func (ctl *CoreControllerV1) NextUid(c *gin.Context) {
	ctl.logger.Info("fetch NextUid, debug only!!")
	uid, err := ctl.chain.NextUid()
	if err != nil {
		c.String(http.StatusInternalServerError, "get nextuid failed %s", err.Error())
		return
	} else {
		c.String(http.StatusOK, "%d", uid)
		return
	}
}
