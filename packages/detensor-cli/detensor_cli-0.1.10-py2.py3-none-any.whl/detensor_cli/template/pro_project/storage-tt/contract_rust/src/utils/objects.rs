use crate::{chainmaker_sdk::sim_context::SimContext, objects::Object};

const TABLE_PREFIX: &str = "t";
const OBJECT_TABLE_ID: &str = "1c";

const INDEX_PREFIX: &str = "i";
const OBJECT_INDEX_ID: &str = "1c";

/// 如果是全局对象, 那么 `NAMESPACE_NAME` 为空字符串
const GLOBAL_NAMESPACE: &str = "";

fn table_key<O: Object>(obj: &O) -> String {
    format!("{}{}_{:011}", TABLE_PREFIX, OBJECT_TABLE_ID, obj.uid())
}

fn index_key<O: Object>(obj: &O) -> String {
    let namespace = match obj.namespace() {
        Some(ns) => ns,
        None => GLOBAL_NAMESPACE,
    };

    format!(
        "{}{}_{}_{}",
        INDEX_PREFIX,
        OBJECT_INDEX_ID,
        namespace,
        obj.name()
    )
}

pub fn insert_table<C: SimContext, O: Object>(ctx: &mut C, obj: &O) {
    let key = table_key(obj);
    let value = obj.to_json().unwrap();
    ctx.put_state_from_key(&key, &value);
    ctx.ok(&value);
}

pub fn insert_index<C: SimContext, O: Object>(ctx: &mut C, obj: &O) {
    let key = index_key(obj);
    let version = obj.version().unwrap_or("");
    let uid = obj.uid().to_le_bytes();
    ctx.put_state(&key, version, &uid);
    ctx.ok(&uid);
}

#[cfg(test)]
mod test {
    use super::*;
    use crate::objects::{core::v1::*, meta::*};

    #[test]
    fn test_table_key() {
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

        assert_eq!(table_key(&obj), "t1c_00000000001".to_string());
    }

    #[test]
    fn test_index_key() {
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

        assert_eq!(index_key(&obj), "i1c__testns".to_string());
    }
}
