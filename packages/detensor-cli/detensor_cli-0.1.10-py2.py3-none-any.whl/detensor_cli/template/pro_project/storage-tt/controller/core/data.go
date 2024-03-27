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

// CreateData 创建私有数据
// @Summary 创建私有数据API
// @Schemes
// @Description 按照请求创建私有数据, 返回创建的私有数据
// @Tags Data 私有数据
// @Accept application/json
// @Produce application/json
// @Param data body objects.Data true "待创建的私有数据对象"
// @Success 201 {object} objects.Data "私有数据对象创建成功"
// @Router /core/v1/data [post]
func (ctl *CoreControllerV1) CreateData(c *gin.Context) {
	var count int64
	data := &objects.Data{}
	if err := c.ShouldBind(data); err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}

	if data.ApiVersion != "core/v1" || data.Kind != "data" {
		c.JSON(http.StatusBadRequest, "invalid apiVersion and kind")
		return
	}

	if !IsValidRFC1035(data.Metadata.Name) {
		c.JSON(http.StatusBadRequest, "invalid name")
		return
	}

	db := ctl.db
	dataModel := data.ToModel()

	temp := &objects.DataModel{}
	dataName := data.Metadata.Name //取得URL中参数
	ctl.logger.Info("CreateData:", zap.Any("data", data))
	//查找在存储中是否存在与要创建的data对象重名的data对象
	if err := db.Where("name=?", dataName).Find(&temp).Count(&count).Error; err != nil {
		ctl.logger.Error("failed in CreateData when check duplicated data name: ", zap.Error(err))
		c.JSON(http.StatusNotImplemented, "failed in CreateData when check duplicated data name")
		return
	}
	//重名
	if count != 0 {
		ctl.logger.Error("duplicated data name:", zap.String("data_name", dataName))
		c.JSON(http.StatusNotImplemented, data)
		return
	} else {
		//未重名，保存到私有存储中
		if err := db.Create(&dataModel).Error; err != nil {
			ctl.logger.Error("failed in CreateData when create a data", zap.Error(err))
			c.JSON(http.StatusNotImplemented, data)
		} else {
			ctl.logger.Info("CreateData succeed:", zap.Any("data", data))
			c.JSON(http.StatusCreated, dataModel.ToView())
		}
	}
}

// FindData 查找私有数据对象
// @Summary 查找私有数据对象 API
// @Schemes
// @Description 按照请求创建私有数据, 返回创建的私有数据
// @Tags Data 私有数据
// @Accept application/json
// @Produce application/json
// @Param declare query uint64 false  "限制私有数据对象要属于某个数据声明"
// @Param contract query uint64 false "限制私有数据对象要被某个计算合约使用"
// @Success 201 {array} objects.Data "查找出的私有数据对象"
// @Router /core/v1/data [get]
func (ctl *CoreControllerV1) FindData(c *gin.Context) {

	datas := []objects.Data{}
	dataModels := []objects.DataModel{}
	var err error = nil

	declare := c.Query("declare")
	var declareUid uint64
	if declare != "" {
		declareUid, err = strconv.ParseUint(declare, 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, "invalid declare uid: "+err.Error())
			return
		}
	}

	contract := c.Query("contract")
	var contractUid uint64
	if contract != "" {
		contractUid, err = strconv.ParseUint(contract, 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, "invalid declare uid: "+err.Error())
			return
		}
	}

	if declare == "" && contract == "" {
		db := ctl.db
		ctl.logger.Info("FindData: find all data instances")
		if err := db.Find(&dataModels).Error; err != nil {
			ctl.logger.Error("failed in FindData", zap.Error(err))
			c.JSON(http.StatusNotImplemented, "failed in FindData")
		} else {

			for _, f := range dataModels {
				datas = append(datas, f.ToView())
			}
			ctl.logger.Info("FindData succeed", zap.Any("data", datas))
			c.JSON(http.StatusOK, datas)
		}
		return
	}

	SQL := `SELECT * 
		FROM data_models 
		INNER JOIN data_binding_models b ON data_models.id = b.data_uid
		WHERE 1=1 
		`
	args := []interface{}{}

	if declare != "" {
		SQL += " and b.data_declare_uid = ?"
		args = append(args, declareUid)
	}

	if contract != "" {
		SQL += " and b.contract_uid = ?"
		args = append(args, contractUid)
	}

	if err := ctl.db.Raw(SQL, args...).Scan(&dataModels).Error; err != nil {
		ctl.logger.Error("find data failed",
			zap.String("declare", declare),
			zap.String("contract", contract),
			zap.Error(err))
		c.JSON(http.StatusInternalServerError, "find data failed")
		return
	}

	for _, f := range dataModels {
		datas = append(datas, f.ToView())
	}
	ctl.logger.Info("FindData succeed", zap.Any("data", datas))
	c.JSON(http.StatusOK, datas)
}

