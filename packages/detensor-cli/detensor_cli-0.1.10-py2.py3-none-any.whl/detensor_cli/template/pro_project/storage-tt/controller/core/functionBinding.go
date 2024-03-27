package core

import (
	"errors"
	"net/http"
	"strconv"

	"go.uber.org/zap"
	"gorm.io/gorm"

	"buaa.edu.cn/storage/objects"
	"github.com/gin-gonic/gin"
)

// CreateFuncBinding 创建私有函数绑定
// @Summary 创建私有函数绑定API
// @Schemes
// @Description 按照请求创建私有函数绑定, 返回创建的私有函数绑定
// @Tags FunctionBinding 私有函数绑定
// @Accept application/json
// @Produce application/json
// @Param data body objects.FunctionBinding true "待创建的私有函数绑定对象"
// @Success 201 {object} objects.FunctionBinding "私有函数绑定对象创建成功"
// @Router /core/v1/functionbinding [post]
func (ctl *CoreControllerV1) CreateFuncBinding(c *gin.Context) {
	var count int64
	functionBinding := &objects.FunctionBinding{}
	if err := c.ShouldBind(functionBinding); err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}

	if functionBinding.ApiVersion != "core/v1" || functionBinding.Kind != "functionbinding" {
		c.JSON(http.StatusBadRequest, "invalid apiVersion and kind")
		return
	}

	if !IsValidRFC1035(functionBinding.Metadata.Name) {
		c.JSON(http.StatusBadRequest, "invalid name")
		return
	}

	db := ctl.db
	functionBindingModel := functionBinding.ToModel()

	temp := &objects.FunctionBindingModel{}
	functionBindingName := functionBinding.Metadata.Name //取得URL中参数
	ctl.logger.Info("CreateFuncBinding:", zap.Any("functionBinding", functionBinding))
	//查找在存储中是否存在与要创建的functionBinding对象重名的functionBinding对象
	if err := db.Where("name=?", functionBindingName).Find(&temp).Count(&count).Error; err != nil {
		ctl.logger.Error("failed in CreateFuncBinding when check duplicated functionBinding name: ", zap.Error(err))
		c.JSON(http.StatusNotImplemented, "failed in CreateFuncBinding when check duplicated functionBinding name")
		return
	}
	//重名
	if count != 0 {
		ctl.logger.Error("duplicated functionBinding name:", zap.String("function_binding_name", functionBindingName))
		c.JSON(http.StatusNotImplemented, functionBinding)
		return
	} else {
		//未重名，保存到私有存储中
		if err := db.Create(&functionBindingModel).Error; err != nil {
			ctl.logger.Error("failed in CreateFuncBinding when create a functionBinding", zap.Error(err))
			c.JSON(http.StatusNotImplemented, functionBinding)
		} else {
			ctl.logger.Info("CreateFuncBinding succeed:", zap.Any("functionBinding", functionBinding))
			c.JSON(http.StatusCreated, functionBinding)
		}
	}
}

// FindFuncBinding 查找私有函数绑定对象
// @Summary 查找私有函数绑定对象 API
// @Schemes
// @Description 按照请求创建私有函数绑定, 返回创建的私有函数绑定
// @Tags FunctionBinding 私有函数绑定
// @Accept application/json
// @Produce application/json
// @Param contract query uint64 false "私有函数绑定对应的合约UID"
// @Param declare query uint64 false "私有函数绑定对应的声明UID"
// @Param function query uint64 false "私有函数绑定对应的合约UID"
// @Success 200 {array} objects.FunctionBinding "查找出的私有函数绑定对象"
// @Router /core/v1/functionbinding [get]
func (ctl *CoreControllerV1) FindFuncBinding(c *gin.Context) {
	functionBindings := []objects.FunctionBinding{}
	functionBindingModels := []objects.FunctionBindingModel{}

	contract := c.Query("contract")
	declare := c.Query("declare")
	function := c.Query("function")

	db := ctl.db

	if contract != "" {
		// add contract uid condition
		uid, err := strconv.ParseUint(contract, 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, "parse contract uid failed: "+err.Error())
			return
		}
		db = db.Where("contract_uid = ?", uid)
	}

	if declare != "" {
		// add declare uid condition
		uid, err := strconv.ParseUint(declare, 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, "parse declare uid failed: "+err.Error())
			return
		}
		db = db.Where("function_declare_uid = ?", uid)
	}

	if function != "" {
		// add function uid condition
		uid, err := strconv.ParseUint(function, 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, "parse declare uid failed: "+err.Error())
			return
		}
		db = db.Where("function_uid = ?", uid)
	}

	ctl.logger.Info("FindFuncBinding: find functionBinding instances",
		zap.String("contract", contract),
		zap.String("declare", declare),
		zap.String("function", function),
	)
	if err := db.Find(&functionBindingModels).Error; err != nil {
		ctl.logger.Error("failed in FindFuncBinding", zap.Error(err))
		c.JSON(http.StatusNotImplemented, "failed in FindFuncBinding")
	} else {
		for _, f := range functionBindingModels {
			functionBindings = append(functionBindings, f.ToView())
		}
		ctl.logger.Info("FindFuncBinding succeed", zap.Any("functionBinding", functionBindings))
		c.JSON(http.StatusOK, functionBindings)
	}
}

