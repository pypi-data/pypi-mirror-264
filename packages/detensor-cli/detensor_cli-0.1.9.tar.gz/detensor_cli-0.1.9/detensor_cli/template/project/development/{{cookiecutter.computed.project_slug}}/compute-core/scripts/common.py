import os
import shutil
import os.path as osp
import json
import signal
from io import IOBase
from typing import List, Union

PID_FILENAME = './pids'

def init_pwd():
    '''change pwd to project root'''
    path = osp.dirname(osp.dirname(osp.abspath(__file__)))
    os.chdir(path)

class Proc(object):
    '''
    系统测试运行时的一个进程
    '''
    
    def __init__(self, pid: int, kind: str, index: Union[str, None] = None, binary: Union[str, None] = None) -> None:
        self._pid = pid
        self._kind = kind
        self._index = index
        self._binary = binary
    
    @property
    def pid(self) -> int:
        return self._pid

    @property
    def kind(self) -> str:
        return self._kind
    
    @property
    def index(self) -> Union[str, None]:
        return self._index

    @property
    def binary(self) -> Union[str, None]:
        return self._binary
    
    def to_json(self) -> str:
        d = dict()
        d['pid'] = self.pid
        d['kind'] = self.kind
        if self.index is not None:
            d['index'] = self.index
        if self.binary is not None:
            d['binary'] = self.binary
        return json.dumps(d, indent=None, sort_keys=True)

    def from_json(o: dict):
        return Proc(
            o['pid'],
            o['kind'],
            o.get('index'),
            o.get('binary')
        )


def parse_pid_file(f: IOBase) -> List[Proc]:
    lines = f.readlines()
    out = []
    for line in lines:
        line = line.strip()
        if line == '':
            continue
        out.append(json.loads(line, object_hook=Proc.from_json))
    return out

def stop_procs(procs: List[Proc]):
    for proc in procs:
        pid = proc if type(proc) is int else proc.pid
        print(f'kill process [{pid}]')
        try:
            os.kill(pid, signal.SIGTERM)
        except Exception as e:
            print(e)
            continue

def stop_and_clean_pid(pid_f: IOBase):
    procs = parse_pid_file(pid_f)
    stop_procs(procs)
    pid_f.truncate(0)
    pid_f.seek(0, 0)

def clean_db():
    '''clean db directory'''
    if os.path.exists('./multi/db'):
        shutil.rmtree('./multi/db')
    os.makedirs('./multi/db')