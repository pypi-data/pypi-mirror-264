# STORAGE

## 开发说明

### 需要的工具

### cmc 长安链命令行工具
参考[长安链的文档](https://docs.chainmaker.org.cn/dev/%E5%91%BD%E4%BB%A4%E8%A1%8C%E5%B7%A5%E5%85%B7.html)进行编译, 将编译产物`cmc`放置到本项目的根目录下.


#### docker, docker-compose
为了在本地环境下启动长安链的测试链, 你需要安装docker和docker-compose.

#### golang

你需要最近两个版本的golang环境, 安装和下载可以参考golang的[官方网站](https://golang.google.cn/).

#### swag
这个工具用来从注释中自动生成swagger 2 API定义文件. 方便我们使用swagger进行API调试.

安装方法
```bash
$ go install github.com/swaggo/swag/cmd/swag@latest
```

#### rust
我们的智能合约在长安链和雄安链上均以WebAssembly的形式实现.
这两条链也提供了基于rust的SDK.
所以开发语言使用rust语言.

开发智能合约,你需要最新的rust编译器,cargo和rustup. 
安装方法可以参考rust的[官方网站](https://www.rust-lang.org/zh-CN/).

你还需要安装wasm32-unknown-unknown的工具链.
安装方法
```bash
$ rustup target add wasm32-unknown-unknown
```

### 启动与停止

关闭所有当前运行的系统,并重新编译代码并启动整个系统.
可以运行命令
`make boot-all`

关闭所有当前运行的系统, 可以运行命令.
`make clean-all`


系统启动后, 会启动四个实例, 分别对应四个组织.

1. 端口 9001, 组织wx-org1.chainmaker.org
2. 端口 9002, 组织wx-org2.chainmaker.org
3. 端口 9003, 组织wx-org3.chainmaker.org
4. 端口 9004, 组织wx-org4.chainmaker.org

### swagger

系统启动后, 访问路径 `http://localhost:9001/swagger/index.html`.
可以访问实例1的swagger页面, 可以使用不同的端口访问不同实例的swagger页面.


### 自动测试

执行`make contract-test`, 对智能合约进行自动测试.

执行`make backend-test`, 对后端整体进行自动测试.

