use sim_context::SimContext;

use crate::chainmaker_sdk::sim_context;

pub mod compute;

pub use compute::*;

pub mod object;

pub use object::*;

pub mod proposal;

pub use proposal::*;

pub mod globalproposal;

pub use globalproposal::*;

pub mod declare;

pub use declare::*;

pub(crate) mod utils;

#[no_mangle]
pub extern "C" fn init_contract() {
    sim_context::log("init_contract");
    let ctx = &mut sim_context::get_sim_context();
    ctx.put_state_from_key("t0_nextuid", &1u64.to_be_bytes());
}

#[cfg(feature = "test")]
#[no_mangle]
pub extern "C" fn reinit_state() {
    use crate::context::Context;
    sim_context::log("reinit_contract");
    let ctx = sim_context::get_sim_context();
    let mut ctx = Context::new(ctx);

    let mut out = ctx.iter_prefix_key("t1c").unwrap();
    while let Some((key, field, _)) = out.next_item().unwrap() {
        sim_context::log(&format!("reinit key: {}, field: {}", key, field));
        ctx.delete_state(&key, &field).unwrap();
    }
    let mut out = ctx.iter_prefix_key("i1c").unwrap();
    while let Some((key, field, _)) = out.next_item().unwrap() {
        sim_context::log(&format!("reinit key: {}, field: {}", key, field));
        ctx.delete_state(&key, &field).unwrap();
    }

    let mut out = ctx.iter_prefix_key(NODE_TABLE_PREFIX).unwrap();
    while let Some((key, field, _)) = out.next_item().unwrap() {
        sim_context::log(&format!("reinit key: {}, field: {}", key, field));
        ctx.delete_state(&key, &field).unwrap();
    }

    ctx.reinit_uid();
    ctx.ok(b"ok").unwrap();
}

/// 调试用接口, 返回next_uid
#[cfg(feature = "test")]
#[no_mangle]
pub extern "C" fn next_uid() {
    use std::convert::TryInto;
    sim_context::log("debug next_uid");
    let ctx = &mut sim_context::get_sim_context();
    let out = ctx
        .get_state_from_key("t0_nextuid")
        .expect("get nextuid failed");
    let bytes = match out.try_into() {
        Ok(v) => v,
        Err(err) => {
            ctx.error(&format!("get t0_nextuid failed, origin data: {:?}", err));
            return;
        }
    };
    let next_uid = u64::from_be_bytes(bytes);
    ctx.ok(format!("{}", next_uid).as_bytes());
}

#[no_mangle]
pub extern "C" fn upgrade() {
    sim_context::log("upgrade");
    let ctx = &mut sim_context::get_sim_context();
    ctx.ok("upgrade success".as_bytes());
}

#[no_mangle]
pub extern "C" fn save() {
    let ctx = &mut sim_context::get_sim_context();

    let key = ctx.arg_as_utf8_str("key");
    let value = match ctx.arg("value") {
        Ok(v) => v,
        Err(err) => {
            ctx.log(&format!("get value failed: '{}'", err));
            ctx.error(&err);
            return;
        }
    };

    ctx.put_state_from_key(&key, &value);
}

#[no_mangle]
pub extern "C" fn load() {
    let ctx = &mut sim_context::get_sim_context();
    let key = ctx.arg_as_utf8_str("key");

    let value = match ctx.get_state_from_key(&key) {
        Ok(v) => v,
        Err(err) => {
            ctx.log("can't find key");
            ctx.error(&format!("can't find key, error code: {}", err));
            return;
        }
    };
    ctx.ok(&value);
}

#[no_mangle]
pub extern "C" fn whoami() {
    let ctx = &mut sim_context::get_sim_context();
    let out = ctx.get_sender_org_id();
    ctx.ok(out.as_bytes());
}
