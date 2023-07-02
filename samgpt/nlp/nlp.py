"""This module contains the functions used to interact with the NLP model"""

from typing import List, Optional
from enum import Enum
import configuration.options as options
import dotenv
from utils.http import get_chat_completion

OPENAI_API_KEY : Optional[str] = dotenv.get_key('.env', 'OPENAI_API_KEY')

class Model(Enum):
    OPENAI = ['https://api.openai.com/v1/chat/completions', OPENAI_API_KEY]
    FREE = ['https://free.churchless.tech/v1/chat/completions', '']

# Get the model from the Model enum
model: List[str] = Model.FREE.value


# Start the inference
def start_simple_inference(role, prompt, callback) -> str:
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