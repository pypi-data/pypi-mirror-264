use std::collections::{BTreeMap, HashSet};

use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use super::{CreateObjectAction, DeleteObjectAction, ObjectByAction};
use crate::{
    errors::{ActionFnError, ActionFnError::*},
    model::ChainModel,
    objects::{
        controller::{ActionFn, Controller},
        meta::TypeMeta,
        BaseObject, BaseTypedObject, TypedObject,
    },
};

type ExecPattern = Vec<String>;

#[derive(Clone, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct ContractSpec {
    /// 合约的内容
    content: String,

    #[serde(default)]
    /// 合约引用的数据声明
    data: BTreeMap<String, u64>,

    #[serde(default)]
    /// 合约引用的函数声明
    functions: BTreeMap<String, u64>,

    /// 合约执行模式
    exec_patterns: Vec<ExecPattern>,
}

impl ContractSpec {
    pub fn data(&self) -> &BTreeMap<String, u64> {
        &self.data
    }

    pub fn functions(&self) -> &BTreeMap<String, u64> {
        &self.functions
    }
}

#[derive(Default, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct ContractStatus {}


#[derive(Default, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct ContractMetadata {
    /// 对象名称
    name: String,

    /// 计算合约所属命名空间
    namespace: String,

    /// 计算合约的版本
    version: String,

    /// 计算合约的uid
    #[serde(default)]
    uid: u64,

    /// 计算合约上的注解
    #[serde(default)]
    pub annotations: Option<BTreeMap<String, serde_json::Value>>,
}

#[derive(Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct Contract {
    /// 类型元数据
    #[serde(flatten)]
    type_meta: TypeMeta,

    /// 对象元数据
    metadata: ContractMetadata,

    /// 计算合约的定义
    spec: ContractSpec,

    /// 计算合约的状态
    #[serde(default)]
    status: ContractStatus,
}

impl BaseTypedObject for Contract {
    const API_VERSION: &'static str = "core/v1";

    const KIND: &'static str = "contract";

    const NAMESPACED: bool = true;

    const VERSIONED: bool = true;

    fn controller() -> Controller {
        Self::controller()
    }
}

impl BaseObject for Contract {
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
        Some(&self.metadata.version)
    }

    fn namespace(&self) -> Option<&str> {
        Some(&self.metadata.namespace)
    }
}

impl TypedObject for Contract {}

impl Contract {

    pub fn spec(&self) -> &ContractSpec {
        &self.spec
    }

    fn get_contract_orgs(&self) -> HashSet<String> {
        let set: HashSet<String> = self
            .spec
            .exec_patterns
            .iter()
            .flat_map(|pattern| pattern.iter().map(|it| it.to_owned()))
            .collect();
        set
    }

    fn create_support(
        model: &ChainModel,
        action: &CreateObjectAction,
    ) -> Result<(), ActionFnError> {
        let obj = Self::parse_from_value(action.object.clone())?;
        if model
            .get_raw_object_by_name_version(
                &<Self as BaseTypedObject>::type_meta(),
                obj.name(),
                obj.namespace(),
                None,
            )?
            .is_some()
        {
            return Err(NotSupport(
                "create".to_string(),
                "duplicate in name or version".to_string(),
            ));
        };

        Ok(())
    }

    fn create_relevent(
        _model: &ChainModel,
        action: &CreateObjectAction,
        org_id: &str,
    ) -> Result<(), ActionFnError> {
        let obj = Self::parse_from_value(action.object.clone())?;
        let orgs = obj.get_contract_orgs();
        if !orgs.contains(org_id) {
            Err(NotRelevant(
                "create".to_string(),
                "not in orgs of contract".to_string(),
            ))
        } else {
            Ok(())
        }
    }

