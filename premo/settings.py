

POSTGRES = dict(
    URI='postgresql://postgres:@localhost/premo',
)


AMQP = dict(
    EXCHANGE='exchange',
    IP_ADDRESS='0.0.0.0',
    PORT=5672,
    USER='guest',
    PASSWORD='guest',
    QUEUES=[
        # (queue, exchange, routing_key)
        ('messages', 'exchange', 'messages'),
    ],
)


AMQP['URI'] = 'amqp://{user}:{password}@{host}:{port}/'.format(
    user=AMQP['USER'],
    password=AMQP['PASSWORD'],
    host=AMQP['IP_ADDRESS'],
    port=AMQP['PORT'],
)
