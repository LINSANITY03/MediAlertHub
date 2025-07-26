"""
RabbitMQ worker that listens for tasks and runs the summarize_patient_data function.
"""

import logging
import json
import os
import pika
import time

from common.logger import set_request_id, setup_logging
from rag import summarize_patient_data

setup_logging()
logger = logging.getLogger(__name__)

RABBITMQ_DEFAULT_USER = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_DEFAULT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS")

# Create credentials object
credentials = pika.PlainCredentials(RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS)

# Retry logic to wait for RabbitMQ to be ready
for attempt in range(10):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host="rabbitmq",
                port=5672,
                credentials=credentials
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue="rag_tasks", durable=True)
        print("[*] Connected to RabbitMQ and queue declared.")
        break
    except pika.exceptions.AMQPConnectionError:
        print(f"[!] RabbitMQ not ready. Retrying in 3 seconds... (Attempt {attempt + 1}/10)")
        time.sleep(3)
else:
    raise Exception("Failed to connect to RabbitMQ after 10 attempts.")


def callback(ch, method, properties, body):
    """
    RabbitMQ message callback function.

    Processes a message from the 'rag_tasks' queue by:
    - Parsing the message body as JSON to extract patient form data.
    - Calling the summarize_patient_data function with the extracted data.
    - Printing the resulting clinical summary.
    - Acknowledging the message to RabbitMQ to mark it as processed.

    Args:
        ch: pika.Channel - The channel object.
        method: pika.spec.Basic.Deliver - Delivery method.
        properties: pika.spec.BasicProperties - Message properties.
        body: bytes - The message body received from the queue, expected to be a JSON string.
    """
    print(f" [x] Received {body}")

    try:
        # Assume body is JSON string representing form_data dict
        form_data = json.loads(body)
    except json.JSONDecodeError:
        print(" [!] Received invalid JSON, ignoring message")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return
    summary = summarize_patient_data(form_data=form_data)
    logger.info(summary)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="rag_tasks", on_message_callback=callback)

print("[*] RAG Worker listening for tasks...")
channel.start_consuming()
