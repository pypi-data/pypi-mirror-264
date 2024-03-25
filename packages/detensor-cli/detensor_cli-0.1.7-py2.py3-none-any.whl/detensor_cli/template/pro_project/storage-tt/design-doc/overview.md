# STORAGE API 总体文档

storage API 是一个用于管理链上链下数据对象与计算合约的RESTful API.
它的设计参考了k8s的API设计.

storage API 将链上链下的数据对象与计算合约使用统一的对象模型进行管理.

对象分为两种, 公开对象与私有对象.
- 公开对象包括私有数据,私有函数的接口与计算合约, 
  所以不包含任何实际的私有数据, 这些对象都保存在区块链上.

- 私有数据包括实际的私有数据与私有函数接口的实际定义,
  因为包含实际的私有数据, 所以这些对象都保存在私有的关系数据库中.


## 对象的基本结构
每个对象, 都有其对应的API组(apiVersion)和类型(kind),
API组起到API版本化的能力.

一个对象, 除了API组与类型, 可以分为3个部分.
- 元数据(metadata) 描述了对象的名称, uid, 命名空间和注解等.
- 对象具体定义(spec) 描述了对象的实际定义内容.
- 对象状态定义(status) 描述了对象的当前状态. 这个部分是可选的. 私有对象通常没有这个部分.


对象的元数据主要包括对象的uid, 名称, 版本与命名空间. 其中版本和命名空间是可选的.
只有某些类型的对象具有版本或命名空间.

对象的uid是一个非负整数, 是对象的唯一标识, 在一个storage API的实例中, 
所有的公开对象的uid都是唯一的, 且所有有效的uid均大于0,
即使不同类型的对象的uid都不会重复, 已经删除的对象的uid不会重复使用.

但私有对象的uid在不同类型的对象之间会重复, 已经删除的对象的uid会重复使用.
请注意到这个差别.

对象的名称是可以修改的, 但是出于API的设计考虑, 所有对象的名称都必须满足RFC1035的DNS label的要求, 即:
- 长度在1-63个字节之间.
- 由小写英文字符,数字和连字符'-'组成.
- 第一个字符必须是小写英文字符.
- 最后一个字符不能是连字符'-'.

## API的基本结构

使用名称访问一个具有命名空间的对象的路径基本构成是:
`/{apiVersion}/namespace/{namespace}/{kind}/{name}`.

使用名称访问一个没有命名空间的对象的路径的基本构成是:
`/{apiVersion}/{kind}/{name}`

使用uid访问一个对象的路径是:
`/{apiVersion}/{kind}/{uid}`


注意,由于对象名称的限制, storage API的实现会根据请求的URL自行判断是使用uid或名称访问对象.

如果对象的元数据中包含了版本, 那么使用名称进行查询, 将直接返回该名称的全部版本的对象.
如果要限制查询的版本, 可以使用`version`查询参数.

对于公开对象, 还提供了直接通过`uid`查询具体对象的API接口.
`/core/v1/objects/{uid}`

如果要按照类型获取同一类型的所有对象, 可以使用路径
`/{apiVersion}/{kind}/`.

如果要限制类型的命名空间, 可以使用路径
`/{apiVersion}/namespace/{namespace}/{kind}`


对于对象的查询, 均使用GET方法.

一些对象类型, 会具有特有的修改状态的API接口, 这些接口通常在基本的路径上拓展.

## 公开对象的修改与提议机制

由于公开对象定义了涉及多个参与方的对象, 所以不能由单个参与方直接进行公开对象的操作.

所以创建,修改,删除对象需要通过以下的流程.
1. 创建提议
2. 各个组织批准提议
3. 提议创建者提交提议
4. 提议自动执行, 实现对象的创建, 修改与删除

提议本身也是对象, 只是可以由storage API的用户直接进行操作.
用户通过storage API可以直接创建, 批准, 撤回或提交提议.

提议一经创建, 就会保留在链上, 
撤回后, 会进入撤回状态, 但是不会从链上删除.

