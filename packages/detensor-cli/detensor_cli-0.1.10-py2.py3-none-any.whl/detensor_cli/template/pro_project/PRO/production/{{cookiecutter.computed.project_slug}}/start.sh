#!/bin/bash
# 安装apt和wget

pwd

sudo apt install apt
sudo apt install apt-get
sudo apt update
sudo apt install wget

# 安装Git
sudo apt-get update
sudo apt-get install git -y

# 验证安装
git --version



#安装rust
# 设置清华大学镜像源
export RUSTUP_DIST_SERVER=https://mirrors.tuna.tsinghua.edu.cn/rustup
export RUSTUP_UPDATE_ROOT=https://mirrors.tuna.tsinghua.edu.cn/rustup/rustup

# 检查是否已安装 Rust
if command -v rustc &> /dev/null
then
    echo "Rust 已安装."
else
    echo "Rust 未安装，将进行安装"

    # 安装 Rust
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable --profile default --no-modify-path
    source $HOME/.cargo/env
    echo "Rust 安装完成."
fi

# 添加 Cargo 环境变量
export PATH="$HOME/.cargo/bin:$PATH"
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> $HOME/.bashrc
source $HOME/.bashrc

# 检测并显示 Cargo 和 rustc 的版本信息
cargo --version
rustc --version


rustup target add wasm32-unknown-unknown

#!/bin/bash

# 安装 Docker
install_docker() {
    echo "正在安装 Docker..."
    sudo apt-get update
    sudo apt-get remove docker docker-engine docker.io containerd runc -y
    sudo apt-get install apt-transport-https ca-certificates curl software-properties-common -y
    curl -fsSL https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io -y
    sudo usermod -aG docker $USER
    sudo systemctl enable docker
    sudo systemctl start docker
    echo "Docker 安装完成."
}

# 安装 Docker Compose
install_docker_compose() {
    echo "正在安装 Docker Compose..."
    sudo curl -L "https://get.daocloud.io/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "Docker Compose 安装完成."
}

# 检查是否已安装 Docker
if command -v docker &> /dev/null
then
    echo "Docker 已安装，将进行卸载并重新安装"

    # 卸载并重新安装 Docker
    install_docker
else
    echo "Docker 未安装，将进行安装"

    # 安装 Docker
    install_docker
fi

# 检查是否已安装 Docker Compose
if command -v docker-compose &> /dev/null
then
    echo "Docker Compose 已安装，将进行卸载并重新安装"

    # 卸载并重新安装 Docker Compose
    sudo rm /usr/local/bin/docker-compose
    install_docker_compose
else
    echo "Docker Compose 未安装，将进行安装"

    # 安装 Docker Compose
    install_docker_compose
fi


# Update package list and install necessary tools
sudo apt update
sudo apt install -y wget

#!/bin/bash

# Check if Go 1.18 is installed
if command -v go &> /dev/null; then
    go_version=$(go version)
    if [[ $go_version == *"go1.18"* ]]; then
        echo "Go 1.18 is already installed."
    else
        echo "A different version of Go is installed. Installing Go 1.18."
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

    fi
else
    echo "Go is not installed. Installing Go 1.18."
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

fi

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

#安装swagger
echo "安装 swagger..."
go install github.com/swaggo/swag/cmd/swag@latest




# 下载 MySQL
sudo apt install mysql-server -y

# 启动 MySQL 服务
sudo systemctl start mysql

# 设置 MySQL 开机自启动
sudo systemctl enable mysql

# 等待 MySQL 服务启动
sleep 5

# 设置 root 用户的密码为 123456
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456';"

# 重启 MySQL 服务
sudo systemctl restart mysql

# 显示 MySQL 服务状态
sudo systemctl status mysql


#安装hurl
VERSION=4.2.0
curl --location --remote-name https://github.com/Orange-OpenSource/hurl/releases/download/$VERSION/hurl_${VERSION}_amd64.deb
sudo apt update && sudo apt install ./hurl_${VERSION}_amd64.deb && rm ./hurl_${VERSION}_amd64.deb



# 部署长安链
rm go.sum && go mod download chainmaker.org/chainmaker/chainconf/v2 && go mod tidy
cd chainmaker-cryptogen
make


cd ../chainmaker-go
rm go.sum && go mod download chainmaker.org/chainmaker/chainconf/v2 && go mod tidy

cd tools
ln -s ../../chainmaker-cryptogen/ .

cd cmc
go build
cp cmc ../../../storage-tt

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

#部署storage-tt
cd ../../storage-tt
make boot-all