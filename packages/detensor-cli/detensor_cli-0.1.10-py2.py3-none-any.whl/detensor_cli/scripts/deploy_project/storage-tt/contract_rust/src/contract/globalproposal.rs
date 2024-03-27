use super::check_relavent;
use crate::{
    context::Context,
    errors::ProposalError::*,
    model::ChainModel,
    objects::{
        controller,
        core::v1::{GlobalProposal, ProposalAction, ProposalStage, ProposalStatus},
        get_type_meta,
        meta::TypeMeta,
        namespaced, BaseObject, BaseTypedObject, TypedObject,
    },
};

#[no_mangle]
pub extern "C" fn create_global_proposal() {
    let ctx = crate::chainmaker_sdk::sim_context::get_sim_context();
    let mut ctx = Context::new(ctx);

    let object = match ctx.arg("object") {
        Ok(v) => v,
        Err(e) => {
            ctx.error(&e.to_string()).unwrap();
            return;
        }
    };
    let creator: String = ctx.get_sender_org_id();

    let mut model = ChainModel::new(&mut ctx);
    match create_global_proposal_impl(&mut model, object, creator) {
        Ok(v) => ctx.ok(&v.to_be_bytes()).unwrap(),
        Err(err) => ctx.error(&err.to_string()).unwrap(),
    }
}

fn create_global_proposal_impl(
    model: &mut ChainModel,
    object: Vec<u8>,
    creator: String,
) -> anyhow::Result<u64> {
    let mut proposal = GlobalProposal::parse_from_slice(&object)?;
    proposal.metadata.creator = creator;
    proposal.status = ProposalStatus::init(&proposal.spec.actions);

    check_global_proposal_action_support(model, &proposal)?;

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
    };

    model.put_object(&proposal)?;
    Ok(new_uid)
}

