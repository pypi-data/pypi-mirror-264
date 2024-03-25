#! /usr/bin/env python3

from typing import List
import json
import requests

NAMESPACE = 'example-ns'
BASE_URL = 'http://zhongtai.servers.unicde.com.cn:81/masa/api/bizflow/executeApi/1/0/7a287095505a4d3bb8e5c85db33ff3da'

out = requests.post(BASE_URL).json()
schema = out['data']['result']

RECORD_META = {
    'name': 'schema-record',
    'namespace': NAMESPACE
}

AUTHORS: List[str] = [
    "wx-org1.chainmaker.org",
]

ret = {
    "apiVersion": "core/v1",
    "kind": "proposal",
    "metadata": {
        "name": "create-schema-record-proposal",
        "namespace": NAMESPACE,
    },
    "spec": {
        'actions': [
            {
                "create": {
                    "object": {
                        "apiVersion": "core/v1",
                        "kind": "record",
                        "metadata": RECORD_META,
                        "spec": {
                            "authors": AUTHORS,
                            "content": schema,
                        }
                    }
                }
            }
        ]
    }
}



print(json.dumps(ret, ensure_ascii=False, indent=4))

