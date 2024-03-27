package core

import (
	"io/ioutil"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
)

type permitReq struct {
	Comment string `json:"comment"`
}

// CreateGlobalProposal 创建全局提议
// @Summary 创建全局提议API
// @Schemes
// @Description 获取命名空间中某个类型的全部对象的接口, 如果使用UID, 请在UID前加下划线_
// @Tags GlobalProposal 全局提议
// @Accept application/json
// @Produce application/json
// @Param proposal body interface{} true "要创建的提议对象"
// @Success 201 {integer} json "创建的全局对象的uid"
// @Router /core/v1/globalproposal [post]
func (ctl *CoreControllerV1) CreateGlobalProposal(c *gin.Context) {
	ctl.logger.Info("create global proposal")
	object, err := ioutil.ReadAll(c.Request.Body)
	if err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}
	ctl.logger.Debug("global proposal", zap.String("object", string(object)))
	uid, err := ctl.chain.CreateGlobalProposal(object)
	if err != nil {
		ctl.logger.Error("create global proposal, blockchain error", zap.Error(err))
		c.JSON(http.StatusInternalServerError, "blockchain error: "+err.Error())
		return
	}

	c.JSON(http.StatusCreated, uid)
	return
}

// RevokeGlobalProposal 撤回全局提议
// @Summary 撤回全局提议API
// @Schemes
// @Description 按照名称或UID撤回某个全局提议, 如果使用UID
// @Tags GlobalProposal 全局提议
// @Accept application/json
// @Produce application/json
// @Param name path string true "提议对象的名称"
// @Success 200 {string} json "ok"
// @Router /core/v1/globalproposal/{name} [delete]
func (ctl *CoreControllerV1) RevokeGlobalProposal(c *gin.Context) {
	name := c.Param("name")
	if name == "" {
		c.JSON(http.StatusBadRequest, "name can't be empty")
		return
	}
	ch := name[0]
	if ch >= '0' && ch <= '9' {
		// 按照uid进行撤回
		uid, err := strconv.ParseUint(name, 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, "parse uid failed: "+err.Error())
			return
		}
		ctl.logger.Info("revoke global proposal", zap.Uint64("uid", uid))
		err = ctl.chain.RevokeGlobalProposal(uid)
		if err == nil {
			c.JSON(http.StatusOK, "ok")
			return
		} else {
			ctl.logger.Error("revoke global proposal by uid, blockchain error", zap.Error(err))
			c.JSON(http.StatusInternalServerError, err.Error())
			return
		}
	} else {
		// 按照名称进行撤回
		ctl.logger.Info("revoke global proposal", zap.String("name", name))
		err := ctl.chain.RevokeGlobalProposalByName(name)
		if err == nil {
			c.JSON(http.StatusOK, "ok")
			return
		} else {
			ctl.logger.Error("revoke global proposal by name, blockchain error", zap.Error(err))
			c.JSON(http.StatusInternalServerError, err.Error())
		}
	}
}

// PermitGlobalProposal 批准全局提议
// @Summary 批准全局提议 API
// @Schemes
// @Description 按照名称或UID撤回某个全局提议, 如果使用UID
// @Tags GlobalProposal 全局提议
// @Accept application/json
// @Produce application/json
// @Param name     path string true "要批准对象的UID或名称"
// @Param comment  body permitReq true "要添加的批准注释信息"
// @Success 200 {string} json "ok"
// @Router /core/v1/globalproposal/{name}/permission [put]
func (ctl *CoreControllerV1) PermitGlobalProposal(c *gin.Context) {
	name := c.Param("name")
	ctl.logger.Info("permit global proposal", zap.String("uid", name))
	if name == "" {
		c.JSON(http.StatusBadRequest, "name can't be empty")
		return
	}

	req := permitReq{}
	if err := c.ShouldBind(&req); err != nil {
		c.JSON(http.StatusBadRequest, "parse request body failed: "+err.Error())
		return
	}
	comment := req.Comment

	ch := name[0]
	if ch >= '0' && ch <= '9' {
		// 按照uid进行批准
		ctl.logger.Info("permit global proposal", zap.String("uid", name))
		uid, err := strconv.ParseUint(name, 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, "parse uid failed: "+err.Error())
			return
		}

		_, err = ctl.chain.PermitGlobalProposal(uid, true, comment)
		if err != nil {
			ctl.logger.Error("PermitGlobalProposal, permit by uid, blockchain error", zap.Error(err))
			c.JSON(http.StatusInternalServerError, "permit failed: "+err.Error())
		} else {
			c.JSON(http.StatusOK, "ok")
		}
		return
	} else {
		// 按照名称进行批准
		ctl.logger.Info("permit global proposal", zap.String("name", name))
		_, err := ctl.chain.PermitGlobalProposalByName(name, true, comment)
		if err != nil {
			ctl.logger.Error("PermitGlobalProposal, permit by name, blockchain error",
				zap.String("name", name),
				zap.String("comment", comment),
				zap.Error(err),
			)
			c.JSON(http.StatusInternalServerError, "permit failed: "+err.Error())
		} else {
			c.JSON(http.StatusOK, "ok")
		}
		return
	}
}

