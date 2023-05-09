from typing import List


def format_plan_as_json(extractedPlan: str) -> List:
    # Split the output into tasks using newline character
    tasks = extractedPlan.strip().split("\n")

    # Create a list of dictionaries for each task
    plan = [
        {
            "id": f"{i + 1}",
            "description": task,
            "status": "Pending",
            "tasks": []
        }
        for i, task in enumerate(tasks)
    ]
    return plan

def format_subtask_as_json(extractedSubtask: str, parentIndex: str) -> List:
    # Split the output into tasks using newline character
    subtasks = extractedSubtask.strip().split("\n")

    # Create a list of dictionaries for each task
    subtasks = [
        {
            "id": generate_task_id(parentIndex, i),
            "description": task,
            "status": "Pending",
            "tasks": []
        }
        for i, task in enumerate(subtasks)
    ]
    return subtasks

def generate_task_id(prefix, task_index):
    return f"{prefix}.{task_index + 1}"