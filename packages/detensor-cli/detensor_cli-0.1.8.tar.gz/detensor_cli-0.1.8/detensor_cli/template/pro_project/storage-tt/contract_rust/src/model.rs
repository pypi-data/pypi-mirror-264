use std::convert::TryInto;

use crate::{
    context::Context,
    errors::ChainModelError,
    objects::{controllers, get_type_meta, meta::TypeMeta, parse_fn, Object},
};

const OBJECT_TABLE_PREFIX: &str = "t1c";

const OBJECT_INDEX_PREFIX: &str = "i1c";

const GLOBAL_NAMESPACE: &str = "";

/// 链上数据模型
pub struct ChainModel<'a> {
    /// 链上下文
    context: &'a mut Context,
}

impl<'a> ChainModel<'a> {
    pub fn new(ctx: &'a mut Context) -> Self {
        ChainModel { context: ctx }
    }

    pub fn new_uid(&mut self) -> u64 {
        self.context.new_uid()
    }

    pub fn ctx(&self) -> &Context {
        self.context
    }

    pub fn ctx_mut(&mut self) -> &mut Context {
        self.context
    }

    fn parse_object(raw: &[u8]) -> Result<Box<dyn Object>, ChainModelError> {
        let json_value: serde_json::Value = serde_json::from_slice(raw)?;
        let type_meta = get_type_meta(&json_value)?;
        let parse_fn = parse_fn(&type_meta).ok_or(ChainModelError::UnsupportedObject(
            type_meta.api_version,
            type_meta.kind,
        ))?;
        let out = parse_fn(json_value)?;
        Ok(out)
    }

    fn be_uid_from_vec(be_bytes: Vec<u8>) -> Result<u64, ChainModelError> {
        let ret = u64::from_be_bytes(be_bytes.try_into().map_err(|e| {
            ChainModelError::StateError(format!(
                "invalid uid from object_name_index, error content: {:?}",
                e
            ))
        })?);
        Ok(ret)
    }

    fn convert_api_version(api_version: &str) -> String {
        let mut ret = String::new();
        for c in api_version.chars() {
            ret.push(if c == '/' { '_' } else { c })
        }
        ret
    }

    /// 根据对象的uid, 构造对象表的键
    #[inline]
    fn object_table_key(uid: u64) -> String {
        let b62 = base62::encode(uid);
        format!("{}_{:0>11}", OBJECT_TABLE_PREFIX, b62)
    }

    /// 根据对象kind, 命名空间和对象名称, 该获取在对象名称索引的键.
    #[inline]
    fn object_index_key(type_meta: &TypeMeta, namespace: &str, name: &str) -> String {
        format!(
            "{}_{}_{}_{}_{}",
            OBJECT_INDEX_PREFIX,
            Self::convert_api_version(&type_meta.api_version),
            type_meta.kind,
            namespace,
            name
        )
    }

    /// 根据对象的kind和命名空间, 获取对象名称索引的前缀,
    /// 这个前缀通常用来扫描一个命名空间下所有该kind的对象的uid
    #[allow(unused)]
    #[inline]
    fn ns_index_prefix(type_meta: &TypeMeta, namespace: &str) -> String {
        format!(
            "{}_{}_{}_{}_",
            OBJECT_INDEX_PREFIX,
            Self::convert_api_version(&type_meta.api_version),
            type_meta.kind,
            namespace
        )
    }

    #[inline]
    fn type_prefix(type_meta: &TypeMeta) -> String {
        format!(
            "{}_{}_{}_",
            OBJECT_INDEX_PREFIX,
            Self::convert_api_version(&type_meta.api_version),
            type_meta.kind
        )
    }

    #[inline]
    fn object_index_key_by_obj(o: &dyn Object) -> String {
        Self::object_index_key(
            o.type_meta(),
            o.namespace().unwrap_or(GLOBAL_NAMESPACE),
            o.name(),
        )
    }

    /// 向对象名称索引中,添加索引条目
    ///
    /// 有意让这个函数私有, 主要是不希望用户直接修改索引,
    /// 索引的维护应该尽可能自动完成
    fn add_index_key(&mut self, o: &dyn Object) -> Result<(), ChainModelError> {
        let uid = o.uid();
        let encoded_uid = uid.to_be_bytes();
        let index_key = Self::object_index_key_by_obj(o);
        self.ctx().log(&format!(
            "add_index_key, uid: {}, index_key: {}",
            uid, index_key
        ));
        match o.version() {
            Some(v) => {
                self.context.put_state(&index_key, v, &encoded_uid)?;
            }
            None => {
                self.context.put_state_from_key(&index_key, &encoded_uid)?;
            }
        }
        Ok(())
    }

