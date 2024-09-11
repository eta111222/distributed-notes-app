import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_URL = 'amqp://rabbitmq:5672'
print(f"Connecting to RabbitMQ at {RABBITMQ_URL}")

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASS')


