package objects

type FunctionBinding struct {
	TypeMeta
	Metadata Metadata              `json:"metadata"`
	Spec     FunctionBindingSpec   `json:"spec"`
	Status   FunctionBindingStatus `json:"status"`
}

type FunctionBindingSpec struct {
	FunctionUid        uint64 `json:"functionUid"`
	FunctionDeclareUid uint64 `json:"functionDeclareUid"`
	ContractUid        uint64 `json:"contractUid"`
}

type FunctionBindingStatus struct {
	Available bool `json:"available"`
}

type FunctionBindingModel struct {
	Id                 uint64 `gorm:"id"`
	Name               string `gorm:"name"`
	FunctionUid        uint64 `gorm:"function_uid"`
	FunctionDeclareUid uint64 `gorm:"function_declare_uid"`
	ContractUid        uint64 `gorm:"contract_uid"`
	Available          bool   `gorm:"available"`
}

func (f FunctionBinding) ToModel() FunctionBindingModel {

	fm := FunctionBindingModel{
		Id:                 f.Metadata.Uid,
		Name:               f.Metadata.Name,
		FunctionUid:        f.Spec.FunctionUid,
		FunctionDeclareUid: f.Spec.FunctionDeclareUid,
		ContractUid:        f.Spec.ContractUid,
		Available:          f.Status.Available,
	}
	return fm
}

func (fm FunctionBindingModel) ToView() FunctionBinding {

	t := TypeMeta{
		ApiVersion: "core/v1",
		Kind:       "functionbinding",
	}
	m := Metadata{
		Name: fm.Name,
		Uid:  fm.Id,
	}
	sp := FunctionBindingSpec{
		FunctionUid:        fm.FunctionUid,
		FunctionDeclareUid: fm.FunctionDeclareUid,
		ContractUid:        fm.ContractUid,
	}
	st := FunctionBindingStatus{
		Available: fm.Available,
	}
	f := FunctionBinding{
		TypeMeta: t,
		Metadata: m,
		Spec:     sp,
		Status:   st,
	}
	return f

}
