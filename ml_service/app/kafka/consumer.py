from aiokafka import AIOKafkaConsumer
import json
import asyncio
from app.vllm_client import query_vllm
from app.kafka.producer import send_kafka_message

KAFKA_BOOTSTRAP = "kafka:9092"
INPUT_TOPIC = "skin_analysis_request"
OUTPUT_TOPIC = "skin_analysis_result"

async def consume_messages():
    consumer = AIOKafkaConsumer(
        INPUT_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="ml-group"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print("Received message:", msg.value)
            user_id = msg.value["user_id"]
            features = msg.value["features"]

            prompt = f"Analyze the following skin features: {features}. Provide skincare advice."
            recommendation = await query_vllm(prompt)

            await send_kafka_message(OUTPUT_TOPIC, {
                "user_id": user_id,
                "recommendation": recommendation
            })
    finally:
        await consumer.stop()
