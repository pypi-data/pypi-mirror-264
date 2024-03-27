package core

import (
	"fmt"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/tidwall/gjson"
	"go.uber.org/zap"
)

// GetObjectByKind 根据命名空间和对象类型获取对象
// @Summary 获取命名空间中某个类型的全部对象的接口
// @Schemes
// @Description 获取命名空间中某个类型的全部对象的接口
// @Tags Object 对象
// @Accept application/json
// @Produce application/json
// @Param namespace path string true "命名空间的名称"
// @Param kind path string true "对象的类型名称"
// @Success 200 {array} interface{}
// @Router /core/v1/namespace/{namespace}/{kind} [get]
func (ctl *CoreControllerV1) GetObjectByKind(c *gin.Context) {
	namespace := c.Param("namespace")
	kind := c.Param("kind")
	apiVersion := "core/v1"
	out, err := ctl.chain.GetObjectByKind(apiVersion, kind, namespace)
	if err != nil {
		ctl.logger.Error("GetObjectByKind::Blockchain error", zap.Error(err))
		c.JSON(http.StatusInternalServerError, "Blockchain error: "+err.Error())
		return
	}
	c.JSON(http.StatusOK, out)
	return
}

// GetObjectByName 根据命名空间和对象类型和对象名称获取对象
// @Summary 根据命名空间和对象的类型与名称获取对象
// @Description 根据命名空间和对象的类型或名称获取对象
// @Tags Object 对象
// @Accept application/json
// @Produce application/json
// @Param namespace path string true "命名空间的名称"
// @Param kind path string true "对象的类型"
// @Param name path string true "对象的类型"
// @Param version query string true "对象的版本" default("")
// @Success 200 {object} interface{} "如果对象不使用版本, 返回JSON编码的对象, 否则返回版本为键,对象为值的字典"
// @Failure 404 "找不到对应类型,名称的对象"
// @Router /core/v1/namespace/{namespace}/{kind}/{name} [get]
func (ctl *CoreControllerV1) GetObjectByName(c *gin.Context) {
	namespace := c.Param("namespace")
	kind := c.Param("kind")
	name := c.Param("name")
	version := c.Query("version")
	ctl.logger.Debug(
		"GetObjectByName",
		zap.String("namespace", namespace),
		zap.String("kind", kind),
		zap.String("name", name),
		zap.String("version", version),
	)

	out, err := ctl.chain.GetObjectByName(VERSION_CORE_V1, kind, namespace, name, version)
	if err != nil {
		ctl.logger.Error("GetObjectByName::Blockchain error", zap.Error(err))
		c.JSON(http.StatusInternalServerError, "Blockchain error: "+err.Error())
		return
	}

	if out == nil {
		c.Status(http.StatusNotFound)
		return
	}
	c.JSON(http.StatusOK, out)
	return
}

func (ctl *CoreControllerV1) GetNamespaceByName(c *gin.Context) {
	name := c.Param("namespace")
	if name == "" {
		c.JSON(http.StatusBadRequest, "name can't be empty")
		return
	}
	kind := "namespace"
	version := ""
	out, err := ctl.chain.GetObjectByName(VERSION_CORE_V1, kind, "", name, version)
	if err != nil {
		ctl.logger.Error("GetGlobalObjectByName::Blockchain error", zap.Error(err))
		c.JSON(http.StatusInternalServerError, "Blockchain error: "+err.Error())
		return
	}

	if out == nil {
		c.Status(http.StatusNotFound)
		return
	}
	c.JSON(http.StatusOK, out)
}