func (ctl *CoreControllerV1) findDataByName(c *gin.Context, name string) {
	model := objects.DataModel{}
	if err := ctl.db.Where("name = ?", name).First(&model).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			c.Status(http.StatusNotFound)
		} else {
			ctl.logger.Error("failed in findDataByUid:", zap.Error(err))
			c.JSON(http.StatusInternalServerError, "failed in FindDataByName")
		}
		return
	}
	c.JSON(http.StatusOK, model.ToView())
	return
}

func (ctl *CoreControllerV1) findDataByUid(c *gin.Context, uid uint64) {
	model := objects.DataModel{}
	if err := ctl.db.First(&model, uid).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			c.Status(http.StatusNotFound)
		} else {
			ctl.logger.Error("failed in findDataByName:", zap.Error(err))
			c.JSON(http.StatusInternalServerError, "failed in FindDataByName")
		}
		return
	}
	c.JSON(http.StatusOK, model.ToView())
}

// FindData 按照名称查找私有数据对象
// @Summary 按照名称查找私有数据对象 API
// @Schemes
// @Description 根据私有数据对象的名称,在本地数据库中查找私有数据对象
// @Tags Data 私有数据
// @Accept application/json
// @Produce application/json
// @Param name path string true "私有数据对象的名称或uid"
// @Success 201 {array} objects.Data "查找出的私有数据对象"
// @Router /core/v1/data/{name} [get]
func (ctl *CoreControllerV1) FindDataByName(c *gin.Context) {

	name := c.Param("name") //取得URL中参数
	if len(name) == 0 {
		c.JSON(http.StatusBadRequest, "name can't be empty")
		return
	}

	first := name[0]
	if first >= '0' && first <= '9' {
		uid, err := strconv.ParseUint(name, 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, "parse uid failed:"+err.Error())
			return
		}
		ctl.findDataByUid(c, uid)
	} else {
		ctl.findDataByName(c, name)
	}
}

func (ctl *CoreControllerV1) deleteDataByName(c *gin.Context, name string) {
	ctl.logger.Info("deleteDataByName:", zap.String("name", name))
	model := objects.DataModel{}

	if result := ctl.db.Where("name = ?", name).Delete(&model); result.Error != nil {
		ctl.logger.Error("delete data by name failed:", zap.Error(result.Error))
		c.JSON(http.StatusInternalServerError, "delete data by uid failed")
		return
	} else if result.RowsAffected == 0 {
		c.Status(http.StatusNotFound)
		return
	}
	c.JSON(http.StatusOK, model.ToView())
	return
}

func (ctl *CoreControllerV1) deleteDataByUid(c *gin.Context, uid uint64) {
	ctl.logger.Info("deleteDataByUid:", zap.Uint64("uid", uid))
	model := objects.DataModel{}

	if result := ctl.db.Delete(&model, uid); result.Error != nil {
		ctl.logger.Error("delete data by uid failed:", zap.Error(result.Error))
		c.JSON(http.StatusInternalServerError, "delete data by uid failed")
		return
	} else if result.RowsAffected == 0 {
		c.Status(http.StatusNotFound)
		return
	}
	c.JSON(http.StatusOK, model.ToView())
	return
}

