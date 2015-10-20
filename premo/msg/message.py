from datetime import datetime
import uuid

from pilo import FieldError, Form
from pilo.fields import Datetime, String

from premo import mimes


class Message(Form):

    broker = None

    encoding = 'utf-8'

    mime = mimes.Json

    id = String(default=lambda: uuid.uuid4().hex)
    timestamp = Datetime(format='iso8601', default=lambda: datetime.utcnow())
    content_encoding = String(default=encoding)
    content_type = String(default=mime.content_type)
    body = String()

    def send(self, topic):
        self.broker.send(topic, self)
