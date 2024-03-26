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

// CreateDataBinding 创建私有数据绑定
// @Summary 创建私有数据绑定API
// @Schemes
// @Description 按照请求创建私有数据绑定, 返回创建的私有数据绑定
// @Tags DataBinding 私有数据绑定
// @Accept application/json
// @Produce application/json
// @Param dataBinding body objects.DataBinding true "待创建的私有数据绑定对象"
// @Success 201 {object} objects.DataBinding "私有数据绑定对象创建成功"
// @Router /core/v1/databinding [post]
func (ctl *CoreControllerV1) CreateDataBinding(c *gin.Context) {
	var count int64
	dataBinding := &objects.DataBinding{}
	if err := c.ShouldBind(dataBinding); err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}

	if dataBinding.ApiVersion != "core/v1" || dataBinding.Kind != "databinding" {
		c.JSON(http.StatusBadRequest, "invalid apiVersion and kind")
		return
	}

	if !IsValidRFC1035(dataBinding.Metadata.Name) {
		c.JSON(http.StatusBadRequest, "invalid name")
		return
	}

	db := ctl.db
	dataBindingModel := dataBinding.ToModel()

	temp := &objects.DataBindingModel{}
	dataBindingName := dataBinding.Metadata.Name //取得URL中参数
	ctl.logger.Info("CreateDataBinding:", zap.Any("dataBinding", dataBinding))
	//查找在存储中是否存在与要创建的dataBinding对象重名的dataBinding对象
	if err := db.Where("name=?", dataBindingName).Find(&temp).Count(&count).Error; err != nil {
		ctl.logger.Error("failed in CreateDataBinding when check duplicated dataBinding name: ", zap.Error(err))
		c.JSON(http.StatusNotImplemented, "failed in CreateDataBinding when check duplicated dataBinding name")
		return
	}
	//重名
	if count != 0 {
		ctl.logger.Error("duplicated dataBinding name:", zap.String("data_binding_name", dataBindingName))
		c.JSON(http.StatusNotImplemented, dataBinding)
		return
	} else {
		//未重名，保存到私有存储中
		if err := db.Create(&dataBindingModel).Error; err != nil {
			ctl.logger.Error("failed in CreateDataBinding when create a dataBinding", zap.Error(err))
			c.JSON(http.StatusNotImplemented, dataBinding)
		} else {
			ctl.logger.Info("CreateDataBinding succeed:", zap.Any("dataBinding", dataBinding))
			c.JSON(http.StatusCreated, dataBinding)
		}
	}
}

// FindDataBinding 查找私有数据绑定对象
// @Summary 查找私有数据绑定对象 API
// @Schemes
// @Description 按照请求创建私有数据绑定, 返回创建的私有数据绑定
// @Tags DataBinding 私有数据绑定
// @Accept application/json
// @Produce application/json
// @Param contract query uint64 false "私有数据绑定对应的合约的UID"
// @Param declare query uint64 false "私有数据绑定对应的数据声明UID"
// @Param data query uint64 false "私有数据绑定对应的数据UID"
// @Success 201 {array} objects.DataBinding "查找出的私有数据绑定对象"
// @Router /core/v1/databinding [get]
func (ctl *CoreControllerV1) FindDataBinding(c *gin.Context) {

	dataBindings := []objects.DataBinding{}
	dataBindingModels := []objects.DataBindingModel{}

	contract := c.Query("contract")
	declare := c.Query("declare")
	data := c.Query("data")

	db := ctl.db

	if contract != "" {
		uid, err := strconv.ParseUint(contract, 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, "parse contract uid failed: "+err.Error())
			return
		}
		db = db.Where("contract_uid = ?", uid)
	}

	if declare != "" {
		uid, err := strconv.ParseUint(declare, 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, "parse declare uid failed: "+err.Error())
			return
		}
		db = db.Where("data_declare_uid = ?", uid)
	}

	if data != "" {
		uid, err := strconv.ParseUint(data, 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, "parse data uid failed: "+err.Error())
			return
		}
		db = db.Where("data_uid = ?", uid)
	}

	ctl.logger.Info("FindDataBinding: find all dataBinding instances")
	if err := db.Find(&dataBindingModels).Error; err != nil {
		ctl.logger.Error("failed in FindDataBinding", zap.Error(err))
		c.JSON(http.StatusNotImplemented, "failed in FindDataBinding")
		return
	} else {
		for _, f := range dataBindingModels {
			dataBindings = append(dataBindings, f.ToView())
		}
		ctl.logger.Info("FindDataBinding succeed", zap.Any("dataBinding", dataBindings))
		c.JSON(http.StatusOK, dataBindings)
	}

}

