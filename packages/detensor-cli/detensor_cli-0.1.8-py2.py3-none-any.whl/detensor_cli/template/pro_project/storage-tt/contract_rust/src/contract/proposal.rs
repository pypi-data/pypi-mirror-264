//! 这个模块主要负责实现 IChainProposal 接口需要的链码方法
//!
//! - 创建提议
//! `CreateProposal(object json.RawMessage, defaultNamespace string) (uint64, error)`
//!
//! - 撤回提议
//! `RevokeProposal(uid uint64) error`
//!
//! - 按照名称撤回提议
//! `RevokeProposalByName(namespace, name string) error`
//!
//! - 提交一个提议
//! `CommitProposal(uid uint64) error`
//!
//! - 对一个提议设置,本组织对该提议的批准状态
//! `Permit(uid uint64, status bool, comment string) (bool, error)`

use proposal::ProposalStage;

use crate::{
    context::Context,
    errors::ProposalError::*,
    model::ChainModel,
    objects::{
        controller,
        core::v1::{proposal, Proposal, ProposalAction, ProposalStatus},
        get_namespace, get_type_meta,
        meta::TypeMeta,
        namespaced, BaseObject, BaseTypedObject, TypedObject,
    },
};

#[no_mangle]
pub extern "C" fn create_proposal() {
    let ctx = crate::chainmaker_sdk::sim_context::get_sim_context();
    let mut ctx = Context::new(ctx);

    let namespace = ctx.arg_as_utf8_str("namespace");
    let object = match ctx.arg("object") {
        Ok(v) => v,
        Err(e) => {
            ctx.error(&format!("can't get argument 'object', error: {}", e))
                .unwrap();
            return;
        }
    };
    let creator = ctx.get_sender_org_id();

    let mut model = ChainModel::new(&mut ctx);

    match create_proposal_impl(&mut model, object, namespace, creator) {
        Ok(v) => ctx.ok(&v.to_be_bytes()).unwrap(),
        Err(err) => ctx.error(&err.to_string()).unwrap(),
    }
}

fn check_proposal_action_commitable(model: &ChainModel, proposal: &Proposal) -> anyhow::Result<()> {
    if proposal.spec.actions.is_empty() {
        return Err(NoAction.into());
    }

    for action in &proposal.spec.actions {
        let type_meta = action.get_type_meta(model)?;
        if let Some(control) = controller(&type_meta) {
            control.check_commitable(model, action, &proposal.status.permission)?;
        } else {
            return Err(ControllerNotFound(format!("{:?}", type_meta)).into());
        };       
    }
    Ok(())
}

fn check_proposal_action_support(model: &ChainModel, proposal: &Proposal) -> anyhow::Result<()> {
    if proposal.spec.actions.is_empty() {
        return Err(NoAction.into());
    }

    // 这是命名空间下的提议, 所以涉及的所有动作, 必须在这个命名空间下
    for action in &proposal.spec.actions {
        let type_meta = match action {
            ProposalAction::Create(it) => {
                let type_meta = get_type_meta(&it.object)?;
                if !namespaced(&type_meta) {
                    return Err(ObjectNotNamespaced(format!("{:?}", type_meta)).into());
                }
                if let Some(ns) = get_namespace(&it.object)? {
                    if ns != proposal.metadata.namespace {
                        return Err(ObjectNamespaceMismatch(
                            ns,
                            proposal.metadata.namespace.clone(),
                        )
                        .into());
                    }
                } else {
                    return Err(ObjectNamespaceMismatch(
                        "".into(),
                        proposal.metadata.namespace.clone(),
                    )
                    .into());
                }
                type_meta
            }
            ProposalAction::Update(it) => {
                let uid = it.uid;
                if let Some(obj) = model.get_object_by_uid(uid)? {
                    if let Some(ns) = obj.namespace() {
                        if ns != proposal.metadata.namespace {
                            return Err(ObjectNamespaceMismatch(
                                ns.to_string(),
                                proposal.metadata.namespace.clone(),
                            )
                            .into());
                        }
                        TypeMeta {
                            api_version: obj.api_version().to_owned(),
                            kind: obj.kind().to_owned(),
                        }
                    } else {
                        return Err(ObjectNamespaceMismatch(
                            "".into(),
                            proposal.metadata.namespace.clone(),
                        )
                        .into());
                    }
                } else {
                    return Err(ObjectNotFound(uid).into());
                }
            }
            ProposalAction::Delete(it) => {
                let uid = it.uid;
                if let Some(obj) = model.get_object_by_uid(uid)? {
                    if let Some(ns) = obj.namespace() {
                        if ns != proposal.metadata.namespace {
                            return Err(ObjectNamespaceMismatch(
                                ns.to_string(),
                                proposal.metadata.namespace.clone(),
                            )
                            .into());
                        }
                        TypeMeta {
                            api_version: obj.api_version().to_owned(),
                            kind: obj.kind().to_owned(),
                        }
                    } else {
                        return Err(ObjectNamespaceMismatch(
                            "".into(),
                            proposal.metadata.namespace.clone(),
                        )
                        .into());
                    }
                } else {
                    return Err(ObjectNotFound(uid).into());
                }
            }
        };

        if let Some(control) = controller(&type_meta) {
            control.check_support(model, action)?;
        } else {
            return Err(ControllerNotFound(format!("{:?}", type_meta)).into());
        };
    }

    Ok(())
}

