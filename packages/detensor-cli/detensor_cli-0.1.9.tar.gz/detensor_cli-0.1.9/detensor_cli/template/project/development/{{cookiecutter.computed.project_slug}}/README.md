# 多方共识计算系统 示例说明

## 注意

在使用docker部署前，请先使用main分支部署测试一下，安装必要的环境。在运行之前，请先清空storage-layer-mock和external-fn容器。

## 系统需求

**Ubuntu 22.04 LTS**

安装 protoc ，可能需要管理员权限

```bash
apt install protobuf-compiler
```

安装 podman， 可能需要管理员权限

```bash
apt install podman
```

安装 podman-compose，可能需要管理员权限

```bash
pip3 install podman-compose
```



**Python 3.10**

安装 grpc

```bash
pip3 install grpcio
```

安装&更新 protobuf

```bash
pip3 install --upgrade protobuf
```



## 准备工作

拉取项目到本地并切换到jlx分支

```bash
git clone https://gitlab.distribute-compute.cn/dist-compute/mpcc-demo.git
git checkout jlx
```



拉取镜像到本地

**motif_py**

```bash
podman pull harbor.distribute-compute.cn/mpcc-demo/motif_py:latest
```



**storage-layer-mock**

```bash
podman pull harbor.distribute-compute.cn/mpcc-demo/storage-layer-mock:latest
```



**external-fn**

```bash
podman pull harbor.distribute-compute.cn/mpcc-demo/external-fn:latest
```



**tps-test**

```
podman pull harbor.distribute-compute.cn/jlx/tps-test:1.0.1
```



创建网络并配置网段

```
config_dir="$HOME/.config/cni/net.d"                                                                                                             
sudo apt-get update                                                                                                                              
sudo apt-get install jq                                                                                                                          
cni=$(find $config_dir -type f -name "*podman.conflist" -exec sh -c 'jq -r .cniVersion {}' \;)                                                   
podman network create mpcc-bridge                                                                                                                
jq ".cniVersion = \"$cni\"" $HOME/.config/cni/net.d/mpcc-bridge.conflist > temp.json && mv temp.json $HOME/.config/cni/net.d/mpcc-bridge.conflist
```

创建之后打开网络配置文件（默认在用户目录下.config/cni/net.d）

可能需要更新版本号为0.4.0，与同目录下的podman.comflist一致



配置子网和网关，要求节点实际ip在这个网段内,示例中ip如下所示

```
"subnet": "10.89.0.0/24",
"gateway": "10.89.0.1"
```



## 重启服务

使用start脚本启动时会自动启动storage-mock和external-fn，stop脚本会关闭并清空所有的tps-test容器和storage-mock容器，如果对storage文件有更新，请先清除原有的storage-layer-mock并重新启动。启动流程参考main下的readme文件



## 示例

### 示例1 - Hello World

1. 启动1个计算节点

   在`/compute-core`目录下执行

   ```bash
   scripts/start -c 1
   ```

2. 发起计算请求

   在`/compute-core`目录下执行

   ```bash
   scripts/python_exec_sync -u 1 -m org0 
   ```

   预期结果

   ```bash
   (org0, 0)
   process status: 0
   procsse stdout: b'Hello World!\n'
   process stderr: b''
   ```

3. 关闭计算节点

   在`/compute-core`目录下执行

   ```bash
   scripts/stop
   ```



### 示例2 - motif使用实例

1. 启动2个计算节点

   在`/compute-core`目录下执行

   ```bash
   scripts/start -c 2
   ```
   
3. 发起计算请求

   在`/compute-core`目录下执行。A节点发起计算合约2的请求，参与方有org0, org1 分别对应代码中的 A, B。

   ```bash
   scripts/python_exec_sync -u 2 -m org0 org1
   ```

   预期结果

   ```bash
   (org0, 0)
   process status: 0
   procsse stdout: b'30\n'
   process stderr: b''
   ```

4. 关闭节点

   ```bash
   scripts/stop
   ```
   





