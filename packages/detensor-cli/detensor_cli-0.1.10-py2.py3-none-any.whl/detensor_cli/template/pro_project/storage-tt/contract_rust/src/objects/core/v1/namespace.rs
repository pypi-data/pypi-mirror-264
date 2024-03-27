use std::collections::BTreeMap;

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

/// 命名空间的对象内容
#[derive(Serialize, Deserialize, JsonSchema, Eq, PartialEq, Debug)]
#[serde(rename_all = "camelCase")]
pub struct NamespaceSpec {
    /// 命名空间的成员组织
    members: Vec<String>,
}

impl NamespaceSpec {
    pub fn new(members: Vec<String>) -> Self {
        Self { members }
    }
}

/// 命名空间的元数据
#[derive(Serialize, Deserialize, JsonSchema, Eq, PartialEq, Debug)]
#[serde(rename_all = "camelCase")]
pub struct NamespaceMetadata {
    /// 对象名称
    pub name: String,

    /// 对象UID
    #[serde(default)]
    pub uid: u64,

    /// 对象注解
    #[serde(default)]
    pub annotations: Option<BTreeMap<String, serde_json::Value>>,
}

/// 命名空间对象
#[derive(Serialize, Deserialize, JsonSchema, Eq, PartialEq, Debug)]
#[serde(rename_all = "camelCase")]
pub struct Namespace {
    /// 类型元数据
    #[serde(flatten)]
    type_meta: TypeMeta,

    /// 对象的元数据
    metadata: NamespaceMetadata,

    /// 命名空间的对象内容
    spec: NamespaceSpec,
}

impl BaseTypedObject for Namespace {
    const API_VERSION: &'static str = "core/v1";
    const KIND: &'static str = "namespace";

    const NAMESPACED: bool = false;

    fn controller() -> Controller {
        Self::controller()
    }
}

impl BaseObject for Namespace {
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

impl TypedObject for Namespace {}

impl Namespace {
    pub fn new(
        type_meta: TypeMeta, 
        metadata: NamespaceMetadata, 
        spec: NamespaceSpec,
    ) -> Self {
        Self {
            type_meta,
            metadata,
            spec,
        }
    }

    fn create_support(
        model: &ChainModel,
        action: &CreateObjectAction,
    ) -> Result<(), ActionFnError> {
        let out = Self::parse_from_value(action.object.clone())?;
        if model
            .get_raw_object_by_name_version(
                &<Self as BaseTypedObject>::type_meta(),
                out.name(),
                None,
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
        if !obj.spec.members.contains(&org_id.into()) {
            Err(NotRelevant(
                "create".to_string(),
                "you must in members to permit".to_string(),
            ))
        } else {
            Ok(())
        }
    }

    fn create_commitable(
        _model: &ChainModel,
        action: &CreateObjectAction,
        permitted: &BTreeMap<String, String>,
    ) -> Result<(), ActionFnError> {
        let obj = Self::parse_from_value(action.object.clone())?;
        for member in obj.spec.members {
            if !permitted.contains_key(&member) {
                return Err(NotCommitable(
                    "create".into(),
                    format!("member {} not permitted yet", member),
                ));
            }
        }

        Ok(())
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
        if !obj.spec.members.contains(&org_id.into()) {
            return Err(NotRelevant(
                "delete".to_string(),
                "you must in members to permit".to_string(),
            ));
        }

        Ok(())
    }

    fn delete_commitable(
        model: &ChainModel,
        action: &DeleteObjectAction,
        permitted: &BTreeMap<String, String>,
    ) -> Result<(), ActionFnError> {
        let uid = action.uid;
        let raw_object = match model.get_raw_object_by_uid(uid)? {
            Some(v) => v,
            None => {
                return Err(NotCommitable(
                    "delete".into(),
                    "object not found".to_string(),
                ));
            }
        };

        let obj = Self::parse_from_slice(&raw_object)?;
        for member in obj.spec.members {
            if !permitted.contains_key(&member) {
                return Err(NotCommitable(
                    "delete".into(),
                    format!("member {} not permitted yet", member),
                ));
            }
        }
        Ok(())
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
        let namespace = &obj.metadata.name;

        // 删除命名空间下所有的对象
        let uids = model.get_uid_by_ns(namespace)?;
        for uid in uids {
            model.delete_object_by_uid(uid)?;
        }

        // 删除命名空间本身
        model.delete_object_by_uid(obj.uid())?;

        Ok(ObjectByAction::Delete(serde_json::to_value(obj)?))
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
