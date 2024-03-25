use thiserror::Error;

use crate::context::ResultSetCursorError;

/// 上下文可能返回的错误
#[derive(Debug, Error)]
pub enum ContextError {
    #[error("create kv iterator failed, code: {0}")]
    KvIteratorCreateFailed(i32),

    #[error("get_state failed, code: {0}")]
    GetStateFailed(i32),

    #[error("get_state_from_key failed, code: {0}")]
    GetStateFromKeyFailed(i32),

    #[error("put_state failed, code: {0}")]
    PutStateFailed(i32),

    #[error("put_state_from_key failed, code: {0}")]
    PutStateFromKeyFailed(i32),

    #[error("delete_state failed, code: {0}")]
    DeleteStateFailed(i32),

    #[error("delete_state_from_key failed, code: {0}")]
    DeleteStateFromKeyFailed(i32),

    #[error("send ok failed, code: {0}")]
    OkError(i32),

    #[error("send error failed, code: {0}")]
    ErrError(i32),

    #[error("get arg failed, key: {key}, msg: {msg}")]
    GetArgError { key: String, msg: String },
}

#[derive(Debug, Error)]
pub enum DeserializeError {
    #[error("json error: {0}")]
    JsonError(#[from] serde_json::Error),

    #[error("type meta error: {0}")]
    MismatchTypeMeta(String),

    #[error("invalid name: {0}")]
    InvalidName(String),
}

#[derive(Debug, Error)]
#[error("{0}")]
pub struct InvalidObjectError(String);

impl InvalidObjectError {
    pub fn new(reason: String) -> Self {
        InvalidObjectError(reason)
    }
}

#[derive(Debug, Error)]
pub enum ChainModelError {
    #[error("json error: {0}")]
    JsonError(#[from] serde_json::Error),

    #[error("deserialize error: {0}")]
    DeserializeError(#[from] DeserializeError),

    #[error("context error: {0}")]
    ContextError(#[from] ContextError),

    #[error("result set error: {0}")]
    ResultSetError(#[from] ResultSetCursorError),

    #[error("invalid object: {0}")]
    InvalidObject(#[from] InvalidObjectError),

    #[error("unsupported object, apiVersion: {0}, kind: {1}")]
    UnsupportedObject(String, String),

    #[error("mismatched object, uid: {uid}, old_kind: {old_kind}, new_kind: {new_kind}")]
    MismatchedKind {
        uid: u64,
        old_kind: String,
        new_kind: String,
    },

    #[error("state error, state consistency broken!: {0}")]
    StateError(String),
}

/// 操作函数相关错误
#[derive(Debug, Error)]
pub enum ActionFnError {
    #[error("chain model error: {0}")]
    ChainModel(#[from] ChainModelError),

    #[error("not support action {0}")]
    ActionNotSupported(String),

    #[error("{0} not support, {1}")]
    NotSupport(String, String),

    #[error("{0} not relevent, {1}")]
    NotRelevant(String, String),

    #[error("{0} not commitable, {1}")]
    NotCommitable(String, String),

    #[error("{0} exec failed, {1}")]
    ExecFailed(String, String),

    #[error("deserialize error: {0}")]
    Deserialize(#[from] DeserializeError),

    #[error("json error: {0}")]
    JsonError(#[from] serde_json::Error),
}

/// 提议相关合约的错误
#[derive(Debug, Error)]
pub enum ProposalError {
    #[error("target object must be a proposal or globalproposal, not a {0}")]
    NotProposal(String),

    #[error("name conflict")]
    Conlict,

    #[error("can't create empty proposal")]
    NoAction,

    #[error("object in globalproposal must be global")]
    ObjectNotGlobal,

    #[error("{0} is not namespaced object")]
    ObjectNotNamespaced(String),

    #[error("namespace of object {0} is different with namespace of proposal {1}")]
    ObjectNamespaceMismatch(String, String),

    #[error("can't find object with uid {0}")]
    ObjectNotFound(u64),

    #[error("can't find object with name {0}")]
    ObjectNotFoundByName(String),

    #[error("update can't change object type")]
    UpdateType,

    #[error("controller of kind {0} not found")]
    ControllerNotFound(String),

    #[error("proposal is inactive, uid: {0}")]
    InActive(u64),

    #[error("only the creator of proposal can commit proposal")]
    CommitForbidden,

    #[error("can't revoke proposal created by other")]
    RevokeForbidden,

    #[error("action function error: {0}")]
    ActionFn(#[from] ActionFnError),
}