// DenyGlobalProposal 取消批准全局提议
// @Summary 取消批准全局提议 API
// @Schemes
// @Description 按照名称或UID取消批准某个全局提议, 如果使用UID, 请在UID前加下划线_
// @Tags GlobalProposal 全局提议
// @Accept application/json
// @Produce application/json
// @Param name path string true "要取消批准的全局提议对象的名称或UID"
// @Success 200 {string} json "ok"
// @Router /core/v1/globalproposal/{name}/permission [delete]
func (ctl *CoreControllerV1) DenyGlobalProposal(c *gin.Context) {
	name := c.Param("name")
	if name == "" {
		c.JSON(http.StatusBadRequest, "name can't be empty")
		return
	}
	first := name[0]
	if first >= '0' && first <= '9' {
		// 按照UID取消批准
		uid, err := strconv.ParseUint(name, 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, "parse uid failed: "+err.Error())
			return
		}
		_, err = ctl.chain.PermitGlobalProposal(uid, false, "")
		if err != nil {
			ctl.logger.Error("DenyGlobalProposal by uid blockchain failed: ",
				zap.Uint64("uid", uid),
				zap.Error(err),
			)
			c.JSON(http.StatusInternalServerError, "deny failed: "+err.Error())
			return
		}
	} else {
		// 按照名称取消批准
		_, err := ctl.chain.PermitGlobalProposalByName(name, false, "")
		if err != nil {
			ctl.logger.Error("DenyGlobalProposal by name, blockchain failed: ",
				zap.String("name", name),
				zap.Error(err),
			)
			c.JSON(http.StatusInternalServerError, "deny failed: "+err.Error())
			return
		}
	}

	c.JSON(http.StatusOK, "ok")
}

// CommitGlobalProposal 提交全局提议
// @Summary 提交全局提议 API
// @Schemes
// @Description 按照名称或UID提交某个全局提议, 如果使用UID
// @Tags GlobalProposal 全局提议
// @Accept application/json
// @Produce application/json
// @Param name path string true "要提交的批准对象的名称或UID"
// @Success 200 {array} interface{} "提交成功, 返回提议执行的结果"
// @Router /core/v1/globalproposal/{name}/commit [put]
func (ctl *CoreControllerV1) CommitGlobalProposal(c *gin.Context) {
	name := c.Param("name")
	if name == "" {
		c.JSON(http.StatusBadRequest, "name can't be empty")
		return
	}
	ch := name[0]
	if ch >= '0' && ch <= '9' {
		// 按照UID进行提交
		uid, err := strconv.ParseUint(name, 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, "parse uid failed: "+err.Error())
			return
		}

		objectList, err := ctl.chain.CommitGlobalProposal(uid)
		if err == nil {
			c.JSON(http.StatusOK, objectList)
		} else {
			ctl.logger.Error("commit global proposal by uid, blockchain error",
				zap.Uint64("uid", uid),
				zap.Error(err),
			)
			c.JSON(http.StatusInternalServerError, "commit proposal failed: "+err.Error())
		}
		return
	} else {
		// 按照名称进行提交
		objectList, err := ctl.chain.CommitGlobalProposalByName(name)
		if err == nil {
			c.JSON(http.StatusOK, objectList)
		} else {
			ctl.logger.Error("commit global proposal by name, blockchain error",
				zap.String("name", name),
				zap.Error(err),
			)
			c.JSON(http.StatusInternalServerError, "commit proposal failed: "+err.Error())
		}
		return
	}
}

