from typing import List, Dict
from samgpt.planning.task_manager import traverse

def test_traverse():
    task_list = [
        {
            'status': 'Complete',
            'tasks': []
        },
        {
            'status': 'Completed',
            'tasks': [
                {
                    'status': 'Complete',
                    'tasks': []
                },
                {
                    'status': 'Complete',
                    'tasks': []
                }
            ]
        },
        {
            'status': 'Incomplete',
            'tasks': []
        }
    ]
    #assert traverse(task_list, 'status',  'Completed') == task_list[0]
    #assert traverse(task_list, 'status',  'Completed') == task_list[1]['tasks'][0]
    assert traverse(task_list, 'status',  'Incomplete') == task_list[0]