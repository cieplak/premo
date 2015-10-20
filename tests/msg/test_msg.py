import uuid

from premo import mimes, msg, settings
from tests import TestCase


class TestRabbitMQ(TestCase):

    def setUp(self):
        super(TestRabbitMQ, self).setUp()
        msg.init(settings)
        self.queue = msg.brokers.rabbitmq.Engine.Queue(
            'messages', 'exchange', 'messages'
        )
        msg.brokers.rabbitmq.Engine.Consumer.registry = []
        self.consumer = msg.brokers.rabbitmq.Engine.Consumer()
        self.log = []
        self.messages = [dict(guid=uuid.uuid4().hex) for _ in xrange(10)]

    def publish_msg(self, payload):
        message = msg.Message(body=mimes.Json.encode(payload))
        message.send('messages')

    def test_pubsub(self):
        @msg.Message.broker.receive(self.queue.name)
        def process_event(payload):
            self.log.append(payload)

        map(self.publish_msg, self.messages)
        list(self.consumer.consume(limit=len(self.messages)))

        # Validate message schemas
        messages = map(msg.Message, self.log)
