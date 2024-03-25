#! /usr/bin/env python3
import os
import os.path as osp
import shutil
import sys

if len(sys.argv) < 2:
    INSTANCE = 'test-instance'
else:
    INSTANCE = sys.argv[1]

LOG_LEVEL = 'DEBUG'
NET_PORT = '11301'
RPC_PORT = '12301'
MONITOR_PORT = '14321'
PPROF_PORT = '24321'
CHAIN_ID = 'chain1'

print('chain instance name:', INSTANCE)
print('log level:', LOG_LEVEL)
print('chain id:', CHAIN_ID)
print('net port:', NET_PORT)
print('rpc port:', RPC_PORT)


print('begin generate crypto and config file:')
shutil.copy(
    './crypto_config_template.yml',
    './crypto_config.yml'
    )

shutil.copy(
    './deployment_template.yml',
    './deployment.yml'
    )
os.system('sed -i s/{{instance}}/%s/ %s' % (INSTANCE, './crypto_config.yml'))
os.system('sed -i s/{{instance}}/%s/ %s' % (INSTANCE, './deployment.yml'))

if os.system(f'chainmaker-cryptogen -c ./crypto_config.yml generate') != 0:
    print('chainmaker-cryptogen failed')
    exit(-2) 

os.mkdir('./crypto')
os.mkdir('./flat')
os.mkdir('./ca')


# collect ca certs
for dir in os.listdir('./crypto-config'):
    print(f'collocate ca from org: {dir}')
    target_dir = osp.join('./ca', dir)
    os.mkdir(target_dir)
    shutil.copy(osp.join('./crypto-config', dir, 'ca/ca.crt'), target_dir)

def get_peer_id(org: str):
    path = osp.join('./crypto-config', org, 'node/consensus1/consensus1.nodeid')
    with open(path, 'r') as f:
        return f.read().strip()

def org_addr(org_index: int) -> str:
    return f"wx-org{org_index}-chainmaker-org-{INSTANCE}"

def gen_seeds():
    orgs = os.listdir('./crypto-config')
    orgs.sort()
    ret = []
    for i, org in enumerate(orgs):
        peer_id = get_peer_id(org)
        seed = f'/dns/{org_addr(i + 1)}/tcp/{NET_PORT}/p2p/{peer_id}'
        ret.append(seed)
    return ret


def gen_chainmaker_config(org_id: str):
    with open('./config_tpl/chainmaker.tpl', 'r') as f:
        content = f.read()
    content = content.replace('{chain_id}', CHAIN_ID)
    content = content.replace('{enable_dockervm}', 'false')
    content = content.replace('{dockervm_container_name}', '')
    content = content.replace('{org_id}', org_id)
    content = content.replace('{org_path}', 'k8s')
    content = content.replace('{net_port}', NET_PORT)
    content = content.replace('{monitor_port}', MONITOR_PORT)
    content = content.replace('{pprof_port}', PPROF_PORT)
    content = content.replace('{node_cert_path}', 'node/consensus1/consensus1.sign')
    content = content.replace('{rpc_port}', RPC_PORT)
    content = content.replace('{rpc_cert_path}', 'node/consensus1/consensus1.tls')
    content = content.replace('{net_cert_path}', 'node/consensus1/consensus1.tls')

    seeds = '\n'.join([ f'    - {s}' for s in gen_seeds()])
    content = content.replace('seeds:', 'seeds:\n' + seeds)

    return content

def gen_flat_chainmaker_config(org_id: str):
    with open('./config_tpl/flat_chainmaker.tpl', 'r') as f:
        content = f.read()
    content = content.replace('{chain_id}', CHAIN_ID)
    content = content.replace('{enable_dockervm}', 'false')
    content = content.replace('{dockervm_container_name}', '')
    content = content.replace('{org_id}', org_id)
    content = content.replace('{org_path}', 'k8s')
    content = content.replace('{net_port}', NET_PORT)
    content = content.replace('{monitor_port}', MONITOR_PORT)
    content = content.replace('{pprof_port}', PPROF_PORT)
    content = content.replace('{node_cert_path}', 'consensus1.sign')
    content = content.replace('{rpc_port}', RPC_PORT)
    content = content.replace('{rpc_cert_path}', 'consensus1.tls')
    content = content.replace('{net_cert_path}', 'consensus1.tls')

    seeds = '\n'.join([ f'    - {s}' for s in gen_seeds()])
    content = content.replace('seeds:', 'seeds:\n' + seeds)

    return content

