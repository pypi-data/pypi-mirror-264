package core

import (
	"errors"
	"net/http"
	"strconv"

	"buaa.edu.cn/storage/objects"
	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
	"gorm.io/gorm"
)

// CreateFunc 创建私有函数
// @Summary 创建私有函数API
// @Schemes
// @Description 按照请求创建私有函数, 返回创建的私有函数
// @Tags Function 私有函数
// @Accept application/json
// @Produce application/json
// @Param function body objects.Function true "待创建的私有函数对象"
// @Success 201 {object} objects.Function "私有函数对象创建成功"
// @Router /core/v1/function [post]
func (ctl *CoreControllerV1) CreateFunc(c *gin.Context) {

	function := &objects.Function{}
	if err := c.ShouldBind(function); err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}

	if function.ApiVersion != "core/v1" || function.Kind != "function" {
		c.JSON(http.StatusBadRequest, "invalid api version and kind")
		return
	}

	if !IsValidRFC1035(function.Metadata.Name) {
		c.JSON(http.StatusBadRequest, "invalid name")
		return
	}

	db := ctl.db
	functionModel := function.ToModel()

	temp := &objects.FunctionModel{}
	functionName := function.Metadata.Name //取得URL中参数
	ctl.logger.Info("CreateFunc:", zap.Any("function", function))

	var count int64
	//查找在存储中是否存在与要创建的function对象重名的function对象
	if err := db.Where("name=?", functionName).Find(&temp).Count(&count).Error; err != nil {
		ctl.logger.Error("failed in CreateFunc when check duplicated function name: ", zap.Error(err))
		c.JSON(http.StatusConflict, "failed in CreateFunc when check duplicated function name")
		return
	}
	//重名
	if count != 0 {
		ctl.logger.Error("duplicated function name:", zap.String("function_name", functionName))
		c.JSON(http.StatusConflict, function)
		return
	} else {
		//未重名，保存到私有存储中
		if err := db.Create(&functionModel).Error; err != nil {
			ctl.logger.Error("failed in CreateFunc when create a function", zap.Error(err))
			c.JSON(http.StatusInternalServerError, function)
		} else {
			ctl.logger.Info("CreateFunction succeed:", zap.Any("function", function))
			c.JSON(http.StatusCreated, functionModel.ToView())
		}
	}
}

// FindFunc 查找私有函数对象
// @Summary 查找私有函数对象 API
// @Schemes
// @Description 按照请求创建私有函数, 返回创建的私有函数
// @Tags Function 私有函数
// @Accept application/json
// @Produce application/json
// @Param declare query uint64 false "限制私有函数对象要属于某个数据声明"
// @Param contract query uint64 false "限制私有函数对象要被某个计算合约使用"
// @Success 201 {array} objects.Function "查找出的私有函数对象"
// @Router /core/v1/function [get]
func (ctl *CoreControllerV1) FindFunc(c *gin.Context) {

	functions := []objects.Function{}
	functionModels := []objects.FunctionModel{}
	var err error = nil

	declare := c.Query("declare")
	var declareUid uint64
	if declare != "" {
		declareUid, err = strconv.ParseUint(declare, 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, "invalid declare uid:"+err.Error())
			return
		}
	}

	contract := c.Query("contract")
	var contractUid uint64
	if contract != "" {
		contractUid, err = strconv.ParseUint(contract, 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, "invalid contract uid:"+err.Error())
			return
		}
	}

	if declare == "" && contract == "" {
		db := ctl.db
		ctl.logger.Info("FindFunc: find all function instances")
		if err := db.Find(&functionModels).Error; err != nil {
			ctl.logger.Error("failed in FindFunc", zap.Error(err))
			c.JSON(http.StatusNotImplemented, "failed in FindFunc")
		} else {

			for _, f := range functionModels {
				functions = append(functions, f.ToView())
			}
			ctl.logger.Info("FindFunc succeed", zap.Any("function", functions))
			c.JSON(http.StatusOK, functions)
		}
		return
	}

	SQL := `SELECT *
		FROM function_models
		INNER JOIN function_binding_models b ON function_models.id = b.function_uid
		WHERE 1=1
	`
	args := []interface{}{}

	if declare != "" {
		SQL += " and b.function_declare_uid = ?"
		args = append(args, declareUid)
	}

	if contract != "" {
		SQL += " and b.contract_uid = ?"
		args = append(args, contractUid)
	}

	if err := ctl.db.Raw(SQL, args...).Scan(&functionModels).Error; err != nil {
		ctl.logger.Error("find function failed",
			zap.String("declare", declare),
			zap.String("contract", contract),
			zap.Error(err),
		)
		c.JSON(http.StatusInternalServerError, "find function failed")
		return
	}

	for _, f := range functionModels {
		functions = append(functions, f.ToView())
	}
	ctl.logger.Info("FindFunc succeed", zap.Any("function", functions))
	c.JSON(http.StatusOK, functions)
}

