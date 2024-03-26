# 对象查询与过滤的API设计与规范

API 设计签名如下:

```golang
GetObjectWith(conds string) ([]json.RawMessage, error)
```

考虑参考 K8s 的[字段选择器的设计](https://kubernetes.io/zh/docs/concepts/overview/working-with-objects/field-selectors/).

## 介绍

K8s 的字段选择器(Field selectors)允许根据一个或多个资源字段的值来筛选资源. 下面是一些使用字段选择器查询的例子：

```shell
metadata.name=my-service
metadata.namespace!=default
status.phase=Pending
```

下面这个 kubectl 命令将筛选出 status.phase 字段值为 Running 的所有 Pod:

kubectl get pods --field-selector status.phase=Running

我们可以参考上述命令构造 `GetObjectWith` 的 `conds`.

## 支持的操作符

K8s 中可在字段选择器中使用 =, == 和 !=(= 和 == 的意义是相同的)操作符. 例如，下面这个 kubectl 命令将筛选所有不属于 default 命名空间的 K8s 服务:

```shell
kubectl get services  --all-namespaces --field-selector metadata.namespace!=default
```

目前考虑仅仅支持 = 以及 != 两种操作符.

## 链式选择器

同标签和其他选择器一样, 字段选择器可以通过使用逗号分隔的列表组成一个选择链. 下面这个 kubectl 命令将筛选 status.phase 字段不等于 Running 同时 spec.restartPolicy 字段等于 Always 的所有 Pod:

```shell
kubectl get pods --field-selector=status.phase!=Running,spec.restartPolicy=Always
```

通过链式选择器可以实现几个条件的 `AND` 操作.
