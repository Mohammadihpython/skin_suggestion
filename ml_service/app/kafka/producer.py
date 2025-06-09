from aiokafka import AIOKafkaProducer
import json
import asyncio

producer = None

async def init_kafka_producer(bootstrap_servers="kafka:9092"):
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    await producer.start()

async def send_kafka_message(topic: str, message: dict):
    if not producer:
        await init_kafka_producer()
    await producer.send_and_wait(topic, message)

async def shutdown_producer():
    if producer:
        await producer.stop()