提议的生命周期状态, 批准情况与提议的执行结果都会保存在提议对象的状态上.

根据提议的作用范围, 提议分为全局提议对象与提议对象两种对象.
- 全局提议对象(globalproposal)用来操作无命名空间的公开对象
- 提议对象(proposal)用来操作有命名空间的公开对象.
  注意,提议对象本身就具有命名空间, 它只能操作自己所在命名空间内的公开对象.

## 公开对象的类型定义
处于开发的便利, 我们在文档中列出公开对象的类型定义.

这里我们直接使用`typescript`的类型定义.


### 提议 proposal

提议不能通过提议机制进行更改. 对提议的变动可以直接使用
对应的API.

首先是提议(proposal)对象的类型定义.
```typescript
interface Proposal {
    // 常量: core/v1
    apiVersion: string;

    // 常量: proposal
    kind: string;

    // 对象的元数据
    metadata: ProposalMetadata;

    // 对象的具体定义
    spec: ProposalSpec;

    // 提议对象的状态
    status: ProposalStatus;
}

// 提议对象的元数据
interface ProposalMetadata {
    // 提议的名称
    name: string;

    // 提议所属的命名空间
    namespace: string;

    // 提议的uid, 创建提议对象时可以省略
    uid: number;

    // 创建提议的组织, 创建提议对象时可以省略
    creator: string;
}


// 提议对象的具体定义
interface ProposalSpec {
    // 提议中所包含的动作.
    // 不能为空
    actions: [ProposalAction]
}

// 提议中涉及到的一个动作
// 注意, create, update, delete 三个字段只能同时存在一个
interface ProposalAction {
    // 创建一个对象的动作
    create?: CreateObjectAction,

    // 更新一个对象的动作
    update?: UpdateObjectAction,

    // 删除一个对象的动作
    delete?: DeleteObjectAction,
}

interface CreateObjectAction {
    // 要创建的对象的JSON表示
    object: any
}

interface UpdateObjectAction {
    // 要更新的对象的UID
    uid: number,

    // 要更新的新对象的JSON表示
    object: any,
}

interface DeleteObjectAction {
    // 要删除的对象的uid
    uid: number
}

// 提议对象的状态
interface ProposalStatus {
    // 提议对象的声明周期状态
    stage: "Active" | "Submitted" | "Revoke",

    // 提议的批准状态.
    // 这是一个以批准的组织名为键的JSON对象,
    // JSON对象的值是批准的说明.
    permission: {[org_name: string]: string},

    // 提议提交的结果
    results?: [ObjectByAction],
}

// 提议对象对于每个动作的执行结果
// 注意, create, update, delete 三个字段只能同时存在一个
interface ObjectByAction {
    // 创建操作所产生的对象
    create?: any,

    // 更新操作前后的对象
    update?: {
        // 操作前的对象
        old: any,

        // 操作后的对象
        updated: any,
    },

    // 删除操作所删除的对象
    delete?: any,
}
```

### 全局提议 globalproposal

全局提议不能通过提议机制进行修改. 对全局提议的改动, 可以直接使用相应的API.

以下是全局提议(globalproposal)对象的类型定义.
```typescript
interface GlobalProposal {
    // 常量: core/v1
    apiVersion: string;

    // 常量: globalproposal
    kind: string;

    // 对象的元数据
    metadata: GlobalProposalMetadata;

    // 对象的具体定义
    spec: ProposalSpec;

    // 提议对象的状态
    status: ProposalStatus;
}

// 全局提议对象的元数据
interface GlobalProposalMetadata {
    // 提议的名称
    name: string,

    // 提议的uid, 创建提议对象时可以省略
    uid: number,

    // 创建提议的组织, 创建提议对象时可以省略
    creator: string,
}
```

### 命名空间 namespace

命名空间支持通过提议创建和删除, 目前暂不支持更改, 将尽快添加功能.

