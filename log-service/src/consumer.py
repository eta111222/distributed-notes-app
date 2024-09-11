import pika
import json
import os
from pymongo import MongoClient
from config import Config
import logging

if Config.LOG_FILE_PATH:
    os.makedirs(os.path.dirname(Config.LOG_FILE_PATH), exist_ok=True)

logging.basicConfig(filename=Config.LOG_FILE_PATH, level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

client = MongoClient(Config.MONGO_URI)
db = client.get_database('logs')  

connection = pika.BlockingConnection(pika.URLParameters(Config.RABBITMQ_URI))
channel = connection.channel()

channel.exchange_declare(exchange='note_events', exchange_type='fanout')

channel.queue_declare(queue='logs')
channel.queue_bind(exchange='note_events', queue='logs') 

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"Received log: {data}")
    
    db.logs.insert_one(data)
    
    logging.info(f"Log received: {data}")

def start_consumer():
    print(' [*] Waiting for logs. To exit press CTRL+C')
    channel.basic_consume(queue='logs', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
    
