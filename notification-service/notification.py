import asyncio
import websockets
import pika
import json
import os

RABBITMQ_URL = 'amqp://rabbitmq:5672'

clients = set()

async def notify_clients(message):
    if clients:  
        await asyncio.wait([asyncio.create_task(client.send(message)) for client in clients])

async def websocket_handler(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            pass
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Client disconnected: {e}")
    finally:
        clients.remove(websocket)

def on_message(ch, method, properties, body):
    message = body.decode()
    print(f"Received message from RabbitMQ: {message}")
    asyncio.run(notify_clients(message))

def start_rabbitmq_listener():
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()

    channel.exchange_declare(exchange='note_events', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='note_events', queue=queue_name)

    channel.basic_consume(queue=queue_name, on_message_callback=on_message, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

async def start_services():
    websocket_server = websockets.serve(websocket_handler, "0.0.0.0", 6789)
    rabbitmq_listener = asyncio.to_thread(start_rabbitmq_listener)
    
    await asyncio.gather(websocket_server, rabbitmq_listener)

if __name__ == "__main__":
    asyncio.run(start_services())