- 创建 命名空间的创建, 需要待创建命名空间中, 所有成员组织都已经批准同意.
- 删除 命名空间的删除, 需要待删除命名空间中, 所有成员组织都已经批准同意.

以下是命名空间(namespace)对象的类型定义
```typescript
interface Namespace {

    // 常量: core/v1
    apiVersion: string;

    // 常量: namespace
    kind: string;

    // 命名空间对象的元数据
    metadata: NamespaceMetadata;

    // 命名空间对象的具体定义
    spec: NamespaceSpec; 
}

interface NamespaceMetadata {

    // 命名空间的名称
    name: string;

    // 命名空间对象的uid
    uid: u64
}

interface NamespaceSpec {
    // 命名空间的成员组织
    members: [string]
}
```

### 数据声明 datadeclare
数据声明支持通过提议创建,更改与删除.

- 创建 数据声明的创建, 不需要多个组织批准, 单个组织批准即可创建数据声明.
- 更改 数据声明的更改, 需要所有实现了该数据声明的组织的批准.
- 删除 数据声明的删除, 需要所有实现了该数据声明的组织的批准.

数据声明的类型定义

```typescript
interface DataDeclare {

    // 常量: core/v1
    apiVersion: string;

    // 常量: datadeclare
    kind: string;

    // 数据声明的元数据
    metadata: NamespacedMetadata;

    // 数据声明对象的具体定义
    spec: DataDeclareSpec;

    // 数据声明对象的状态
    status: DataDeclareStatus;
}

interface NamespacedMetadata {

    // 对象的名称
    name: string;

    // 对象所属的命名空间
    namespace: string;

    // 对象的uid
    uid: number;

    // 对象的注解, 可选
    annotations?: {[key: string]: any}
}

interface DataDeclareSpec {
    // 数据类型
    dataType: string;
    
    // 关于数据声明的描述
    description: string;
}

interface DataDeclareStatus {
    // 各个组织对于数据声明的实现.
    // 这是一个以实现了数据声明的组织名为键的JSON对象,
    // JSON对象的值是实现的说明.
    implementation: {[key: string]: string}
}
```

### 函数声明 functiondeclare
函数声明支持通过提议创建,更改与删除.

- 创建 函数声明的创建, 不需要多个组织批准, 单个组织批准即可创建函数声明.
- 更改 函数声明的更改, 需要所有实现了该函数声明的组织的批准.
- 删除 函数声明的删除, 需要所有实现了该函数声明的组织的批准.

函数声明的类型定义
```typescript
interface FunctionDeclare {

    // 常量: core/v1
    apiVersion: string;

    // 常量: functiondeclare
    kind: string;

    // 函数声明的元数据
    metadata: NamespacedMetadata;

    // 函数声明对象的具体定义
    spec: FunctionDeclareSpec;

    // 函数声明对象的状态
    status: FunctionDeclareStatus;
}

// 函数声明对象的具体定义
interface FunctionDeclareSpec {
    // 函数参数的声明
    args: [FnArgDeclare];

    // 函数返回类型
    retType: string;

    // 函数的描述
    description: string;
}

// 函数参数的声明
interface FnArgDeclare {
    // 参数的类型
    argType: string;

    // 参数的描述
    description: string;
}

// 函数声明对象的状态
interface FunctionDeclareStatus {
    // 各个组织对于函数声明的实现.
    // 这是一个以实现了函数声明的组织名为键的JSON对象,
    // JSON对象的值是实现的说明.
    implementation: {[key: string]: string}   
}
```

### 计算合约 contract
计算合约支持通过提议创建与删除, 暂不支持修改, 将尽快添加这一功能.

- 创建 计算合约的创建, 需要执行模式中所有涉及的组织的批准.
- 删除 计算合约的删除, 需要执行模式中所有涉及的组织的批准.

