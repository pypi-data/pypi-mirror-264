use std::collections::{HashMap, HashSet};

use once_cell::sync::OnceCell;

use self::{controller::Controller, core::v1::{Namespace, Record}, meta::TypeMeta};
use crate::{
    errors::{DeserializeError, InvalidObjectError},
    objects::core::v1::{
        DataDeclare, FunctionDeclare, GlobalProposal, Proposal,
        Contract,
    },
    utils::validate::is_valid_rfc_1035,
};

/// 控制器模块, 对象控制器相关的定义与实现
pub mod controller;

/// 一个静态的对象类型 应该实现的基本接口
pub trait BaseTypedObject: serde::Serialize + serde::de::DeserializeOwned {
    /// 对象类型对应的 api 版本
    const API_VERSION: &'static str;

    /// 对象类型对应的 kind
    const KIND: &'static str;

    /// 这一类型的对象是否应该放在命名空间中
    const NAMESPACED: bool;

    /// 这一类型的对象是否使用了版本
    const VERSIONED: bool = false;

    /// 返回这一类型的[`Controller`]
    fn controller() -> Controller;

    /// 返回这一类型的[`TypeMeta`]
    fn type_meta() -> TypeMeta {
        TypeMeta {
            api_version: Self::API_VERSION.to_owned(),
            kind: Self::KIND.to_owned(),
        }
    }
}

/// 任何对象最基本的trait, object safe.
///
/// 这个trait 只应该用于impl, 不应该直接出现在参数类型或返回值类型中.
///
/// 如果要表达任何对象这个约束, 应该使用 [`Object`] trait.
pub trait BaseObject {
    /// 获取对象的类型元数据[`TypeMeta`]
    fn type_meta(&self) -> &TypeMeta;

    /// 获取对象uid
    fn uid(&self) -> u64;

    /// 获取对象uid
    fn uid_mut(&mut self) -> &mut u64;

    /// 获取对象名称
    fn name(&self) -> &str;

    /// 获取对象版本, 对象可能没有版本
    fn version(&self) -> Option<&str>;

    /// 获取对象的命名空间, 对象可能没有所属的命名空间
    fn namespace(&self) -> Option<&str>;
}

/// 对象trait, object safe.
/// 所有的对象都必须实现的trait, 包括动态类型的对象.
///
/// 这个trait是对于[`BaseObject`]的一个拓展.
/// 如果类型同时实现了 [`BaseObject`] 和 [`BaseTypedObject`].
/// 那么它会自动实现 [`Object`].
pub trait Object: BaseObject {
    /// 获取对象的api version
    fn api_version(&self) -> &str;

    /// 获取对象的kind
    fn kind(&self) -> &str;

    /// 对象是否是一个命名空间下的对象
    fn namespaced(&self) -> bool;

    /// 返回对象类型对应的Controller
    fn controller(&self) -> Controller;

    /// 将对象编码为json
    fn to_json(&self) -> Result<Vec<u8>, serde_json::Error>;
}

/// 对于实现了[`BaseObject`]和[`BaseTypedObject`]的类型
/// 自动实现[`Object`]trait.
impl<T> Object for T
where
    T: BaseObject + BaseTypedObject,
{
    fn api_version(&self) -> &str {
        T::API_VERSION
    }

    fn kind(&self) -> &str {
        T::KIND
    }

    fn namespaced(&self) -> bool {
        T::NAMESPACED
    }

    fn controller(&self) -> Controller {
        T::controller()
    }

    fn to_json(&self) -> Result<Vec<u8>, serde_json::Error> {
        serde_json::to_vec(self)
    }
}

/// TypedObject trait
/// 所有明确的静态对象类型最终必须要实现的trait
/// 通常的实现路径是分别实现 [`BaseTypedObject`], [`BaseObject`].
pub trait TypedObject: BaseTypedObject + Object + 'static {
    /// 将静态类型的对象, 转化为动态类型的对象 [`Box<dyn Object>`].
    fn to_dyn(self) -> Box<dyn Object> {
        Box::new(self) as Box<dyn Object>
    }

    /// 从[`serde_json::Value`]中, 按照JSON格式解析对象
    fn parse_from_value(value: serde_json::Value) -> Result<Self, DeserializeError> {
        let out: Self = serde_json::from_value(value)?;
        if out.api_version() != Self::API_VERSION {
            return Err(DeserializeError::MismatchTypeMeta(format!(
                "apiVersion mismatch, expect '{}', but get '{}'",
                Self::API_VERSION,
                out.api_version()
            )));
        }

        if out.kind() != Self::KIND {
            return Err(DeserializeError::MismatchTypeMeta(format!(
                "kind mismatch, expect '{}', but get '{}'",
                Self::KIND,
                out.kind()
            )));
        }

        if !is_valid_rfc_1035(out.name()) {
            return Err(DeserializeError::InvalidName(
                "name is not a valid RFC 1035 label".to_string(),
            ));
        }
        Ok(out)
    }

    /// 从切片中, 按照JSON格式解析对象
    fn parse_from_slice(slice: &[u8]) -> Result<Self, DeserializeError> {
        let out: Self = serde_json::from_slice(slice)?;
        if out.api_version() != Self::API_VERSION {
            return Err(DeserializeError::MismatchTypeMeta(format!(
                "apiVersion mismatch, expect '{}', but get '{}'",
                Self::API_VERSION,
                out.api_version()
            )));
        }

        if out.kind() != Self::KIND {
            return Err(DeserializeError::MismatchTypeMeta(format!(
                "kind mismatch, expect '{}', but get '{}'",
                Self::KIND,
                out.kind()
            )));
        }

        if !is_valid_rfc_1035(out.name()) {
            return Err(DeserializeError::InvalidName(
                "name is not a valid RFC 1035 label".to_string(),
            ));
        }

        Ok(out)
    }
}

