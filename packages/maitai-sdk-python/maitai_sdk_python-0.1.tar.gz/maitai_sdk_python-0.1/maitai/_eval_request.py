from json import JSONEncoder

from maitai._loadable import Loadable


class EvalRequest(Loadable):

    def __init__(self):
        super().__init__()
        self.id = -1
        self.date_created = -1
        self.application_id = -1
        self.session_id = -1
        self.evaluation_content_type = ''
        self.evaluation_content = ''


class EvalRequestEncoder(JSONEncoder):
    def default(self, o):
        try:
            return o.__dict__
        except Exception as e:
            return o