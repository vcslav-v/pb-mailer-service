import asyncio
from aiokafka import AIOKafkaConsumer
from aiokafka.structs import ConsumerRecord
import ssl
from pb_mailer_service import config, mail, schemas
from pb_mailer_service.setup import TOPICS_MAP


async def consume():
    ssl_context = ssl.create_default_context()
    consumer = AIOKafkaConsumer(
        *TOPICS_MAP.keys(),
        bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
        ssl_context=ssl_context,
        security_protocol=config.KAFKA_SECURITY_PROTOCOL,
        sasl_mechanism=config.KAFKA_SASL_MECHANISM,
        sasl_plain_username=config.KAFKA_SASL_USERNAME,
        sasl_plain_password=config.KAFKA_SASL_PASSWORD,
        client_id=config.KAFKA_CLIENT_ID,
        group_id=config.KAFKA_GROUP_ID,
        auto_offset_reset=config.KAFKA_AUTO_OFFSET_RESET,
    )
    sem = asyncio.Semaphore(config.MAX_CONCURRENT_TASKS)
    await consumer.start()
    try:
        async for msg in consumer:
            asyncio.create_task(process_with_limit(msg, sem))
    except Exception as e:
        config.logger.error(f'Error consuming messages: {e}')
    finally:
        await consumer.stop()

async def process_with_limit(msg: ConsumerRecord, sem):
    async with sem:
        email_data = TOPICS_MAP.get(msg.topic)
        if email_data and isinstance(email_data, schemas.general.EmailData) and msg.value:
            try:
                await mail.process(msg.value, email_data)
            except Exception as e:
                config.logger.error(f'Error processing message from {msg.topic}: {e}')

if __name__ == '__main__':
    asyncio.run(consume())