func (ctl *CoreControllerV1) findFuncBindingByName(c *gin.Context, name string) {
	db := ctl.db
	model := objects.FunctionBindingModel{}
	ctl.logger.Info("FindDataBindingByName:", zap.String("name", name))
	if err := db.Where("name = ?", name).First(&model).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			c.Status(http.StatusNotFound)
			return
		}
		ctl.logger.Error("failed in FindDataBindingByName: ", zap.Error(err))
		c.JSON(http.StatusInternalServerError, "failed in FindFuncBindingByName")
	} else {
		view := model.ToView()
		ctl.logger.Info("FindDataBindingByName succeed", zap.Any("funcBinding", view))
		c.JSON(http.StatusOK, view)
	}
}

func (ctl *CoreControllerV1) findFuncBindingByUid(c *gin.Context, uid uint64) {
	db := ctl.db
	model := objects.FunctionBindingModel{}
	ctl.logger.Info("FindFuncBindingByUid:", zap.Uint64("uid", uid))
	if err := db.First(&model, uid).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			c.Status(http.StatusNotFound)
			return
		}
		ctl.logger.Error("failed in FindFuncBindingByUid: ", zap.Error(err))
		c.JSON(http.StatusInternalServerError, "failed in FindFuncBindingByUid")
	} else {
		view := model.ToView()
		ctl.logger.Info("FindFuncBindingByName succeed", zap.Any("funcBinding", view))
		c.JSON(http.StatusOK, view)
	}
}

// FindFuncBindingByName 按照名称查找私有函数绑定对象
// @Summary 按照名称查找私有函数绑定对象 API
// @Schemes
// @Description 根据私有函数绑定对象的名称,在本地数据库中查找私有函数绑定对象
// @Tags FunctionBinding 私有函数绑定
// @Accept application/json
// @Produce application/json
// @Param name path string true "私有函数绑定对象的名称或uid"
// @Success 200 {object} objects.FunctionBinding "查找出的私有函数绑定对象"
// @Router /core/v1/functionbinding/{name} [get]
func (ctl *CoreControllerV1) FindFuncBindingByName(c *gin.Context) {
	name := c.Param("name") //取得URL中参数
	if len(name) == 0 {
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
		ctl.findFuncBindingByUid(c, uid)
	} else {
		ctl.findFuncBindingByName(c, name)
	}
	return
}

func (ctl *CoreControllerV1) deleteFuncBindingByName(c *gin.Context, name string) {

	db := ctl.db
	model := objects.FunctionBindingModel{}

	ctl.logger.Info("deleteFuncBindingByName:", zap.String("name", name))
	if result := db.Where("name=?", name).Delete(&model); result.Error != nil {
		ctl.logger.Error("failed in deleteFuncBindingByName ", zap.Error(result.Error))
		c.JSON(http.StatusInternalServerError, "failed in deleteFuncBindingByName")
		return
	} else if result.RowsAffected == 0 {
		c.Status(http.StatusNotFound)
		return
	}
	c.JSON(http.StatusOK, model.ToView())
}

func (ctl *CoreControllerV1) deleteFuncBindingByUid(c *gin.Context, uid uint64) {
	db := ctl.db
	model := objects.FunctionBindingModel{}

	ctl.logger.Info("deleteDataBindingByUid:", zap.Uint64("uid", uid))
	if result := db.Delete(&model, uid); result.Error != nil {
		ctl.logger.Error("failed in deleteFuncBindingByUid ", zap.Error(result.Error))
		c.JSON(http.StatusInternalServerError, "failed in deleteFuncBindingByName")
		return
	} else if result.RowsAffected == 0 {
		c.Status(http.StatusNotFound)
		return
	}
	c.JSON(http.StatusOK, model.ToView())
}

