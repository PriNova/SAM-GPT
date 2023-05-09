from typing import List, Dict, Any

import samgpt.utils.io_utils as ioutils
import json


# track the tasks and the plan based on the users goal
def get_task(plan: List, index: int) -> Dict:
    #jsonPlan: Dict = json.loads(plan)
    if index < len(plan):
        return plan[index]
    return plan[0]

# create a function to split the plan into a list
def split_plan_into_tasks(plan) -> List[str]:
    # split the plan into a list of tasks
    # return the list of tasks
    return plan.split("\n")


def filter_plan_for_tasks(jsonPlan, filter: str) -> List:
    return [task for task in jsonPlan if task["status"] == filter]

def max_tasks(plan: List)-> int:
    return len(plan)

# Update the plan by replacing the task with the updated task
def update_task_by_id(plan: List, task_id: str, updated_info: Dict):
    # Convert the task and optional sub-task indices to integers
    task_index = int(task_id.split(".")[0]) - 1

    # Check if the task ID has a sub-task index
    if "." in task_id:
        subtask_index = int(task_id.split(".")[1]) - 1
    else:
        subtask_index = None

    if subtask_index is not None:
        # Update a sub-task
        for key, value in updated_info.items():
            plan[task_index]["subtasks"][subtask_index][key] = value
    else:
        # Update a task
        for key, value in updated_info.items():
            plan[task_index][key] = value

    # Return the updated plan
    return plan