import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    MONGO_URI = os.getenv('MONGO_URI') 
    
    RABBITMQ_URI = 'amqp://rabbitmq:5672' 
    
    LOG_FILE_PATH = os.getenv('LOG_FILE_PATH') 
