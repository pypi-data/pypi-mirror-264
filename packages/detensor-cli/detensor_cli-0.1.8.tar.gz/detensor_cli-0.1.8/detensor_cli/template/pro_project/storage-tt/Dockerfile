# 使用Ubuntu 20.04作为基础镜像
FROM ubuntu:20.04

# 设置环境变量
ENV INSTALL_DIR=/tmp

# 定义工作目录
WORKDIR /storage

RUN sed -i 's#http://archive.ubuntu.com/#http://mirrors.tuna.tsinghua.edu.cn/#' /etc/apt/sources.list;

# 更新软件包列表并安装make
# RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update && \
    apt-get install -y make

RUN apt-get update && \ 
    apt-get install -y libxml2-dev
    
RUN apt-get update && \ 
    apt-get install -y libcurl4-openssl-dev
# hurl
RUN apt-get install -y wget \
    && rm -rf /var/lib/apt/lists/* 


# 安装 MySQL 和其他必要的软件包
RUN apt-get update && \
    apt-get install -y mysql-server && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 设置root用户的初始密码为123456
RUN service mysql start && \
    mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456'; FLUSH PRIVILEGES;"

# 暴露MySQL默认端口
EXPOSE 3306


# 设置入口点

COPY  . /storage


RUN tar -xzf hurl-3.0.0-x86_64-linux.tar.gz -C /tmp
    # rm hurl-3.0.0-x86_64-linux.tar.gz 
ENV PATH=$INSTALL_DIR/hurl-3.0.0:$PATH

CMD [ "bash" ]