// CreateProposal 创建提议
// @Summary 创建提议API
// @Schemes
// @Description 创建某个命名空间下的提议
// @Tags Proposal 提议
// @Accept application/json
// @Produce application/json
// @Param namespace path string true "提议对象所属的命名空间"
// @Param proposal body interface{} true "要创建的提议对象"
// @Success 201 {integer} json "创建的提议对象的uid"
// @Router /core/v1/namespace/{namespace}/proposal [post]
func (ctl *CoreControllerV1) CreateProposal(c *gin.Context) {
	ctl.logger.Info("create proposal")
	namespace := c.Param("namespace")
	if len(namespace) == 0 {
		c.JSON(http.StatusBadRequest, "namespace can't by empty")
		return
	}

	object, err := ioutil.ReadAll(c.Request.Body)
	if err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}
	ctl.logger.Debug(
		"proposal",
		zap.String("object", string(object)),
		zap.String("namespace", string(namespace)),
	)
	uid, err := ctl.chain.CreateProposal(object, namespace)
	if err != nil {
		ctl.logger.Error("create proposal failed, blockchain error",
			zap.String("proposal", string(object)),
			zap.String("namespace", namespace),
			zap.Error(err),
		)
		c.JSON(http.StatusInternalServerError, "blockchain error:"+err.Error())
		return
	}

	c.JSON(http.StatusCreated, uid)
	return
}

// PermitProposalByUID 批准提议
// @Summary 批准提议 API
// @Schemes
// @Description 按照UID批准某个提议
// @Tags Proposal 提议
// @Accept application/json
// @Produce application/json
// @Param uid     path string true "要批准对象的UID"
// @Param comment body permitReq true "要添加的批准注释信息"
// @Success 200 {string} json "ok"
// @Router /core/v1/proposal/{uid}/permission [put]
func (ctl *CoreControllerV1) PermitProposalByUID(c *gin.Context) {
	rawUid := c.Param("uid")
	if len(rawUid) == 0 {
		c.JSON(http.StatusBadRequest, "invalid name/uid format")
		return
	}

	req := permitReq{}
	if err := c.ShouldBind(&req); err != nil {
		c.JSON(http.StatusBadRequest, "parse request body failed: "+err.Error())
		return
	}
	comment := req.Comment

	uid, err := strconv.ParseUint(rawUid, 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, "parse uid failed: "+err.Error())
		return
	}

	_, err = ctl.chain.PermitProposal(uid, true, comment)
	if err != nil {
		ctl.logger.Error("PermitProposalByUID failed, blockchain error",
			zap.Uint64("uid", uid),
			zap.String("comment", comment),
			zap.Error(err),
		)
		c.JSON(http.StatusInternalServerError, "permit failed: "+err.Error())
	} else {
		c.JSON(http.StatusOK, "ok")
	}
}

// PermitProposalByName 按照名称批准提议
// @Summary 按照名称批准提议 API
// @Schemes
// @Description 按照名称批准某个提议
// @Tags Proposal 提议
// @Accept application/json
// @Produce application/json
// @Param namespace path string true "要批准对象的命名空间"
// @Param name      path string true "要批准对象的名称"
// @Param comment   body permitReq true "要添加的批准注释信息"
// @Success 200 {string} json "ok"
// @Router /core/v1/namespace/{namespace}/proposal/{name}/permission [put]
func (ctl *CoreControllerV1) PermitProposalByName(c *gin.Context) {
	ns := c.Param("namespace")
	name := c.Param("name")
	if len(ns) == 0 {
		c.JSON(http.StatusBadRequest, "namespace can't be empty")
		return
	}
	if len(name) == 0 {
		c.JSON(http.StatusBadRequest, "name can't be empty")
		return
	}

	req := permitReq{}
	if err := c.ShouldBind(&req); err != nil {
		c.JSON(http.StatusBadRequest, "parse request body failed")
		return
	}

	comment := req.Comment

	_, err := ctl.chain.PermitProposalByName(ns, name, true, comment)
	if err != nil {
		ctl.logger.Error("PermitProposalByName failed, blockchain error",
			zap.String("name", name),
			zap.Error(err),
		)
		c.JSON(http.StatusInternalServerError, "permit failed: "+err.Error())
	} else {
		c.JSON(http.StatusOK, "ok")
	}
	return
}

