use std::{
    convert::TryInto,
    ops::{Deref, DerefMut},
};

use thiserror::Error;

use crate::{
    chainmaker_sdk::{
        sim_context::{SimContext, SUCCESS_CODE},
        sim_context_rs::ResultSet,
    },
    errors::ContextError,
};

/// 结果集游标, 对状态数据库进行范围或前缀查询返回的结果集游标
pub struct ResultSetCursor {
    raw_cursor: Box<dyn ResultSet>,
}

/// 结果集游标可能返回的错误
#[derive(Debug, Error)]
pub enum ResultSetCursorError {
    #[error("NextRowError, code: {0}")]
    NextRowError(i32),

    #[error("GetKeyError, msg: {0}")]
    GetKeyError(String),

    #[error("GetFieldError, msg: {0}")]
    GetFieldError(String),

    #[error("GetValueError, msg: {0}")]
    GetValueError(String),
}

impl ResultSetCursor {
    pub fn next_item(&mut self) -> Result<Option<(String, String, Vec<u8>)>, ResultSetCursorError> {
        if !self.raw_cursor.has_next() {
            Ok(None)
        } else {
            match self.raw_cursor.next_row() {
                Ok(codec) => {
                    let key = codec
                        .get_string("key")
                        .map_err(ResultSetCursorError::GetKeyError)?;

                    let field = codec
                        .get_string("field")
                        .map_err(ResultSetCursorError::GetKeyError)?;

                    let value = codec
                        .get_bytes("value")
                        .map_err(ResultSetCursorError::GetValueError)?;

                    Ok(Some((key, field, value)))
                }
                Err(code) => Err(ResultSetCursorError::NextRowError(code)),
            }
        }
    }
}

/// 我们自己封装的合约上下文, 用来保证next_id之类的功能
pub struct Context {
    /// 上下文中保存的next_id, 当上下文对象释放时, 会将next_id写回世界状态数据库
    inner: Box<dyn SimContext>,
    next_id: u64,
}

impl Drop for Context {
    fn drop(&mut self) {
        // 将next_id写回世界状态数据库
        if self
            .inner
            .put_state_from_key("t0_nextuid", &self.next_id.to_be_bytes())
            != SUCCESS_CODE
        {
            panic!("pub next_uid back to database failed")
        };
    }
}

