from confluent_kafka import Consumer, KafkaError, Producer

from dotenv import find_dotenv, load_dotenv
from sqlalchemy.exc import IntegrityError

import json
import os
import logging

from src.database.connection import get_session
from src.models.db_models import TransactionDBModel

logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

KAFKA_BROKER = os.environ["KAFKA_BROKER"]
GROUP_ID = os.environ["KAFKA_GROUP_ID"]

consumer_config = {
      'bootstrap.servers': KAFKA_BROKER,
      'group.id': GROUP_ID,
      'auto.offset.reset': 'earliest',
      'enable.auto.commit': False,
}

running = True
def process_transaction(msg):
      try:
            transaction_data = json.loads(msg.value().decode('utf-8'))
      except Exception as e:
            logger.error(f"Failed to process transaction: {e}")
            return False

      try:
            with get_session() as session:
                  session.add(TransactionDBModel(**transaction_data))
                  session.commit()
            return True

      except IntegrityError as e:
            logger.warning(f"Integrity error while processing transaction: {e}")
            return True
      
      except Exception as e:
            logger.error(f"Failed to process transaction: {e}")
            return False

def consume_transactions(consumer, topics, producer):
      global running
      try:
            consumer.subscribe(topics)
            while running:
                  msg = consumer.poll(timeout=1.0)
                  if msg is None: continue
                  if msg.error():
                        if msg.error().code() == KafkaError._PARTITION_EOF:
                              continue
                        else:
                              logger.error(f"Kafka error: {msg.error()}")
                              break
                  success = process_transaction(msg)
                  if success:
                        consumer.commit(msg, asynchronous=False)
                  else:
                        try: 
                              raw_value = msg.value()
                              producer.produce(
                                    "transactions.dlq", 
                                    value=raw_value,
                                    key=msg.key()
                              )
                              producer.flush(timeout=0.5)
                              logger.warning(f"Sent message to DLQ: {raw_value}")
                        except Exception as e:
                              logger.error(f"Failed to send message to DLQ: {e}")
                        consumer.commit(msg, asynchronous=False)
      except Exception as e:
            print(f"Error consuming transactions: {e}")
      finally:
            consumer.close()

def shutdown():
      global running
      running = False

if __name__ == "__main__":
      consumer = Consumer(consumer_config) 
      producer = Producer({'bootstrap.servers': KAFKA_BROKER})
      topics = ["transactions.stream"]

      logger.info("Starting transaction consumer...")
      try:
            consume_transactions(consumer, topics, producer)
      except KeyboardInterrupt:
            logger.info("Shutting down transaction consumer...")
            shutdown()
