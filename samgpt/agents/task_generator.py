from typing import List, Dict
import os
import json

import samgpt.utils.io_utils as ioutils
# track the tasks and the plan based on the users goal
def task_tracking(goal: str, plan: str) -> None:
    # Filter for all pending tasks
    jsonPlan = json.loads(plan)
    firstTask: Dict = jsonPlan[0]
    save_current_task(goal, firstTask)

# create a function to split the plan into a list
def split_plan_into_tasks(plan) -> List[str]:
    # split the plan into a list of tasks
    # return the list of tasks
    return plan.split("\n")

# safe current task into file
def save_current_task(goal: str, jsonTask: Dict) -> None:
    path = ioutils.get_working_dir(goal)
    taskID = jsonTask['id']
    task = json.dumps(jsonTask)
    with open(os.path.join(path, '')+f"task_{taskID}.json", "w") as f:
        f.write(task)

def filter_plan_for_tasks(jsonPlan, filter: str) -> List:
    return [task for task in jsonPlan if task["status"] == filter]
