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