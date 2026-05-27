import asyncio
from typing import List

import httpx
from langchain_core.embeddings import Embeddings

from app.conf.app_config import EmbeddingConfig, app_config


class TEIEmbeddings(Embeddings):
    """直接调用 TEI (Text Embeddings Inference) HTTP 接口的 Embeddings 实现。"""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        texts = [t.replace("\n", " ") for t in texts]
        with httpx.Client() as client:
            resp = client.post(
                f"{self.base_url}/embed",
                json={"inputs": texts},
                timeout=3000,
            )
            resp.raise_for_status()
            return resp.json()

    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        texts = [t.replace("\n", " ") for t in texts]
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/embed",
                json={"inputs": texts},
                timeout=3000,
            )
            resp.raise_for_status()
            return resp.json()

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]

    async def aembed_query(self, text: str) -> List[float]:
        return (await self.aembed_documents([text]))[0]


class EmbeddingClientManager:
    def __init__(self, config: EmbeddingConfig):
        self.client: TEIEmbeddings | None = None
        self.config = config

    def _get_url(self):
        return f"http://{self.config.host}:{self.config.port}"

    def init(self):
        self.client = TEIEmbeddings(base_url=self._get_url())

embedding_client_manager = EmbeddingClientManager(app_config.embedding)

if __name__ == "__main__":
    embedding_client_manager.init()
    client = embedding_client_manager.client

    async def test():
        text = "hello"
        resp = await client.aembed_query(text)
        print(resp[:3])

    asyncio.run(test())