import contextlib
import requests


import json
from typing import Any, Callable, Dict, List


def get_headers(token: str) -> Dict[str, str]:
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }


def get_body(messages: List[Dict[str, str]], config: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'messages': messages,
        **config
    }

def send_request(url: str, headers: Dict[str, str], body: Dict[str, Any]) -> requests.Response:
    for _ in range(5, 0, -1):
        with contextlib.suppress(requests.exceptions.RequestException):
            response = requests.post(url, headers=headers, data=json.dumps(body))
            if response.status_code == 200:
                return response
    return requests.Response()


def get_content(data: Dict[str, Any]) -> str:
    return data['choices'][0]['delta'].get('content', '')


def is_stream_ended(data: Dict[str, Any]) -> bool:
    return data['choices'][0]['finish_reason'] is not None


def get_chat_completion(model: List[Any], messages: List[Dict[str, str]], config: Dict[str, Any], callback: Callable[[str], None]) -> str:
    headers = get_headers(model[1])
    body = get_body(messages, config)


    response = send_request(model[0], headers, body)
    #response.raise_for_status()

    text = ""
    for line in response.iter_lines(chunk_size=1, decode_unicode=True):
        if line.startswith('data: '):
            data = json.loads(line[6:])
            content = get_content(data)
            text += content
            callback(content)
            if is_stream_ended(data):
                break

    return text