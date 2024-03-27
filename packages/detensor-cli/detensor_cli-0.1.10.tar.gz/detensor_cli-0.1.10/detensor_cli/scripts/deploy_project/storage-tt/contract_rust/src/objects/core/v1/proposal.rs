use std::collections::BTreeMap;

use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use crate::{
    errors::{ChainModelError, InvalidObjectError},
    model::ChainModel,
    objects::{
        controller::Controller,
        get_type_meta,
        meta::{ProposalMetadata, TypeMeta},
        BaseObject, BaseTypedObject, TypedObject,
    },
};

/// Proposal 的内容
#[derive(Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct ProposalSpec {
    /// Proposal 中包括的所有操作动作
    pub actions: Vec<ProposalAction>,
}

/// Proposal 中涉及的操作
#[derive(Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum ProposalAction {
    /// 创建对象操作
    Create(CreateObjectAction),
    /// 更新对象操作
    Update(UpdateObjectAction),
    /// 删除对象操作
    Delete(DeleteObjectAction),
}

impl ProposalAction {
    pub fn get_type_meta(&self, model: &ChainModel) -> Result<TypeMeta, ChainModelError> {
        match self {
            ProposalAction::Create(it) => {
                let meta = get_type_meta(&it.object)?;
                Ok(meta)
            }
            ProposalAction::Update(it) => {
                let uid = it.uid;
                if let Some(obj) = model.get_object_by_uid(uid)? {
                    Ok(TypeMeta {
                        api_version: obj.api_version().to_owned(),
                        kind: obj.kind().to_owned(),
                    })
                } else {
                    Err(InvalidObjectError::new("can't find object for update".to_string()).into())
                }
            }
            ProposalAction::Delete(it) => {
                let uid = it.uid;
                if let Some(obj) = model.get_object_by_uid(uid)? {
                    Ok(TypeMeta {
                        api_version: obj.api_version().to_owned(),
                        kind: obj.kind().to_owned(),
                    })
                } else {
                    Err(InvalidObjectError::new("can't find object for delete".to_string()).into())
                }
            }
        }
    }
}

/// 创建对象操作
#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct CreateObjectAction {
    /// 操作要创建的对象
    pub object: serde_json::Value,
}

/// 更新对象操作
#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct UpdateObjectAction {
    /// 操作要更新的对象的UID
    pub uid: u64,

    /// 操作要更新的对象
    pub object: serde_json::Value,
}

/// 删除对象操作
#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct DeleteObjectAction {
    /// 要删除对象的UID
    pub uid: u64,
}

/// 提议的生命周期
#[derive(Serialize, Deserialize, JsonSchema)]
pub enum ProposalStage {
    /// 活跃期, 提议可以被批准或提交
    Active,

    /// 合约已提交
    Submitted,

    /// 合约已撤回
    Revoked,
}

impl ProposalStage {
    /// 提议是否活跃
    pub fn is_active(&self) -> bool {
        return matches!(self, Self::Active);
    }

    /// 提议是否已经提交
    pub fn is_submitted(&self) -> bool {
        return matches!(self, Self::Submitted);
    }

    /// 提议是否已撤回
    pub fn is_revoked(&self) -> bool {
        return matches!(self, Self::Revoked);
    }
}

/// 提议提交后, 执行相关操作所产生的对象
#[derive(Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub enum ObjectByAction {
    /// 创建操作所产生的对象
    Create(serde_json::Value),
    /// 更新操作前后的对象
    Update{
        old: serde_json::Value, 
        updated: serde_json::Value
    },
    /// 删除操作所删对象
    Delete(serde_json::Value),
}

/// Proposal 的状态
#[derive(Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct ProposalStatus {
    /// 合约所属的状态
    pub stage: ProposalStage,

    /// 已经批准的组织名和批准的说明
    pub permission: BTreeMap<String, String>,

    /// 提交后, 执行操作所产生的对象
    #[serde(default)]
    pub results: Option<Vec<ObjectByAction>>,
}

impl ProposalStatus {
    /// 创建一个初始化的提议状态
    pub fn init(_actions: &[ProposalAction]) -> Self {
        ProposalStatus {
            stage: ProposalStage::Active,
            permission: BTreeMap::new(),
            results: None,
        }
    }
}

impl Default for ProposalStatus {
    fn default() -> Self {
        Self {
            stage: ProposalStage::Revoked,
            permission: Default::default(),
            results: Default::default(),
        }
    }
}

#[derive(Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct Proposal {
    /// 类型元数据
    #[serde(flatten)]
    pub type_meta: TypeMeta,

    /// 对象元数据
    pub metadata: ProposalMetadata,

    /// Proposal的内容
    pub spec: ProposalSpec,

    #[serde(default)]
    /// Proposal的状态
    pub status: ProposalStatus,
}

impl BaseTypedObject for Proposal {
    const API_VERSION: &'static str = "core/v1";

    const KIND: &'static str = "proposal";

    const NAMESPACED: bool = true;

    /// 合约暂时不接受任何调整
    fn controller() -> crate::objects::controller::Controller {
        Controller {
            create: None,
            update: None,
            delete: None,
        }
    }
}

impl BaseObject for Proposal {
    fn type_meta(&self) -> &TypeMeta {
        &self.type_meta
    }

    fn uid(&self) -> u64 {
        self.metadata.uid
    }

    fn uid_mut(&mut self) -> &mut u64 {
        &mut self.metadata.uid
    }

    fn name(&self) -> &str {
        &self.metadata.name
    }

    fn version(&self) -> Option<&str> {
        None
    }

    fn namespace(&self) -> Option<&str> {
        Some(&self.metadata.namespace)
    }
}

impl TypedObject for Proposal {}
