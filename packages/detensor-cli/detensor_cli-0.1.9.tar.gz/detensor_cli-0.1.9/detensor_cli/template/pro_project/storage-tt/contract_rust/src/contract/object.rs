//! 这个模块主要负责实现 IChainObject 所需要的链码接口
//!
//! - `GetObjectByUid(uid uint64)`
//! - `GetObjectByName(apiVersion, kind, namespace, name, version string) (json.RawMessage, error)`
//! - `GetObjectByKind(apiVersion, kind, namespace string) ([]json.RawMessage, error)`

use crate::{
    context::Context,
    errors::{ChainModelError, InvalidObjectError},
    model::ChainModel,
    objects::{controller, meta::TypeMeta, namespaced, versioned},
};

#[no_mangle]
pub extern "C" fn get_object_by_uid() {
    let ctx = crate::chainmaker_sdk::sim_context::get_sim_context();
    let mut ctx = Context::new(ctx);

    match get_object_by_uid_impl(&mut ctx) {
        Ok(v) => {
            let out = match v {
                Some(v) => v,
                None => vec![],
            };
            ctx.ok(&out).unwrap();
        }
        Err(err) => {
            ctx.error(&err.to_string()).unwrap();
        }
    }
}

fn get_object_by_uid_impl(ctx: &mut Context) -> anyhow::Result<Option<Vec<u8>>> {
    let uid = ctx.arg_u64("uid")?;
    ctx.log(&format!("get object by uid, uid: {}", uid));
    let model = ChainModel::new(ctx);
    let out = model.get_raw_object_by_uid(uid)?;
    Ok(out)
}

#[no_mangle]
pub extern "C" fn get_object_by_kind() {
    let ctx = crate::chainmaker_sdk::sim_context::get_sim_context();
    let mut ctx = Context::new(ctx);
    let namespace = ctx.arg_as_utf8_str("namespace");
    let api_version = ctx.arg_as_utf8_str("apiVersion");
    let kind = ctx.arg_as_utf8_str("kind");
    let model = ChainModel::new(&mut ctx);

    match get_object_by_kind_impl(&model, api_version, kind, namespace) {
        Ok(v) => {
            ctx.ok(&v).unwrap();
        }
        Err(err) => {
            ctx.error(&err.to_string()).unwrap();
        }
    }
}

fn get_object_by_kind_impl(
    model: &ChainModel,
    api_version: String,
    kind: String,
    namespace: String,
) -> anyhow::Result<Vec<u8>> {
    let type_meta = TypeMeta { api_version, kind };

    let uids = model.get_uid_by_type(&type_meta, &namespace)?;
    let mut ret = vec![b'['];
    let mut first: bool = true;

    for uid in uids {
        let mut raw = model.get_raw_object_by_uid(uid)?.ok_or_else(|| {
            ChainModelError::StateError(format!("invalid uid {} from object index", uid))
        })?;
        if first {
            first = false;
        } else {
            ret.push(b',');
        }
        ret.append(&mut raw);
    }

    ret.push(b']');
    Ok(ret)
}

#[no_mangle]
pub extern "C" fn get_object_by_name() {
    let ctx = crate::chainmaker_sdk::sim_context::get_sim_context();
    let mut ctx = Context::new(ctx);
    let api_version = ctx.arg_as_utf8_str("apiVersion");
    let kind = ctx.arg_as_utf8_str("kind");
    let namespace = ctx.arg_as_utf8_str("namespace");
    let name = ctx.arg_as_utf8_str("name");
    let version = ctx.arg_as_utf8_str("version");

    let model = ChainModel::new(&mut ctx);

    match get_object_by_name_impl(&model, api_version, kind, namespace, name, version) {
        Ok(v) => {
            ctx.ok(&v).unwrap();
        }
        Err(err) => {
            ctx.error(&err.to_string()).unwrap();
        }
    }
}

fn get_object_by_name_impl(
    model: &ChainModel,
    api_version: String,
    kind: String,
    namespace: String,
    name: String,
    version: String,
) -> anyhow::Result<Vec<u8>> {
    model.ctx().log(&format!(
        "get object by name, api_version: {}, kind: {}, namespace: {}, name: {}, version: {}",
        api_version, kind, namespace, name, version,
    ));

    let type_meta = TypeMeta { api_version, kind };

    if controller(&type_meta).is_none() {
        // 查询了一个不支持的对象类型
        return Err(
            InvalidObjectError::new(format!("unsupported object type {}", type_meta)).into(),
        );
    }

    let ty_namespaced = namespaced(&type_meta);

    let ns = if namespace.is_empty() {
        if ty_namespaced {
            return Err(InvalidObjectError::new(format!(
                "object type {} is namespaced, but request has no namespace",
                type_meta
            ))
            .into());
        }
        None
    } else {
        if !ty_namespaced {
            return Err(InvalidObjectError::new(format!(
                "object type {} is not namespaced, but request has namespace",
                type_meta
            ))
            .into());
        }
        Some(namespace.as_str())
    };

    if !version.is_empty() {
        if !versioned(&type_meta) {
            // 查询请求带有版本
            // 但是请求的对象没有版本
            return Err(InvalidObjectError::new(format!(
                "object type {}, not support version",
                type_meta
            ))
            .into());
        }
        // 请求带有版本, 所以一定是对于某个特定对象的查询请求,
        // 使用点查询API
        let out = model
            .get_raw_object_by_name_version(&type_meta, &name, ns, Some(version.as_str()))?
            .unwrap_or_default();
        Ok(out)
    } else {
        // 请求不带有版本, 按照类型是否带有版本, 判断是否是点查询
        if versioned(&type_meta) {
            // 类型是带有版本的, 范围查询
            let out = model
                .get_raw_object_by_ns_name(&type_meta, &name, ns)?
                .unwrap_or_default();
            Ok(out)
        } else {
            // 类型是无版本的, 点查询
            model.ctx().log("call get_raw_object_by_name_version");
            let out = model
                .get_raw_object_by_name_version(&type_meta, &name, ns, None)?
                .unwrap_or_default();
            Ok(out)
        }
    }
}
