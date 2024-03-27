package chain

import (
	"encoding/json"

	"buaa.edu.cn/storage/objects"
)

// 提议相关的区块链的接口
type IChainProposal interface {
	// 创建一个提议, 返回提议对象的uid.
	// 参数是提议对象的JSON与提议所属的命名空间
	CreateProposal(object json.RawMessage, namespace string) (uint64, error)

	// 撤回一个提议
	RevokeProposal(uid uint64) error

	// 按照名称撤回提议
	RevokeProposalByName(namespace, name string) error

	// 提交一个提议, 返回该提议中所有 action 涉及的对象
	CommitProposal(uid uint64) ([]json.RawMessage, error)

	// 按照名称提交一个提议, 返回该提议中所有 action 涉及的对象
	CommitProposalByName(namespace, name string) ([]json.RawMessage, error)

	// 对一个提议设置, 设置本组织对该提议的批准状态
	// 返回合约是否已经可以提交
	PermitProposal(uid uint64, status bool, comment string) (bool, error)

	// 对一个提议设置, 设置本组织对该提议的批准状态.
	// 按照名称与命名空间选择提议.
	// 返回合约是否已经可以提交.
	PermitProposalByName(namespace, name string, status bool, comment string) (bool, error)

	// 创建一个全局提议, 返回提议对象的uid
	CreateGlobalProposal(object json.RawMessage) (uint64, error)

	// 撤回一个全局提议
	RevokeGlobalProposal(uid uint64) error

	// 按照名称撤回一个全局提议
	RevokeGlobalProposalByName(name string) error

	// 提交一个全局提议, 返回该提议中所有 action 涉及的对象
	CommitGlobalProposal(uid uint64) ([]json.RawMessage, error)

	// 按名称提交一个全局提议, 返回该提议中所有 action 涉及的对象
	CommitGlobalProposalByName(name string) ([]json.RawMessage, error)

	// 对一个全局提议进行批准, 设置本组织对该提议的批准状态
	// 返回合约是否已经可以提交
	PermitGlobalProposal(uid uint64, status bool, comment string) (bool, error)

	// 按照名称批准一个全局提议
	PermitGlobalProposalByName(name string, status bool, comment string) (bool, error)
}

type IChainDataDeclare interface {
	// 标注是否实现某个数据声明
	SetDataImplement(uid uint64, status bool, comment string) error

	// 标注是否实现某个数据声明
	SetDataImplementByName(namespace, name string, status bool, comment string) error
}

type IChainFunctionDeclare interface {
	// 标注是否实现某个函数声明
	SetFunctionImplement(uid uint64, status bool, comment string) error

	// 标注是否实现某个函数声明
	SetFunctionImplementByName(namespace, name string, status bool, comment string) error
}

// 对象相关的区块链接口
type IChainObject interface {
	// 根据uid查询对象内容
	GetObjectByUid(uid uint64) (json.RawMessage, error)

	// 根据名称查询对象内容
	// version 和 namespace 可以为空字符串
	GetObjectByName(apiVersion, kind, namespace, name, version string) (json.RawMessage, error)

	// 根据对象的种类查询对象, 应该返回对象的列表
	// 命名空间为空, 表示搜索所有命名空间下, 该对象类型的类型
	// 命名空间的资源, 如果命名空间为空, 则返回所有命名空间下该类型的对象
	GetObjectByKind(apiVersion, kind, namespace string) ([]json.RawMessage, error)

	// TODO: 淦子衡 设计这个接口对应的规范
	GetObjectWith(conds string) ([]json.RawMessage, error)
}

// 组织相关的区块链接口
type IChainOrg interface {
	// 获取链上的所有组织名称
	GetAllOrg() ([]string, error)
}

// 计算层直接需要的区块链接口
type IChainCompute interface {
	// 注册本组织的计算节点地址, 如果之前已经注册过, 将用新地址覆盖旧地址.
	RegisterNode(addr string) error

	// 注销本组织的计算节点地址.
	LogoutNode() error

	// 根据组织名称查询注册的计算节点地址.
	DiscoverNodes(orgs []string) (map[string]string, error)

	// 查询链上所有组织的计算节点地址
	DiscoverAllNodes() (map[string]string, error)

	GetContract(uid uint64) (*objects.GetContractRes, error)
}

// 各种区块链必须实现的接口
type IChain interface {
	IChainProposal
	IChainObject
	IChainOrg
	IChainCompute
	IChainDataDeclare
	IChainFunctionDeclare

	// 这个接口在生产环境中是一个空接口
	IChainDebug

	// 返回实现区块链实现的名称
	ProviderName() (string, error)
}
