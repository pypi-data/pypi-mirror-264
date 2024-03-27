package core

import (
	"net/http"

	"buaa.edu.cn/storage/chain"
	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
)

type NodeController struct {
	// 链的实现
	chain  chain.IChain
	logger *zap.Logger
}

func NewNodeController(chain chain.IChain) *NodeController {
	return &NodeController{
		chain: chain,
	}
}

// RegisterRoute 将NodeController的handler绑定到对应的路由上
func (ctl *NodeController) RegisterRoute(group *gin.RouterGroup) {

	// 获取节点的地址
	group.GET("/", ctl.DiscoverNode)

	// 更新本组织计算节点的地址
	group.POST("/", ctl.RegisterNode)

	// 删除本组织计算节点的地址
	group.DELETE("/", ctl.LogoutNode)

	group.GET("/org", ctl.GetNodeByOrg)
}

// 注册节点的请求
type RegisterNodeReq struct {
	// 计算节点的地址
	Addr string `json:"addr"`
}

// RegisterNode 将计算节点的地址注册到组织名下
// @Summary 计算节点地址注册
// @Description 调用链上合约, 将计算节点地址注册到本组织名下
// @Tags Node 节点
// @Accept application/json
// @Produce application/json
// @Param data body RegisterNodeReq true "注册节点的请求"
// @Success 200 "节点注册成功"
// @Router /core/v1/nodes [post]
func (ctl *NodeController) RegisterNode(ctx *gin.Context) {
	req := RegisterNodeReq{}
	if err := ctx.ShouldBindJSON(&req); err != nil {
		ctx.JSON(http.StatusBadRequest, "parse body failed: "+err.Error())
		return
	}

	err := ctl.chain.RegisterNode(req.Addr)
	if err != nil {
		ctl.logger.Error("RegisterNode, blockchain error", zap.Error(err))
		ctx.JSON(http.StatusInternalServerError, err.Error())
		return
	}
	ctx.Status(http.StatusOK)
}

// LogoutNode 注销本组织名下的计算节点地址
// @Summary 注销计算节点地址
// @Description 调用链上合约, 注销本组织名下的计算节点地址
// @Tags Node 节点
// @Accept application/json
// @Produce application/json
// @Success 200 "节点注销成功"
// @Router /core/v1/nodes [delete]
func (ctl *NodeController) LogoutNode(ctx *gin.Context) {
	err := ctl.chain.LogoutNode()
	if err != nil {
		ctl.logger.Error("LogoutNode, blockchain error", zap.Error(err))
		ctx.JSON(http.StatusInternalServerError, "blockchain error: "+err.Error())
		return
	}
	ctx.Status(http.StatusOK)
}

// LogoutNode 根据组织名查找计算节点的地址
// @Summary 计算节点发现服务
// @Description 调用链上合约, 根据给定的组织名查找这些组织计算节点的地址
// @Tags Node 节点
// @Accept application/json
// @Produce application/json
// @Param orgs query []string false "请求的组织名, 可以有多个"
// @Success 200 {object} map[string]string "节点注销成功"
// @Router /core/v1/nodes [get]
func (ctl *NodeController) DiscoverNode(ctx *gin.Context) {
	orgs := ctx.QueryArray("orgs")
	if len(orgs) == 0 {
		// discover all nodes
		ctl.discoverAllNode(ctx)
		return
	}
	ret, err := ctl.chain.DiscoverNodes(orgs)
	if err != nil {
		ctl.logger.Error("DiscoverNode, blockchain error", zap.Error(err))
		ctx.JSON(http.StatusInternalServerError, "blockchain error: "+err.Error())
		return
	}
	ctx.JSON(http.StatusOK, ret)
}

func (ctl *NodeController) GetNodeByOrg(c *gin.Context) {
	org := c.Query("org")
	if org == "" {
		c.JSON(http.StatusBadRequest, "missing requested org")
		return
	}

	addr, err := ctl.chain.DiscoverNodes([]string{org})
	if err != nil {
		ctl.logger.Error("DiscoverNode, blockchain error", zap.Error(err))
		c.JSON(http.StatusInternalServerError, "blockchain error: "+err.Error())
		return
	}
	ret, ok := addr[org]
	if !ok {
		c.JSON(http.StatusNotFound, "not found")
		return
	}
	c.JSON(http.StatusOK, ret)
}

func (ctl *NodeController) discoverAllNode(ctx *gin.Context) {
	ret, err := ctl.chain.DiscoverAllNodes()
	if err != nil {
		ctl.logger.Error("discoverAllNode, blockchain error", zap.Error(err))
		ctx.JSON(http.StatusInternalServerError, "blockchain error: "+err.Error())
		return
	}
	ctx.JSON(http.StatusOK, ret)
}
