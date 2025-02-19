import pika
import json
import django
import os
from models import Book

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frontend_api.settings")
django.setup()

def process_message(ch, method, properties, body):
    data = json.loads(body)
    if data.get("event") == "book_added":
        book_data = data.get("data")
        Book.objects.create(
            id=book_data["id"], 
            title=book_data["title"],
            publisher=book_data["publisher"], 
            category=book_data["category"],
            expected_return_date=book_data["expected_return_date"]
        )

connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
channel = connection.channel()
channel.queue_declare(queue="book_updates")
channel.basic_consume(queue="book_updates", on_message_callback=process_message, auto_ack=True)

print("Listening for messages...")
channel.start_consuming()