// DenyProposalByUID 按照UID取消批准提议
// @Summary 按照UID取消批准提议 API
// @Schemes
// @Description 按照UID取消批准某个提议
// @Tags Proposal 提议
// @Accept application/json
// @Produce application/json
// @Param uid path string true "要取消批准的提议对象的UID"
// @Success 200 {string} json "ok"
// @Failure 404 "找不到对应的提议对象"
// @Router /core/v1/proposal/{uid}/permission [delete]
func (ctl *CoreControllerV1) DenyProposalByUID(c *gin.Context) {
	rawUid := c.Param("uid")
	if len(rawUid) == 0 {
		c.JSON(http.StatusBadRequest, "invalid uid format")
		return
	}
	uid, err := strconv.ParseUint(rawUid, 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, "parse uid failed: "+err.Error())
		return
	}

	_, err = ctl.chain.PermitProposal(uid, false, "")
	if err != nil {
		ctl.logger.Error("DenyProposalByUID failed, blockchain error",
			zap.Uint64("uid", uid),
			zap.Error(err),
		)
		c.JSON(http.StatusInternalServerError, "deny failed: "+err.Error())
	} else {
		c.JSON(http.StatusOK, "ok")
	}
	return
}

// DenyProposalByName 按照名称取消批准提议
// @Summary 按照名称取消批准提议 API
// @Schemes
// @Description 按照名称取消批准某个提议
// @Tags Proposal 提议
// @Accept application/json
// @Produce application/json
// @Param namespace path string true "要取消批准的提议对象的命名空间"
// @Param name      path string true "要取消批准的提议对象的名称"
// @Success 200 {string} json "ok"
// @Router /core/v1/namespace/{namespace}/proposal/{name}/permission [delete]
func (ctl *CoreControllerV1) DenyProposalByName(c *gin.Context) {
	ns := c.Param("namespace")
	name := c.Param("name")

	if len(ns) == 0 {
		c.JSON(http.StatusBadRequest, "namespace can't be empty")
		return
	}

	if len(name) == 0 {
		c.JSON(http.StatusBadRequest, "name can't be empty")
		return
	}

	_, err := ctl.chain.PermitProposalByName(ns, name, false, "")
	if err != nil {
		ctl.logger.Error(
			"DenyProposalByName failed",
			zap.String("namespace", ns),
			zap.String("name", name),
			zap.Error(err),
		)
		c.JSON(http.StatusInternalServerError, "deny failed: "+err.Error())
	} else {
		c.JSON(http.StatusOK, "ok")
	}
	return
}

// RevokeProposalByUID 撤回提议
// @Summary 撤回提议API
// @Schemes
// @Description 按照UID撤回某个提议
// @Tags Proposal 提议
// @Accept application/json
// @Produce application/json
// @Param uid path string true "提议对象的UID"
// @Success 200 {string} json "ok"
// @Router /core/v1/proposal/{uid} [delete]
func (ctl *CoreControllerV1) RevokeProposalByUID(c *gin.Context) {
	rawUid := c.Param("uid")
	if len(rawUid) == 0 {
		c.JSON(http.StatusBadRequest, "invalid uid format")
		return
	}

	uid, err := strconv.ParseUint(rawUid, 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}

	ctl.logger.Info("revoke global proposal", zap.Uint64("uid", uid))
	err = ctl.chain.RevokeProposal(uid)
	if err == nil {
		c.JSON(http.StatusOK, "ok")
		return
	} else {
		ctl.logger.Error("RevokeProposalByUID failed, blockchain error",
			zap.Uint64("uid", uid),
			zap.Error(err),
		)
		c.JSON(http.StatusInternalServerError, err.Error())
		return
	}
}

