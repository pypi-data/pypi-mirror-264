//go:build !debug

// 这个文件定义的是生产版本的IChainDebug
// 所以是个空文件
// 这个文件只会在没有启用debug编译标记的情况下被编译
// 这个文件与debugInterface_debug.go是一对.
// 两个文件仅会有一个被编译

package chain

// IChainDebug 调试用的区块链接口.
// 这个接口仅在测试版本有效,
// 在生产版本中, 这个接口是一个空接口.
type IChainDebug interface {
}