    /// 从对象名称索引中,删除索引条目
    ///
    /// 有意让这个函数私有, 主要是不希望用户直接修改索引,
    /// 索引的维护应该尽可能自动完成
    fn delete_index_key(&mut self, o: &dyn Object) -> Result<(), ChainModelError> {
        let index_key = Self::object_index_key_by_obj(o);
        match o.version() {
            None => self.context.delete_state_from_key(&index_key)?,
            Some(v) => self.context.delete_state(&index_key, v)?,
        };
        Ok(())
    }

    /// 向对象表中放置对象, 索引将自动被更新
    pub fn put_object(&mut self, obj: &dyn Object) -> Result<(), ChainModelError> {
        let uid = obj.uid();
        let key = Self::object_table_key(uid);
        let value = self.context.get_state_from_key(&key)?;
        let json_bytes = obj.to_json()?;
        if value.is_empty() {
            // 原来的uid中没有对象
            // 插入对象, 并更新索引
            self.context.put_state_from_key(&key, &json_bytes[..])?;
            self.add_index_key(obj)?;
        } else {
            // 原来的uid中有对象
            let old_obj = Self::parse_object(&value[..])?;

            // 检查, 更新对象是否修改了对象的类型
            if old_obj.kind() != obj.kind() {
                return Err(ChainModelError::MismatchedKind {
                    uid,
                    old_kind: old_obj.kind().to_owned(),
                    new_kind: obj.kind().to_owned(),
                });
            }

            // 删除旧的对象索引
            self.delete_index_key(old_obj.as_ref())?;

            // 添加新的对象索引
            self.add_index_key(obj)?;

            // 将新的对象插入数据库
            self.context.put_state_from_key(&key, &json_bytes[..])?;
        }
        Ok(())
    }

    /// 按照uid查找对象, 返回对象JSON编码的 [`Vec<u8>`] 形式.
    pub fn get_raw_object_by_uid(&self, uid: u64) -> Result<Option<Vec<u8>>, ChainModelError> {
        let key = Self::object_table_key(uid);
        let out = self.context.get_state_from_key(&key)?;
        if out.is_empty() {
            return Ok(None);
        }

        Ok(Some(out))
    }

    /// 按照名称和版本查找对象, 返回对象的 [`Box<dyn Object>`] 形式.
    pub fn get_object_by_name_version(
        &self,
        type_meta: &TypeMeta,
        name: &str,
        namespace: Option<&str>,
        version: Option<&str>,
    ) -> Result<Option<Box<dyn Object>>, ChainModelError> {
        match self.get_raw_object_by_name_version(type_meta, name, namespace, version)? {
            None => Ok(None),
            Some(raw) => Ok(Some(Self::parse_object(&raw)?)),
        }
    }

    /// 按照名称和版本查找对象, 返回对象编码的 [`Vec<u8>`] 形式.
    ///
    /// 注意, 这一接口仅返回一个对象
    pub fn get_raw_object_by_name_version(
        &self,
        type_meta: &TypeMeta,
        name: &str,
        namespace: Option<&str>,
        version: Option<&str>,
    ) -> Result<Option<Vec<u8>>, ChainModelError> {
        let index_key =
            Self::object_index_key(type_meta, namespace.unwrap_or(GLOBAL_NAMESPACE), name);
        self.ctx().log(&format!(
            "get_raw_object_by_name_version, index_key: {}",
            index_key
        ));
        let field = version.unwrap_or("");
        let raw_uid = self.context.get_state(&index_key, field)?;
        if raw_uid.is_empty() {
            return Ok(None);
        }
        let uid = Self::be_uid_from_vec(raw_uid)?;

        if let Some(out) = self.get_raw_object_by_uid(uid)? {
            Ok(Some(out))
        } else {
            Err(ChainModelError::StateError(format!(
                "index error, uid {} is empty in object table",
                uid
            )))
        }
    }

