
source ./.venv/bin/activate

echo -e "\033[32m 激活虚拟环境 \033[0m"
echo -e "\033[32m 当前目录： \033[0m"
pwd


echo -e "\033[32m installing protobuf-compiler \033[0m"
sudo apt install protobuf-compiler -y
echo -e "\033[32m installing protobuf-compiler done \033[0m"


echo -e "\033[32m installing podman \033[0m"
sudo apt install podman -y
echo -e "\033[32m installing podman done \033[0m"

echo -e "\033[32m 下载依赖包 \033[0m"
pip install -r requirements.txt

echo -e "\033[32m installing podman-compose \033[0m"
pip3 install podman-compose
echo -e "\033[32m installing podman-compose done \033[0m"


echo -e "\033[32m installing grpcio \033[0m"
pip3 install grpcio
echo -e "\033[32m installing grpcio done \033[0m"



echo -e "\033[32m installing protobuf \033[0m"
pip3 install --upgrade protobuf
echo -e "\033[32m installing protobuf done \033[0m"


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





