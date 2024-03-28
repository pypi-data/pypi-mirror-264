import json
import threading

import requests

from maitai._eval_request import EvalRequestEncoder
from maitai.config import global_config
from maitai import MaiTaiObject, EvalRequest


class Evaluator(MaiTaiObject):

    def __init__(self):
        super().__init__()

    @classmethod
    def evaluate(cls, session_id, content):
        eval_request: EvalRequest = cls.create_eval_request(session_id, content)
        cls.send_to_maitai(eval_request)

    @classmethod
    def create_eval_request(cls, session_id, content):
        eval_request: EvalRequest = EvalRequest()
        eval_request.application_id = global_config.application_id
        eval_request.session_id = session_id
        eval_request.evaluation_content = content
        eval_request.evaluation_content_type = 'text'
        return eval_request

    @classmethod
    def send_to_maitai(cls, eval_request):
        def send_request():
            host = 'https://maitai.ai.yewpay.com'
            url = f'{host}/evaluation/request'
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': global_config.api_key
            }
            response = requests.post(url, headers=headers, data=json.dumps(eval_request, cls=EvalRequestEncoder))
            if response.status_code != 200:
                error_text = response.text
                print(f"Failed to send evaluation request. Status code: {response.status_code}. Error: {error_text}")

        # Start a new thread to send the request without waiting for the response
        threading.Thread(target=send_request).start()