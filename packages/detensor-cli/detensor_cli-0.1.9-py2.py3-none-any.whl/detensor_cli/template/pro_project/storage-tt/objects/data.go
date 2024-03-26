package objects

type Data struct {
	TypeMeta
	Metadata Metadata   `json:"metadata"`
	Spec     DataSpec   `json:"spec"`
	Status   DataStatus `json:"status,omitempty"`
}

type DataSpec struct {
	Content     string `json:"content"`
	Description string `json:"description"`
}

type DataStatus struct {
	Available bool `json:"available"`
}

func (d Data) ToModel() DataModel {
	// var fm DataModel
	dm := DataModel{
		Id:          d.Metadata.Uid,
		Name:        d.Metadata.Name,
		Content:     d.Spec.Content,
		Description: d.Spec.Description,
		Available:   d.Status.Available,
	}
	return dm
}

type DataModel struct {
	Id          uint64 `gorm:"id"`
	Name        string `gorm:"name"`
	Content     string `gorm:"content"`
	Description string `gorm:"description"`
	Available   bool   `gorm:"available"`
}

func (dm DataModel) ToView() Data {

	t := TypeMeta{
		ApiVersion: "core/v1",
		Kind:       "data",
	}
	m := Metadata{
		Name: dm.Name,
		Uid:  dm.Id,
	}
	sp := DataSpec{
		Content:     dm.Content,
		Description: dm.Description,
	}
	st := DataStatus{
		Available: dm.Available,
	}
	d := Data{
		TypeMeta: t,
		Metadata: m,
		Spec:     sp,
		Status:   st,
	}
	return d

}