def bc_config():
    with open('./config_tpl/chainconfig/bc_4_7.tpl', 'r') as f:
        content = f.read()
    content = content.replace('{chain_id}', CHAIN_ID)
    content = content.replace('{version}', 'v1.0.0')
    content = content.replace('{consensus_type}', '1')
    orgs = os.listdir('./crypto-config')
    orgs.sort()
    for (i, org) in enumerate(orgs):
        content = content.replace('{org%d_id}' % (i + 1,), org)
        content = content.replace('{org%d_peerid}' % (i + 1,), get_peer_id(org))
        content = content.replace('{org_path}', 'k8s')
    return content

def flat_bc_config():
    with open('./config_tpl/chainconfig/flat_bc.tpl', 'r') as f:
        content = f.read()
    content = content.replace('{chain_id}', CHAIN_ID)
    content = content.replace('{version}', 'v1.0.0')
    content = content.replace('{consensus_type}', '1')
    orgs = os.listdir('./crypto-config')
    orgs.sort()
    for (i, org) in enumerate(orgs):
        content = content.replace('{org%d_id}' % (i + 1,), org)
        content = content.replace('{org%d_peerid}' % (i + 1,), get_peer_id(org))
        content = content.replace('{org_path}', 'k8s')
    return content

def gen_log():
    with open('./config_tpl/log.tpl', 'r') as f:
        content = f.read()
    content = content.replace('{log_level}', LOG_LEVEL)
    return content

def gen_sdk_config():
    orgs = os.listdir('./crypto-config')
    orgs.sort()
    with open('./sdk_config_template.yml', 'r') as f:
        template = f.read()
    for (i, org) in enumerate(orgs):
        index = i + 1
        print(f'generate sdk config for org{index}:', org)
        content = template.replace('{org_id}', org)
        content = content.replace('{org_addr}', f'{org_addr(index)}')
        content = content.replace('{chain_id}', CHAIN_ID)
        with open(f'./sdk_config{index}.yaml', 'w') as f:
            f.write(content)

bc_config_content = bc_config()
flat_bc_config_content = flat_bc_config()
log_config_content = gen_log()

for dir in os.listdir('./crypto-config'):
    print(f'processing org: {dir}')
    os.makedirs(f'./crypto/{dir}/certs')
    os.makedirs(f'./crypto/{dir}/chainconfig')
    shutil.copytree('./ca', osp.join('./crypto', dir, 'certs/ca'))
    shutil.copytree(
        osp.join('./crypto-config', dir, 'node'), 
        osp.join('./crypto', dir, 'certs/node'))
    shutil.copytree(
        osp.join('./crypto-config', dir, 'user'), 
        osp.join('./crypto', dir, 'certs/user'))
    shutil.copy('./config_tpl/chainmaker.tpl', osp.join('./crypto', dir, 'chainmaker.yml'))
    with open(osp.join('./crypto', dir, 'chainmaker.yml'), 'w') as f:
        f.write(gen_chainmaker_config(dir))
    with open(osp.join('./crypto', dir, 'chainconfig/bc1.yml'), 'w') as f:
        f.write(bc_config_content)
    with open(osp.join('./crypto', dir, 'log.yml'), 'w') as f:
        f.write(log_config_content)

print('process flat:')
for dir in os.listdir('./crypto-config'):
    print(f'processing org: {dir}')
    os.makedirs(osp.join('./flat', dir))
    for org in os.listdir('./crypto-config'):
        target_dir = f'./flat/{dir}/ca_{org}.crt'
        shutil.copy(osp.join('./crypto-config', org, 'ca/ca.crt'), target_dir)
    shutil.copy(osp.join('./crypto-config', dir, 'node/consensus1/consensus1.sign.key'), f'./flat/{dir}')
    shutil.copy(osp.join('./crypto-config', dir, 'node/consensus1/consensus1.sign.crt'), f'./flat/{dir}')
    shutil.copy(osp.join('./crypto-config', dir, 'node/consensus1/consensus1.tls.key'), f'./flat/{dir}')
    shutil.copy(osp.join('./crypto-config', dir, 'node/consensus1/consensus1.tls.crt'), f'./flat/{dir}')
    with open(osp.join('./flat', dir, 'chainmaker.yml'), 'w') as f:
        f.write(gen_flat_chainmaker_config(dir))
    with open(osp.join('./flat', dir, 'bc1.yml'), 'w') as f:
        f.write(flat_bc_config_content)
    with open(osp.join('./flat', dir, 'log.yml'), 'w') as f:
        f.write(log_config_content)

print('gen sdk_config:')
gen_sdk_config()



