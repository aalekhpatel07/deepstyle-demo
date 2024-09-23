#!/usr/bin/env python
import logging
import typing
import urllib
from datetime import datetime


from qdrant_client import QdrantClient
import qdrant_client.http.exceptions
from qdrant_client.models import Distance, VectorParams, PointStruct
import requests


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


qdrant = QdrantClient("http://qdrant:6333")
extractor = None


class EmbeddingExtractor:
    def __init__(self, *args, **kwargs):
        self.url = "http://deepstyle/"
        self.session = requests.Session()

    def get_embeddings(self, text: str) -> typing.List[float]:
        response = self.session.post(self.url, json={"text": text})
        response.raise_for_status()
        return response.json()["embeddings"]


def create_collection():
    global qdrant
    qdrant.create_collection(
        collection_name="text_embeddings",
        vectors_config=VectorParams(size=768, distance=Distance.COSINE)
    )


def insert_embeddings(identifier, embeddings, **metadata):
    qdrant.upsert(
        collection_name="text_embeddings",
        wait=True,
        points=[
            PointStruct(id=identifier, vector=embeddings, payload=metadata)
        ]
    )


CORPUS = {
    # some identifier: actual contents
    1: "Hello world!",
    2: "Some other text.",
}


def main():
    try:
        create_collection()
    except qdrant_client.http.exceptions.UnexpectedResponse as exc:
        logger.info(f"Found collection: {exc}")
        pass


    global extractor
    extractor = EmbeddingExtractor()
    
    for key, value in CORPUS.items():
        embeddings = extractor.get_embeddings(value)
        insert_embeddings(key, embeddings, timestamp=datetime.utcnow())

if __name__ == '__main__':
    main()

