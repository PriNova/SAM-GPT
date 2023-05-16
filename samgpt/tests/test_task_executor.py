from samgpt.agents.task_executor import execute_task
from samgpt.ui.command_line import ai_message

def test_executor():
    response = """Command: webSearch

Thoughts: The best command for this task would be $webSearch as it allows me to search the web for potential locations for the pet shop. I can look for areas with high foot traffic, proximity to other pet-related businesses, and areas with a high concentration of pet owners.

Critics: While $decomposeTask could be useful in breaking down the task into smaller subtasks, it may not be necessary for this particular task as it is relatively straightforward.

Decomposition:
1. Determine the criteria for a suitable location (e.g., foot traffic, proximity to other pet-related businesses, etc.)
2. Conduct a web search for potential locations based on the criteria.
3. Evaluate the potential locations based on the criteria and narrow down the options.
4. Visit the top locations in person to assess their suitability.
5. Choose the best location and begin the process of opening the pet shop."""
    assert execute_task(response, userGoal="A goal", currentTaskDescription="Find the best location for a pet shop", callback=ai_message) == "webSearch"
    #assert False, "This test should fail"