func (ctl *CoreControllerV1) findDataBindingByName(c *gin.Context, name string) {
	db := ctl.db
	model := objects.DataBindingModel{}
	ctl.logger.Info("FindDataBindingByName:", zap.String("name", name))
	if err := db.Where("name = ?", name).First(&model).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			c.Status(http.StatusNotFound)
			return
		}
		ctl.logger.Error("failed in FindDataBindingByName: ", zap.Error(err))
		c.JSON(http.StatusInternalServerError, "failed in FindDataBindingByName")
	} else {
		view := model.ToView()
		ctl.logger.Info("FindDataBindingByName succeed", zap.Any("dataBinding", view))
		c.JSON(http.StatusOK, view)
	}
}

func (ctl *CoreControllerV1) findDataBindingByUid(c *gin.Context, uid uint64) {
	db := ctl.db
	model := objects.DataBindingModel{}
	ctl.logger.Info("FindDataBindingByUid:", zap.Uint64("uid", uid))
	if err := db.First(&model, uid).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			c.Status(http.StatusNotFound)
			return
		}
		ctl.logger.Error("failed in FindDataBindingByUid: ", zap.Error(err))
		c.JSON(http.StatusInternalServerError, "failed in FindDataBindingByUid")
	} else {
		view := model.ToView()
		ctl.logger.Info("FindDataBindingByName succeed", zap.Any("dataBinding", view))
		c.JSON(http.StatusOK, view)
	}
}

// FindDataBindingByName 按照名称查找私有数据绑定对象
// @Summary 按照名称查找私有数据绑定对象 API
// @Schemes
// @Description 根据私有数据绑定对象的名称,在本地数据库中查找私有数据绑定对象
// @Tags DataBinding 私有数据绑定
// @Accept application/json
// @Produce application/json
// @Param name path string true "私有数据绑定对象的名称或uid"
// @Success 201 {array} objects.DataBinding "查找出的私有数据绑定对象"
// @Router /core/v1/databinding/{name} [get]
func (ctl *CoreControllerV1) FindDataBindingByName(c *gin.Context) {
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
		ctl.findDataBindingByUid(c, uid)
	} else {
		ctl.findDataBindingByName(c, name)
	}
	return
}

func (ctl *CoreControllerV1) deleteDataBindingByName(c *gin.Context, name string) {

	db := ctl.db
	model := objects.DataBindingModel{}

	ctl.logger.Info("deleteDataBindingByName:", zap.String("name", name))
	if result := db.Where("name=?", name).Delete(&model); result.Error != nil {
		ctl.logger.Error("failed in deleteDataBindingByName ", zap.Error(result.Error))
		c.JSON(http.StatusInternalServerError, "failed in deleteDataBindingByName")
		return
	} else if result.RowsAffected == 0 {
		c.Status(http.StatusNotFound)
		return
	}
	c.JSON(http.StatusOK, model.ToView())
}

func (ctl *CoreControllerV1) deleteDataBindingByUid(c *gin.Context, uid uint64) {
	db := ctl.db
	model := objects.DataBindingModel{}

	ctl.logger.Info("deleteDataBindingByUid:", zap.Uint64("uid", uid))
	if result := db.Delete(&model, uid); result.Error != nil {
		ctl.logger.Error("failed in deleteDataBindingByUid ", zap.Error(result.Error))
		c.JSON(http.StatusInternalServerError, "failed in deleteDataBindingByName")
		return
	} else if result.RowsAffected == 0 {
		c.Status(http.StatusNotFound)
		return
	}
	c.JSON(http.StatusOK, model.ToView())
}

