/// chainmaker SDK
#[allow(clippy::all)]
pub mod chainmaker_sdk;

/// 我们自己封装的上下文
pub mod context;

/// 合约模块, 智能合约是在这个模块中实现的
pub mod contract;

/// 对象模块, 所有的存储对象的定义
pub mod objects;

/// 编码相关, 主要是用于对于数据库键进行编码.
pub mod codec;

/// 数据模型相关, 数据模型抽象层
pub mod model;

/// 错误类型定义相关.
pub mod errors;

// 一些工具函数的实现
pub mod utils;

/// 使用区块链进行的测试
mod tests;