// DeleteFuncBindingByName 删除私有函数绑定
// @Summary 删除私有函数绑定 API
// @Description 按照请求删除私有函数绑定, 返回删除的私有函数绑定
// @Tags FunctionBinding 私有函数绑定
// @Accept application/json
// @Produce application/json
// @Param name path string true "要删除的私有函数绑定对象的名称或uid"
// @Success 200 {object} objects.FunctionBinding "删除成功, 返回删除的对象"
// @Failure 404 "找不到对应的私有对象"
// @Router /core/v1/functionbinding/{name} [delete]
func (ctl *CoreControllerV1) DeleteFuncBindingByName(c *gin.Context) {
	name := c.Param("name") //取得URL中参数
	if len(name) == 0 {
		c.JSON(http.StatusBadRequest, "name can't be empty")
		return
	}
	first := name[0]
	if first <= '9' && first >= '0' {
		uid, err := strconv.ParseUint(name, 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, "parse uid failed: "+err.Error())
			return
		}
		ctl.deleteFuncBindingByUid(c, uid)
	} else {
		ctl.deleteFuncBindingByName(c, name)
	}
}

func (ctl *CoreControllerV1) putFuncBindingByName(c *gin.Context, name string, newModel *objects.FunctionBindingModel) {
	model := objects.FunctionBindingModel{}
	if err := ctl.db.Where("name = ?", name).First(&model).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			c.Status(http.StatusNotFound)
			return
		} else {
			c.JSON(http.StatusInternalServerError, "find functionBinding by name failed")
			return
		}
	}

	if newModel.Id == 0 {
		newModel.Id = model.Id
	}

	if model.Id != newModel.Id {
		c.JSON(http.StatusBadRequest, "can't change uid")
		return
	}

	//更新该functionBinding对象
	model.Name = newModel.Name
	model.FunctionUid = newModel.FunctionUid
	model.FunctionDeclareUid = newModel.FunctionDeclareUid
	model.ContractUid = newModel.ContractUid
	model.Available = newModel.Available

	if err := ctl.db.Save(model).Error; err != nil {
		ctl.logger.Error("save functionBinding by name failed", zap.Error(err))
		c.JSON(http.StatusInternalServerError, "save functionBinding by name failed")
		return
	}
	c.JSON(http.StatusOK, model.ToView())
}

func (ctl *CoreControllerV1) putFuncBindingByUid(c *gin.Context, uid uint64, newModel *objects.FunctionBindingModel) {

	model := objects.FunctionBindingModel{}
	if err := ctl.db.First(&model, uid).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			c.Status(http.StatusNotFound)
			return
		} else {
			c.JSON(http.StatusInternalServerError, "find functionBinding by name failed")
			return
		}
	}

	//更新该functionBinding对象
	model.Name = newModel.Name
	model.FunctionUid = newModel.FunctionUid
	model.FunctionDeclareUid = newModel.FunctionDeclareUid
	model.ContractUid = newModel.ContractUid
	model.Available = newModel.Available

	if err := ctl.db.Save(model).Error; err != nil {
		ctl.logger.Error("save functionBinding by name failed", zap.Error(err))
		c.JSON(http.StatusInternalServerError, "save functionBinding by name failed")
		return
	}
	c.JSON(http.StatusOK, model.ToView())
}

// PutFuncBinding 更改私有函数绑定
// @Summary 更改私有函数绑定API
// @Description 按照请求更改私有函数绑定, 返回更改后的私有函数绑定
// @Tags FunctionBinding 私有函数绑定
// @Accept application/json
// @Produce application/json
// @Param name    path string           true "要更新的私有函数绑定对象的名称或uid"
// @Param newFunc body objects.FunctionBinding true "要更新的新私有函数绑定对象"
// @Success 200 {object} objects.FunctionBinding "更新成功, 返回更新后的对象"
// @Failure 401 {string} string "对象格式有误"
// @Failure 404 "找不到对应的私有对象"
// @Router /core/v1/functionbinding/{name} [put]
func (ctl *CoreControllerV1) PutFuncBinding(c *gin.Context) {
	name := c.Param("name") //取得URL中参数
	if len(name) == 0 {
		c.JSON(http.StatusBadRequest, "name can't be empty")
	}

	view := objects.FunctionBinding{}
	if err := c.ShouldBind(&view); err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}

	if view.ApiVersion != "core/v1" || view.Kind != "functionbinding" {
		c.JSON(http.StatusBadRequest, "invalid apiVersion and kind")
		return
	}

	if !IsValidRFC1035(view.Metadata.Name) {
		c.JSON(http.StatusBadRequest, "invalid name")
		return
	}

	model := view.ToModel()
	ctl.logger.Info("PutFuncBinding: update funcBinding", zap.String("name", name), zap.Any("funcBinding", view))

	first := name[0]
	if first <= '9' && first >= '0' {
		uid, err := strconv.ParseUint(name, 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, uid)
			return
		}
		ctl.putFuncBindingByUid(c, uid, &model)
	} else {
		ctl.putFuncBindingByName(c, name, &model)
	}
}
