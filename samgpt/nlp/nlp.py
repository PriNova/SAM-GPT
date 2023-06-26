"""This module contains the functions used to interact with the NLP model"""

from typing import Any, Dict, List, Optional

import configuration.options as options
import dotenv
from utils.http import get_chat_completion

OPENAI_API_KEY : Optional[str] = dotenv.get_key('.env', 'OPENAI_API_KEY')

openaiModel: List[Any] = ['https://api.openai.com/v1/chat/completions', OPENAI_API_KEY]
freeModel: List[Any] = ['https://free.churchless.tech/v1/chat/completions', '']

# define the Model enum
Model: Dict[str, List[Any]] = {
    'openai': openaiModel,
    'free': freeModel
    }

# Get the model from the Model enu
model: List[Any] = Model['free']

# Get the chat completion from the model
from typing import Any, Dict, List


# Start the inference
def start__simple_inference(role, prompt, callback) -> str:
    return get_chat_completion(
        model=model,
        messages=[{'role': role, 'content': prompt}],
        config=options.defaultChatConfig,
        callback=callback,
    )

def start_multi_prompt_inference(message, callback) -> str:
    return get_chat_completion(
        model=model,
        messages=message,
        config=options.defaultChatConfig,
        callback=callback,
    )