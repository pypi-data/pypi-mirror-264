use std::collections::BTreeMap;

use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use super::{CreateObjectAction, DeleteObjectAction, ObjectByAction, UpdateObjectAction};
use crate::{
    errors::{ActionFnError, ActionFnError::*, InvalidObjectError},
    model::ChainModel,
    objects::{
        controller::{ActionFn, Controller},
        meta::{NamespacedMetadata, TypeMeta},
        BaseObject, BaseTypedObject, TypedObject,
    },
};

/// 数据声明的定义
#[derive(Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct DataDeclareSpec {
    data_type: String,
    description: String,
}

/// 数据声明的状态
#[derive(Clone, Default, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct DataDeclareStatus {
    /// 数据声明的具体实现
    /// 实现数据的组织名和备注.
    implementation: BTreeMap<String, String>,
}

impl DataDeclareStatus {
    pub fn impls(&self) -> &BTreeMap<String, String> {
        &self.implementation
    }
}

#[derive(Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct DataDeclare {
    /// 类型元数据
    #[serde(flatten)]
    type_meta: TypeMeta,

    /// 对象元数据
    metadata: NamespacedMetadata,

    /// 数据声明的定义
    spec: DataDeclareSpec,

    /// 数据声明的状态
    #[serde(default)]
    status: DataDeclareStatus,
}

#[derive(Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct FnArgDeclare {
    /// 参数的类型
    arg_type: String,
    /// 参数的描述
    description: String,
}

#[derive(Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct FunctionDeclareSpec {
    /// 函数参数的声明
    args: Vec<FnArgDeclare>,
    /// 函数的返回类型
    ret_type: String,
    /// 函数的描述
    description: String,
}

#[derive(Clone, Serialize, Deserialize, JsonSchema, Default)]
#[serde(rename_all = "camelCase")]
pub struct FunctionDeclareStatus {
    /// 数据声明的具体实现
    /// 实现数据的组织名和备注.
    implementation: BTreeMap<String, String>,
}

impl FunctionDeclareStatus {
    pub fn impls(&self) -> &BTreeMap<String, String> {
        &self.implementation
    }
}

#[derive(Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct FunctionDeclare {
    /// 类型元数据
    #[serde(flatten)]
    type_meta: TypeMeta,

    /// 对象元数据
    metadata: NamespacedMetadata,

    /// 函数声明的定义
    spec: FunctionDeclareSpec,

    /// 函数声明的状态
    #[serde(default)]
    status: FunctionDeclareStatus,
}

// TODO(gan): Use macro to reduce redundant code.

impl BaseTypedObject for DataDeclare {
    const API_VERSION: &'static str = "core/v1";

    const KIND: &'static str = "datadeclare";

    const NAMESPACED: bool = true;

    fn controller() -> Controller {
        Self::controller()
    }
}

impl BaseObject for DataDeclare {
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

impl BaseTypedObject for FunctionDeclare {
    const API_VERSION: &'static str = "core/v1";

    const KIND: &'static str = "functiondeclare";

    const NAMESPACED: bool = true;

    fn controller() -> Controller {
        Self::controller()
    }
}

impl BaseObject for FunctionDeclare {
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

impl TypedObject for DataDeclare {}

impl TypedObject for FunctionDeclare {}

impl DataDeclare {

    pub fn status(&self) -> &DataDeclareStatus {
        &self.status
    }

    pub fn spec(&self) -> &DataDeclareSpec {
        &self.spec
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
        _action: &CreateObjectAction,
        _org_id: &str,
    ) -> Result<(), ActionFnError> {
        Ok(())
    }

    fn create_commitable(
        _model: &ChainModel,
        _action: &CreateObjectAction,
        _permitted: &BTreeMap<String, String>,
    ) -> Result<(), ActionFnError> {
        Ok(())
    }

    fn create_exec(
        model: &mut ChainModel,
        action: &CreateObjectAction,
    ) -> Result<ObjectByAction, ActionFnError> {
        let mut obj = Self::parse_from_value(action.object.clone())?;
        let new_uid = model.new_uid();
        obj.metadata.uid = new_uid;
        obj.status = Default::default();

        model.put_object(&obj)?;

        Ok(ObjectByAction::Create(serde_json::to_value(obj)?))
    }