// GetGlobalObjectByName 根据对象类型和对象名称获取全局对象
// @Summary 根据对象的类型与名称获取全局对象
// @Description 根据对象的类型或名称获取全局对象
// @Tags Object 对象
// @Accept application/json
// @Produce application/json
// @Param kind path string true "对象的类型"
// @Param name path string true "对象的名称或uid"
// @Param version query string false "对象的版本"
// @Success 200 {object} interface{} "如果对象不使用版本, 返回JSON编码的对象, 否则返回版本为键,对象为值的字典"
// @Failure 404 "找不到对应类型,名称的对象"
// @Router /core/v1/{kind}/{name} [get]
func (ctl *CoreControllerV1) GetGlobalObjectByName(c *gin.Context) {
	kind := c.Param("kind")
	if kind == "" {
		c.JSON(http.StatusBadRequest, "kind can't be empty")
		return
	}

	name := c.Param("name")
	if name == "" {
		c.JSON(http.StatusBadRequest, "name can't be empty")
		return
	}

	first := name[0]

	if first >= '0' && first <= '9' {
		uid, err := strconv.ParseUint(name, 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, "parse uid failed: "+err.Error())
			return
		}
		out, err := ctl.chain.GetObjectByUid(uid)
		if err != nil {
			ctl.logger.Error("GetGlobalObjectByName, get by uid, Blockchain error",
				zap.Uint64("uid", uid),
				zap.Error(err),
			)
			c.JSON(http.StatusInternalServerError, "Blockchain error: "+err.Error())
			return
		}

		if out == nil {
			c.Status(http.StatusNotFound)
			return
		}

		outKind := gjson.Get(string(out), "kind").String()
		if outKind != kind {
			c.JSON(http.StatusBadRequest,
				fmt.Sprintf("mismatch kind, expect '%s' get '%s'", kind, outKind),
			)
			return
		}
		c.JSON(http.StatusOK, out)
	} else {
		version := c.Query("version")
		out, err := ctl.chain.GetObjectByName(VERSION_CORE_V1, kind, "", name, version)
		if err != nil {
			ctl.logger.Error("GetGlobalObjectByName::Blockchain error", zap.Error(err))
			c.JSON(http.StatusInternalServerError, "Blockchain error: "+err.Error())
			return
		}

		if out == nil {
			c.Status(http.StatusNotFound)
			return
		}
		c.JSON(http.StatusOK, out)
	}

	return
}

// GetAllObjectByKind 根据对象类型获取对象
// @Summary 获取某个类型的全部对象的接口
// @Schemes
// @Description 获取某个类型的全部对象的接口
// @Tags Object 对象
// @Accept application/json
// @Produce application/json
// @Param kind path string true "对象的类型名称"
// @Success 200 {array} interface{}
// @Router /core/v1/{kind} [get]
func (ctl *CoreControllerV1) GetAllObjectByKind(c *gin.Context) {
	kind := c.Param("kind")
	if kind == "" {
		c.JSON(http.StatusBadRequest, "kind can't be empty")
		return
	}

	apiVersion := "core/v1"
	out, err := ctl.chain.GetObjectByKind(apiVersion, kind, "")
	if err != nil {
		ctl.logger.Error("GetAllObjectByKind::Blockchain error", zap.Error(err))
		c.JSON(http.StatusInternalServerError, "Blockchain error: "+err.Error())
		return
	}

	c.JSON(http.StatusOK, out)
	return
}

// GetObjectByUid 根据对象的UID查询对象
// @Summary 根据UID查询单个对象
// @Schemes
// @Description 获取命名空间中某个类型的全部对象的接口
// @Tags Object 对象
// @Accept application/json
// @Produce application/json
// @Param uid path uint64 true "对象的UID"
// @Success 200 {object} interface{} "JSON编码的对象"
// @Failure 404 "找不到拥有该UID的对象"
// @Router /core/v1/object/{uid} [get]
func (ctl *CoreControllerV1) GetObjectByUid(c *gin.Context) {
	strUid := c.Param("uid")
	uid, err := strconv.ParseUint(strUid, 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}

	obj, err := ctl.chain.GetObjectByUid(uid)
	if err != nil {
		ctl.logger.Error("GetObjectByUid::Blockchain error", zap.Error(err))
		c.JSON(http.StatusInternalServerError, "Blockchain error: "+err.Error())
		return
	}

	c.JSON(http.StatusOK, obj)
}
