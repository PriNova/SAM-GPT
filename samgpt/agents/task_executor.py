from typing import Dict
import agents.websearch_agent as webSearchAgent
import ui.command_line as cmd

def execute_task(response: str, userGoal: str, currentTaskDescription: str, callback) -> str:
    command = ""
    match response.split():
        case ["Command:", *object]:
            command = object[0][1:] if object[0][0] == '$' else object[0]
        case _:
            command = "No match"
    cmd.system_message(f"Command: {command}")

    result = ""
    match command:
        case "webSearch":
            result =webSearchAgent.execute(userGoal, currentTaskDescription, callback)
        case _:
            result = "No match"
    return result
        