// DeleteDataBinding 删除私有数据绑定
// @Summary 删除私有数据绑定 API
// @Description 按照请求删除私有数据绑定, 返回删除的私有数据绑定
// @Tags DataBinding 私有数据绑定
// @Accept application/json
// @Produce application/json
// @Param name path string true "要删除的私有数据绑定对象的名称或uid"
// @Success 200 {object} objects.DataBinding "删除成功, 返回删除的对象"
// @Failure 404 "找不到对应的私有对象"
// @Router /core/v1/databinding/{name} [delete]
func (ctl *CoreControllerV1) DeleteDataBinding(c *gin.Context) {

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
		ctl.deleteDataBindingByUid(c, uid)
	} else {
		ctl.deleteDataBindingByName(c, name)
	}
}

func (ctl *CoreControllerV1) putDataBindingByName(c *gin.Context, name string, newModel *objects.DataBindingModel) {
	model := objects.DataBindingModel{}
	if err := ctl.db.Where("name = ?", name).First(&model).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			c.Status(http.StatusNotFound)
			return
		} else {
			c.JSON(http.StatusInternalServerError, "find databinding by name failed")
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
	model.DataUid = newModel.DataUid
	model.DataDeclareUid = newModel.DataDeclareUid
	model.ContractUid = newModel.ContractUid
	model.Available = newModel.Available

	if err := ctl.db.Save(model).Error; err != nil {
		ctl.logger.Error("save databinding by name failed", zap.Error(err))
		c.JSON(http.StatusInternalServerError, "save databinding by name failed")
		return
	}
	c.JSON(http.StatusOK, model.ToView())
}

func (ctl *CoreControllerV1) putDataBindingByUid(c *gin.Context, uid uint64, newModel *objects.DataBindingModel) {

	model := objects.DataBindingModel{}
	if err := ctl.db.First(&model, uid).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			c.Status(http.StatusNotFound)
			return
		} else {
			c.JSON(http.StatusInternalServerError, "find databinding by name failed")
			return
		}
	}

	model.Name = newModel.Name
	model.DataUid = newModel.DataUid
	model.DataDeclareUid = newModel.DataDeclareUid
	model.ContractUid = newModel.ContractUid
	model.Available = newModel.Available

	if err := ctl.db.Save(model).Error; err != nil {
		ctl.logger.Error("save function by name failed", zap.Error(err))
		c.JSON(http.StatusInternalServerError, "save databinding by name failed")
		return
	}
	c.JSON(http.StatusOK, model.ToView())
}

// PutDataBinding 更改私有数据绑定
// @Summary 更改私有数据绑定API
// @Description 按照请求更改私有数据绑定, 返回更改后的私有数据绑定
// @Tags DataBinding 私有数据绑定
// @Accept application/json
// @Produce application/json
// @Param name    path string           true "要更新的私有数据绑定对象的名称或uid"
// @Param newDataBinding body objects.DataBinding true "要更新的新私有数据绑定对象"
// @Success 200 {object} objects.DataBinding "更新成功, 返回更新后的对象"
// @Failure 401 {string} string "对象格式有误"
// @Failure 404 "找不到对应的私有对象"
// @Router /core/v1/databinding/{name} [put]
func (ctl *CoreControllerV1) PutDataBinding(c *gin.Context) {

	name := c.Param("name") //取得URL中参数
	if len(name) == 0 {
		c.JSON(http.StatusBadRequest, "name can't be empty")
	}

	view := objects.DataBinding{}
	if err := c.ShouldBind(&view); err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}

	if view.ApiVersion != "core/v1" || view.Kind != "databinding" {
		c.JSON(http.StatusBadRequest, "invalid apiVersion and kind")
		return
	}

	if !IsValidRFC1035(view.Metadata.Name) {
		c.JSON(http.StatusBadRequest, "invalid name")
		return
	}

	model := view.ToModel()
	ctl.logger.Info("PutDataBinding: update dataBinding", zap.String("name", name), zap.Any("dataBinding", view))

	first := name[0]
	if first <= '9' && first >= '0' {
		uid, err := strconv.ParseUint(name, 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, uid)
			return
		}
		ctl.putDataBindingByUid(c, uid, &model)
	} else {
		ctl.putDataBindingByName(c, name, &model)
	}
}
