use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use super::{ProposalStatus, ProposalSpec};
use crate::objects::{
    meta::{GlobalProposalMetadata, TypeMeta},
    BaseObject, BaseTypedObject, TypedObject,
};


#[derive(Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct GlobalProposal {
    /// 类型元数据
    #[serde(flatten)]
    pub type_meta: TypeMeta,

    /// 对象元数据
    pub metadata: GlobalProposalMetadata,

    /// Proposal的内容
    pub spec: ProposalSpec,

    /// Proposal的状态
    #[serde(default)]
    pub status: ProposalStatus,
}

impl GlobalProposal {
    /// 全局提议是否处于活跃状态
    pub fn is_active(&self) -> bool {
        self.status.stage.is_active()
    }

    /// 全局提议是否处于被撤回的状态
    pub fn is_revoked(&self) -> bool {
        self.status.stage.is_revoked()
    }

    /// 全局提议是否处于已经提交的状态
    pub fn is_committed(&self) -> bool {
        self.status.stage.is_submitted()
    }
}

impl BaseTypedObject for GlobalProposal {
    const API_VERSION: &'static str = "core/v1";

    const KIND: &'static str = "globalproposal";

    const NAMESPACED: bool = false;

    /// 合约暂时不接受任何调整
    fn controller() -> crate::objects::controller::Controller {
        crate::objects::controller::Controller {
            create: None,
            update: None,
            delete: None,
        }
    }
}

impl BaseObject for GlobalProposal {
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
        None
    }
}

impl TypedObject for GlobalProposal {}
