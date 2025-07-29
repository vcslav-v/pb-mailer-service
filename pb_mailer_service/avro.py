import aiohttp
import struct
import json
import io
import avro.schema
from avro.io import DatumReader, BinaryDecoder
from pb_mailer_service import config
from cachetools import TTLCache
from pydantic import BaseModel
from typing import Type, cast, TypeVar

SCHEMA_REGISTRY_AUTH = aiohttp.BasicAuth(config.SCHEMA_REGISTRY_KEY, config.SCHEMA_REGISTRY_SECRET)

schema_cache = TTLCache(maxsize=1000, ttl=3600)


T = TypeVar('T', bound=BaseModel)

async def get_schema(schema_id):
    if schema_id in schema_cache:
        return schema_cache[schema_id]
    async with aiohttp.ClientSession(auth=SCHEMA_REGISTRY_AUTH) as session:
        url = f'{config.SCHEMA_REGISTRY_URL}/schemas/ids/{schema_id}'
        async with session.get(url) as resp:
            data = await resp.json()
            schema = data['schema']
            schema_cache[schema_id] = schema
            return schema

async def decode_avro_message(raw_bytes: bytes, target_schema: Type[T]) -> T:
    if raw_bytes[0] != 0:
        raise ValueError('Unknown magic byte')

    schema_id = struct.unpack('>I', raw_bytes[1:5])[0]

    schema_str = await get_schema(schema_id)
    schema_dict = json.loads(schema_str)
    schema = avro.schema.parse(json.dumps(schema_dict))
    payload = io.BytesIO(raw_bytes[5:])
    decoder = BinaryDecoder(payload)
    reader = DatumReader(schema)

    data = reader.read(decoder)
    return target_schema.model_validate(data)