fn check_global_proposal_action_commitable(
    model: &ChainModel,
    proposal: &GlobalProposal,
) -> anyhow::Result<()> {
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

fn check_global_proposal_action_support(
    model: &ChainModel,
    proposal: &GlobalProposal,
) -> anyhow::Result<()> {
    if proposal.spec.actions.is_empty() {
        return Err(NoAction.into());
    }

    for action in &proposal.spec.actions {
        let type_meta = match action {
            ProposalAction::Create(it) => {
                let type_meta = get_type_meta(&it.object)?;
                if namespaced(&type_meta) {
                    return Err(ObjectNotGlobal.into());
                }
                type_meta
            }
            ProposalAction::Update(it) => {
                let uid = it.uid;
                let new_type_meta = get_type_meta(&it.object)?;
                if let Some(obj) = model.get_object_by_uid(uid)? {
                    if obj.namespaced() {
                        return Err(ObjectNotGlobal.into());
                    }
                    let old_type_meta = TypeMeta {
                        api_version: obj.api_version().to_owned(),
                        kind: obj.kind().to_owned(),
                    };

                    if new_type_meta != old_type_meta {
                        return Err(UpdateType.into());
                    }
                    new_type_meta
                } else {
                    return Err(ObjectNotFound(uid).into());
                }
            }
            ProposalAction::Delete(it) => {
                let uid = it.uid;
                if let Some(obj) = model.get_object_by_uid(uid)? {
                    if obj.namespaced() {
                        return Err(ObjectNotGlobal.into());
                    }
                    let old_type_meta = TypeMeta {
                        api_version: obj.api_version().to_owned(),
                        kind: obj.kind().to_owned(),
                    };
                    old_type_meta
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

fn exec_permit_global_proposal(
    model: &mut ChainModel,
    proposal: &mut GlobalProposal,
    status: bool,
    comment: String,
    org_id: String,
) -> anyhow::Result<()> {
    if !proposal.is_active() {
        return Err(InActive(proposal.uid()).into());
    }

    check_relavent(model, &proposal.spec.actions, &org_id)?;

    if status {
        proposal.status.permission.insert(org_id, comment);
    } else {
        proposal.status.permission.remove(&org_id);
    }

    model.put_object(proposal)?;
    Ok(())
}

#[no_mangle]
pub extern "C" fn permit_global_proposal() {
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
    match permit_global_proposal_impl(&mut model, uid, status, comment, org_id) {
        Ok(_) => ctx.ok(b"ok").unwrap(),
        Err(err) => ctx.error(&err.to_string()).unwrap(),
    }
}

fn permit_global_proposal_impl(
    model: &mut ChainModel,
    uid: u64,
    status: bool,
    comment: String,
    org_id: String,
) -> anyhow::Result<()> {
    let object_json = model.get_raw_object_by_uid(uid)?;
    if object_json.is_none() {
        return Err(ObjectNotFound(uid).into());
    }

    let mut proposal = GlobalProposal::parse_from_slice(&object_json.unwrap())?;
    exec_permit_global_proposal(model, &mut proposal, status, comment, org_id)
}

#[no_mangle]
pub extern "C" fn permit_global_proposal_by_name() {
    let ctx = crate::chainmaker_sdk::sim_context::get_sim_context();
    let mut ctx = Context::new(ctx);
    let uid = ctx.arg_as_utf8_str("name");
    if uid.is_empty() {
        ctx.error("name can't be empty").unwrap();
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
    match permit_global_proposal_by_name_impl(&mut model, uid, status, comment, org_id) {
        Ok(_) => ctx.ok(b"ok").unwrap(),
        Err(err) => ctx.error(&err.to_string()).unwrap(),
    }
}

fn permit_global_proposal_by_name_impl(
    model: &mut ChainModel,
    name: String,
    status: bool,
    comment: String,
    org_id: String,
) -> anyhow::Result<()> {
    let object_json = model.get_raw_object_by_name_version(
        &<GlobalProposal as BaseTypedObject>::type_meta(),
        &name,
        None,
        None,
    )?;
    if object_json.is_none() {
        return Err(ObjectNotFoundByName(name).into());
    }

    let mut proposal = GlobalProposal::parse_from_slice(&object_json.unwrap())?;
    exec_permit_global_proposal(model, &mut proposal, status, comment, org_id)
}

#[no_mangle]
pub extern "C" fn commit_global_proposal() {
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
    match commit_global_proposal_impl(&mut model, uid, org_id) {
        Ok(v) => ctx.ok(&v).unwrap(),
        Err(err) => ctx.error(&err.to_string()).unwrap(),
    }
}

fn exec_commit_global_proposal(
    model: &mut ChainModel,
    proposal: &mut GlobalProposal,
    org_id: String,
) -> anyhow::Result<Vec<u8>> {
    if !proposal.is_active() {
        return Err(InActive(proposal.uid()).into());
    }

    if proposal.metadata.creator != org_id {
        return Err(CommitForbidden.into());
    }

    check_global_proposal_action_support(model, proposal)?;
    check_global_proposal_action_commitable(model, proposal)?;

    let mut ret = vec![b'['];
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

    model.put_object(proposal)?;

    if ret.len() > 1 {
        assert_eq!(ret.pop(), Some(b','));
    }
    ret.push(b']');

    Ok(ret)
}

fn commit_global_proposal_impl(
    model: &mut ChainModel,
    uid: u64,
    org_id: String,
) -> anyhow::Result<Vec<u8>> {
    let object_json = model.get_raw_object_by_uid(uid)?;

    if object_json.is_none() {
        return Err(ObjectNotFound(uid).into());
    }

    let mut proposal = GlobalProposal::parse_from_slice(&object_json.unwrap())?;

    exec_commit_global_proposal(model, &mut proposal, org_id)
}

#[no_mangle]
pub extern "C" fn commit_global_proposal_by_name() {
    let ctx = crate::chainmaker_sdk::sim_context::get_sim_context();
    let mut ctx = Context::new(ctx);
    let name = ctx.arg_as_utf8_str("name");
    if name.is_empty() {
        ctx.error("name can't by empty").unwrap();
        return;
    }

    let org_id = ctx.get_sender_org_id();
    let mut model = ChainModel::new(&mut ctx);
    match commit_global_proposal_by_name_impl(&mut model, name, org_id) {
        Ok(v) => ctx.ok(&v).unwrap(),
        Err(err) => ctx.error(&err.to_string()).unwrap(),
    }
}

fn commit_global_proposal_by_name_impl(
    model: &mut ChainModel,
    name: String,
    org_id: String,
) -> anyhow::Result<Vec<u8>> {
    let object_json = model.get_raw_object_by_name_version(
        &<GlobalProposal as BaseTypedObject>::type_meta(),
        &name,
        None,
        None,
    )?;

    if object_json.is_none() {
        return Err(ObjectNotFoundByName(name).into());
    }

    let mut proposal = GlobalProposal::parse_from_slice(&object_json.unwrap())?;
    exec_commit_global_proposal(model, &mut proposal, org_id)
}

#[no_mangle]
pub extern "C" fn revoke_global_proposal() {
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
    match revoke_global_proposal_impl(&mut model, uid, org_id) {
        Ok(_) => ctx.ok(b"ok").unwrap(),
        Err(err) => ctx.error(&err.to_string()).unwrap(),
    }
}

fn exec_revoke_global_proposal(
    model: &mut ChainModel,
    proposal: &mut GlobalProposal,
    org_id: String,
) -> anyhow::Result<()> {
    if !proposal.is_active() {
        return Err(InActive(proposal.uid()).into());
    }

    if proposal.metadata.creator != org_id {
        return Err(RevokeForbidden.into());
    }

    proposal.status.stage = ProposalStage::Revoked;
    model.put_object(proposal)?;

    Ok(())
}

fn revoke_global_proposal_impl(
    model: &mut ChainModel,
    uid: u64,
    org_id: String,
) -> anyhow::Result<()> {
    let raw_object_json = model.get_raw_object_by_uid(uid)?;
    if raw_object_json.is_none() {
        return Err(ObjectNotFound(uid).into());
    }

    let mut proposal = GlobalProposal::parse_from_slice(&raw_object_json.unwrap())?;
    exec_revoke_global_proposal(model, &mut proposal, org_id)
}

#[no_mangle]
pub extern "C" fn revoke_global_proposal_by_name() {
    let ctx = crate::chainmaker_sdk::sim_context::get_sim_context();
    let mut ctx = Context::new(ctx);
    let name = ctx.arg_as_utf8_str("name");
    if name.is_empty() {
        ctx.error("name can't be empty").unwrap();
        return;
    }

    let org_id = ctx.get_sender_org_id();
    let mut model = ChainModel::new(&mut ctx);
    match revoke_global_proposal_by_name_impl(&mut model, name, org_id) {
        Ok(_) => ctx.ok(b"ok").unwrap(),
        Err(err) => ctx.error(&err.to_string()).unwrap(),
    }
}

fn revoke_global_proposal_by_name_impl(
    model: &mut ChainModel,
    name: String,
    org_id: String,
) -> anyhow::Result<()> {
    let raw_object_json = model.get_raw_object_by_name_version(
        &<GlobalProposal as BaseTypedObject>::type_meta(),
        &name,
        None,
        None,
    )?;

    if raw_object_json.is_none() {
        return Err(ObjectNotFoundByName(name).into());
    }

    let mut proposal = GlobalProposal::parse_from_slice(&raw_object_json.unwrap())?;
    exec_revoke_global_proposal(model, &mut proposal, org_id)
}