```typescript
interface Contract {

    // 常量: core/v1
    apiVersion: string;
    
    // 常量: contract
    kind: string;

    // 计算合约的元数据
    metadata: ContractMetatdata;

    // 计算合约对象的具体定义
    spec: ContractSpec;

    // 计算合约对象的状态
    status: ContractStatus;

}

interface ContractMetadata {

    // 对象的名称
    name: string;

    // 计算合约所属的命名空间
    namespace: string;
    
    // 计算合约的版本
    version: string;

    // 计算合约对象的uid
    uid: number;

    // 计算合约对象的注解
    annotations?: {[key: string]: any}
}

// 合约的执行模式, 就是一个组织名的数组
type ExecPattern = [string];

interface ContractSpec {

    // 合约的内容
    content: string;

    // 合约中引用的数据声明
    // 合约中数据声明引用的标识符为键, 数据声明的uid为值
    data: {[ident: string]: number};

    // 合约中引用的数据声明
    // 合约中数据声明引用的标识符为键, 函数声明的uid为值
    functions: {[ident: string]: number};

    // 合约允许的执行模式
    execPatterns: [ExecPattern],
}


interface ContractStatus {
    
}


```


## 私有对象的类型定义


### 私有数据的定义

```typescript
interface Data {

    // 常量 core/v1
    apiVersion: string;

    // 常量 data
    kind: string;

    // 私有数据对象的元数据
    metadata: Metadata;
    
    // 私有数据对象的具体定义
    spec: DataSpec;

    // 私有数据对象的状态
    status: DataStatus;
}

// 私有数据对象的具体定义
interface DataSpec {
    // 私有数据的具体内容
    content: string;

    // 私有数据的描述
    description: string;
}

interface DataStatus {
    // 私有数据是否可用
    available: boolean;
}

interface Metadata {

    // 对象的uid
    uid: number;

    // 对象的名称
    name: string;
}


```

### 私有函数的定义

```typescript
interface Function {

    // 常量 core/v1
    apiVersion: string;

    // 常量 function
    kind: string;

    // 私有函数的元数据
    metadata: Metadata;

    // 私有函数对象的具体定义
    spec: FunctionSpec;

    // 私有函数对象的状态
    status: FunctionStatus;
}

interface FunctionSpec {
    // 外部函数的url
    content: string;

    // 外部函数的描述
    description: string;
}

interface FunctionStatus {
    // 私有函数是否可用
    available: boolean;
}

```


### 私有数据绑定的定义

```typescript
interface DataBinding {

    // 常量 core/v1
    apiVersion: string;

    // 常量 databinding
    kind: string;

    // 元数据
    metadata: Metadata;

    // 数据绑定的具体定义
    spec: DataBindingSpec;

    // 数据绑定对象的状态
    status: DataBindingStatus;
}

interface DataBindingSpec {
    // 对应的私有数据的uid
    dataUid: number;

    // 对应的私有数据声明的uid
    dataDeclareUid: number;

    // 对应的计算合约的uid
    contractUid: number;
}

interface DataBindingStatus {
    // 是否启用
    available: boolean;
}

```

### 函数绑定的定义

```typescript
interface FunctionBinding {

    // 常量 core/v1
    apiVersion: string;

    // 常量 functionbinding
    kind: string;

    // 元数据
    metadata: Metadata;

    // 数据绑定的具体定义
    spec: FunctionBindingSpec;

    // 数据绑定对象的状态
    status: FunctionBindingStatus;
}

interface FunctionBindingSpec {
    // 对应的私有函数的uid
    functionUid: number;

    // 对应的私有函数声明的uid
    functionDeclareUid: number;

    // 对应的计算合约的uid
    contractUid: number;
}

interface FunctionBindingStatus {
    // 是否启用
    available: boolean;
}

```

## 错误处理

storage API 返回错误, 通常会使用`application/json`的`Content-Type`. 返回JSON编码的错误消息.
错误消息通常是一个字符串.


## swagger

对于详细的API接口, storage API提供了API的swagger定义.
我们提供了`swagger.json`和`swagger.yaml`.

可以使用[swagger editor](https://editor.swagger.io/?utm=22b02)来浏览swagger API文档.


