from .message import Message


def init(config):
    Message.broker = brokers.rabbitmq


class Broker(object):

    def send(self, message):
        raise NotImplementedError()

    def receive(self, topic):
        raise NotImplementedError()

    def process(self, *args, **kwargs):
        raise NotImplementedError()

    class Engine(object):
        pass


from . import brokers
