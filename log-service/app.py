import sys
sys.path.append('src')
import os
from threading import Thread
from src.consumer import start_consumer

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src import create_app

def run_rabbitmq_consumer():
    start_consumer()

if __name__ == '__main__':
    consumer_thread = Thread(target=run_rabbitmq_consumer)
    consumer_thread.start()

    print("Starting Flask application on port 5001...")
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)

    consumer_thread.join()