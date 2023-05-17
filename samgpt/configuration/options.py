# Dictionary of options to display
taskOptions = {
    1: "Approve Task",
    2: "Modify Task",
    3: "Skip Task"
}

decompOrExecute = {
    1: "Execute Task",
    2: "Decompose Task",
    3: "Retry"
}

defaultChatConfig: Dict[str, Any] = { # type: ignore
    "model": 'gpt-3.5-turbo',
    "max_tokens": 1000,
    "temperature": 1,
    "presence_penalty": 0.0,
    "top_p": 1,
    "frequency_penalty": 0,
    "stream": True
}