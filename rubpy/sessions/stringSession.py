import json
import base64


class StringSession(object):
    def __init__(self, session: str = None) -> None:
        self.session = self.load(session)

    @classmethod
    def load(cls, session):
        if isinstance(session, str):
            return json.loads(base64.b64decode(session))

    @classmethod
    def dump(cls, session):
        if isinstance(session, list):
            session = json.dumps(session).encode('utf-8')
            return base64.b64encode(session).decode('utf-8')

    @classmethod
    def from_sqlite(cls, session):
        session = cls.dump(session.information())
        return StringSession(session)

    def insert(self, phone_number, auth, guid, user_agent, *args, **kwargs):
        self.session = [phone_number, auth, guid, user_agent]

    def information(self):
        return self.session

    def save(self, file_name=None):
        result = self.dump(self.session)
        if result is None:
            if isinstance(file_name, str):
                if not file_name.endswith('.txt'):
                    file_name += '.txt'
                with open(file_name, 'w+') as file:
                    file.write(result)
        return result
