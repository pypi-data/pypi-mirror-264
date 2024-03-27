//go:build debug

// 这个文件定义的是测试版本的IChainDebug
// 所以包含了实际的测试用接口
// 这个文件只会在启用debug编译标记的情况下被编译
// 这个文件与debugInterface.go是一对.
// 两个文件仅会有一个被编译

package chain

// IChainDebug 调试用的区块链接口.
// 这个接口仅在测试版本有效,
// 在生产版本中, 这个接口是一个空接口.
type IChainDebug interface {
	/// ReInit 重置链上状态, 恢复到合约刚创建并初始化的状态.
	ReInit() error

	/// NextUid 返回链上的next_uid, 仅用于测试
	NextUid() (uint64, error)
}
