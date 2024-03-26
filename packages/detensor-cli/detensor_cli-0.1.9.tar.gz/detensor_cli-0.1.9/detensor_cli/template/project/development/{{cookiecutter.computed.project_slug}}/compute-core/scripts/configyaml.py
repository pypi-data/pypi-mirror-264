import yaml
import os
import json
def generate_config_file(number,ip):
    for index in range(number):
        config = {
            'org_name': f'org{index}',
            'addr': f'10.89.0.{10+index}',
            'port': 13000 + index,
            'user_addr': f'10.89.0.{10+index}',
            'user_port': 3000 + index,
            'external_url': f'http://{ip}:{13000 + index}',
            'storage_url': f'http://{ip}:30000',
            'storage_layer_token': f'org{index}',
            'db_path': './rocksdb',
            'ps_controller_socket': './sockets/ps_socket.sock',
            'compute_image': 'motif_py:latest',
            'container_remove': 'false',
            'compiler': ['./hbc', '@', '-o', '@']
        }
        # 获取当前脚本所在的目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建上级目录的路径
        parent_dir = os.path.dirname(current_dir)
        # 指定生成文件的路径
        filename = os.path.join(parent_dir, f'config{index}.yaml')
        with open(filename, 'w') as f:
            yaml.dump(config, f)

        print(f'Generated {filename}.')
    import json

#更改external路径
def generate_external_json(ip):
    data = {
        "org0": {
            "calculate": {
                "calling_convention": "simple-json",
                "url": f"http://{ip}:7000/calculate"
            },
            "get_int": {
                "calling_convention": "simple-json",
                "url": f"http://{ip}:7000/get_int"
            }
        }
    }
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(os.path.dirname(current_dir))
    filename=os.path.join(root_dir,'storage-layer-mock','multi','externals.json')
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)