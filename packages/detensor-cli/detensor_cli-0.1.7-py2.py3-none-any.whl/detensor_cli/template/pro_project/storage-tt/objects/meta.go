package objects

type TypeMeta struct {
	ApiVersion string `json:"apiVersion"`
	Kind       string `json:"kind"`
}

type Metadata struct {
	Name string `json:"name"`
	Uid  uint64 `json:"uid,omitempty"`
}
