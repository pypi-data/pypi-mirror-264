package core

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
)

// 实现声明的请求
type SetImplementReq struct {
	Comment string `json:"comment"`
}

// AddDataImplement 添加数据声明实现
// @Summary 添加数据声明实现API
// @Description 按照请求在指定的数据声明中添加数据实现
// @Tags DataDeclare 数据声明
// @Accept application/json
// @Produce application/json
// @Param uid path uint64 true "数据声明的uid"
// @Param data body SetImplementReq true "实现声明的请求"
// @Success 200 "添加实现成功"
// @Router /core/v1/datadeclare/{uid}/implementation [put]
func (ctl *CoreControllerV1) AddDataImplement(c *gin.Context) {
	ctl.logger.Info("add data implement")

	name := c.Param("uid")
	uid, err := strconv.ParseUint(name, 10, 64)

	if err != nil {
		c.JSON(http.StatusBadRequest, "parse uid failed: "+err.Error())
		return
	}
	req := &SetImplementReq{}
	ctl.logger.Debug(req.Comment)
	if err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}

	err = ctl.chain.SetDataImplement(uid, true, req.Comment)
	if err == nil {
		c.JSON(http.StatusOK, "ok")
		return
	} else {
		ctl.logger.Error("add data implementation by uid failed",
			zap.Uint64("uid", uid),
			zap.Any("req", req),
			zap.Error(err),
		)
		c.JSON(http.StatusInternalServerError, err.Error())
		return
	}
}

// RemoveDataImplement 移除数据声明实现
// @Summary 移除数据声明实现API
// @Description 按照请求在指定的数据声明中移除实现
// @Tags DataDeclare 数据声明
// @Accept application/json
// @Produce application/json
// @Param uid path string true "数据声明的uid"
// @Success 200 "移除实现成功"
// @Router /core/v1/datadeclare/{uid}/implementation [delete]
func (ctl *CoreControllerV1) RemoveDataImplement(c *gin.Context) {
	ctl.logger.Info("delete data implement")
	name := c.Param("uid")
	uid, err := strconv.ParseUint(name, 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, "parse uid failed: "+err.Error())
		return
	}
	err = ctl.chain.SetDataImplement(uid, false, "")
	if err == nil {
		c.JSON(http.StatusOK, "ok")
		return
	} else {
		ctl.logger.Error("remove data implementation by uid failed",
			zap.Uint64("uid", uid),
			zap.Error(err),
		)
		c.JSON(http.StatusInternalServerError, err.Error())
		return
	}
}

// AddDataImplementByName 按照名称添加数据声明实现
// @Summary 按照名称添加数据声明实现API
// @Description 按照请求在指定的数据声明中添加数据实现
// @Tags DataDeclare 数据声明
// @Accept application/json
// @Produce application/json
// @Param namespace path string true "数据声明所属的命名空间"
// @Param name path string true "数据声明所属的名称"
// @Param data body SetImplementReq true "实现声明的请求"
// @Success 200 "添加实现成功"
// @Router /core/v1/namespace/{namespace}/datadeclare/{name}/implementation [put]
func (ctl *CoreControllerV1) AddDataImplementByName(c *gin.Context) {
	ctl.logger.Info("add data implement")

	ns := c.Param("namespace")
	if ns == "" {
		c.JSON(http.StatusBadRequest, "namespace can't be empty")
		return
	}

	name := c.Param("name")
	if ns == "" {
		c.JSON(http.StatusBadRequest, "name can't be empty")
		return
	}

	req := &SetImplementReq{}
	if err := c.ShouldBind(req); err != nil {
		c.JSON(http.StatusBadRequest, "parse SetImplementReq failed: "+err.Error())
		return
	}

	if err := ctl.chain.SetDataImplementByName(ns, name, true, req.Comment); err == nil {
		c.JSON(http.StatusOK, "ok")
		return
	} else {
		ctl.logger.Error("add data implementation by name failed",
			zap.String("namespace", ns),
			zap.String("name", name),
			zap.Any("req", req),
			zap.Error(err),
		)
		c.JSON(http.StatusInternalServerError, err.Error())
		return
	}
}

// RemoveDataImplement 移除数据声明实现
// @Summary 移除数据声明实现API
// @Description 按照请求在指定的数据声明中移除实现
// @Tags DataDeclare 数据声明
// @Accept application/json
// @Produce application/json
// @Param namespace path string true "数据声明所属的命名空间"
// @Param name path string true "数据声明的名称, 不能使用uid"
// @Success 200 "移除实现成功"
// @Router /core/v1/namespace/{namespace}/datadeclare/{name}/implementation [delete]
func (ctl *CoreControllerV1) RemoveDataImplementByName(c *gin.Context) {
	ctl.logger.Info("remove data implement")

	ns := c.Param("namespace")
	if ns == "" {
		c.JSON(http.StatusBadRequest, "namespace can't be empty")
		return
	}

	name := c.Param("name")
	if ns == "" {
		c.JSON(http.StatusBadRequest, "name can't be empty")
		return
	}

	if err := ctl.chain.SetDataImplementByName(ns, name, false, ""); err == nil {
		c.JSON(http.StatusOK, "ok")
		return
	} else {
		ctl.logger.Error("remove data implementation by name failed",
			zap.String("namespace", ns),
			zap.String("name", name),
			zap.Error(err),
		)
		c.JSON(http.StatusInternalServerError, err.Error())
		return
	}
}