// FindFuncByName 按照名称查找私有函数对象
// @Summary 按照名称查找私有函数对象 API
// @Schemes
// @Description 根据私有函数对象的名称,在本地数据库中查找私有函数对象
// @Tags Function 私有函数
// @Accept application/json
// @Produce application/json
// @Param name path string true "私有函数对象的名称或uid"
// @Success 201 {array} objects.Function "查找出的私有函数对象"
// @Router /core/v1/function/{name} [get]
func (ctl *CoreControllerV1) FindFuncByName(c *gin.Context) {

	function := objects.Function{}
	functionModel := objects.FunctionModel{}

	db := ctl.db
	name := c.Param("name") //取得URL中参数
	if len(name) == 0 {
		c.JSON(http.StatusBadRequest, "name can't be empty")
		return
	}

	first := name[0]
	if first >= '0' && first <= '9' {
		ctl.logger.Info("FindFuncByName:", zap.String("uid", name))
		uid, err := strconv.ParseUint(name, 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, "invalid uid: "+err.Error())
			return
		}
		if err = db.First(&functionModel, uid).Error; err != nil {
			if errors.Is(err, gorm.ErrRecordNotFound) {
				c.JSON(http.StatusNotFound, "")
			} else {
				ctl.logger.Error("find function by uid failed:", zap.Error(err))
				c.JSON(http.StatusInternalServerError, err.Error())
			}
			return
		}
		c.JSON(http.StatusOK, functionModel.ToView())
		return
	} else {
		ctl.logger.Info("FindFuncByName:", zap.String("name", name))
		if err := db.Where("name=?", name).Find(&functionModel).Error; err != nil {
			ctl.logger.Error("failed in FindFuncByName: ", zap.Error(err))
			c.JSON(http.StatusNotFound, "failed in FindFuncByName")
		} else {
			function = functionModel.ToView()
			ctl.logger.Info("FindFuncByName succeed", zap.Any("function", function))
			c.JSON(http.StatusOK, function)
		}
		return
	}
}

func (ctl *CoreControllerV1) deleteFuncByName(c *gin.Context, name string) {
	ctl.logger.Info("DeleteFuncByName:", zap.String("name", name))

	db := ctl.db
	functionModel := objects.FunctionModel{}
	var count int64

	if err := db.Where("name=?", name).Find(&functionModel).Count(&count).Error; err != nil {
		ctl.logger.Error("failed in DeleteFuncByName when search for the function: ", zap.Error(err))
		c.JSON(http.StatusInternalServerError, "failed in DeleteFuncByName when search the function")
		return
	}

	if count == 0 {
		ctl.logger.Error("failed in DeleteFuncByName: no such function", zap.String("name", name))
		c.Status(http.StatusNotFound)
		return
	} else {
		if err := db.Where("name=?", name).Delete(&functionModel).Error; err != nil {
			ctl.logger.Error("DeleteFuncByName failed: ", zap.Error(err))
			c.JSON(http.StatusInternalServerError, "error")
			return
		}
		ctl.logger.Info("DeleteFuncByName succeed:", zap.Any("function", functionModel.ToView()))
		c.Status(http.StatusOK)
		return
	}
}

func (ctl *CoreControllerV1) deleteFuncByUid(c *gin.Context, uid uint64) {
	ctl.logger.Info("DeleteFuncByUid:", zap.Uint64("uid", uid))
	functionModel := objects.FunctionModel{}
	if err := ctl.db.Delete(&functionModel, uid).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			c.Status(http.StatusNotFound)
			return
		}
		c.JSON(http.StatusInternalServerError, "delete failed")
		return
	}
	c.JSON(http.StatusOK, functionModel.ToView())
	return
}

