import pika
import json
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin_api.settings")
django.setup()

from books.models import Book

def process_message(ch, method, properties, body):
    data = json.loads(body)
    if data.get("event") == "book_borrowed":
        book_id = data.get("data").get("book_id")
        book = Book.objects.get(id=book_id)
        book.is_borrowed = True
        book.save()

connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
channel = connection.channel()
channel.queue_declare(queue="borrow_updates")
channel.basic_consume(queue="borrow_updates", on_message_callback=process_message, auto_ack=True)

print("Listening for borrow messages...")
channel.start_consuming()
