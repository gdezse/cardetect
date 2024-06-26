'''Listen to messages coming from the detection server'''

from os import getenv

import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

exchange_name = getenv('EXCHANGE_NAME')
channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange=exchange_name, queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(_ch, _method, _properties, body):
    '''Print queue messages'''
    print(f" [x] {body.decode()}")

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