// RevokeProposalByName 撤回提议
// @Summary 撤回提议API
// @Schemes
// @Description 按照名称撤回某个提议
// @Tags Proposal 提议
// @Accept application/json
// @Produce application/json
// @Param namespace path string true "提议对象的所属的命名空间"
// @Param name path string true "提议对象的名称"
// @Success 200 {string} json "ok"
// @Router /core/v1/namespace/{namespace}/proposal/{name} [delete]
func (ctl *CoreControllerV1) RevokeProposalByName(c *gin.Context) {
	ns := c.Param("namespace")
	name := c.Param("name")

	if len(ns) == 0 {
		c.JSON(http.StatusBadRequest, "namespace can't be empty")
		return
	}

	if len(name) == 0 {
		c.JSON(http.StatusBadRequest, "name can't be empty")
		return
	}

	err := ctl.chain.RevokeProposalByName(ns, name)
	if err == nil {
		c.JSON(http.StatusOK, "ok")
	} else {
		ctl.logger.Error("RevokeProposalByName failed, blockchain error",
			zap.String("name", name),
			zap.Error(err),
		)
		c.JSON(http.StatusInternalServerError, err.Error())
	}
	return

}

// CommitProposalByUID 提交提议
// @Summary 按照UID提交提议 API
// @Schemes
// @Description 按照UID提交某个提议
// @Tags Proposal 提议
// @Accept application/json
// @Produce application/json
// @Param uid path string true "要提交的批准对象的uid"
// @Success 200 {array} interface{} "提交成功, 返回提议的执行结果"
// @Router /core/v1/proposal/{uid}/commit [put]
func (ctl *CoreControllerV1) CommitProposalByUID(c *gin.Context) {
	rawUid := c.Param("uid")
	if len(rawUid) == 0 {
		c.JSON(http.StatusBadRequest, "uid can't be empty")
		return
	}
	uid, err := strconv.ParseUint(rawUid, 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, "parse uid failed: "+err.Error())
		return
	}

	objectList, err := ctl.chain.CommitProposal(uid)
	if err == nil {
		c.JSON(http.StatusOK, objectList)
	} else {
		ctl.logger.Error("CommitProposalByUID failed, blockchain error",
			zap.Uint64("uid", uid),
			zap.Error(err),
		)
		c.JSON(http.StatusInternalServerError, "commit proposal by uid failed: "+err.Error())
	}
}

// CommitProposalByName 按照名称提交提议
// @Summary 按照名称提交提议 API
// @Schemes
// @Description 按照名称提交某个提议
// @Tags Proposal 提议
// @Accept application/json
// @Produce application/json
// @Param namespace path string true "要提交的批准对象的名称"
// @Param name      path string true "要提交的批准对象的名称"
// @Success 200 {array} interface{} "提交成功, 返回提议的执行结果"
// @Failure 403 "提议对象不能被批准"
// @Failure 404 "找不到对应的提议对象"
// @Router /core/v1/namespace/{namespace}/proposal/{name}/commit [put]
func (ctl *CoreControllerV1) CommitProposalByName(c *gin.Context) {
	ns := c.Param("namespace")
	name := c.Param("name")
	if len(ns) == 0 {
		c.JSON(http.StatusBadRequest, "namespace can't be empty")
		return
	}
	if len(name) == 0 {
		c.JSON(http.StatusBadRequest, "name can't be empty")
		return
	}

	objectList, err := ctl.chain.CommitProposalByName(ns, name)
	if err == nil {
		c.JSON(http.StatusOK, objectList)
	} else {
		ctl.logger.Error("CommitProposalByName failed, blockchain error",
			zap.String("namespace", ns),
			zap.String("name", name),
			zap.Error(err),
		)
		c.JSON(http.StatusInternalServerError, "commit proposal by name failed: "+err.Error())
	}
}
