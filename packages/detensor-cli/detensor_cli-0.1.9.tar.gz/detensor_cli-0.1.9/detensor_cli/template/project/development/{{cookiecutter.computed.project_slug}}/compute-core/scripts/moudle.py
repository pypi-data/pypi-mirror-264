import subprocess
import os
import os.path as osp
def init_pwd():
    '''change pwd to project root'''
    path = osp.dirname(osp.dirname(osp.abspath(__file__)))
    os.chdir(path)
#执行并输出到终端
def execute_cmd(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            print(output.decode().strip())
    return process.poll()
#停止并删除
def stop():
    #清除storage-mock
    command='podman rm -f storage-layer-mock'
    try:
        process = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        pass
    #删除tps-test
    command = 'podman ps -aqf "name=tps-test"'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 获取命令输出
    output, error = process.communicate()
    if process.returncode == 0:
        # 解析输出结果
        container_ids = output.decode().strip().split('\n')
        # print(output)
        if container_ids[0]=='':
            count=0
        else:
            count = len(container_ids)
        #删除容器
        if count!=0:
            for i in container_ids:
                cmd=f'podman rm -f {i}'
                remove = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                remove.wait()
        print("清空容器")
    else:
        print("执行命令出错:", error.decode())


