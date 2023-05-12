from typing import Dict
import samgpt.agents.websearch_agent as webSearchAgent
import samgpt.ui.command_line as cmd

def execute_task(response: str, userGoal: str, currentTaskDescription: str) -> None:
    command = ""
    match response.split():
        case ["Command:", *object]:
            if object[0][0] == '$':
                command =  object[0][1:]
            else:
                command = object[0]
        case _:
            command = "No match"
    cmd.system_message(f"Command: {command}")

    query = ""
    match command:
        case "webSearch":
            query = webSearchAgent.execute(userGoal, currentTaskDescription)
        case _:
            query = "No query found!"
    print(query)