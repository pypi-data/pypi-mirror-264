# 私有存储相关对象设计文档

## 数据 core/v1 data (data)

data对象由类型，元数据，内容，状态构成：

### TypeMeta

ApiVersion字段为对象所属的API版本。

Kind字段为对象类型名，data对象对应值为"data"。

### Metadata

Name字段为对象名。

Uid字段为对象UID，是对象的唯一标识。

Namespace字段为对象所属命名空间，对于私有对象此处为空。

### DataSpec

Content字段为data对象的数据内容。

Description字段为data对象的数据内容描述。

### DataStatus

Available字段为data对象的数据可用状态，值为true时数据可用，为false时数据不可用。

## 函数 core/v1 function (functions)

function对象由类型，元数据，内容，状态构成：

### TypeMeta

ApiVersion字段为对象所属的API版本。

Kind字段为对象类型名，function对象对应值为"function"。

### Metadata

Name字段为对象名。

Uid字段为对象UID，是对象的唯一标识。

Namespace字段为对象所属命名空间，对于私有对象此处为空。

### FunctionSpec

Content字段为function对象的函数内容。

Description字段为function对象的函数描述。

### FunctionStatus

Available字段为function对象的函数可用状态，值为true时函数可用，为false时函数不可用。

## 数据绑定 core/v1 databinding (databindings)

databinding功能为把一个私有数据绑定在计算合约上。

databinding对象由类型，元数据，内容，状态构成：

### TypeMeta

ApiVersion字段为对象所属的API版本。

Kind字段为对象类型名，databinding对象对应值为"databinding"。

### Metadata

Name字段为对象名。

Uid字段为对象UID，是对象的唯一标识。

Namespace字段为对象所属命名空间，对于私有对象此处为空。

### DataBindingSpec

DataUid字段为被绑定的data对象的UID。

DataDeclareUid字段为被绑定的data对象对应的datadeclare对象的UID。

ContractUid字段为data对象被绑定到的contract对象的UID。

### DataBindingStatus

Available字段为databinding对象的绑定状态，值为true时绑定可用，为false时绑定不可用。

## 函数绑定 core/v1 functionbinding (functionbindings)

functionbinding功能为把一个私有函数绑定在计算合约上。

functionbinding对象由类型，元数据，内容，状态构成：

### TypeMeta

ApiVersion字段为对象所属的API版本。

Kind字段为对象类型名，functionbinding对象对应值为"functionbinding"。

### Metadata

Name字段为对象名。

Uid字段为对象UID，是对象的唯一标识。

Namespace字段为对象所属命名空间，对于私有对象此处为空。

### FunctionBindingSpec

FunctionUid字段为被绑定的fucntion对象的UID。

FunctionDeclareUid字段为被绑定的fucntion对象对应的functiondeclare对象的UID。

ContractUid字段为function对象被绑定到的contract对象的UID。

### FunctionBindingStatus

Available字段为functionbinding对象的绑定状态，值为true时绑定可用，为false时绑定不可用。
