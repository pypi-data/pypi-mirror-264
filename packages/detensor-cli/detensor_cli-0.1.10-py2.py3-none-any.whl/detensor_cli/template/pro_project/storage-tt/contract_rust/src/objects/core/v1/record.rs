use std::collections::BTreeMap;

use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use crate::{
    errors::ActionFnError::{self, *},
    model::ChainModel,
    objects::{meta::TypeMeta, BaseObject, BaseTypedObject, Object, TypedObject, controller::{ActionFn, Controller}},
};

use super::{CreateObjectAction, ObjectByAction, DeleteObjectAction, UpdateObjectAction};

#[derive(Debug, Serialize, Deserialize, JsonSchema)]
pub struct RecordSpec {
    content: serde_json::Value,
    authors: Vec<String>,
}

#[derive(Debug, Serialize, Deserialize, JsonSchema)]
pub struct RecordMetadata {
    /// 记录名称
    pub name: String,

    /// 记录所属命名空间
    pub namespace: String,

    /// 记录对象的uid
    #[serde(default)]
    pub uid: u64,

}

#[derive(Debug, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "camelCase")]
pub struct Record {
    /// 类型元数据
    #[serde(flatten)]
    pub type_meta: TypeMeta,

    /// 对象元数据
    pub metadata: RecordMetadata,

    /// 对象的内容
    pub spec: RecordSpec,
}

impl Record {
    fn create_support(
        model: &ChainModel,
        action: &CreateObjectAction,
    ) -> Result<(), ActionFnError> {
        let out = Self::parse_from_value(action.object.clone())?;
        if model
            .get_raw_object_by_name_version(
                &<Self as BaseTypedObject>::type_meta(), 
                out.name(), 
                out.namespace(), 
                out.version(),
            )?
            .is_some()
        {
            return Err(NotSupport(
                "create".to_string(),
                "duplicate in name or version".to_string(),
            ));
        }

        if out.spec.authors.is_empty() {
            return Err(NotSupport(
                "create".to_string(),
                "record author can't be empty".to_string(),
            ))
        };

        let mut authors = out.spec.authors;
        authors.sort();
        let l = authors.len();
        authors.dedup();
        if l != authors.len() {
            return Err(NotSupport(
                "create".to_string(),
                "record author can't be duplicate".to_string(),
            ))
        }
        Ok(())
    }

    fn create_relevent(
        _model: &ChainModel,
        action: &CreateObjectAction,
        org_id: &str,
    ) -> Result<(), ActionFnError> {
        let obj = Self::parse_from_value(action.object.clone())?;
        if !obj.spec.authors.contains(&org_id.into()) {
            Err(NotRelevant(
                "create".to_string(), 
                "you must be author to permit".to_string(),
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
        for author in obj.spec.authors {
            if !permitted.contains_key(&author) {
                return Err(NotCommitable(
                    "create".to_owned(), 
                    format!("author {} not permitted yet", author)
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
        action: &DeleteObjectAction
    ) -> Result<(), ActionFnError> {
        let uid = action.uid;
        let raw_object = match model.get_raw_object_by_uid(uid)? {
            Some(v) => v,
            None => {
                return Err(NotSupport(
                    "delete".to_string(),
                    "object to delete not exist".to_string()
                ))
            },
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
                ))
            }
        };

        let obj = Self::parse_from_slice(&raw_object)?;
        if !obj.spec.authors.contains(&org_id.into()) {
            return Err(NotRelevant(
                "delete".to_string(), 
                "you must in authors to permit".to_string(),
            ));
        }

        Ok(())
    }

    fn delete_commitable(
        model: &ChainModel,
        action: &DeleteObjectAction,
        permitted: &BTreeMap<String, String>
    ) -> Result<(), ActionFnError> {
        let uid = action.uid;
        let raw_object = match model.get_raw_object_by_uid(uid)? {
            Some(v) => v,
            None => {
                return Err(NotCommitable(
                    "delete".into(), 
                    "object not found".to_string(),
                ));
            },
        };

        let obj = Self::parse_from_slice(&raw_object)?;
        for org in obj.spec.authors.iter() {
            if !permitted.contains_key(org) {
                return Err(NotCommitable(
                    "delete".into(), 
                    format!("org {} not permitted yet", org)
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
                    "object to delete not exist".to_string()
                ));
            },
        };

        let obj = Self::parse_from_slice(&raw_object)?;

        model.delete_object_by_uid(uid)?;
        Ok(ObjectByAction::Delete(serde_json::to_value(obj)?))
    }

    fn update_support(
        model: &ChainModel,
        action: &UpdateObjectAction,
    ) -> Result<(), ActionFnError> {
        let obj = Self::parse_from_value(action.object.clone())?;
        let out = match model.get_raw_object_by_uid(action.uid)? {
            Some(v) => v,
            None => return Err(NotSupport(
                "update".to_string(),
                "object not exist".to_string(),
            )),
        };

        let old_obj = Self::parse_from_slice(&out)?;

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

        let new = Self::parse_from_value(action.object.clone())?;
        let old = Self::parse_from_slice(&raw_old)?;
        if old.spec.authors.contains(&org_id.to_owned()) || new.spec.authors.contains(&org_id.to_owned()) {
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

        let new = Self::parse_from_value(action.object.clone())?;
        let old = Self::parse_from_slice(&raw_uid)?;
        for author in old.spec.authors.iter() {
            if !permitted.contains_key(author) {
                return Err(NotCommitable(
                    "update".to_string(),
                    format!("org {} haven't permitted", author),
                ));
            }
        }

        for author in new.spec.authors.iter() {
            if !permitted.contains_key(author) {
                return Err(NotCommitable(
                    "update".to_string(),
                    format!("org {} haven't permitted", author),
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

        model.put_object(&obj)?;

        Ok(ObjectByAction::Update {
            old: serde_json::to_value(old_obj)?,
            updated: serde_json::to_value(obj)?,
        })
    }


}

impl BaseTypedObject for Record {
    const API_VERSION: &'static str = "core/v1";

    const KIND: &'static str = "record";

    const NAMESPACED: bool = true;

    const VERSIONED: bool = false;

    fn controller() -> crate::objects::controller::Controller {
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

impl BaseObject for Record {
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

impl TypedObject for Record {}
