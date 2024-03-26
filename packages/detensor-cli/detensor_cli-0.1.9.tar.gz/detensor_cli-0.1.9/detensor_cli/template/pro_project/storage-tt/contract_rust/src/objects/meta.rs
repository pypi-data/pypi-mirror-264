use std::{collections::BTreeMap, fmt::Display};

use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

/// 类型元对象, 用来描述对象所属的API组和类型
#[derive(Debug, Serialize, Deserialize, JsonSchema, PartialEq, Eq, Hash, Clone)]
#[serde(rename_all = "camelCase")]
pub struct TypeMeta {
    /// 对象所属的API版本
    pub api_version: String,

    /// 对象类型名
    pub kind: String,
}

impl Display for TypeMeta {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_fmt(format_args!("({}, {})", self.api_version, self.kind))
    }
}

/// 元数据对象, 描述对象的名称和UID
#[derive(Serialize, Deserialize, JsonSchema, Eq, PartialEq, Debug)]
#[serde(rename_all = "camelCase")]
pub struct Metadata {
    /// 对象名称
    pub name: String,

    /// 对象所属命名空间, 可能是空的
    pub namespace: Option<String>,

    /// 对象UID
    #[serde(default)]
    pub uid: u64,

    /// 对象注解
    #[serde(default)]
    pub annotations: Option<BTreeMap<String, serde_json::Value>>,
}

/// 包含命名空间的元数据对象, 描述对象的名称和UID
#[derive(Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct NamespacedMetadata {
    /// 对象名称
    pub name: String,

    /// 对象所属命名空间, 可能是空的
    pub namespace: String,

    /// 对象UID
    #[serde(default)]
    pub uid: u64,

    /// 对象注解
    #[serde(default)]
    pub annotations: Option<BTreeMap<String, serde_json::Value>>,
}

/// 命名空间下的提议的元数据
#[derive(Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct ProposalMetadata {
    /// 提议名称
    pub name: String,

    /// 提议所属命名空间
    pub namespace: String,

    /// 提议对象的uid
    #[serde(default)]
    pub uid: u64,

    /// 创建提议对象的组织
    #[serde(default)]
    pub creator: String,
}

/// 命名空间下的提议的元数据
#[derive(Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct GlobalProposalMetadata {
    /// 提议名称
    pub name: String,

    /// 提议对象的uid
    #[serde(default)]
    pub uid: u64,

    /// 创建提议对象的组织
    #[serde(default)]
    pub creator: String,
}
