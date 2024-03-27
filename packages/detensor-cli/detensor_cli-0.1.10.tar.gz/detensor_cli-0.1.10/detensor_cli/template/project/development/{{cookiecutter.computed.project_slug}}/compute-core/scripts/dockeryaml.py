import yaml
import os
def generate_docker_compose_file(num_services,ip):
    #storage-mock
    external_compose={
        'version': '3',
        'services': {},
    }
    service = {
        'image': 'external-fn:latest',
        'container_name': 'external-fn',
        'environment': [
            f'ADDR={ip}',
            'PORT=7000',
        ],
        'ports': [
                '7000:7000',  # usr_port:宿主机任意不冲突端口
            ],
        'network_mode': 'host',
    }
    external_compose['services']['external-fn'] = service

   
    #external-fn
    storage_compose={
        'version': '3',
        'services': {},
    }
    service = {
        'image': 'storage-layer-mock:latest',
        'container_name': 'storage-layer-mock',
        'environment': [
            f'ADDR={ip}',
            'PORT=30000',
            'SOURCE_DIR=/test-src',
            'PRIVATES_PATH=/multi/privates.json',
            'EXTERNALS_PATH=/multi/externals.json',
            'COMPILE_CMD=none'
        ],
        'volumes': [
            './test-src:/test-src',
            './multi:/multi'
        ],
        'network_mode': 'host',
    }
    storage_compose['services']['storage-layer-mock'] = service

    #compute-core
    docker_compose = {
        'version': '3',
        'services': {},
        'networks': {
            'mpcc-bridge': {
                'external': True
            }
        }
    }
    
    
    
    for i in range(num_services):
        service_name = f'tps-test{i}'
        config_file = f'./config{i}.yaml'
        container_name = f'tps-test{i}'
        network_address = f'10.89.0.{10+i}'
        service = {
            'image': 'tps-test:1.0.1',
            'container_name': container_name,
            'volumes': [
                f'{config_file}:/MPCC/config.yaml'
            ],
            'environment': {
                'RUST_LOG': 'debug',
                'WAIT_HOSTS': f'{ip}:30000',  # 和storage_url一致
                'WAIT_HOSTS_TIMEOUT': 120
            },
            'ports': [
                f'{3000+i}:{3000+i}',  # usr_port:宿主机任意不冲突端口
                f'{13000+i}:{13000+i}'  # port:external_url的端口
            ],
            'privileged': True,
            'networks': {
                'mpcc-bridge': {
                    'ipv4_address': network_address
                }
            }
        }

        docker_compose['services'][service_name] = service
    # 获取当前脚本所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建上级目录的路径
    parent_dir = os.path.dirname(current_dir)
    # 指定生成文件的路径
    filename = os.path.join(parent_dir, 'docker-compose.yaml')
    with open(filename, 'w') as f:
        yaml.dump(docker_compose, f)
    print(f'Generated {filename}.')
    #找到根目录
    root_dir = os.path.dirname(parent_dir)
    #在storage-layer-mock生成dockerfile
    filename = os.path.join(root_dir,'storage-layer-mock','docker-compose.yaml')
    with open(filename, 'w') as f:
        yaml.dump(storage_compose, f)
    print(f'Generated {filename}.')
    #external-fn生成dockerfile
    filename = os.path.join(root_dir,'external-fn','docker-compose.yaml')
    with open(filename, 'w') as f:
        yaml.dump(external_compose, f)
    print(f'Generated {filename}.')