    /// 检查是否所有执行模式涉及的组织均同意.
    fn create_commitable(
        _model: &ChainModel,
        action: &CreateObjectAction,
        permitted: &BTreeMap<String, String>,
    ) -> Result<(), ActionFnError> {
        let obj = Self::parse_from_value(action.object.clone())?;
        let orgs = obj.get_contract_orgs();
        if orgs.iter().all(|org| permitted.contains_key(org)) {
            Ok(())
        } else {
            Err(NotCommitable(
                "create".into(),
                "not get all permit".to_string(),
            ))
        }
    }

    fn create_exec(
        model: &mut ChainModel,
        action: &CreateObjectAction,
    ) -> Result<ObjectByAction, ActionFnError> {
        let mut obj = Self::parse_from_value(action.object.clone())?;
        let new_uid = model.new_uid();
        obj.metadata.uid = new_uid;

        model.put_object(&obj)?;

        Ok(ObjectByAction::Create(serde_json::to_value(obj)?))
    }

    fn delete_support(
        model: &ChainModel,
        action: &DeleteObjectAction,
    ) -> Result<(), ActionFnError> {
        let uid = action.uid;
        let raw_object = match model.get_raw_object_by_uid(uid)? {
            Some(v) => v,
            None => {
                return Err(NotSupport(
                    "delete".to_string(),
                    "object to delete not exist".to_string(),
                ));
            }
        };

        Self::parse_from_slice(&raw_object)?;
        Ok(())
    }

    fn delete_relevent(
        model: &ChainModel,
        action: &DeleteObjectAction,
        org_id: &str,
    ) -> Result<(), ActionFnError> {
        let uid = action.uid;
        let raw_object = match model.get_raw_object_by_uid(uid)? {
            Some(v) => v,
            None => {
                return Err(NotRelevant(
                    "delete".to_string(),
                    "object not found".to_string(),
                ));
            }
        };

        let obj = Self::parse_from_slice(&raw_object)?;
        let orgs = obj.get_contract_orgs();
        if !orgs.contains(org_id) {
            Err(NotRelevant(
                "delete".to_string(),
                "not in orgs of contract".to_string(),
            ))
        } else {
            Ok(())
        }
    }

    /// 检查是否所有执行模式涉及的组织均同意.
    fn delete_commitable(
        model: &ChainModel,
        action: &DeleteObjectAction,
        permitted: &BTreeMap<String, String>,
    ) -> Result<(), ActionFnError> {
        let uid = action.uid;
        let raw_model = model.get_raw_object_by_uid(uid)?;
        if let Some(raw) = raw_model {
            let obj: Self = serde_json::from_slice(&raw)?;
            let orgs = obj.get_contract_orgs();
            if orgs.iter().all(|org| permitted.contains_key(org)) {
                Ok(())
            } else {
                Err(NotCommitable(
                    "delete".into(),
                    "not get all permit".to_string(),
                ))
            }
        } else {
            Err(NotCommitable(
                "delete".into(),
                "object not found".to_string(),
            ))
        }
    }

    fn delete_exec(
        model: &mut ChainModel,
        action: &DeleteObjectAction,
    ) -> Result<ObjectByAction, ActionFnError> {
        let uid = action.uid;
        let raw_object = match model.get_raw_object_by_uid(uid)? {
            Some(v) => v,
            None => {
                return Err(ExecFailed(
                    "delete".to_string(),
                    "object to delete not exist".to_string(),
                ));
            }
        };

        let obj = Self::parse_from_slice(&raw_object)?;

        model.delete_object_by_uid(obj.uid())?;

        Ok(ObjectByAction::Create(serde_json::to_value(obj)?))
    }

    pub fn controller() -> Controller {
        let create = ActionFn {
            support: Self::create_support,
            relevent: Self::create_relevent,
            commitable: Self::create_commitable,
            exec: Self::create_exec,
        };

        let delete = ActionFn {
            support: Self::delete_support,
            relevent: Self::delete_relevent,
            commitable: Self::delete_commitable,
            exec: Self::delete_exec,
        };

        Controller {
            create: Some(create),
            update: None,
            delete: Some(delete),
        }
    }
}
