import json

class Code:
    def __init__(self, system, code, display):
        self.system = system
        self.code = code
        self.display = display

    def to_json(self):
        return json.dumps({
            'system': self.system,
            'code': self.code,
            'display': self.display
        }, indent=4)

