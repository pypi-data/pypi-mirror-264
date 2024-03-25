#!/bin/bash
# 安装apt和wget

pwd

sudo apt install apt
sudo apt install apt-get
sudo apt update
sudo apt install wget

sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak

# 替换源为清华大学源
echo "替换为清华大学源..."
sudo sh -c 'echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ $(lsb_release -sc) main restricted universe multiverse" > /etc/apt/sources.list'
sudo sh -c 'echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ $(lsb_release -sc)-updates main restricted universe multiverse" >> /etc/apt/sources.list'
sudo sh -c 'echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ $(lsb_release -sc)-backports main restricted universe multiverse" >> /etc/apt/sources.list'
sudo sh -c 'echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ $(lsb_release -sc)-security main restricted universe multiverse" >> /etc/apt/sources.list'

# 更新软件包列表
echo "更新软件包列表..."
sudo apt update

echo "替换为清华大学源完成！"

# 安装Git
sudo apt-get update
sudo apt-get install git -y

# 验证安装
git --version

# Update package list and install necessary tools
sudo apt update
sudo apt install -y wget

# 下载 Go 1.18 压缩文件
wget -O go1.18.linux-amd64.tar.gz https://mirrors.ustc.edu.cn/golang/go1.18.linux-amd64.tar.gz

# 检查下载文件的完整性
if [ $? -eq 0 ]; then
    echo "File download successful. Proceeding with extraction."
    # 解压下载的压缩文件到 /usr/local 目录
    sudo tar -C /usr/local -xzf go1.18.linux-amd64.tar.gz
else
    echo "File download failed. Please try downloading again."
fi

# 设置 GOROOT 环境变量
export GOROOT=/usr/local/go

# 创建 GOPATH 目录并包含 bin、src、pkg 三个子目录
mkdir -p ~/gopath/bin
mkdir -p ~/gopath/src
mkdir -p ~/gopath/pkg

# 设置 GOPATH 环境变量
export GOPATH=~/gopath

# 将 Go 可执行文件路径添加到 PATH 中
export PATH=$PATH:$GOROOT/bin

# 将 GOROOT 和 GOPATH 添加到 ~/.bashrc 文件中
echo 'export GOROOT=/usr/local/go' >> ~/.bashrc
echo 'export GOPATH=~/gopath' >> ~/.bashrc
echo 'export PATH=$PATH:$GOROOT/bin' >> ~/.bashrc
echo 'export GOPROXY=https://goproxy.cn' >> ~/.bashrc


# 输出 Go 版本信息
go version

#卸载安装包
rm go1.18.linux-amd64.tar.gz

# 安装GCC
sudo apt-get install build-essential -y

# 验证安装
gcc --version

pwd

# 获取当前目录的绝对路径
CURRENT_DIR=$(pwd)

# 将当前目录下的 main 目录添加到 PATH 环境变量中
echo "export PATH=\$PATH:$CURRENT_DIR/chainmaker-go/main" >> ~/.bashrc

# 使更改生效
source ~/.bashrc

echo "环境变量已成功添加并已生效。"





cd chainmaker-cryptogen
make

cd ../chainmaker-go
rm go.sum && go mod download chainmaker.org/chainmaker/chainconf/v2 && go mod tidy

cd tools
ln -s ../../chainmaker-cryptogen/ .





cd cmc
go build
cp cmc ../../../storage

cd ../../scripts
./prepare.sh 4 1
tree -L 3 ../build/
./build_release.sh
tree ../build/release/
./cluster_quick_start.sh normal
mkdir -p ../build/bak
mv ../build/release/*.tar.gz ../build/bak
ps -ef|grep chainmaker | grep -v grep
netstat -lptn | grep 1230
cat ../build/release/*/log/system.log |grep "ERROR\|put block\|all necessary"




cd ../../storage


#安装swagger
echo "安装 swagger..."
go install github.com/swaggo/swag/cmd/swag@latest

# 安装 Docker
echo "安装 Docker..."
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install -y docker-ce

# 启动 Docker 服务
sudo systemctl start docker
sudo systemctl enable docker

# 添加当前用户到 docker 用户组，以免每次都需要 sudo
sudo usermod -aG docker $USER

# 安装 Docker Compose
echo "安装 Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 显示 Docker 和 Docker Compose 版本信息
docker --version
docker-compose --version

echo "Docker 和 Docker Compose 安装完成。请注销并重新登录以使用户组更改生效。"

#!/bin/bash

# 下载并运行 Rust 官方安装脚本
echo "安装rust"
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 添加 Rust 工具链到 PATH 环境变量
source $HOME/.cargo/env

# 显示 Rust 版本信息
rustc --version
cargo --version

rustup target add wasm32-unknown-unknown

# 下载 MySQL
sudo apt install mysql-server -y

# 启动 MySQL 服务
sudo systemctl start mysql

# 设置 MySQL 开机自启动
sudo systemctl enable mysql

# 等待 MySQL 服务启动
sleep 5

# 设置 root 用户的密码为 root
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';"

# 重启 MySQL 服务
sudo systemctl restart mysql

# 显示 MySQL 服务状态
sudo systemctl status mysql


#安装hurl
VERSION=4.2.0
curl --location --remote-name https://github.com/Orange-OpenSource/hurl/releases/download/$VERSION/hurl_${VERSION}_amd64.deb
sudo apt update && sudo apt install ./hurl_${VERSION}_amd64.deb && rm ./hurl_${VERSION}_amd64.deb

make boot-all