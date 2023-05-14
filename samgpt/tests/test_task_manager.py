from typing import List, Dict
from samgpt.planning.task_manager import first_by_key_value
from samgpt.planning.task_manager import extract_plan_tasks

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
    assert first_by_key_value(task_list, 'status',  'Incomplete') == task_list[2]

def test_extract_plan_tasks():
    plan = [{
        "id" : "1.",
        "description" : "Get a new car",
        "tasks" : []},
        {
        "id" : "2.",
        "description" : "Get a new house",
        "tasks" : [
            {
                "id" : "2.1.",
                "description" : "Research the location",
                "tasks" : []},
            {
                "id" : "2.2.",
                "description" : "Ask rental price",
                "tasks" : [
                    {
                        "id" : "2.2.1.",
                        "description" : "Research real estate manager",
                        "tasks" : []
                    },
                    {
                        "id" : "2.2.2.",
                        "description" : "Ask bank loan",
                        "tasks" : []
                    }
                ]
            }
        ]
        },
        {
            "id" : "3.",
            "description" : "Get a new house",
            "tasks" : []
        },
        {
            "id" : "4.",
            "description" : "Get a house",
            "tasks" : []
        }
    ]
    assert extract_plan_tasks(plan) == """1. Get a new car
2. Get a new house
2.1. Research the location
2.2. Ask rental price
2.2.1. Research real estate manager
2.2.2. Ask bank loan
3. Get a new house
4. Get a house"""