package objects

type DataBinding struct {
	TypeMeta
	Metadata Metadata          `json:"metadata"`
	Spec     DataBindingSpec   `json:"spec"`
	Status   DataBindingStatus `json:"status"`
}

type DataBindingSpec struct {
	DataUid        uint64 `json:"dataUid"`
	DataDeclareUid uint64 `json:"dataDeclareUid"`
	ContractUid    uint64 `json:"contractUid"`
}

type DataBindingStatus struct {
	Available bool `json:"available"`
}

type DataBindingModel struct {
	Id             uint64 `gorm:"id"`
	Name           string `gorm:"name"`
	DataUid        uint64 `gorm:"data_uid"`
	DataDeclareUid uint64 `gorm:"data_declare_uid"`
	ContractUid    uint64 `gorm:"contract_uid"`
	Available      bool   `gorm:"available"`
}

func (d DataBinding) ToModel() DataBindingModel {

	dm := DataBindingModel{
		Id:             d.Metadata.Uid,
		Name:           d.Metadata.Name,
		DataUid:        d.Spec.DataUid,
		DataDeclareUid: d.Spec.DataDeclareUid,
		ContractUid:    d.Spec.ContractUid,
		Available:      d.Status.Available,
	}
	return dm
}

func (dm DataBindingModel) ToView() DataBinding {

	t := TypeMeta{
		ApiVersion: "core/v1",
		Kind:       "databinding",
	}
	m := Metadata{
		Name: dm.Name,
		Uid:  dm.Id,
	}
	sp := DataBindingSpec{
		DataUid:        dm.DataUid,
		DataDeclareUid: dm.DataDeclareUid,
		ContractUid:    dm.ContractUid,
	}
	st := DataBindingStatus{
		Available: dm.Available,
	}
	d := DataBinding{
		TypeMeta: t,
		Metadata: m,
		Spec:     sp,
		Status:   st,
	}
	return d

}
