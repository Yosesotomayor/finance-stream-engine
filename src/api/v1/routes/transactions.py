import os
import json

from dotenv import find_dotenv, load_dotenv
from fastapi import APIRouter, Header, HTTPException, status
from confluent_kafka import Producer

from src.generator.generator import TransactionGenerator

import logging

logger = logging.getLogger(__name__)
load_dotenv(find_dotenv())

router = APIRouter()
CLIENT_TOKEN = os.environ["X_CLIENT_TOKEN"]
KAFKA_BROKER = os.environ["KAFKA_BROKER"]

producer_config = {
      'bootstrap.servers': KAFKA_BROKER,
}
producer = Producer(producer_config)

def delivery_report(err, msg):
      """
      Callback function to handle delivery reports from Kafka.

      This function is called once for each message produced to indicate
      whether the delivery was successful or if there was an error.
      """
      if err is not None:
            logger.error(f"Delivery failed for record {msg.key()}: {err}")
      else:
            logger.info(f"Record {msg.key()} successfully produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

@router.post("/generate_transaction", status_code=status.HTTP_202_ACCEPTED, tags=["Transactions"])
async def generate_transaction(
    x_client_token: str | None = Header(default=None, alias="X-Client-Token"),
):
      if not x_client_token or x_client_token != CLIENT_TOKEN:
            raise HTTPException(
                  status_code=status.HTTP_401_UNAUTHORIZED,
                  detail="Unauthorized",
            )

      transaction = TransactionGenerator().generate_transaction()
      transaction_dict = transaction.model_dump()

      topic = "transactions.stream"
      key = transaction.transaction_id.encode("utf-8")

      try:
            producer.produce(
                  topic,
                  key=key,
                  value=json.dumps(str(transaction_dict)).encode("utf-8"),
                  callback=delivery_report,
            )
            producer.poll(0)  # Trigger delivery report callbacks
      except Exception as e:
            raise HTTPException(
                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                  detail=f"Failed to produce message to Kafka: {str(e)}",
            )

      return {
            "status": "accepted",
            "message": "Transaction event published to stream successfully",
            "transaction": transaction_dict
    }
