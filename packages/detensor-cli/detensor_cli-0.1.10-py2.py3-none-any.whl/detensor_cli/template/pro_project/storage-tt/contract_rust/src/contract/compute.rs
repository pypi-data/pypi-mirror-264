use std::{
    collections::{BTreeMap, HashMap},
    string::FromUtf8Error,
};

use chrono::format;
use serde::Serialize;
use sim_context::SimContext;
use thiserror::Error;

use super::utils::{sys_call, sys_call_err, SysCallError};
use crate::{chainmaker_sdk::sim_context::{self, result_code}, context::Context, model::ChainModel, objects::core::v1::{Contract, DataDeclare, FunctionDeclare, ContractSpec}};

pub(crate) const NODE_TABLE_PREFIX: &str = "t1d_";

#[no_mangle]
pub extern "C" fn register_node() {
    let ctx = &mut crate::chainmaker_sdk::sim_context::get_sim_context();
    match register_node_impl(ctx) {
        Ok(_) => {
            ctx.ok("ok".as_bytes());
        }
        Err(err) => {
            ctx.error(&format!("{}", err));
        }
    }
}

fn register_node_impl<C: SimContext>(ctx: &mut C) -> Result<(), result_code> {
    // let ctx = &mut sim_context::get_sim_context();
    let addr = ctx.arg_as_utf8_str("addr");
    let org_id = ctx.get_sender_org_id();
    ctx.put_state(NODE_TABLE_PREFIX, &org_id, addr.as_bytes());
    Ok(())
}

#[no_mangle]
pub extern "C" fn logout_node() {
    let ctx = &mut crate::chainmaker_sdk::sim_context::get_sim_context();
    match logout_node_impl(ctx) {
        Ok(_) => {
            ctx.ok("ok".as_bytes());
        }
        Err(err) => {
            ctx.error(&format!("{}", err));
        }
    }
}

fn logout_node_impl<C: SimContext>(ctx: &mut C) -> Result<(), SysCallError> {
    let org_id = ctx.get_creator_org_id();
    sys_call("delete_state", ctx.delete_state(NODE_TABLE_PREFIX, &org_id))?;
    sim_context::log(&format!("logout node for org: {}", org_id));
    Ok(())
}

#[no_mangle]
pub extern "C" fn discover_nodes() {
    let ctx = &mut crate::chainmaker_sdk::sim_context::get_sim_context();
    match discover_nodes_impl(ctx) {
        Ok(v) => {
            ctx.ok(&v);
        }
        Err(err) => {
            sim_context::log(&format!("discover_nodes error: {}", err));
            ctx.error(&format!("{}", err));
        }
    }
}

