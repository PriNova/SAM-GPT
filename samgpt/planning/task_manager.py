from typing import List, Dict
import json

import samgpt.utils.io_utils as ioutils


# track the tasks and the plan based on the users goal
def get_task(plan: str, index: int) -> Dict:
    jsonPlan: Dict = json.loads(plan)
    if index < len(jsonPlan):
        return jsonPlan[index]
    return jsonPlan[0]

# create a function to split the plan into a list
def split_plan_into_tasks(plan) -> List[str]:
    # split the plan into a list of tasks
    # return the list of tasks
    return plan.split("\n")


def filter_plan_for_tasks(jsonPlan, filter: str) -> List:
    return [task for task in jsonPlan if task["status"] == filter]

def max_tasks(plan: Dict)-> int:
    return len(plan)

# Update the plan by replacing the task with the updated task
def update_task_by_id(plan, task_id: str, updated_info: Dict):
    # Find the task and optional sub-task indices from the task ID
    task_index, subtask_index = (int(x) - 1 for x in task_id.split("."))

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
