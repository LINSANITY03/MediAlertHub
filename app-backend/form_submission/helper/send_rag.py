"""
Module to publish form data messages to a RabbitMQ queue using pika.

Loads environment variables, sets up logging, and defines a RabbitMQProducer class
to handle connection, message publishing, and connection closure.
"""
import json
import logging
import os
import pika
import pika.exceptions
import time

from fastapi import HTTPException
from common.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

form_data = {
    "age_group": "30-40",
    "province": "Bagmati",
    "district": "Kathmandu",
    "disease_status": "The patient is showing a set of symptoms that may be consistent with a viral infection, "
                        "possibly Dengue or Chikungunya, but Malaria can’t be ruled out either at this point. "
                        "Given the persistence of high fever, joint stiffness, and rashes that have appeared intermittently, further lab confirmation is required."
                        "Initial blood tests showed low platelet count and mild dehydration. However, the patient also recently returned from an area where there was an uptick in enteric fever cases. So, there's also a slight possibility it could be typhoid fever. The overlap of symptoms makes a definitive diagnosis tricky without further diagnostic support like NS1 antigen or PCR. Until then, symptomatic management and isolation precautions have been advised. The provisional diagnosis is Dengue with possible co-infection, but it’s being treated conservatively.",
    "current_condition": "Patient presented with sustained fever for 5 days, around 102–103°F, accompanied by chills, headache, pain behind the eyes, and fatigue. "
                    "On physical examination, there is notable tenderness in joints and muscle soreness, particularly in the lower limbs. "
                     "Patient also reported intermittent episodes of nausea, some vomiting, and occasional abdominal discomfort. "
                     "No known underlying chronic illness, but the patient appeared visibly weak and dehydrated. "
                     "The rashes appeared on Day 3 and have not spread further. Slight swelling of lymph nodes in the neck. "
                     "Pulse and blood pressure within normal range but trending downward. Advised bed rest, fluid intake, and paracetamol. "
                     "CBC indicated reduced platelets and elevated hematocrit. Skin turgor is mildly reduced. "
                     "Patient remains conscious, alert, but complains of severe tiredness. Rehydration via ORS and monitoring vitals every 4 hours.",
    "disease_symptoms": "Initial symptoms included fever, chills, and intense headache, followed by a dull pain in the joints and behind the eyes. "
                    "On Day 2, patient began experiencing fatigue and minor vomiting. As the fever persisted, red patches resembling rashes started developing, first on the chest and then near the elbows. "
                    "The rash was not itchy but slightly raised and warm to touch. Joint stiffness and tenderness increased over time, especially during mornings. "
                    "The patient also experienced a metallic taste and occasional dizziness when standing. By Day 4, there were signs of dehydration — dry mouth and low urine output. "
                    "Other noted symptoms: sensitivity to light, mild cough, no sore throat. Appetite has decreased significantly. "
                    "The patient hasn’t had diarrhea but complains of a “weird sensation” in the stomach, possibly bloating. "
                    "Occasional shivering noted during nighttime. Swelling of hands and feet reported on Day 5. "
                    "Patient reports improvement in fever with paracetamol, but symptoms quickly return after 6–7 hours. "
                    "leeping patterns have been disturbed, and anxiety due to illness has made the patient irritable. No signs of severe respiratory distress yet.",
  }

class RabbitMQProducer:
    """
    Singleton class for managing a RabbitMQ producer connection.

    This class ensures only one connection to RabbitMQ exists per process.
    It handles connection retries, queue declaration, message publishing,
    and cleanup.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Override __new__ to enforce Singleton pattern.

        If no instance exists, create one and initialize the RabbitMQ
        connection. Otherwise, return the existing instance.

        Args:
            *args: Positional arguments for connection initialization.
            **kwargs: Keyword arguments for connection initialization.

        Returns:
            RabbitMQProducer: A singleton instance of the producer.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_connection(*args, **kwargs)
        return cls._instance

    def _init_connection(self, host="rabbitmq", port=5672):
        """
        Initialize the RabbitMQ connection and declare the task queue.

        Args:
            host (str): Hostname of the RabbitMQ server. Defaults to "rabbitmq".
            port (int): Port number of the RabbitMQ server. Defaults to 5672.

        Raises:
            ValueError: If RabbitMQ credentials are not set in environment variables.
            ConnectionError: If unable to connect to RabbitMQ after retries.
        """
        self.username = os.getenv("RABBITMQ_DEFAULT_USER")
        self.password = os.getenv("RABBITMQ_DEFAULT_PASS")
        if not self.username or not self.password:
            raise ValueError("RabbitMQ credentials not set in .env")

        credentials = pika.PlainCredentials(self.username, self.password)
        for attempt in range(10):
            try:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=host, port=port, credentials=credentials)
                )
                break
            except pika.exceptions.AMQPConnectionError as e:
                logger.info(f"RabbitMQ connection failed (attempt {attempt + 1}/10): {e}")
                time.sleep(3)
        else:
            raise ConnectionError("Failed to connect to RabbitMQ after retries")

        self.channel = self.connection.channel()
        self.queue_name = "rag_tasks"
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def publish(self, message: dict):
        """
        Publish a message to the RabbitMQ queue.

        Args:
            message (dict): A dictionary containing the message payload.

        Raises:
            HTTPException: If publishing fails due to a connection or serialization error.
        """
        try:
            self.channel.basic_publish(
                exchange="",
                routing_key=self.queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2),
            )
            logger.info("Form data published to RabbitMQ.")
        except Exception as e:
            logger.error(f"RabbitMQ publish error: {e}")
            raise HTTPException(status_code=500, detail=f"RabbitMQ error: {str(e)}")

    def close(self):
        """
        Close the RabbitMQ connection if it is open.

        Logs a warning if closing the connection fails.
        """
        try:
            if self.connection.is_open:
                self.connection.close()
        except Exception as e:
            logger.warning(f"Error closing RabbitMQ connection: {e}")
