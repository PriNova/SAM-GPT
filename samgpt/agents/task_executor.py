from typing import Dict

def execute_task(response: str) -> str:
    match response.split():
        case ["Command:", *object]:
            if object[0][0] == '$':
                return object[0][1:]
            return object[0]
        case _:
            return "No match"