fn create_proposal_impl(
    model: &mut ChainModel,
    object: Vec<u8>,
    namespace: String,
    creator: String,
) -> anyhow::Result<u64> {
    let mut proposal = Proposal::parse_from_slice(&object)?;

    // 设置并检查提议的命名空间
    // TODO: 需要检查命名空间是否存在
    if proposal.metadata.namespace.is_empty() {
        proposal.metadata.namespace = namespace;
    } else if proposal.metadata.namespace != namespace {
        return Err(ObjectNamespaceMismatch(namespace, proposal.metadata.namespace.clone()).into());
    }

    // 设置提议的创建组织
    proposal.metadata.creator = creator;

    proposal.status = ProposalStatus::init(&proposal.spec.actions);
    check_proposal_action_support(model, &proposal)?;

    let new_uid = model.new_uid();
    *proposal.uid_mut() = new_uid;

    if model
        .get_raw_object_by_name_version(
            proposal.type_meta(),
            proposal.name(),
            proposal.namespace(),
            proposal.version(),
        )?
        .is_some()
    {
        return Err(Conlict.into());
    }

    model.put_object(&proposal)?;
    Ok(new_uid)
}

#[no_mangle]
pub extern "C" fn permit_proposal() {
    let ctx = crate::chainmaker_sdk::sim_context::get_sim_context();
    let mut ctx = Context::new(ctx);
    let uid = match ctx.arg_u64("uid") {
        Ok(v) => v,
        Err(e) => {
            ctx.error(&format!("can't get argument 'uid', error: {}", e))
                .unwrap();
            return;
        }
    };

    let status = match ctx.arg_bool("status") {
        Ok(v) => v,
        Err(e) => {
            ctx.error(&format!("can't get argument 'status', error: {}", e))
                .unwrap();
            return;
        }
    };
    let comment = ctx.arg_as_utf8_str("comment");
    let org_id = ctx.get_sender_org_id();
    let mut model = ChainModel::new(&mut ctx);
    match permit_proposal_impl(&mut model, uid, status, comment, org_id) {
        Ok(_) => ctx.ok(b"ok").unwrap(),
        Err(err) => ctx.error(&err.to_string()).unwrap(),
    }
}

pub(crate) fn check_relavent(
    model: &ChainModel,
    actions: &[ProposalAction],
    org_id: &str,
) -> anyhow::Result<()> {
    for action in actions {
        let type_meta = match action {
            ProposalAction::Create(it) => get_type_meta(&it.object)?,
            ProposalAction::Update(it) => {
                if let Some(obj) = model.get_object_by_uid(it.uid)? {
                    TypeMeta {
                        api_version: obj.api_version().to_owned(),
                        kind: obj.kind().to_owned(),
                    }
                } else {
                    return Err(ObjectNotFound(it.uid).into());
                }
            }
            ProposalAction::Delete(it) => {
                if let Some(obj) = model.get_object_by_uid(it.uid)? {
                    TypeMeta {
                        api_version: obj.api_version().to_owned(),
                        kind: obj.kind().to_owned(),
                    }
                } else {
                    return Err(ObjectNotFound(it.uid).into());
                }
            }
        };

        if let Some(control) = controller(&type_meta) {
            control.check_relevent(model, action, org_id)?;
        } else {
            return Err(ControllerNotFound(format!("{:?}", type_meta)).into());
        };
    }

    Ok(())
}

fn permit_proposal_impl(
    model: &mut ChainModel,
    uid: u64,
    status: bool,
    comment: String,
    org_id: String,
) -> anyhow::Result<()> {
    let raw_object_json = model.get_raw_object_by_uid(uid)?;
    if raw_object_json.is_none() {
        return Err(ObjectNotFound(uid).into());
    }

    let mut proposal = Proposal::parse_from_slice(&raw_object_json.unwrap())?;
    if !proposal.status.stage.is_active() {
        return Err(InActive(uid).into());
    }

    check_relavent(model, &proposal.spec.actions, &org_id)?;

    if status {
        proposal.status.permission.insert(org_id, comment);
    } else {
        proposal.status.permission.remove(&org_id);
    }

    model.put_object(&proposal)?;
    Ok(())
}

