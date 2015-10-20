from datetime import datetime
import json
import uuid

import premo
from . import TestCase


class TestMimes(TestCase):

    def test_init(self):
        guid = uuid.uuid4()
        timestamp = datetime.utcnow()
        record = {'id': guid, 'value': 123, 'timestamp': timestamp}
        encoded_record = premo.mimes.Json.encode(record)


