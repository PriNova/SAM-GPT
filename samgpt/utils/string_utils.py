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
            "subtasks": []
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
            "id": f"{parentIndex}.{i + 1}",
            "description": task,
            "status": "Pending",
            "parent": parentIndex
        }
        for i, task in enumerate(subtasks)
    ]
    return subtasks