#[no_mangle]
pub extern "C" fn permit_proposal_by_name() {
    let ctx = crate::chainmaker_sdk::sim_context::get_sim_context();
    let mut ctx = Context::new(ctx);
    let name = ctx.arg_as_utf8_str("name");
    if name.is_empty() {
        ctx.error("name can't be empty").unwrap();
        return;
    }

    let namespace = ctx.arg_as_utf8_str("namespace");
    if namespace.is_empty() {
        ctx.error("namespace can't be empty").unwrap();
        return;
    }

    let status = match ctx.arg_bool("status") {
        Ok(v) => v,
        Err(e) => {
            ctx.error(&format!("can't get argument 'status', error: {}", e))
                .unwrap();
            return;
        }
    };
    let comment = ctx.arg_as_utf8_str("comment");
    let org_id = ctx.get_sender_org_id();
    let mut model = ChainModel::new(&mut ctx);
    match permit_proposal_by_name_impl(&mut model, name, namespace, status, comment, org_id) {
        Ok(_) => ctx.ok(b"ok").unwrap(),
        Err(err) => ctx.error(&err.to_string()).unwrap(),
    }
}

fn permit_proposal_by_name_impl(
    model: &mut ChainModel,
    name: String,
    namespace: String,
    status: bool,
    comment: String,
    org_id: String,
) -> anyhow::Result<()> {
    let raw_object_json = model.get_raw_object_by_name_version(
        &<Proposal as BaseTypedObject>::type_meta(),
        &name,
        Some(&namespace),
        None,
    )?;
    if raw_object_json.is_none() {
        return Err(ObjectNotFoundByName(name).into());
    }

    let mut proposal = Proposal::parse_from_slice(&raw_object_json.unwrap())?;
    if !proposal.status.stage.is_active() {
        return Err(InActive(proposal.metadata.uid).into());
    }

    check_relavent(model, &proposal.spec.actions, &org_id)?;

    if status {
        proposal.status.permission.insert(org_id, comment);
    } else {
        proposal.status.permission.remove(&org_id);
    }

    model.put_object(&proposal)?;
    Ok(())
}

#[no_mangle]
pub extern "C" fn commit_proposal() {
    let ctx = crate::chainmaker_sdk::sim_context::get_sim_context();
    let mut ctx = Context::new(ctx);
    let uid = match ctx.arg_u64("uid") {
        Ok(v) => v,
        Err(e) => {
            ctx.error(&format!("can't get argument 'uid', error: {}", e))
                .unwrap();
            return;
        }
    };

    let org_id = ctx.get_sender_org_id();
    let mut model = ChainModel::new(&mut ctx);

    match commit_proposal_impl(&mut model, uid, org_id) {
        Ok(v) => ctx.ok(&v).unwrap(),
        Err(err) => ctx.error(&err.to_string()).unwrap(),
    }
}

fn commit_proposal_impl(
    model: &mut ChainModel,
    uid: u64,
    org_id: String,
) -> anyhow::Result<Vec<u8>> {
    let mut ret = vec![b'['];
    let object_json = model.get_raw_object_by_uid(uid)?;
    if object_json.is_none() {
        return Err(ObjectNotFound(uid).into());
    }

    let mut proposal = Proposal::parse_from_slice(&object_json.unwrap())?;
    if !proposal.status.stage.is_active() {
        return Err(InActive(uid).into());
    }

    if proposal.metadata.creator != org_id {
        return Err(CommitForbidden.into());
    }

    check_proposal_action_support(model, &proposal)?;
    check_proposal_action_commitable(model, &proposal)?;

    let mut results = vec![];
    for action in &proposal.spec.actions {
        let type_meta = action.get_type_meta(model)?;
        if let Some(control) = controller(&type_meta) {
            let obj = control.exec(model, action)?;

            ret.append(&mut serde_json::to_vec(&obj)?);
            ret.push(b',');

            results.push(obj);
        } else {
            return Err(ControllerNotFound(format!("{:?}", type_meta)).into());
        };
    }

    proposal.status.results = Some(results);
    proposal.status.stage = ProposalStage::Submitted;

    model.put_object(&proposal)?;

    // pop the last ','
    if ret.len() > 1 {
        assert_eq!(ret.pop(), Some(b','));
    }
    ret.push(b']');

    Ok(ret)
}

#[no_mangle]
pub extern "C" fn commit_proposal_by_name() {
    let ctx = crate::chainmaker_sdk::sim_context::get_sim_context();
    let mut ctx = Context::new(ctx);
    let name = ctx.arg_as_utf8_str("name");
    if name.is_empty() {
        ctx.error("name can't by empty").unwrap();
        return;
    }

    let namespace = ctx.arg_as_utf8_str("namespace");
    if name.is_empty() {
        ctx.error("namespace can't by empty").unwrap();
        return;
    }

    let org_id = ctx.get_sender_org_id();
    let mut model = ChainModel::new(&mut ctx);

    match commit_proposal_by_name_impl(&mut model, name, namespace, org_id) {
        Ok(v) => ctx.ok(&v).unwrap(),
        Err(err) => ctx.error(&err.to_string()).unwrap(),
    }
}

