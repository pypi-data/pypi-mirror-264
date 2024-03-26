//go:build !debug

package core

import "github.com/gin-gonic/gin"

/// 设置CoreV1 控制器的Debug功能.
//  这是生产版本的代码, 所以这个函数是一个空函数
func SetupDebug(g *gin.RouterGroup, ctl *CoreControllerV1) {
	ctl.logger.Info("prod environment")
}