// DeleteFuncByName 删除私有函数
// @Summary 删除私有函数 API
// @Description 按照请求删除私有函数, 返回删除的私有函数
// @Tags Function 私有函数
// @Accept application/json
// @Produce application/json
// @Param name path string true "要删除的私有函数对象的名称, 或是UID"
// @Success 200 {object} objects.Function "删除成功, 返回删除的对象"
// @Failure 404 "找不到对应的私有对象"
// @Router /core/v1/function/{name} [delete]
func (ctl *CoreControllerV1) DeleteFuncByName(c *gin.Context) {
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
		ctl.deleteFuncByUid(c, uid)
		return
	} else {
		ctl.deleteFuncByName(c, name)
		return
	}
}

func (ctl *CoreControllerV1) putFuncByName(c *gin.Context, name string, function *objects.Function) {

	newModel := function.ToModel()
	model := objects.FunctionModel{}
	if err := ctl.db.Where("name = ?", name).First(&model).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			c.Status(http.StatusNotFound)
			return
		} else {
			c.JSON(http.StatusInternalServerError, "find function by name failed")
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

	model.Name = newModel.Name
	model.Content = newModel.Content
	model.Description = newModel.Description
	model.Available = newModel.Available

	if err := ctl.db.Save(model).Error; err != nil {
		ctl.logger.Error("save function by name failed", zap.Error(err))
		c.JSON(http.StatusInternalServerError, "save function by name failed")
		return
	}
	c.JSON(http.StatusOK, model.ToView())
}

func (ctl *CoreControllerV1) putFuncByUid(c *gin.Context, uid uint64, function *objects.Function) {
	ctl.logger.Info("PutFunc: update an exist function instance", zap.Uint64("uid", uid))

	newModel := function.ToModel()
	model := objects.FunctionModel{}
	if err := ctl.db.First(&model, uid).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			c.Status(http.StatusNotFound)
			return
		} else {
			c.JSON(http.StatusInternalServerError, "find function by uid failed")
			return
		}
	}

	// 允许用户省略uid
	if newModel.Id != 0 && newModel.Id != uid {
		c.JSON(http.StatusBadRequest, "can't change uid")
		return
	}

	model.Name = newModel.Name
	model.Content = newModel.Content
	model.Description = newModel.Description
	model.Available = newModel.Available

	if err := ctl.db.Save(model).Error; err != nil {
		ctl.logger.Error("save function by uid failed", zap.Error(err))
		c.JSON(http.StatusInternalServerError, "save function by uid failed")
		return
	}
	c.JSON(http.StatusOK, model.ToView())
}

// PutFunction 更改私有函数
// @Summary 更改私有函数API
// @Description 按照请求更改私有函数, 返回更改后的私有函数
// @Tags Function 私有函数
// @Accept application/json
// @Produce application/json
// @Param name    path string           true "要更新的私有函数对象的名称或uid"
// @Param newFunc body objects.Function true "要更新的新私有函数对象"
// @Success 200 {object} objects.Function "更新成功, 返回更新后的对象"
// @Failure 401 {string} string "对象格式有误"
// @Failure 404 "找不到对应的私有对象"
// @Router /core/v1/function/{name} [put]
func (ctl *CoreControllerV1) PutFunc(c *gin.Context) {

	name := c.Param("name") //取得URL中参数
	if len(name) == 0 {
		c.JSON(http.StatusBadRequest, "name can't be empty")
		return
	}

	function := objects.Function{}
	if err := c.ShouldBindJSON(&function); err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}

	if function.ApiVersion != "core/v1" || function.Kind != "function" {
		c.JSON(http.StatusBadRequest, "bad api version and kind")
		return
	}

	if !IsValidRFC1035(function.Metadata.Name) {
		c.JSON(http.StatusBadRequest, "invalid name")
		return
	}

	ctl.logger.Info("PutFunc: update an exist function instance",
		zap.String("name", name),
		zap.Any("function", function),
	)

	first := name[0]
	if first >= '0' && first <= '9' {
		uid, err := strconv.ParseUint(name, 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, "invalid uid")
			return
		}
		ctl.putFuncByUid(c, uid, &function)
		return
	} else {
		ctl.putFuncByName(c, name, &function)
		return
	}
}