fn commit_proposal_by_name_impl(
    model: &mut ChainModel,
    name: String,
    namespace: String,
    org_id: String,
) -> anyhow::Result<Vec<u8>> {
    let mut ret = vec![b'['];
    let object_json = model.get_raw_object_by_name_version(
        &<Proposal as BaseTypedObject>::type_meta(),
        &name,
        Some(&namespace),
        None,
    )?;
    if object_json.is_none() {
        return Err(ObjectNotFoundByName(name).into());
    }

    let mut proposal = Proposal::parse_from_slice(&object_json.unwrap())?;
    if !proposal.status.stage.is_active() {
        return Err(InActive(proposal.metadata.uid).into());
    }

    if proposal.metadata.creator != org_id {
        return Err(CommitForbidden.into());
    }

    check_proposal_action_support(model, &proposal)?;

    let mut results = vec![];
    for action in &proposal.spec.actions {
        let type_meta = action.get_type_meta(model)?;
        if let Some(control) = controller(&type_meta) {
            let obj = control.exec(model, action)?;

            ret.append(&mut serde_json::to_vec(&obj)?);
            ret.push(b',');

            results.push(obj);
        } else {
            return Err(ControllerNotFound(format!("{:?}", type_meta)).into());
        };
    }

    proposal.status.results = Some(results);
    proposal.status.stage = ProposalStage::Submitted;

    model.put_object(&proposal)?;

    // pop the last ','
    if ret.len() > 1 {
        assert_eq!(ret.pop(), Some(b','));
    }
    ret.push(b']');

    Ok(ret)
}

#[no_mangle]
pub extern "C" fn revoke_proposal() {
    let ctx = crate::chainmaker_sdk::sim_context::get_sim_context();
    let mut ctx = Context::new(ctx);
    let uid = match ctx.arg_u64("uid") {
        Ok(v) => v,
        Err(e) => {
            ctx.error(&format!("can't get argument 'uid', error: {}", e))
                .unwrap();
            return;
        }
    };

    let org_id = ctx.get_sender_org_id();
    let mut model = ChainModel::new(&mut ctx);

    match revoke_proposal_impl(&mut model, uid, org_id) {
        Ok(_) => ctx.ok(b"ok").unwrap(),
        Err(err) => ctx.error(&err.to_string()).unwrap(),
    }
}

fn revoke_proposal_impl(model: &mut ChainModel, uid: u64, org_id: String) -> anyhow::Result<()> {
    let raw_object_json = model.get_raw_object_by_uid(uid)?;
    if raw_object_json.is_none() {
        return Err(ObjectNotFound(uid).into());
    }

    let mut proposal = Proposal::parse_from_slice(&raw_object_json.unwrap())?;
    if !proposal.status.stage.is_active() {
        return Err(InActive(proposal.uid()).into());
    }

    if proposal.metadata.creator != org_id {
        return Err(RevokeForbidden.into());
    }

    proposal.status.stage = ProposalStage::Revoked;
    model.put_object(&proposal)?;
    Ok(())
}

#[no_mangle]
pub extern "C" fn revoke_proposal_by_name() {
    let ctx = crate::chainmaker_sdk::sim_context::get_sim_context();
    let mut ctx = Context::new(ctx);
    let name = ctx.arg_as_utf8_str("name");
    let namespace = ctx.arg_as_utf8_str("namespace");

    let org_id = ctx.get_sender_org_id();
    let mut model = ChainModel::new(&mut ctx);

    match revoke_proposal_by_name_impl(&mut model, name, namespace, org_id) {
        Ok(_) => ctx.ok(b"ok").unwrap(),
        Err(err) => ctx.error(&err.to_string()).unwrap(),
    }
}

fn revoke_proposal_by_name_impl(
    model: &mut ChainModel,
    name: String,
    namespace: String,
    org_id: String,
) -> anyhow::Result<()> {
    let raw_object_json = model.get_raw_object_by_name_version(
        &<Proposal as BaseTypedObject>::type_meta(),
        &name,
        Some(&namespace),
        None,
    )?;
    if raw_object_json.is_none() {
        return Err(ObjectNotFoundByName(name).into());
    }

    let mut proposal = Proposal::parse_from_slice(&raw_object_json.unwrap())?;
    if !proposal.status.stage.is_active() {
        return Err(InActive(proposal.uid()).into());
    }

    if proposal.metadata.creator != org_id {
        return Err(RevokeForbidden.into());
    }

    proposal.status.stage = ProposalStage::Revoked;
    model.put_object(&proposal)?;
    Ok(())
}
