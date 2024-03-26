#!/bin/bash
#长安链的节点数
param1=4
#长安链的条数
param2=1
if [ "$#" -eq 2 ]; then
    param1=$1
    param2=$2
fi
# 进入scripts目录并运行prepare.sh脚本
cd ../ && cd scripts && echo -e "\n\n\n" | ./prepare.sh $param1 $param2

# 在scripts目录下构建发布版本
cd ../ && cd scripts && ./build_release.sh

# 在scripts目录下快速启动集群
cd ../ && cd scripts && ./cluster_quick_start.sh normal

# 删除tools/cmc/testdata目录下的crypto-config文件夹
cd ../ && rm -rf tools/cmc/testdata/crypto-config

# 复制build目录下的crypto-config文件夹到tools/cmc/testdata目录
cp -r build/crypto-config tools/cmc/testdata
echo "长安链部署完成"