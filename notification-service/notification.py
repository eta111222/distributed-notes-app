import pika
import smtplib

from email.mime.text import MIMEText

from config import RABBITMQ_URL, SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS

def send_email_notification(subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = 'recipient@example.com'

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, 'recipient@example.com', msg.as_string())
        server.quit()
        print('Email sent!')
    except Exception as e:
        print(f'Error sending email: {e}')

def on_message(ch, method, properties, body):
    message = body.decode('utf-8')
    print(f"Received message: {message}")
    send_email_notification("New Note Event", message)

def start_consuming():
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()

    channel.exchange_declare(exchange='note_events', exchange_type='fanout')

    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='note_events', queue=queue_name)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_consume(queue=queue_name, on_message_callback=on_message, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    start_consuming()