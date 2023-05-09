from typing import List, Dict
import json

import samgpt.utils.io_utils as ioutils

# track the tasks and the plan based on the users goal
def task_tracking(goal: str, plan: str) -> Dict:
    jsonPlan = json.loads(plan)
    return jsonPlan[0]
    save_current_task(goal, firstTask)

# create a function to split the plan into a list
def split_plan_into_tasks(plan) -> List[str]:
    # split the plan into a list of tasks
    # return the list of tasks
    return plan.split("\n")


def filter_plan_for_tasks(jsonPlan, filter: str) -> List:
    return [task for task in jsonPlan if task["status"] == filter]
