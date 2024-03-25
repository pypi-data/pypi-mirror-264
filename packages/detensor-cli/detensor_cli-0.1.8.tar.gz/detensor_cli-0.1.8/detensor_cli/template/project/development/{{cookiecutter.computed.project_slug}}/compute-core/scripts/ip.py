#! /usr/bin/env python3
import socket
import requests
def get_local_ip():
    try:
        # 创建一个socket连接
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))  # 连接到一个公共的IP地址
        # 获取本地IP地址
        local_ip = sock.getsockname()[0]
        sock.close()
        return local_ip
    except socket.error:
        return "Unable to get local IP"

# 另一种获取公网ip的方式
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        data = response.json()
        ip = data['ip']
        return ip
    except requests.RequestException:
        return "Unable to get public IP"

def get_ip():
    return get_local_ip()

