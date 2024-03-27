# 用户部署环境使用说明

## 长安链系统需求

#### golang

要求golang版本在1.16-1.19

#### gcc

版本大于7.3

#### 7z

```
# ubuntu
apt-get install p7zip-full p7zip-rar

# centos
yum -y install epel-release
yum -y install p7zip p7zip-plugins
```

#### docker

参考官网：https://docs.docker.com/engine/install/

## storage系统需求

#### swag

这个工具用来从注释中自动生成swagger 2 API定义文件. 方便我们使用swagger进行API调试.

安装方法

```shell
go install github.com/swaggo/swag/cmd/swag@latest
```

#### rust

我们的智能合约在长安链和雄安链上均以WebAssembly的形式实现. 这两条链也提供了基于rust的SDK. 所以开发语言使用rust语言.

开发智能合约,你需要最新的rust编译器,cargo和rustup. 安装方法可以参考rust的[官方网站](https://www.rust-lang.org/zh-CN/).

你还需要安装wasm32-unknown-unknown的工具链. 安装方法

```
rustup target add wasm32-unknown-unknown
```

#### mysql

配置mysql，密码设置为123456

## 计算层系统需求

参考mpcc-demo

https://gitlab.distribute-compute.cn/dist-compute/mpcc-demo/-/blob/main/README.md

## 部署流程

### 1.启动长安链

将目录切换到chainmaker-go/scripts/

执行develop.sh

```
cd chainmaker-go/scripts
./develop.sh
```

### 2.启动storage

将目录切换到storage-tt

```
cd storage-tt
make boot-all
```

## 示例

### 示例1

切换到storage-tt

```
cd storage-tt
```

#### 创建命名空间

```Shell
./http-request namespace
```

#### 创建函数

**创建函数声明**

```Shell
./http-request function-declare
```

**创建合约**

```Shell
./http-request contract
```

**创建函数和函数绑定**

```Shell
./http-request funtion
```

#### 启动计算层

切换到compute-core

```
./scripts/start -c 1 --real 9001
./scripts/python_exec_sync -u 6 -m wx-org1.chainmaker.org
```

计算结果

```
(wx-org1.chainmaker.org, 0)
process status: 0
procsse stdout: b"{'sum': 20, 'dif': 0}\n20\n"
process stderr: b''
```

## 停止实例

#### 停止计算层

```
cd compute-core
./scripts/stop
```

#### 停止storage

```
cd storage-tt
make clean-all
```

#### 停止长安链

```
cd chainmaker-go/scripts
./cluster_quick_stop.sh
```



###### 
