package objects

type Function struct {
	TypeMeta
	Metadata Metadata       `json:"metadata"`
	Spec     FunctionSpec   `json:"spec"`
	Status   FunctionStatus `json:"status,omitempty"`
}

func (f Function) ToModel() FunctionModel {
	// var fm FunctionModel
	fm := FunctionModel{
		Id:          f.Metadata.Uid,
		Name:        f.Metadata.Name,
		Content:     f.Spec.Content,
		Description: f.Spec.Description,
		Available:   f.Status.Available,
	}
	return fm
}

type FunctionSpec struct {
	Content     string `json:"content"`
	Description string `json:"description"`
}

type FunctionStatus struct {
	Available bool `json:"available"`
}

type FunctionModel struct {
	Id          uint64 `gorm:"id"`
	Name        string `gorm:"name"`
	Content     string `gorm:"content"`
	Description string `gorm:"description"`
	Available   bool   `gorm:"available"`
}

func (fm FunctionModel) ToView() Function {

	t := TypeMeta{
		ApiVersion: "core/v1",
		Kind:       "function",
	}
	m := Metadata{
		Name: fm.Name,
		Uid:  fm.Id,
	}
	sp := FunctionSpec{
		Content:     fm.Content,
		Description: fm.Description,
	}
	st := FunctionStatus{
		Available: fm.Available,
	}
	f := Function{
		TypeMeta: t,
		Metadata: m,
		Spec:     sp,
		Status:   st,
	}
	return f

}
