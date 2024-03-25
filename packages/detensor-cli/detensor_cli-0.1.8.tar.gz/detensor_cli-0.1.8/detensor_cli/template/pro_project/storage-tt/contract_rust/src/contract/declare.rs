use crate::{
    context::Context,
    errors::InvalidObjectError,
    model::ChainModel,
    objects::{
        core::v1::{DataDeclare, FunctionDeclare},
        BaseTypedObject, TypedObject,
    },
};

#[no_mangle]
pub extern "C" fn set_data_implement() {
    let ctx = crate::chainmaker_sdk::sim_context::get_sim_context();
    let mut ctx = Context::new(ctx);

    match set_data_implement_impl(&mut ctx) {
        Ok(_) => ctx.ok(b"ok").unwrap(),
        Err(err) => ctx.error(&err.to_string()).unwrap(),
    }
}

fn set_data_implement_impl(ctx: &mut Context) -> anyhow::Result<()> {
    // 只能为本组织实现声明.
    let org_id = ctx.get_sender_org_id();

    let uid = ctx.arg_u64("uid")?;
    let status = ctx.arg_bool("status")?;
    let comment = ctx.arg_as_utf8_str("comment");

    let mut model = ChainModel::new(ctx);

    let raw_object = model.get_raw_object_by_uid(uid)?;
    if raw_object.is_none() {
        return Err(InvalidObjectError::new(format!("object not found by uid: {}", uid)).into());
    }

    let mut data_declare = DataDeclare::parse_from_slice(&raw_object.unwrap())?;
    data_declare.set_implement(org_id, status, comment)?;
    model.put_object(data_declare.to_dyn().as_ref())?;

    Ok(())
}

#[no_mangle]
pub extern "C" fn set_data_implement_by_name() {
    let ctx = crate::chainmaker_sdk::sim_context::get_sim_context();
    let mut ctx = Context::new(ctx);

    match set_data_implement_by_name_impl(&mut ctx) {
        Ok(_) => ctx.ok(b"ok").unwrap(),
        Err(err) => ctx.error(&err.to_string()).unwrap(),
    }
}

fn set_data_implement_by_name_impl(ctx: &mut Context) -> anyhow::Result<()> {
    // 只能为本组织实现声明.
    let org_id = ctx.get_sender_org_id();

    let namespace = ctx.arg_as_utf8_str("namespace");
    let name = ctx.arg_as_utf8_str("name");
    let status = ctx.arg_bool("status")?;
    let comment = ctx.arg_as_utf8_str("comment");

    let mut model = ChainModel::new(ctx);

    let raw_object = model.get_raw_object_by_name_version(
        &<DataDeclare as BaseTypedObject>::type_meta(),
        &name,
        Some(&namespace),
        None,
    )?;
    if raw_object.is_none() {
        return Err(InvalidObjectError::new(format!(
            "object not found by namespace: {}, name: {}",
            namespace, name
        ))
        .into());
    }

    let mut data_declare = DataDeclare::parse_from_slice(&raw_object.unwrap())?;
    data_declare.set_implement(org_id, status, comment)?;
    model.put_object(data_declare.to_dyn().as_ref())?;

    Ok(())
}

#[no_mangle]
pub extern "C" fn set_function_implement() {
    let ctx = crate::chainmaker_sdk::sim_context::get_sim_context();
    let mut ctx = Context::new(ctx);

    match set_function_implement_impl(&mut ctx) {
        Ok(_) => ctx.ok(b"ok").unwrap(),
        Err(err) => ctx.error(&err.to_string()).unwrap(),
    }
}

fn set_function_implement_impl(ctx: &mut Context) -> anyhow::Result<()> {
    // 只能为本组织实现声明.
    let org_id = ctx.get_sender_org_id();

    let uid = ctx.arg_u64("uid")?;
    let status = ctx.arg_bool("status")?;
    let comment = ctx.arg_as_utf8_str("comment");

    let mut model = ChainModel::new(ctx);

    let raw_object = model.get_raw_object_by_uid(uid)?;
    if raw_object.is_none() {
        return Err(InvalidObjectError::new(format!("object not found by uid: {}", uid)).into());
    }

    let mut function_declare = FunctionDeclare::parse_from_slice(&raw_object.unwrap())?;
    function_declare.set_implement(org_id, status, comment)?;
    model.put_object(function_declare.to_dyn().as_ref())?;

    Ok(())
}

#[no_mangle]
pub extern "C" fn set_function_implement_by_name() {
    let ctx = crate::chainmaker_sdk::sim_context::get_sim_context();
    let mut ctx = Context::new(ctx);

    match set_function_implement_by_name_impl(&mut ctx) {
        Ok(_) => ctx.ok(b"ok").unwrap(),
        Err(err) => ctx.error(&err.to_string()).unwrap(),
    }
}

fn set_function_implement_by_name_impl(ctx: &mut Context) -> anyhow::Result<()> {
    // 只能为本组织实现声明.
    let org_id = ctx.get_sender_org_id();

    let namespace = ctx.arg_as_utf8_str("namespace");
    let name = ctx.arg_as_utf8_str("name");
    let status = ctx.arg_bool("status")?;
    let comment = ctx.arg_as_utf8_str("comment");

    let mut model = ChainModel::new(ctx);

    let raw_object = model.get_raw_object_by_name_version(
        &<FunctionDeclare as BaseTypedObject>::type_meta(),
        &name,
        Some(&namespace),
        None,
    )?;
    if raw_object.is_none() {
        return Err(InvalidObjectError::new(format!(
            "object not found by namespace: {}, name: {}",
            namespace, name
        ))
        .into());
    }

    let mut function_declare = FunctionDeclare::parse_from_slice(&raw_object.unwrap())?;
    function_declare.set_implement(org_id, status, comment)?;
    model.put_object(function_declare.to_dyn().as_ref())?;

    Ok(())
}