// DeleteDataByName 删除私有数据
// @Summary 删除私有数据API
// @Schemes
// @Description 按照请求删除私有数据, 返回删除的私有数据
// @Tags Data 私有数据
// @Accept application/json
// @Produce application/json
// @Param name path string true "要删除的私有数据对象的名称和uid"
// @Success 200 {object} objects.Data "删除成功, 返回删除的对象"
// @Failure 404 "找不到对应的私有对象"
// @Router /core/v1/data/{name} [delete]
func (ctl *CoreControllerV1) DeleteDataByName(c *gin.Context) {

	dataName := c.Param("name") //取得URL中参数
	if len(dataName) == 0 {
		c.JSON(http.StatusBadRequest, "name can't be empty")
		return
	}
	ctl.logger.Info("DeleteDataByName:", zap.String("data_name", dataName))
	first := dataName[0]
	if first >= '0' && first <= '9' {
		uid, err := strconv.ParseUint(dataName, 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, "parse uid failed:"+err.Error())
			return
		} else {
			ctl.deleteDataByUid(c, uid)
		}
	} else {
		ctl.deleteDataByName(c, dataName)
	}
	return
}

func (ctl *CoreControllerV1) putDataByName(c *gin.Context, name string, data *objects.Data) {
	newModel := data.ToModel()
	model := objects.DataModel{}
	if err := ctl.db.Where("name = ?", name).First(&model).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			c.Status(http.StatusNotFound)
			return
		} else {
			c.JSON(http.StatusInternalServerError, "find data by name failed")
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
		ctl.logger.Error("save data by name failed", zap.Error(err))
		c.JSON(http.StatusInternalServerError, "save data by name failed")
		return
	}
	c.JSON(http.StatusOK, model.ToView())
}

func (ctl *CoreControllerV1) putDataByUid(c *gin.Context, uid uint64, data *objects.Data) {
	newModel := data.ToModel()
	model := objects.DataModel{}
	if err := ctl.db.First(&model, uid).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			c.Status(http.StatusNotFound)
			return
		} else {
			c.JSON(http.StatusInternalServerError, "find data by name failed")
			return
		}
	}

	if newModel.Id != 0 && newModel.Id != uid {
		c.JSON(http.StatusBadRequest, "can't change uid")
		return
	}

	model.Name = newModel.Name
	model.Content = newModel.Content
	model.Description = newModel.Description
	model.Available = newModel.Available

	if err := ctl.db.Save(model).Error; err != nil {
		ctl.logger.Error("save data by name failed", zap.Error(err))
		c.JSON(http.StatusInternalServerError, "save data by name failed")
		return
	}
	c.JSON(http.StatusOK, model.ToView())
}

// PutData 更改私有数据
// @Summary 更改私有数据API
// @Schemes
// @Description 按照请求更改数据, 返回更改后的私有数据
// @Tags Data 私有数据
// @Accept application/json
// @Produce application/json
// @Param name    path string       true "要更新的私有数据对象的名称或uid"
// @Param newData body objects.Data true "要更新的新私有数据对象"
// @Success 200 {object} objects.Data "更新成功, 返回更新后的对象"
// @Failure 401 {string} string "对象格式有误"
// @Failure 404 "找不到对应的私有对象"
// @Router /core/v1/data/{name} [put]
func (ctl *CoreControllerV1) PutData(c *gin.Context) {
	data := objects.Data{}
	dataName := c.Param("name") //取得URL中参数
	if err := c.ShouldBind(&data); err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}

	if data.ApiVersion != "core/v1" || data.Kind != "data" {
		c.JSON(http.StatusBadRequest, "invalid apiVersion or kind")
		return
	}

	if !IsValidRFC1035(data.Metadata.Name) {
		c.JSON(http.StatusBadRequest, "invalid name")
		return
	}

	ctl.logger.Info("PutData: update an exist data instance", zap.String("name", dataName), zap.Any("data", data))

	first := dataName[0]
	if first >= '0' && first <= '9' {
		uid, err := strconv.ParseUint(dataName, 10, 64)
		if err != nil {
			c.JSON(http.StatusBadRequest, "parse uid failed")
			return
		}
		ctl.putDataByUid(c, uid, &data)
		return
	} else {
		ctl.putDataByName(c, dataName, &data)
		return
	}

}