/// 解析函数, 从JSON形式[`serde_json::Value`]中解析出动态的对象
type ParseFn = fn(serde_json::Value) -> Result<Box<dyn Object>, DeserializeError>;

/// 核心对象
pub mod core;

/// 用来描述对象元数据的元对象, 一般会直接展开在对象内部
pub mod meta;

/// 对所有的对象类型, 展开宏`callback`
///
/// 例如, 可以收集所有对象类型的KIND.
/// ```
/// macro_rules! all_names {
///     ($($ty:ident), *) => {
///         {
///             let mut ret = vec![];
///             $(
///                 ret.push($ty::KIND.to_owned());
///             )*
///             ret
///         }
///     }
/// }
///
/// let names: Vec<String> = call_with_object_types!(example);
/// ```
macro_rules! call_with_object_types {
    ($callback:ident) => {
        $callback!(
            Namespace,
            Proposal,
            GlobalProposal,
            DataDeclare,
            FunctionDeclare,
            Contract,
            Record
        )
    };
}

/// 按照资源的类型, 判断一种资源是否是命名空间下的
pub(crate) fn namespaced(ty: &TypeMeta) -> bool {
    static NAMESPACED_TABLE: OnceCell<HashSet<TypeMeta>> = OnceCell::new();

    macro_rules! gen_namespaced {
        ($($ty:ident),*) => {
            {
                let mut table = HashSet::new();
                $(
                    if $ty::NAMESPACED {
                        table.insert(<$ty as BaseTypedObject>::type_meta());
                    }
                )*
                table
            }
        };
    }

    NAMESPACED_TABLE
        .get_or_init(|| call_with_object_types!(gen_namespaced))
        .contains(ty)
}

/// 按照资源的类型, 判断一种资源是否是版本化的
#[allow(unused)]
pub(crate) fn versioned(ty: &TypeMeta) -> bool {
    macro_rules! gen_versioned {
        ($($ty:ident), *) => {
            {
                let mut table = HashSet::new();
                $(
                    if $ty::VERSIONED {
                        table.insert(<$ty as BaseTypedObject>::type_meta());
                    }
                )*
                table
            }
        };
    }

    static VERSIONED_TABLE: OnceCell<HashSet<TypeMeta>> = OnceCell::new();
    VERSIONED_TABLE
        .get_or_init(|| call_with_object_types!(gen_versioned))
        .contains(ty)
}

/// 返回包含所有资源的控制器的控制器表
pub(crate) fn controllers() -> &'static HashMap<TypeMeta, Controller> {
    static CONTROL_TABLE: OnceCell<HashMap<TypeMeta, Controller>> = OnceCell::new();

    macro_rules! gen_controller {
        ($($ty:ident),*) => {
            {
                let mut table = HashMap::new();
                $(
                    table.insert(
                        <$ty as BaseTypedObject>::type_meta(),
                        <$ty as BaseTypedObject>::controller()
                    );
                )*
                table
            }
        };
    }

    CONTROL_TABLE.get_or_init(|| call_with_object_types!(gen_controller))
}

/// 根据资源的类型[`TypeMeta`], 获取对应的控制器
pub(crate) fn controller(ty: &TypeMeta) -> Option<&'static Controller> {
    controllers().get(ty)
}

/// 根据资源的类型[`TypeMeta`], 获取对应的解析函数
pub(crate) fn parse_fn(ty: &TypeMeta) -> Option<ParseFn> {
    static PARSE_TABLE: OnceCell<HashMap<TypeMeta, ParseFn>> = OnceCell::new();

    macro_rules! gen_parse_fn {
        ($($ty:ident), *) => {
            {
                let mut table = HashMap::new();
                $(
                    let parse_fn: ParseFn = |v: serde_json::Value| match $ty::parse_from_value(v) {
                        Ok(o) => Ok(o.to_dyn()),
                        Err(err) => Err(err),
                    };
                    table.insert(
                        <$ty as BaseTypedObject>::type_meta(),
                        parse_fn,
                    );
                )*
                table
            }
        };
    }

    PARSE_TABLE
        .get_or_init(|| call_with_object_types!(gen_parse_fn))
        .get(ty)
        .cloned()
}

/// 从JSON形式的对象[`serde_json::Value`]中, 获取对象所属的命名空间名称
pub fn get_namespace(value: &serde_json::Value) -> Result<Option<String>, InvalidObjectError> {
    let metadata = match value.get("metadata") {
        Some(v) => Ok(v),
        None => Err(InvalidObjectError::new("missing metadata".to_owned())),
    }?;

    let ns = match metadata.get("namespace") {
        Some(v) => v.as_str().map(|s| s.to_owned()),
        None => None,
    };
    Ok(ns)
}

/// 从JSON形式的对象[`serde_json::Value`]中, 获取对象的类型元数据[`TypeMeta`].
pub fn get_type_meta(value: &serde_json::Value) -> Result<TypeMeta, InvalidObjectError> {
    let api_version = match value.get("apiVersion") {
        Some(v) => match v.as_str() {
            Some(v) => Ok(v.to_owned()),
            None => Err(InvalidObjectError::new(
                "apiVersion must be string".to_owned(),
            )),
        },
        None => return Err(InvalidObjectError::new("missing apiVersion".to_owned())),
    }?;

    let kind = match value.get("kind") {
        Some(v) => match v.as_str() {
            Some(v) => Ok(v.to_owned()),
            None => Err(InvalidObjectError::new("kind must be string".to_owned())),
        },
        None => return Err(InvalidObjectError::new("missing kind".to_owned())),
    }?;

    Ok(TypeMeta { api_version, kind })
}
