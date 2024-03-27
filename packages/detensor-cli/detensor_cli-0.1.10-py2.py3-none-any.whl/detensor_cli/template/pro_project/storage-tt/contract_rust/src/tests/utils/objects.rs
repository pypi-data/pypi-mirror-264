use std::convert::TryInto;

use crate::{
    chainmaker_sdk::sim_context::SimContext,
    objects::{
        core::v1::{Namespace, NamespaceSpec, NamespaceMetadata},
        meta::TypeMeta,
        BaseObject,
    },
    utils::objects::{insert_index, insert_table},
};

#[no_mangle]
pub extern "C" fn test_insert_table() {
    let ctx = &mut crate::chainmaker_sdk::sim_context::get_sim_context();

    let type_meta = TypeMeta {
        api_version: "v1".to_string(),
        kind: "kind".to_string(),
    };
    let metadata = NamespaceMetadata {
        name: "testns".to_string(),
        uid: 1,
        annotations: None,
    };
    let spec = NamespaceSpec::new(vec![]);
    let obj = Namespace::new(type_meta, metadata, spec);

    insert_table(ctx, &obj);

    let find = ctx.get_state_from_key("t1c_00000000001").unwrap();
    let find_obj: Namespace = serde_json::from_slice(&find).unwrap();

    assert_eq!(obj, find_obj);

    ctx.ok("ok".as_bytes());
}

#[no_mangle]
pub extern "C" fn test_insert_index() {
    let ctx = &mut crate::chainmaker_sdk::sim_context::get_sim_context();

    let type_meta = TypeMeta {
        api_version: "v1".to_string(),
        kind: "kind".to_string(),
    };
    let metadata = NamespaceMetadata {
        name: "testns".to_string(),
        uid: 1,
        annotations: None,
    };
    let spec = NamespaceSpec::new(vec![]);
    let obj = Namespace::new(type_meta, metadata, spec);

    insert_index(ctx, &obj);

    let find = ctx.get_state("i1c__testns", "").unwrap();
    let find_uid: u64 = u64::from_le_bytes(find.try_into().unwrap());

    assert_eq!(obj.uid(), find_uid);

    ctx.ok("ok".as_bytes());
}
