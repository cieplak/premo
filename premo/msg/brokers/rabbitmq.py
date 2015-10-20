from collections import namedtuple
import functools
import json
import logging

import kombu
import kombu.mixins
import pika
import pika.credentials

from premo import settings


logger = logging.getLogger(__name__)


def send(topic, message, exchange=settings.AMQP['EXCHANGE']):
    payload = message.mime.encode(message).encode(message.content_encoding)
    with kombu.Connection(settings.AMQP['URI']) as cxn:
        producer = kombu.Producer(
            cxn,
            exchange=kombu.Exchange(exchange),
            routing_key=topic,
            auto_declare=False,
        )
        producer.publish(
            payload,
            content_type=message.content_type,
            content_encoding=message.content_encoding,
            retry=True
        )


def receive(queue):
    def outer(callback):
        Engine.Consumer.register(queue, callback)
        return callback
    return outer


def process(limit=None):
    consumer = Engine.Consumer()
    if limit:
        return list(consumer.consume(limit=limit))
    return consumer.run()


class Engine(object):

    Queue = namedtuple('Queue', [
        'name',
        'exchange',
        'routing_key',
    ])

    cxn_params = pika.ConnectionParameters(
        host=settings.AMQP['IP_ADDRESS'],
        port=settings.AMQP['PORT'],
        credentials=pika.credentials.PlainCredentials(
            settings.AMQP['USER'],
            settings.AMQP['PASSWORD'],
        ),
    )

    @classmethod
    def create_exchanges(cls):
        cxn = pika.BlockingConnection(cls.cxn_params)
        channel = cxn.channel()
        channel.exchange_declare(
            exchange=settings.AMQP['EXCHANGE'], type='topic', durable=True
        )
        cxn.close()

    queues = [Queue(*q) for q in settings.AMQP['QUEUES']]

    @classmethod
    def create_queue(cls, queue):
        cxn = pika.BlockingConnection(cls.cxn_params)
        channel = cxn.channel()
        queue_name, exchange, routing_key = tuple(queue)
        channel.queue_declare(
            queue=queue_name,
            durable=True,
        )
        channel.queue_bind(
            exchange=exchange,
            queue=queue_name,
            routing_key=routing_key,
        )

    @classmethod
    def delete_queue(cls, queue_name):
        cxn = pika.BlockingConnection(cls.cxn_params)
        channel = cxn.channel()
        channel.queue_delete(queue=queue_name)

    class Consumer(kombu.mixins.ConsumerMixin):

        registry = []

        @classmethod
        def register(cls, queue, callback):
            subscriber = {
                'queue': queue,
                'callback': callback,
            }
            cls.registry.append(subscriber)

        def __init__(self, qos=None):
            self.qos = qos or {'prefetch_count': 20}
            self.connection = kombu.Connection(settings.AMQP['URI'])

        def on_message(self, subscriber, body, message):
            try:
                return self._callback(subscriber, body)
            except Exception:
                self._retry(subscriber, body)
            finally:
                message.ack()

        def _callback(self, subscriber, body):
            subscriber['callback'](body)

        def _retry(self, subscriber, body):
            send(subscriber['queue'], body)

        def get_consumers(self, Consumer, channel):
            consumers = []
            for subscriber in self.registry:
                queue = kombu.Queue(subscriber['queue'])
                on_message = functools.partial(
                    self.on_message,
                    subscriber,
                )
                consumer = Consumer(
                    queues=[queue],
                    callbacks=[on_message],
                    auto_declare=False,
                )
                consumer.qos(**self.qos)
                consumers.append(consumer)
            return consumers