impl Context {
    /// 创建上下文
    pub fn new<C: SimContext + 'static>(ctx: C) -> Self {
        let out = ctx
            .get_state_from_key("t0_nextuid")
            .expect("read nextuid from chain failed");
        let next_id = u64::from_be_bytes(out[..].try_into().expect("invalid nextuid storage"));
        Context {
            inner: Box::new(ctx),
            next_id,
        }
    }

    /// 重新初始化uid
    pub fn reinit_uid(&mut self) {
        self.next_id = 1u64;
    }

    /// 记录日志
    pub fn log(&self, msg: &str) {
        self.inner.log(msg);
    }

    /// 返回合约成功
    pub fn ok(&self, value: &[u8]) -> Result<(), ContextError> {
        let code = self.inner.ok(value);
        if code == SUCCESS_CODE {
            Ok(())
        } else {
            Err(ContextError::OkError(code))
        }
    }

    /// 返回合约失败
    pub fn error(&self, body: &str) -> Result<(), ContextError> {
        let code = self.inner.error(body);
        if code == SUCCESS_CODE {
            Ok(())
        } else {
            Err(ContextError::ErrError(code))
        }
    }

    /// 获取发起链码执行的组织名
    pub fn sender_org_id(&self) -> String {
        self.inner.get_sender_org_id()
    }

    /// 按照键, 获取合约执行参数
    pub fn arg(&self, key: &str) -> Result<Vec<u8>, ContextError> {
        self.inner.arg(key).map_err(|m| ContextError::GetArgError {
            key: key.to_owned(),
            msg: m,
        })
    }

    pub fn arg_bool(&self, key: &str) -> Result<bool, ContextError> {
        let out = self.inner.arg(key).map_err(|m| ContextError::GetArgError {
            key: key.to_owned(),
            msg: m,
        })?;
        if out.len() != 1 {
            Err(ContextError::GetArgError {
                key: key.to_owned(),
                msg: format!("bool need 1 byte, but get {}", out.len()),
            })
        } else {
            Ok(out[0] != 0)
        }
    }

    /// 按照键, 获取[`u64`]类型的合约执行参数
    pub fn arg_u64(&self, key: &str) -> Result<u64, ContextError> {
        let out = self.inner.arg(key).map_err(|m| ContextError::GetArgError {
            key: key.to_owned(),
            msg: m,
        })?;

        if out.len() != std::mem::size_of::<u64>() {
            Err(ContextError::GetArgError {
                key: key.to_owned(),
                msg: format!("u64 need 8 bytes, but get {}", out.len()),
            })
        } else {
            Ok(u64::from_be_bytes(out[..].try_into().unwrap()))
        }
    }

    /// 创建新的uid
    pub fn new_uid(&mut self) -> u64 {
        let ret = self.next_id;
        self.next_id += 1;
        ret
    }

    pub fn next_uid(&self) -> u64 {
        self.next_id
    }

    /// 在key范围之间进行遍历
    pub fn iter_range_key(
        &self,
        start_key: &str,
        end_key: &str,
    ) -> Result<ResultSetCursor, ContextError> {
        match self.inner.new_iterator(start_key, end_key) {
            Ok(v) => Ok(ResultSetCursor { raw_cursor: v }),
            Err(code) => Err(ContextError::KvIteratorCreateFailed(code)),
        }
    }

    /// 在对key前缀进行遍历
    pub fn iter_prefix_key(&self, key_prefix: &str) -> Result<ResultSetCursor, ContextError> {
        match self.inner.new_iterator_prefix_with_key(key_prefix) {
            Ok(v) => Ok(ResultSetCursor { raw_cursor: v }),
            Err(code) => Err(ContextError::KvIteratorCreateFailed(code)),
        }
    }

    /// 对某个key下的field按照range查询
    pub fn iter_range_field(
        &self,
        key: &str,
        start_field: &str,
        end_field: &str,
    ) -> Result<ResultSetCursor, ContextError> {
        match self
            .inner
            .new_iterator_with_field(key, start_field, end_field)
        {
            Ok(v) => Ok(ResultSetCursor { raw_cursor: v }),
            Err(code) => Err(ContextError::KvIteratorCreateFailed(code)),
        }
    }

    /// 对某个key下的field按照前缀进行查询
    pub fn iter_prefix_field(
        &self,
        key: &str,
        field_prefix: &str,
    ) -> Result<ResultSetCursor, ContextError> {
        match self
            .inner
            .new_iterator_prefix_with_key_field(key, field_prefix)
        {
            Ok(v) => Ok(ResultSetCursor { raw_cursor: v }),
            Err(code) => Err(ContextError::KvIteratorCreateFailed(code)),
        }
    }

    /// 返回发起合约执行的组织ID
    pub fn get_sender_org_id(&self) -> String {
        self.inner.get_sender_org_id()
    }

    /// 查询状态, 注意如果状态没有值, 不会报错, 而是返回的Vec<u8>为空.
    pub fn get_state(&self, key: &str, field: &str) -> Result<Vec<u8>, ContextError> {
        self.inner
            .get_state(key, field)
            .map_err(ContextError::GetStateFailed)
    }

    /// 查询状态, field为空字符串. 注意如果状态没有值, 不会报错, 而是返回的Vec<u8>为空.
    pub fn get_state_from_key(&self, key: &str) -> Result<Vec<u8>, ContextError> {
        self.inner
            .get_state_from_key(key)
            .map_err(ContextError::GetStateFromKeyFailed)
    }

    /// 设置状态
    pub fn put_state(&mut self, key: &str, field: &str, value: &[u8]) -> Result<(), ContextError> {
        let code = self.inner.put_state(key, field, value);
        if code == SUCCESS_CODE {
            Ok(())
        } else {
            Err(ContextError::PutStateFailed(code))
        }
    }

    /// 设置状态, field为空
    pub fn put_state_from_key(&mut self, key: &str, value: &[u8]) -> Result<(), ContextError> {
        let code = self.inner.put_state_from_key(key, value);
        if code == SUCCESS_CODE {
            Ok(())
        } else {
            Err(ContextError::PutStateFromKeyFailed(code))
        }
    }

    /// 删除key, field对应的状态
    pub fn delete_state(&mut self, key: &str, field: &str) -> Result<(), ContextError> {
        let code = self.inner.delete_state(key, field);
        if code == SUCCESS_CODE {
            Ok(())
        } else {
            Err(ContextError::DeleteStateFailed(code))
        }
    }

    /// 删除key下对应的状态
    pub fn delete_state_from_key(&mut self, key: &str) -> Result<(), ContextError> {
        let code = self.inner.delete_state_from_key(key);
        if code == SUCCESS_CODE {
            Ok(())
        } else {
            Err(ContextError::DeleteStateFromKeyFailed(code))
        }
    }
}

impl Deref for Context {
    type Target = Box<dyn SimContext>;

    fn deref(&self) -> &Self::Target {
        &self.inner
    }
}

impl DerefMut for Context {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.inner
    }
}
