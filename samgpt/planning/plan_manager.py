import re
import json

# extract the plan from text
def extract_with_regex(text, prefix: str) -> str:
    if match := re.search(fr'{prefix}\n+((?:\d+.+\n?)+)', text):
        plan = re.sub(r'\n?\d+\..', '\n', match[1]).strip()
        return plan.strip()

    if match := re.search(fr'{prefix}\n+((?:•\s*.+\n?)+)', text):
        plan = re.sub(r'(•\s*)', '', match[1]).strip()
        return plan.strip()

    if match := re.search(fr'{prefix}\n+((?:-\s*.+\n?)+)', text):
        plan = re.sub(r'(-\s*)', '', match[1]).strip()
        return plan.strip()

    if match := re.search(fr'{prefix}\n+([\s\S]*?)', text):
        plan = match[1].strip()
        return plan.strip()

    # No matching pattern found
    return 'Not successfully extracted!'

# Format extracted plan as a JSON Object.
def set_status_for_task(plan_json: str, task_id: int, status: str) -> str:
    plan = json.loads(plan_json)
    for task in plan:
        if task["id"] == task_id:
            task["status"] = status
    return json.dumps(plan, indent=4)