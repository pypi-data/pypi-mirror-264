package objects

type ContractMetadata struct {
	Uid       uint64 `json:"uid,omitempty"`
	Name      string `json:"name"`
	Namespace string `json:"namespace"`
	Version   string `json:"version"`
}

type ContractSpec struct {
	Content      string            `json:"content"`
	Data         map[string]uint64 `json:"data"`
	Functions    map[string]uint64 `json:"functions"`
	ExecPatterns [][]string        `json:"execPatterns"`
}

type Contract struct {
	TypeMeta
	Metadata ContractMetadata `json:"metadata"`
	Spec     ContractSpec     `json:"spec"`
}

type GetContractRes struct {
	Spec     ContractSpec      `json:"spec"`
	Data     map[string]uint64 `json:"data"`
	Function map[string]uint64 `json:"function"`
}
