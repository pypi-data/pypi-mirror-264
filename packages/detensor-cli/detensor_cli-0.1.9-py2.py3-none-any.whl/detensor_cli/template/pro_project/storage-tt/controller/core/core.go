// 这个文件放置 core/v1 控制器的相关代码
package core

import (
	"buaa.edu.cn/storage/chain"
	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
	"gorm.io/gorm"
)

const (
	VERSION_CORE_V1 = "core/v1"
)

type CoreControllerV1 struct {
	logger *zap.Logger
	chain  chain.IChain
	db     *gorm.DB
}

func RegisterCoreControllerV1(g *gin.RouterGroup, logger *zap.Logger, chain chain.IChain, db *gorm.DB) error {

	ctl := &CoreControllerV1{
		logger: logger,
		chain:  chain,
		db:     db,
	}

	nodeCtl := NewNodeController(chain)

	// 注册Nodes API的路由
	nodeCtl.RegisterRoute(g.Group("nodes"))

	// 提议相关API
	g.POST("/namespace/:namespace/proposal", ctl.CreateProposal)
	g.DELETE("/namespace/:namespace/proposal/:name", ctl.RevokeProposalByName)
	g.PUT("/namespace/:namespace/proposal/:name/permission", ctl.PermitProposalByName)
	g.DELETE("/namespace/:namespace/proposal/:name/permission", ctl.DenyProposalByName)
	g.PUT("/namespace/:namespace/proposal/:name/commit", ctl.CommitProposalByName)

	g.PUT("/proposal/:uid/permission", ctl.PermitProposalByUID)
	g.DELETE("/proposal/:uid/permission", ctl.DenyProposalByUID)
	g.DELETE("/proposal/:uid", ctl.RevokeProposalByUID)
	g.PUT("/proposal/:uid/commit", ctl.CommitProposalByUID)

	// 全局提议相关API
	g.POST("/globalproposal", ctl.CreateGlobalProposal)
	g.PUT("/globalproposal/:name/permission", ctl.PermitGlobalProposal)
	g.DELETE("/globalproposal/:name/permission", ctl.DenyGlobalProposal)
	g.DELETE("/globalproposal/:name/", ctl.RevokeGlobalProposal)
	g.PUT("/globalproposal/:name/commit", ctl.CommitGlobalProposal)

	// 数据声明实现相关API
	g.PUT("/namespace/:namespace/datadeclare/:name/implementation",
		ctl.AddDataImplementByName,
	)
	g.DELETE("/namespace/:namespace/datadeclare/:name/implementation",
		ctl.RemoveDataImplementByName,
	)
	g.PUT("/datadeclare/:uid/implementation", ctl.AddDataImplement)
	g.DELETE("/datadeclare/:uid/implementation", ctl.RemoveDataImplement)

	// 函数声明实现相关API
	g.PUT("/namespace/:namespace/functiondeclare/:name/implementation",
		ctl.AddFunctionImplementByName,
	)
	g.DELETE("/namespace/:namespace/functiondeclare/:name/implementation",
		ctl.RemoveFunctionImplementByName,
	)
	g.PUT("/functiondeclare/:uid/implementation", ctl.AddFunctionImplement)
	g.DELETE("/functiondeclare/:uid/implementation", ctl.RemoveFunctionImplement)

	// 私有数据相关API
	g.POST("/data", ctl.CreateData)
	g.GET("/data", ctl.FindData)
	g.GET("/data/:name", ctl.FindDataByName)
	g.DELETE("/data/:name", ctl.DeleteDataByName)
	g.PUT("/data/:name", ctl.PutData)

	// 私有数据绑定相关API
	g.POST("/databinding", ctl.CreateDataBinding)
	g.GET("/databinding", ctl.FindDataBinding)
	g.GET("/databinding/:name", ctl.FindDataBindingByName)
	g.DELETE("/databinding/:name", ctl.DeleteDataByName)
	g.PUT("/databinding/:name", ctl.PutDataBinding)

	// 私有函数相关API
	g.POST("/function", ctl.CreateFunc)
	g.GET("/function", ctl.FindFunc)
	g.GET("/function/:name", ctl.FindFuncByName)
	g.DELETE("/function/:name", ctl.DeleteFuncByName)
	g.PUT("/function/:name", ctl.PutFunc)

	// 私有函数绑定相关API
	g.POST("/functionbinding", ctl.CreateFuncBinding)
	g.GET("/functionbinding", ctl.FindFuncBinding)
	g.GET("/functionbinding/:name", ctl.FindFuncBindingByName)
	g.DELETE("/functionbinding/:name", ctl.DeleteFuncBindingByName)
	g.PUT("/functionbinding/:name", ctl.PutFuncBinding)

	// 对象API
	g.GET("/namespace/:namespace/", ctl.GetNamespaceByName)
	g.GET("/namespace/:namespace/:kind", ctl.GetObjectByKind)
	g.GET("/namespace/:namespace/:kind/:name", ctl.GetObjectByName)
	g.GET("/object/:uid", ctl.GetObjectByUid)
	g.GET("/:kind/:name", ctl.GetGlobalObjectByName)
	g.GET("/:kind", ctl.GetAllObjectByKind)

	g.POST("/exec/:uid")

	// 设置调试相关HTTP接口
	SetupDebug(g, ctl)

	// 实现声明相关 API
	// g.POST("/setdatadeclare", ctl.SetDataImplement)

	return nil
}