#[derive(Debug, Error)]
pub(crate) enum DiscoverNodesError {
    #[error("SysCallError: {0}")]
    SysCallError(#[from] SysCallError),

    #[error("InvalidJson: {0}")]
    InvalidJson(#[from] serde_json::Error),

    #[error("registered url for org {1} is not valid utf-8: {0}")]
    InvalidUrl(FromUtf8Error, String),
}

fn discover_nodes_impl<C: SimContext>(ctx: &mut C) -> Result<Vec<u8>, DiscoverNodesError> {
    let orgs_json = ctx.arg_as_utf8_str("orgs");
    let orgs: Vec<String> = serde_json::from_str(&orgs_json)?;

    let mut ret = BTreeMap::new();
    for org in orgs {
        let out = ctx
            .get_state(NODE_TABLE_PREFIX, &org)
            .map_err(sys_call_err("get_state"))?;
        if out.is_empty() {
            continue;
        }
        let result =
            String::from_utf8(out).map_err(|e| DiscoverNodesError::InvalidUrl(e, org.clone()))?;
        ret.insert(org, result);
    }
    let ret_json = serde_json::to_vec(&ret)?;
    Ok(ret_json)
}

#[no_mangle]
pub extern "C" fn discover_all_nodes() {
    let ctx = &mut crate::chainmaker_sdk::sim_context::get_sim_context();
    match discover_all_nodes_impl(ctx) {
        Ok(v) => {
            ctx.ok(&v);
        }
        Err(err) => {
            ctx.error(&format!("{}", err));
        }
    }
}

#[derive(Debug, Error)]
pub(crate) enum DiscoverAllNodesError {
    #[error("SysCallError: {0}")]
    SysCallError(#[from] SysCallError),

    #[error("InvalidJson: {0}")]
    InvalidJson(#[from] serde_json::Error),

    #[error("registered url is not valid utf-8: {0}")]
    InvalidUrl(#[from] FromUtf8Error),

    #[error("easy codec get bytes failed {0}")]
    GetBytesFailed(String),
}

fn discover_all_nodes_impl<C: SimContext>(ctx: &mut C) -> Result<Vec<u8>, DiscoverAllNodesError> {
    let mut ret = HashMap::<String, String>::new();
    let iter = ctx
        .new_iterator_prefix_with_key_field(NODE_TABLE_PREFIX, "")
        .map_err(sys_call_err("new_iter_prefix_with_key"))?;
    while iter.has_next() {
        let row = iter.next_row().map_err(sys_call_err("next_row"))?;
        let field = row
            .get_string("field")
            .map_err(DiscoverAllNodesError::GetBytesFailed)?;
        let value = String::from_utf8(
            row.get_bytes("value")
                .map_err(DiscoverAllNodesError::GetBytesFailed)?,
        )?;
        // let field = String::from_utf8(row.get_bytes("field").unwrap()).unwrap();
        // let value = String::from_utf8(row.get_bytes("value").unwrap()).unwrap();
        ret.insert(field, value);
    }
    iter.close();
    // ret.insert("hello".to_owned(), "world".to_owned());
    let ret_json = serde_json::to_vec(&ret)?;
    Ok(ret_json)
}


#[no_mangle]
pub extern "C" fn get_contract() {
    let ctx = crate::chainmaker_sdk::sim_context::get_sim_context();
    let mut ctx = Context::new(ctx);
    match get_contract_impl(&mut ctx) {
        Ok(v) => {
            let out = match v {
                Some(v) => v,
                None => vec![],
            };
            ctx.ok(&out).unwrap();
        }
        Err(err) => {
            ctx.error(&format!("{}", err)).unwrap();
        }
    }
}

#[derive(Debug, Error)]
pub(crate) enum GetContractError {
    #[error("SysCallError: {0}")]
    SysCallError(#[from] SysCallError),

    #[error("InvalidJson: {0}")]
    InvalidJson(#[from] serde_json::Error),

    #[error("registered url is not valid utf-8: {0}")]
    InvalidUrl(#[from] FromUtf8Error),

    #[error("easy codec get bytes failed {0}")]
    GetBytesFailed(String),
}

#[derive(Serialize)]
struct GetContractRes {
    spec: ContractSpec,
    data: BTreeMap<String, u64>,
    function: BTreeMap<String, u64>,
}

fn get_contract_impl(ctx: &mut Context) -> anyhow::Result<Option<Vec<u8>>> {
    let uid = ctx.arg_u64("uid")?;
    let org_id = ctx.get_sender_org_id();
    let model = ChainModel::new(ctx);
    let raw_contract = match model.get_raw_object_by_uid(uid)? {
        None => return Ok(None),
        Some(v) => v,
    };

    let contract: Contract = serde_json::from_slice(&raw_contract)?;
    let spec = contract.spec();
    let data_declare = spec.data();
    let function_declare = spec.functions();

    let mut available_data: BTreeMap<String, u64> = BTreeMap::new();
    let mut available_function: BTreeMap<String, u64> = BTreeMap::new();

    for (delcare_name, declare_uid) in data_declare {
        let raw_declare = match model.get_raw_object_by_uid(*declare_uid)? {
            None => return Ok(None),
            Some(v) => v,
        };

        let declare: DataDeclare = serde_json::from_slice(&raw_declare[..])?;
        if declare.status().impls().contains_key(&org_id) {
            available_data.insert(delcare_name.clone(), *declare_uid);
        }
    }

    for (delcare_name, declare_uid) in function_declare {
        let raw_declare = match model.get_raw_object_by_uid(*declare_uid)? {
            None => return Ok(None),
            Some(v) => v,
        };

        let declare: FunctionDeclare = serde_json::from_slice(&raw_declare[..])?;
        if declare.status().impls().contains_key(&org_id) {
            available_function.insert(delcare_name.clone(), *declare_uid);
        }
    }
    // sim_context::log(&format!("available_data:{:?}", available_data));
    // println!("available_data:{:?}", available_data);
    let res = GetContractRes {
        spec: contract.spec().clone(),
        data: available_data,
        function: available_function
    };

    let ret = serde_json::to_vec(&res)?;
    println!("available_data:{:?}", res.data);
    Ok(Some(ret))
}