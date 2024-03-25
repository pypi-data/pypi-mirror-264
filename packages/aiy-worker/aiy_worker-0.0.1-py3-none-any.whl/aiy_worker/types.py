
from typing import List

class PayloadErrorLocation:
    line: int
    column: int
    def __init__(self, location: dict):
        self.line = location['line']
        self.column = location['column']

class PayloadError:
    message: str
    locations: List[PayloadErrorLocation]
    path: List[str]

    def __init__(self, error: dict):
        self.message = error['message']
        self.locations = [PayloadErrorLocation(i) for i in error['locations']]
        self.path = error['path']

class Text2ImageProps:
    def __init__(self, props: dict) -> None:
        self.prompt = props.get('prompt')
        self.negative_prompt = props.get('negativePrompt')
        self.seed = props.get('seed')

class Task:
    def __init__(self, data: dict):
        subscribe_task: dict = data.get('subscribeTasks')
        if subscribe_task:
            self.id = subscribe_task.get('id')
            self.text2Image = Text2ImageProps(subscribe_task.get('text2Image'))

class Payload:
    def __init__(self, payload: dict) -> None:
        self.errors = [PayloadError(i) for i in payload.get('errors', [])]
        self.task = Task(payload.get('data', {}))


class WsData:
    type: str
    id: str
    def __init__(self, data: dict) -> None:
        self.type = data.get('type')
        self.id = data.get('id')
        self.payload = Payload(data.get('payload'))