    fn update_support(
        model: &ChainModel,
        action: &UpdateObjectAction,
    ) -> Result<(), ActionFnError> {
        let obj = Self::parse_from_value(action.object.clone())?;
        let out = model.get_raw_object_by_uid(action.uid)?;

        if out.is_none() {
            return Err(NotSupport(
                "update".to_string(),
                "object not exist".to_string(),
            ));
        }

        let old_obj = Self::parse_from_slice(&out.unwrap())?;

        if old_obj.name() != obj.name() {
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
                    "update".to_string(),
                    "duplicate in name or version".to_string(),
                ));
            };
        }

        if obj.metadata.uid != 0 && old_obj.metadata.uid != obj.metadata.uid {
            return Err(NotSupport(
                "update".to_string(),
                format!(
                    "uid mismatch, old {}, new {}",
                    old_obj.metadata.uid, obj.metadata.uid
                ),
            ));
        }

        Ok(())
    }

    fn update_relevent(
        model: &ChainModel,
        action: &UpdateObjectAction,
        org_id: &str,
    ) -> Result<(), ActionFnError> {
        let uid = action.uid;
        let raw_old = match model.get_raw_object_by_uid(uid)? {
            Some(v) => v,
            None => {
                return Err(NotSupport(
                    "update".to_string(),
                    format!("object with uid {} not exist", uid),
                ));
            }
        };

        let old = Self::parse_from_slice(&raw_old)?;
        if old.status.implementation.contains_key(org_id) {
            Ok(())
        } else {
            Err(NotRelevant(
                "update".to_string(),
                "not implment datadeclare".to_string(),
            ))
        }
    }

    fn update_commitable(
        model: &ChainModel,
        action: &UpdateObjectAction,
        permitted: &BTreeMap<String, String>,
    ) -> Result<(), ActionFnError> {
        let uid = action.uid;
        let raw_uid = match model.get_raw_object_by_uid(uid)? {
            Some(v) => v,
            None => {
                return Err(NotSupport(
                    "update".to_string(),
                    format!("object with uid {} not exist", uid),
                ));
            }
        };

        let old = Self::parse_from_slice(&raw_uid)?;
        for (k, _) in old.status.implementation.iter() {
            if !permitted.contains_key(k) {
                return Err(NotCommitable(
                    "update".to_string(),
                    format!("org {} haven't permitted", k),
                ));
            }
        }

        Ok(())
    }

    fn update_exec(
        model: &mut ChainModel,
        action: &UpdateObjectAction,
    ) -> Result<ObjectByAction, ActionFnError> {
        let mut obj = Self::parse_from_value(action.object.clone())?;
        let uid = action.uid;

        let out = model.get_raw_object_by_uid(action.uid)?;

        if out.is_none() {
            return Err(NotSupport(
                "update".to_string(),
                "object not exist".to_string(),
            ));
        }

        let old_obj = Self::parse_from_slice(&out.unwrap())?;

        *obj.uid_mut() = uid;

        obj.status = old_obj.status.clone();

        model.put_object(&obj)?;

        Ok(ObjectByAction::Update {
            old: serde_json::to_value(old_obj)?,
            updated: serde_json::to_value(obj)?,
        })
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

    /// 检查 `org_id` 是否实现该 [`DataDeclare`].
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
                    "object to delete not exist".to_string(),
                ));
            }
        };

        let obj = Self::parse_from_slice(&raw_object)?;
        // 只有实现了的组织可以删除
        if !obj.status.implementation.contains_key(org_id) {
            return Err(NotRelevant(
                "delete".to_string(),
                "you must implememt this data declare to delete".to_string(),
            ));
        }

        Ok(())
    }

    /// 检查实现该 [`DataDeclare`] 的所有组织是否均同意.
    fn delete_commitable(
        model: &ChainModel,
        action: &DeleteObjectAction,
        permitted: &BTreeMap<String, String>,
    ) -> Result<(), ActionFnError> {
        let uid = action.uid;
        let raw_model = model.get_raw_object_by_uid(uid)?;
        if let Some(raw) = raw_model {
            let obj: Self = serde_json::from_slice(&raw)?;
            for (impl_org, _) in obj.status.implementation {
                if !permitted.contains_key(&impl_org) {
                    return Err(NotCommitable(
                        "delete".into(),
                        format!(
                            "org '{}' implemented this data declare but still doesn't permit the proposal",
                            impl_org
                        ),
                    ));
                }
            }

            Ok(())
        } else {
            Err(NotCommitable(
                "delete".into(),
                format!("can't find object by uid {}", uid),
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

        let update = ActionFn {
            support: Self::update_support,
            relevent: Self::update_relevent,
            commitable: Self::update_commitable,
            exec: Self::update_exec,
        };

        let delete = ActionFn {
            support: Self::delete_support,
            relevent: Self::delete_relevent,
            commitable: Self::delete_commitable,
            exec: Self::delete_exec,
        };

        Controller {
            create: Some(create),
            update: Some(update),
            delete: Some(delete),
        }
    }
}

impl DataDeclare {
    pub fn set_implement(
        &mut self,
        org_id: String,
        status: bool,
        comment: String,
    ) -> anyhow::Result<()> {
        if status {
            // 覆盖更新
            self.status.implementation.insert(org_id, comment);
            Ok(())
        } else {
            match self.status.implementation.get(&org_id) {
                Some(_) => {
                    self.status.implementation.remove(&org_id);
                    Ok(())
                }
                None => {
                    return Err(InvalidObjectError::new(format!(
                        "{} does not implement data declare with uid {}",
                        org_id,
                        self.uid()
                    ))
                    .into());
                }
            }
        }
    }
}

impl FunctionDeclare {

    pub fn spec(&self) -> &FunctionDeclareSpec {
        &self.spec
    }

    pub fn status(&self) -> &FunctionDeclareStatus {
        &self.status
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
        _action: &CreateObjectAction,
        _org_id: &str,
    ) -> Result<(), ActionFnError> {
        Ok(())
    }

    fn create_commitable(
        _model: &ChainModel,
        _action: &CreateObjectAction,
        _permitted: &BTreeMap<String, String>,
    ) -> Result<(), ActionFnError> {
        Ok(())
    }

    fn create_exec(
        model: &mut ChainModel,
        action: &CreateObjectAction,
    ) -> Result<ObjectByAction, ActionFnError> {
        let mut obj = Self::parse_from_value(action.object.clone())?;
        let new_uid = model.new_uid();
        obj.metadata.uid = new_uid;
        obj.status = Default::default();

        model.put_object(&obj)?;

        Ok(ObjectByAction::Create(serde_json::to_value(obj)?))
    }

    fn update_support(
        model: &ChainModel,
        action: &UpdateObjectAction,
    ) -> Result<(), ActionFnError> {
        let obj = Self::parse_from_value(action.object.clone())?;
        let out = model.get_raw_object_by_uid(action.uid)?;

        if out.is_none() {
            return Err(NotSupport(
                "update".to_string(),
                "object not exist".to_string(),
            ));
        }

        let old_obj = Self::parse_from_slice(&out.unwrap())?;

        if old_obj.name() != obj.name() {
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
                    "update".to_string(),
                    "duplicate in name or version".to_string(),
                ));
            };
        }

        if obj.metadata.uid != 0 && old_obj.metadata.uid != obj.metadata.uid {
            return Err(NotSupport(
                "update".to_string(),
                format!(
                    "uid mismatch, old {}, new {}",
                    old_obj.metadata.uid, obj.metadata.uid
                ),
            ));
        }

        Ok(())
    }

    fn update_relevent(
        model: &ChainModel,
        action: &UpdateObjectAction,
        org_id: &str,
    ) -> Result<(), ActionFnError> {
        let uid = action.uid;
        let raw_old = match model.get_raw_object_by_uid(uid)? {
            Some(v) => v,
            None => {
                return Err(NotSupport(
                    "update".to_string(),
                    format!("object with uid {} not exist", uid),
                ));
            }
        };

        let old = Self::parse_from_slice(&raw_old)?;
        if old.status.implementation.contains_key(org_id) {
            Ok(())
        } else {
            Err(NotRelevant(
                "update".to_string(),
                "not implment datadeclare".to_string(),
            ))
        }
    }

    fn update_commitable(
        model: &ChainModel,
        action: &UpdateObjectAction,
        permitted: &BTreeMap<String, String>,
    ) -> Result<(), ActionFnError> {
        let uid = action.uid;
        let raw_uid = match model.get_raw_object_by_uid(uid)? {
            Some(v) => v,
            None => {
                return Err(NotSupport(
                    "update".to_string(),
                    format!("object with uid {} not exist", uid),
                ));
            }
        };

        let old = Self::parse_from_slice(&raw_uid)?;
        for (k, _) in old.status.implementation.iter() {
            if !permitted.contains_key(k) {
                return Err(NotCommitable(
                    "update".to_string(),
                    format!("org {} haven't permitted", k),
                ));
            }
        }

        Ok(())
    }

    fn update_exec(
        model: &mut ChainModel,
        action: &UpdateObjectAction,
    ) -> Result<ObjectByAction, ActionFnError> {
        let mut obj = Self::parse_from_value(action.object.clone())?;
        let uid = action.uid;

        let out = model.get_raw_object_by_uid(action.uid)?;

        if out.is_none() {
            return Err(NotSupport(
                "update".to_string(),
                "object not exist".to_string(),
            ));
        }

        let old_obj = Self::parse_from_slice(&out.unwrap())?;

        *obj.uid_mut() = uid;

        obj.status = old_obj.status.clone();

        model.put_object(&obj)?;

        Ok(ObjectByAction::Update {
            old: serde_json::to_value(old_obj)?,
            updated: serde_json::to_value(obj)?,
        })
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

    /// 检查 `org_id` 是否实现该 [`FunctionDeclare`].
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
                    "object to delete not exist".to_string(),
                ));
            }
        };

        let obj = Self::parse_from_slice(&raw_object)?;
        // 只有实现了的组织可以删除
        if !obj.status.implementation.contains_key(org_id) {
            return Err(NotRelevant(
                "delete".to_string(),
                "you must implememt this function declare to delete".to_string(),
            ));
        }
        Ok(())
    }

    /// 检查实现该 [`FunctionDeclare`] 的所有组织是否均同意.
    fn delete_commitable(
        model: &ChainModel,
        action: &DeleteObjectAction,
        permitted: &BTreeMap<String, String>,
    ) -> Result<(), ActionFnError> {
        let uid = action.uid;
        let raw_model = model.get_raw_object_by_uid(uid)?;
        if let Some(raw) = raw_model {
            let obj: Self = serde_json::from_slice(&raw)?;
            for (impl_org, _) in obj.status.implementation {
                if !permitted.contains_key(&impl_org) {
                    return Err(NotCommitable(
                        "delete".into(),
                        format!(
                            "org '{}' implemented this function declare but still doesn't permit the proposal",
                            impl_org
                        ),
                    ));
                }
            }

            Ok(())
        } else {
            Err(NotCommitable(
                "delete".into(),
                format!("can't find object by uid {}", uid),
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

        let update = ActionFn {
            support: Self::update_support,
            relevent: Self::update_relevent,
            commitable: Self::update_commitable,
            exec: Self::update_exec,
        };

        let delete = ActionFn {
            support: Self::delete_support,
            relevent: Self::delete_relevent,
            commitable: Self::delete_commitable,
            exec: Self::delete_exec,
        };

        Controller {
            create: Some(create),
            update: Some(update),
            delete: Some(delete),
        }
    }
}

impl FunctionDeclare {
    pub fn set_implement(
        &mut self,
        org_id: String,
        status: bool,
        comment: String,
    ) -> anyhow::Result<()> {
        if status {
            // 覆盖更新
            self.status.implementation.insert(org_id, comment);
            Ok(())
        } else {
            match self.status.implementation.get(&org_id) {
                Some(_) => {
                    self.status.implementation.remove(&org_id);
                    Ok(())
                }
                None => {
                    return Err(InvalidObjectError::new(format!(
                        "{} does not implement function declare with uid {}",
                        org_id,
                        self.uid()
                    ))
                    .into());
                }
            }
        }
    }
}
