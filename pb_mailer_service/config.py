import os
import sys
from dotenv import load_dotenv
from loguru import logger

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    logger.remove()
    logger.add(sys.stderr, level='DEBUG')
    IS_DEV = True
    load_dotenv(dotenv_path)
    logger.info('Loaded .env file')
else:
    logger.remove()
    logger.add(sys.stderr, level='INFO')
    IS_DEV = False

# General configuration
MAX_CONCURRENT_TASKS = int(os.getenv('MAX_CONCURRENT_TASKS', 10))

# email configuration
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), os.getenv('TEMPLATES_DIR', 'templates'))

# SMTP configuration
SMTP_HOSTNAME = os.getenv('SMTP_HOSTNAME', '')
SMTP_PORT = int(os.getenv('SMTP_PORT', 0))
SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
SMTP_START_TLS = os.getenv('SMTP_START_TLS', 'True').lower() in ('true', '1', 'yes')
SMTP_SENDER = os.getenv('SMTP_SENDER', '')
SMTP_FROM_NAME = os.getenv('SMTP_FROM_NAME', '')

# Avro schema registry configuration
SCHEMA_REGISTRY_URL = os.getenv('SCHEMA_REGISTRY_URL', '')
SCHEMA_REGISTRY_KEY = os.getenv('SCHEMA_REGISTRY_KEY', '')
SCHEMA_REGISTRY_SECRET = os.getenv('SCHEMA_REGISTRY_SECRET', '')

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', '')
KAFKA_SECURITY_PROTOCOL = os.getenv('KAFKA_SECURITY_PROTOCOL', 'SASL_SSL')
KAFKA_SASL_MECHANISM = os.getenv('KAFKA_SASL_MECHANISM', 'PLAIN')
KAFKA_SASL_USERNAME = os.getenv('KAFKA_SASL_USERNAME', '')
KAFKA_SASL_PASSWORD = os.getenv('KAFKA_SASL_PASSWORD', '')
KAFKA_CLIENT_ID = os.getenv('KAFKA_CLIENT_ID', 'mailer-service-client')
KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID', 'mailer-service-group')
KAFKA_AUTO_OFFSET_RESET = os.getenv('KAFKA_AUTO_OFFSET_RESET', 'earliest')