use std::collections::BTreeMap;

use super::core::v1::{
    CreateObjectAction, DeleteObjectAction, ObjectByAction, ProposalAction, UpdateObjectAction,
};
use crate::{
    errors::{ActionFnError, ActionFnError::*},
    model::ChainModel,
};

type ActionFnSupport<T> = fn(ctx: &ChainModel, action: &T) -> Result<(), ActionFnError>;

type ActionFnRelevent<T> =
    fn(ctx: &ChainModel, action: &T, org_id: &str) -> Result<(), ActionFnError>;

type ActionFnCommitable<T> = fn(
    ctx: &ChainModel,
    action: &T,
    permitted: &BTreeMap<String, String>,
) -> Result<(), ActionFnError>;

// TODO: Check it.
type ActionFnExec<T> =
    fn(ctx: &mut ChainModel, action: &T) -> Result<ObjectByAction, ActionFnError>;

/// 一个资源动作相关的处理函数的集合
#[derive(Clone)]
pub struct ActionFn<T> {
    /// 判断动作是否支持的函数
    pub support: ActionFnSupport<T>,

    /// 判断批准是否与动作相关的函数
    pub relevent: ActionFnRelevent<T>,

    /// 判断动作是否已经可提交的函数
    pub commitable: ActionFnCommitable<T>,

    /// 动作具体执行的函数
    pub exec: ActionFnExec<T>,
}

/// 用于控制资源增删查改的控制器
#[derive(Clone)]
pub struct Controller {
    /// 创建对象的相关处理函数
    pub create: Option<ActionFn<CreateObjectAction>>,

    /// 更新对象的相关处理函数
    pub update: Option<ActionFn<UpdateObjectAction>>,

    /// 删除对象的相关处理函数
    pub delete: Option<ActionFn<DeleteObjectAction>>,
}

impl Controller {
    pub fn check_support(
        &self,
        model: &ChainModel,
        action: &ProposalAction,
    ) -> Result<(), ActionFnError> {
        match action {
            ProposalAction::Create(it) => {
                if let Some(f) = &self.create {
                    (f.support)(model, it)
                } else {
                    Err(ActionNotSupported(format!("{:?}", it)))
                }
            }
            ProposalAction::Update(it) => {
                if let Some(f) = &self.update {
                    (f.support)(model, it)
                } else {
                    Err(ActionNotSupported(format!("{:?}", it)))
                }
            }
            ProposalAction::Delete(it) => {
                if let Some(f) = &self.delete {
                    (f.support)(model, it)
                } else {
                    Err(ActionNotSupported(format!("{:?}", it)))
                }
            }
        }
    }

    pub fn check_relevent(
        &self,
        model: &ChainModel,
        action: &ProposalAction,
        org_id: &str,
    ) -> Result<(), ActionFnError> {
        match action {
            ProposalAction::Create(it) => {
                if let Some(f) = &self.create {
                    (f.relevent)(model, it, org_id)
                } else {
                    Err(ActionNotSupported(format!("{:?}", it)))
                }
            }
            ProposalAction::Update(it) => {
                if let Some(f) = &self.update {
                    (f.relevent)(model, it, org_id)
                } else {
                    Err(ActionNotSupported(format!("{:?}", it)))
                }
            }
            ProposalAction::Delete(it) => {
                if let Some(f) = &self.delete {
                    (f.relevent)(model, it, org_id)
                } else {
                    Err(ActionNotSupported(format!("{:?}", it)))
                }
            }
        }
    }

    pub fn check_commitable(
        &self,
        model: &ChainModel,
        action: &ProposalAction,
        permitted: &BTreeMap<String, String>,
    ) -> Result<(), ActionFnError> {
        match action {
            ProposalAction::Create(it) => {
                if let Some(f) = &self.create {
                    (f.commitable)(model, it, permitted)
                } else {
                    Err(ActionNotSupported(format!("{:?}", it)))
                }
            }
            ProposalAction::Update(it) => {
                if let Some(f) = &self.update {
                    (f.commitable)(model, it, permitted)
                } else {
                    Err(ActionNotSupported(format!("{:?}", it)))
                }
            }
            ProposalAction::Delete(it) => {
                if let Some(f) = &self.delete {
                    (f.commitable)(model, it, permitted)
                } else {
                    Err(ActionNotSupported(format!("{:?}", it)))
                }
            }
        }
    }


    pub fn exec(
        &self,
        model: &mut ChainModel,
        action: &ProposalAction,
    ) -> Result<ObjectByAction, ActionFnError> {
        match action {
            ProposalAction::Create(it) => {
                if let Some(f) = &self.create {
                    (f.exec)(model, it)
                } else {
                    Err(ActionNotSupported(format!("{:?}", it)))
                }
            }
            ProposalAction::Update(it) => {
                if let Some(f) = &self.update {
                    (f.exec)(model, it)
                } else {
                    Err(ActionNotSupported(format!("{:?}", it)))
                }
            }
            ProposalAction::Delete(it) => {
                if let Some(f) = &self.delete {
                    (f.exec)(model, it)
                } else {
                    Err(ActionNotSupported(format!("{:?}", it)))
                }
            }
        }
    }
}
