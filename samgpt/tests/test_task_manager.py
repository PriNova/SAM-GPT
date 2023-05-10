from samgpt.planning.task_manager import traverse

def test_traverse():
    task_list = [
        {
            'status': 'Completed',
            'tasks': []
        },
        {
            'status': 'Incomplete',
            'tasks': [
                {
                    'status': 'Completed',
                    'tasks': []
                },
                {
                    'status': 'Incomplete',
                    'tasks': [
                        {
                            'status': 'Completed',
                            'tasks': []
                        }
                    ]
                }
            ]
        }
    ]
    assert traverse(task_list, 'status',  'Completed') == task_list[0]
    assert traverse(task_list, 'status',  'Completed') == task_list[1]['tasks'][0]
    assert traverse(task_list, 'status',  'Completed') == task_list[1]['tasks'][1]['tasks'][0]
