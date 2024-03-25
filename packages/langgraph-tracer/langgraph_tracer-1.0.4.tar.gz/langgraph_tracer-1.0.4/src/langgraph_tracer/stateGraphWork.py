from langgraph.graph import StateGraph as StateGraphOrg
from langchain.load.dump import dumps
import inspect
import requests
import string
import random
from langchain_core.runnables.base import (
    RunnableLike,
    coerce_to_runnable,
)
from langgraph.graph.graph import END, START, CompiledGraph, Graph
from typing import Any, Callable, Dict, NamedTuple, Optional, Sequence
import os
import hashlib


def generate_md5(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    return md5_hash.hexdigest()


START = START
END = END


class StateGraphWork(StateGraphOrg):

    def __init__(self, options):
        super().__init__(options)
        self.logList = []
        self.nodeList = []
        self.edgeList = []
        self.start = ''
        self.end = ''
        # self.serverUrl = options.get('server_url', None)
        self.serverUrl = python_path = os.environ.get('LANGGRAPH_TRACER_SERVER')
        self.apiKey = python_path = os.environ.get('LANGGRAPH_TRACER_API_KEY')
        self.last = START

    # 增加节点
    def add_node(self, key: str, action: RunnableLike) -> None:
        # nodelist中添加node节点的输入输出
        self.nodeList.append({
            'type': 'node',
            'data': {
                'key': key,
                'code': inspect.getsource(action) if callable(action) else '',
                'desc': ''
            }
        })

        def on_end(run):
            self.logList.append({
                'type': 'node',
                'last': self.last,
                'key': key,
                'input': run.inputs,
                'output': run.outputs,
            })
            self.last = key

        super().add_node(key, coerce_to_runnable(action).with_listeners(
            on_end=on_end
        ))

    # 增加边
    def add_edge(self, start_key: str, end_key: str) -> None:
        super().add_edge(start_key, end_key)
        self.edgeList.append({
            'type': 'edge',
            'source': start_key,
            'target': end_key
        })

    def add_conditional_edges(
            self,
            start_key: str,
            condition: Callable[..., str],
            conditional_edge_mapping: Optional[Dict[str, str]] = None,
    ) -> None:
        key = 'condEdge_' + str(len(self.nodeList))
        self.edgeList.append({
            'type': 'edge',
            'source': start_key,
            'target': key
        })
        if conditional_edge_mapping is not None:
            for handle, target in conditional_edge_mapping.items():
                self.edgeList.append({
                    'type': 'condEdge',
                    'source': key,
                    'sourceHandle': handle,
                    'target': target
                })
                if target == END:
                    self.end = key

        self.nodeList.append({
            'type': 'condEdge',
            'data': {
                'key': key,
                'code': inspect.getsource(condition),
                'desc': '',
                'mapping': list(conditional_edge_mapping.keys()) if conditional_edge_mapping is not None else []
            }
        })

        def wrapper_condition(state):
            next_state = condition(state)
            self.logList.append({
                'type': 'condEdge',
                'last': start_key,
                'key': key,
                'input': state,
                'next': next_state,
            })
            self.last = key
            if next_state == 'end':
                graph = dumps({
                    'nodes': self.nodeList,
                    'edges': self.edgeList,
                    'start': self.start,
                    'end': self.end,
                })
                data = {
                    'key': self.apiKey,
                    'graph': graph,
                    'md5': generate_md5(graph),
                    'log': dumps(self.logList)
                }
                # Save log to file
                if self.serverUrl:
                    response = requests.post(self.serverUrl + "/api/log", data=data)
                    result = response.json()
                    if response.status_code == 200:
                        id = result.get('data')
                        print('result:',
                              f'{os.environ["LANGGRAPH_TRACER_SERVER"]}/log/{id}')
                    else:
                        print('error:', response.status_code, result.message)
                else:
                    print(dumps(data, sort_keys=True, indent=4, separators=(', ', ': ')))
            return next_state

        super().add_conditional_edges(start_key, wrapper_condition, conditional_edge_mapping)

    def set_entry_point(self, key: str):
        self.start = key
        super().set_entry_point(key)

    def compile(self):
        return super().compile()

    def returnres(self):
        output = {
            'nodes': self.nodeList,
            'edges': self.edgeList,
            'logs': self.logList,
        }
        return output
