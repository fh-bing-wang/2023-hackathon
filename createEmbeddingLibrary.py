from AzureOpenAIServer import AzureOpenAIServer
from createTextFromPdfDocs import createTextArrayFromPdfDocs
from itertools import islice
from dotenv import load_dotenv
import os
from RedisServer import RedisServer
import logging

aiServer = AzureOpenAIServer()
folder_path = './mBC(English)'

load_dotenv()
logger = logging.getLogger(__name__)

redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
redis_password = os.getenv('REDIS_PASSWORD') or ''
redisServer = RedisServer(redis_host, redis_port, redis_password)

def chunker(it, size):
    iterator = iter(it)
    res = []
    while chunk := list(islice(iterator, size)):
        res.append(chunk)
    return res

items = os.listdir(folder_path)
for item in items:
    texts = createTextArrayFromPdfDocs(folder_path, item)

    text_chunks = chunker(texts, 16)
    all_embeddings = []
    for chunk in text_chunks:
        all_embeddings += aiServer.get_embeddings(chunk)
    redisServer.create_hash('patient_a', texts, all_embeddings, item.replace('.pdf', ''))
    print("Added hash for %s.", item)

redisServer.create_index('patient_a')
