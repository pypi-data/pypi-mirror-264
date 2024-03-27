# STORAGE API 设计

storage 的 API设计从原则上按照RESTful API的原则进行设计.
同时参考了k8s的API组的设计.

通常用
路径
`/{API_VERSION}/namespaces/{NAMESPACE_NAME}/{KIND}/{NAME}`
来访问命名空间中具体的对象, 如果该对象类型使用了版本,
那么上述端点直接`GET`访问会返回版本为键,对象为值的字典.
如果在对象类型使用了版本的情况下, 将版本放到query参数中.
即: `/{API_VERSION}/namespaces/{NAMESPACE_NAME}/{KIND}/{NAME}?version={VERSION}`

对于不在命名空间中的资源, 通常用路径
`/{API_VERSION}/{KIND}/{NAME}`
来访问具体的对象, 如果该对象类型使用了版本,
那么上述端点直接`GET`访问会返回版本为键,对象为值的字典.
如果在对象类型使用了版本的情况下要访问具体的资源, 请将版本放到query参数中.
即: `/{API_VERSION}/{KIND}/{NAME}?version={VERSION}`

对于链上的对象, 可以使用`objects`API, 直接由UID获取对象内容.
即: `/core/v1/objects/{UID}`.

对于私有的对象, 由于其`UID`仅在同一类型中唯一,所以访问方法有所不同.
应使用路径: `/{API_VERSION}/namespaces/{NAMESPACE_NAME}/{KIND}/_{UID}`
或 `/{API_VERSION}/{KIND}/_{UID}`.
即使用`_`作为前缀进行访问. 因为对象的名称必须是合法的DNS label,
因此不能有`_`.所以这样可以将{UID}和对象名称的方式分隔开.

不同的对象,可能需要实现针对自身对象类型独特的API接口,
这些接口应该实现在标准接口的基础上, 可以添加额外的query参数,或是使用更深层级的路径.

所有的API接口,应当有swagger 2的API文档, 生成的方法请参考`swaggo`.
具体需要的工作是按照其标准添加注释. 编译过程中, 
相关工具可以直接从注释生成对应的swagger.json和swagger.yaml.

目前的实现, 已经默认开启了swagger支持, 可以直接访问服务的 `swa`
路径来使用swagger.

项目目前详细的API定义, 请参考`swagger/swagger.yaml`. 或启动应用后在swagger页面中查看.
