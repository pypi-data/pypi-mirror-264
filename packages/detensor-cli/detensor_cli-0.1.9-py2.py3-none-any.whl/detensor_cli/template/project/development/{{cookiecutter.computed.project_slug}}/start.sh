
source ./.venv/bin/activate
echo -e "\033[32m 已激活虚拟环境 \033[0m"
echo -e "\033[32m 当前目录： \033[0m"
pwd

echo -e "\033[32m 下载依赖包到虚拟环境中 \033[0m"
#!/bin/bash
# 读取 requirements.txt 中的包名
while IFS= read -r package; do
    package=$(echo $package | tr -d '\r\n')
    echo -n "$package... "

    # 使用pip下载包
    pip install $package > /dev/null 2>&1

    # 判断下载是否成功，并在同一行显示绿色的 "Down"
    if [ $? -eq 0 ]; then
        echo -e "\033[1;32mDown\033[0m"
    else
        echo " - Failed"
    fi
done < requirement.txt

# Check for protobuf-compiler
echo "Checking for Protobuf Compiler..."
if dpkg -s protobuf-compiler &> /dev/null; then
    echo "Protobuf Compiler is already installed."
else
    read -p "Protobuf Compiler is not installed. Install it? [Y/n] " response
    response=${response:-Y}
    if [[ $response =~ ^[Yy]$ ]]; then
        echo "Installing Protobuf Compiler..."
        if sudo apt-get install -y protobuf-compiler &> /dev/null; then
            echo -e "Protobuf Compiler  \e[32mDown\e[0m"
        else
            echo "Installation of Protobuf Compiler failed."
        fi
    fi
fi

# Check for podman
echo "Checking for Podman..."
if dpkg -s podman &> /dev/null; then
    echo "Podman is already installed."
else
    read -p "Podman is not installed. Install it? [Y/n] " response
    response=${response:-Y}
    if [[ $response =~ ^[Yy]$ ]]; then
        echo "Installing Podman..."
        if sudo apt-get install -y podman &> /dev/null; then
            echo -e "Podman  \e[32mDown\e[0m"
        else
            echo "Installation of Podman failed."
        fi
    fi
fi

# Check for podman-compose
echo "Checking for Podman-Compose..."
if pip3 list | grep -q podman-compose &> /dev/null; then
    echo "Podman-Compose is already installed."
else
    read -p "Podman-Compose is not installed. Install it using pip3? [Y/n] " response
    response=${response:-Y}
    if [[ $response =~ ^[Yy]$ ]]; then
        echo "Installing Podman-Compose..."
        if pip3 install podman-compose &> /dev/null; then
            echo -e "Podman-Compose  \e[32mDown\e[0m"
        else
            echo "Installation of Podman-Compose failed."
        fi
    fi
fi

#!/bin/bash

# 镜像列表，每行一个镜像名称
images=(
    "harbor.distribute-compute.cn/mpcc-demo/hb_py:latest"
    "harbor.distribute-compute.cn/mpcc-demo/storage-layer-mock:latest"
    "harbor.distribute-compute.cn/mpcc-demo/external-fn:latest"
    "harbor.distribute-compute.cn/jlx/tps-test:1.0.1"
)
for image in "${images[@]}"
do
    echo -n "Pulling image: $image "
    podman pull $image --quiet 2> /dev/null
    result=$?

    if [ $result -eq 0 ]; then
        echo -e "$image  \e[32mDone\e[0m"
    else
        echo -e "$image  \e[31mFail\e[0m"
    fi
done






echo -e "\033[32m pulling harbor.distribute-compute.cn/mpcc-demo/hb_py:latest \033[0m"
podman pull harbor.distribute-compute.cn/mpcc-demo/hb_py:latest
echo -e "\033[32m pulling harbor.distribute-compute.cn/mpcc-demo/hb_py:latest done \033[0m"


echo -e "\033[32m pulling harbor.distribute-compute.cn/mpcc-demo/storage-layer-mock:latest \033[0m"
podman pull harbor.distribute-compute.cn/mpcc-demo/storage-layer-mock:latest
echo -e "\033[32m pulling harbor.distribute-compute.cn/mpcc-demo/storage-layer-mock:latest done \033[0m"


echo -e "\033[32m pulling harbor.distribute-compute.cn/mpcc-demo/external-fn:latest \033[0m"
podman pull harbor.distribute-compute.cn/mpcc-demo/external-fn:latest
echo -e "\033[32m pulling harbor.distribute-compute.cn/mpcc-demo/external-fn:latest done \033[0m"

echo -e "\033[32m pulling harbor.distribute-compute.cn/jlx/tps-test:1.0.1 \033[0m"
podman pull harbor.distribute-compute.cn/jlx/tps-test:1.0.1
echo -e "\033[32m pulling harbor.distribute-compute.cn/jlx/tps-test:1.0.1 done \033[0m"


echo -e "\033[32m 创建mpcc网桥 \033[0m"

nn=$(podman network create mpcc-bridge --subnet=10.89.0.0/24 --gateway=10.89.0.1)

# 更改cniVersion字段为0.4.0
sed -i 's/"cniVersion": "[^"]*"/"cniVersion": "0.4.0"/g' $nn




# 子目录名称
subdir="storage-layer-mock"

# 检查子目录是否存在
if [ -d "$subdir" ]; then
  # 进入子目录
  cd "$subdir" || exit

  # 在此处执行需要的命令
  echo "现在在子目录 $subdir 中"

  podman-compose up -d

  # 返回到原始目录
  cd - > /dev/null
fi

echo "回到了原始目录"

# 子目录名称
subdir="external-fn"

# 检查子目录是否存在
if [ -d "$subdir" ]; then
  # 进入子目录
  cd "$subdir" || exit

  # 在此处执行需要的命令
  echo "现在在子目录 $subdir 中"

  podman-compose up -d

  # 返回到原始目录
  cd - > /dev/null
fi

echo "回到了原始目录"



# 子目录名称
subdir="compute-core/scripts"

# 检查子目录是否存在
if [ -d "$subdir" ]; then
  # 进入子目录
  cd "$subdir" || exit

  # 在此处执行需要的命令
  echo "现在在子目录 $subdir 中"

  chmod +x *

  # 返回到原始目录
  cd - > /dev/null
fi

echo "回到了原始目录"





