/// 命名空间相关对象
pub mod namespace;

pub use namespace::*;

/// 提议相关对象
pub mod proposal;

/// 全局提议相关对象
pub mod global_proposal;

pub use global_proposal::*;
pub use proposal::*;

/// 计算合约相关对象
pub mod contracts;

pub use contracts::*;

/// 声明相关对象
pub mod declare;

pub use declare::*;

/// 记录相关对象
pub mod record;

pub use record::*;