// AddFunctionImplement 添加函数声明实现
// @Summary 添加函数声明实现API
// @Description 按照请求在指定的函数声明中添加实现
// @Tags FunctionDeclare 函数声明
// @Accept application/json
// @Produce application/json
// @Param uid path uint64 true "函数声明的uid"
// @Param data body SetImplementReq true "实现声明的请求"
// @Success 200 "添加实现成功"
// @Router /core/v1/functiondeclare/{uid}/implementation [put]
func (ctl *CoreControllerV1) AddFunctionImplement(c *gin.Context) {
	ctl.logger.Info("add function implement")

	name := c.Param("uid")
	uid, err := strconv.ParseUint(name, 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, "parse uid failed: "+err.Error())
		return
	}
	req := &SetImplementReq{}
	err = c.ShouldBind(req)
	if err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}

	err = ctl.chain.SetFunctionImplement(uid, true, req.Comment)
	if err == nil {
		c.JSON(http.StatusOK, "ok")
		return
	} else {
		ctl.logger.Error("add function implementation by uid failed",
			zap.Uint64("uid", uid),
			zap.Any("req", req),
			zap.Error(err),
		)
		c.JSON(http.StatusInternalServerError, err.Error())
		return
	}
}

// AddFunctionImplementByName 按照函数声明的名称添加函数声明实现
// @Summary 按照函数声明的名称添加函数声明实现
// @Description 按照请求在指定的函数声明中添加实现
// @Tags FunctionDeclare 函数声明
// @Accept application/json
// @Produce application/json
// @Param namespace path string true "函数声明所属的命名空间"
// @Param name path string true "函数声明的名称, 不能使用uid"
// @Param data body SetImplementReq true "实现声明的请求"
// @Success 200 "添加实现成功"
// @Router /core/v1/namespace/{namespace}/functiondeclare/{name}/implementation [put]
func (ctl *CoreControllerV1) AddFunctionImplementByName(c *gin.Context) {
	ctl.logger.Info("add function implement by name")

	ns := c.Param("namespace")
	if ns == "" {
		c.JSON(http.StatusBadRequest, "namespace can't be empty")
		return
	}

	name := c.Param("name")
	if name == "" {
		c.JSON(http.StatusBadRequest, "name can't be empty")
		return
	}

	req := &SetImplementReq{}
	if err := c.ShouldBind(req); err != nil {
		c.JSON(http.StatusBadRequest, "parse set implementation req failed: "+err.Error())
		return
	}

	err := ctl.chain.SetFunctionImplementByName(ns, name, true, req.Comment)
	if err != nil {
		ctl.logger.Error("add function implementation by name failed",
			zap.String("namespace", ns),
			zap.String("name", name),
			zap.Any("req", req),
			zap.Error(err),
		)
		c.JSON(http.StatusInternalServerError, "add function implementation by name failed: "+err.Error())
		return
	}

	c.JSON(http.StatusOK, "ok")
}

// RemoveFunctionImplement 移除函数声明实现
// @Summary 移除函数声明实现API
// @Description 按照请求在指定的函数声明中移除实现
// @Tags FunctionDeclare 函数声明
// @Accept application/json
// @Produce application/json
// @Param uid path string true "函数声明的uid"
// @Success 200 "移除实现成功"
// @Router /core/v1/functiondeclare/{uid}/implementation [delete]
func (ctl *CoreControllerV1) RemoveFunctionImplement(c *gin.Context) {
	ctl.logger.Info("remove data implement")
	name := c.Param("uid")
	uid, err := strconv.ParseUint(name, 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, "parse uid failed: "+err.Error())
		return
	}
	err = ctl.chain.SetFunctionImplement(uid, false, "")
	if err == nil {
		c.JSON(http.StatusOK, "ok")
		return
	} else {
		ctl.logger.Error("remove function implementtation by uid failed",
			zap.Uint64("uid", uid),
			zap.Error(err),
		)
		c.JSON(http.StatusInternalServerError, "remove function implementation by uid failed:"+err.Error())
		return
	}
}

// RemoveFunctionImplementByName 按照名称移除函数声明实现
// @Summary 按照名称移除函数声明实现
// @Description 按照请求在指定的函数声明中移除实现
// @Tags FunctionDeclare 函数声明
// @Accept application/json
// @Produce application/json
// @Param namespace path string true "函数声明的所属的命名空间"
// @Param name path string true "函数声明的名称"
// @Success 200 "移除实现成功"
// @Router /core/v1/namespace/{namespace}/functiondeclare/{name}/implementation [delete]
func (ctl *CoreControllerV1) RemoveFunctionImplementByName(c *gin.Context) {
	ctl.logger.Info("remove function implement by name")

	ns := c.Param("namespace")
	if ns == "" {
		c.JSON(http.StatusBadRequest, "namespace can't be empty")
		return
	}

	name := c.Param("name")
	if name == "" {
		c.JSON(http.StatusBadRequest, "name can't be empty")
		return
	}

	err := ctl.chain.SetFunctionImplementByName(ns, name, false, "")
	if err != nil {
		ctl.logger.Error("remove function implementtation by name failed",
			zap.String("namespace", ns),
			zap.String("name", ns),
			zap.Error(err),
		)
		c.JSON(http.StatusInternalServerError, "remove function implementtation by name failed: "+err.Error())
		return
	}

}