    /// 按照命名空间与名称查找对象, 返回一个JSON格式的[`Vec<u8>`].
    /// 这个接口是一个汇聚查询接口, 直接用来面对查询请求,
    /// 不建议在合约开发中使用这个接口作为查询工具.
    ///
    /// 注意, 这一接口根据扫描索引的不同情况, 会返回不同形式的JSON.
    /// - 如果一个field都没有扫描到, 返回[`Option::None`]
    /// - 如果扫描过程中, field只扫描到一个且为空字符串,
    ///   直接返回对应对象存储在对象表中的JSON形式
    /// - 如果扫描过程中, 扫描到多个field, 那么返回一个JSON数组,
    ///   数组内是所有扫描到的对象的JSON形式
    pub fn get_raw_object_by_ns_name(
        &self,
        type_meta: &TypeMeta,
        name: &str,
        namespace: Option<&str>,
    ) -> Result<Option<Vec<u8>>, ChainModelError> {
        let namespace = namespace.unwrap_or("");
        let index_key = Self::object_index_key(type_meta, namespace, name);
        let mut iter = self.ctx().iter_prefix_key(&index_key)?;
        let mut uids: Vec<u64> = Vec::new();
        let mut has_empty_field = false;
        while let Some((_, field, v)) = iter.next_item()? {
            let uid = Self::be_uid_from_vec(v)?;
            uids.push(uid);
            if field.is_empty() {
                if has_empty_field {
                    return Err(ChainModelError::StateError(format!(
                        "version can't be empty, uid: {}",
                        uid
                    )));
                }
                has_empty_field = true;
            }
        }

        if uids.is_empty() {
            // 一个field都没有扫描到.
            Ok(None)
        } else if uids.len() == 1 && has_empty_field {
            // 仅扫描到一个field, 且field为空, 返回查询到的对象的JSON形式.
            let uid = uids[0];
            let out = self.get_raw_object_by_uid(uid)?.ok_or_else(|| {
                ChainModelError::StateError(format!(
                    "index error, uid {} is empty in object table",
                    uid
                ))
            })?;
            Ok(Some(out))
        } else {
            // 多个field, 返回一个json数组.
            let mut ret = vec![b'['];
            ret.push(b']');

            let mut is_first = true;
            for uid in uids {
                let mut out = self.get_raw_object_by_uid(uid)?.ok_or_else(|| {
                    ChainModelError::StateError(format!(
                        "index error, uid {} is empty in object table",
                        uid
                    ))
                })?;

                if !is_first {
                    ret.push(b',');
                } else {
                    is_first = false;
                }

                ret.append(&mut out);
            }
            Ok(Some(ret))
        }
    }

    /// 按照uid查找对象, 返回对象的 [`Box<dyn Object>`] 形式
    pub fn get_object_by_uid(&self, uid: u64) -> Result<Option<Box<dyn Object>>, ChainModelError> {
        let key = Self::object_table_key(uid);
        let out = self.context.get_state_from_key(&key)?;
        if out.is_empty() {
            return Ok(None);
        }
        Ok(Some(Self::parse_object(&out[..])?))
    }

    /// 按照uid删除对象, 以[`Box<dyn Object>`]的形式返回删除的对象
    pub fn delete_object_by_uid(
        &mut self,
        uid: u64,
    ) -> Result<Option<Box<dyn Object>>, ChainModelError> {
        let key = Self::object_table_key(uid);
        let out = self.context.get_state_from_key(&key)?;

        if out.is_empty() {
            // can't find object to delete
            Ok(None)
        } else {
            // 删除对象储存
            self.context.delete_state_from_key(&key)?;

            let ret = Self::parse_object(&out[..])?;
            // 删除对象索引
            self.delete_index_key(ret.as_ref())?;

            // 返回删除的对象
            Ok(Some(ret))
        }
    }

    /// 根据命名空间的名字查找命名空间下所有对象的uid
    ///
    /// 流程上, 大致是先获取所有的kind,
    /// 之后按照kind和命名空间构造索引的前缀.
    /// 使用每个前缀, 扫描uid, 将所有的uid汇聚返回.
    pub fn get_uid_by_ns(&self, namespace: &str) -> Result<Vec<u64>, ChainModelError> {
        let mut uids = Vec::new();
        for meta in controllers().keys() {
            let prefix = Self::ns_index_prefix(meta, namespace);
            let mut range = self.ctx().iter_prefix_key(&prefix)?;
            while let Some((_, _, v)) = range.next_item()? {
                let uid = u64::from_be_bytes(v.try_into().unwrap());
                uids.push(uid);
            }
        }
        Ok(uids)
    }

    pub fn get_uid_by_type(
        &self,
        type_meta: &TypeMeta,
        namespace: &str,
    ) -> Result<Vec<u64>, ChainModelError> {
        let mut ret = Vec::new();

        let key_prefix = if namespace.is_empty() {
            Self::type_prefix(type_meta)
        } else {
            Self::ns_index_prefix(type_meta, namespace)
        };

        let mut range = self.ctx().iter_prefix_key(&key_prefix)?;
        while let Some((_, _, v)) = range.next_item()? {
            let uid = u64::from_be_bytes(v.try_into().unwrap());
            ret.push(uid)
        }
        Ok(ret)
    }
}

#[cfg(test)]
mod test {
    use super::ChainModel;

    #[test]
    pub fn test_object_table_key() {
        let uid = 1;
        let key = ChainModel::object_table_key(uid);
        assert!(key == "t1c_00000000001")
    }
}
