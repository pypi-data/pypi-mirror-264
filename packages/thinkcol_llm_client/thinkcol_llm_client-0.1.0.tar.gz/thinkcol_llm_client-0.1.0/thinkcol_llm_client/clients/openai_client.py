from openai import AzureOpenAI
import asyncio
from tqdm.asyncio import tqdm
from ..chat_client import ChatClient
from typing import Iterable
from dotenv import load_dotenv
from math import ceil
from ..constants import OPENAI_SYSTEM_PROMPT


class OpenAIClient(ChatClient):

    def __init__(self, api_key: str = None):
        if not api_key:
            load_dotenv()
        self.client = AzureOpenAI(api_version="2023-09-01-preview")

    # async generator for chat completions
    async def batch_invoke(
        self, msg_collection: Iterable, model_name: str, batch_size: int = 50
    ):
        for chunk in self._chunk(msg_collection, lambda x: x, batch_size):
            aws = [
                asyncio.to_thread(
                    lambda msg: self.client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": OPENAI_SYSTEM_PROMPT},
                            {"role": "user", "content": msg},
                        ],
                        temperature=0,
                    ),
                    msg,
                )
                for msg in chunk
            ]

            yield [
                completion.choices[0].message.content
                for completion in await asyncio.gather(*aws)
            ]

    async def batch_embed(
        self,
        texts: Iterable,
        model_name: str = "text-embedding-ada-002",
        batch_size: int = 50,
    ):
        splits = self._chunk(texts, lambda x: x, batch_size)
        for chunk in self._chunk(splits, lambda x: x, batch_size):
            aws = [
                asyncio.to_thread(
                    lambda texts: self.client.embeddings.create(
                        input=texts, model=model_name
                    ),
                    texts,
                )
                for texts in chunk
            ]
            yield [
                d.embedding
                for response in await asyncio.gather(*aws)
                for d in response.data
            ]

    # wrapper for acummulating results from batch_invoke
    async def invoke(self, msgs: list, model_name: str = "gpt-4"):
        return [
            completion
            async for completion_batch in tqdm(
                self.batch_invoke(iter(msgs), model_name), total=ceil(len(msgs) / 50)
            )
            for completion in completion_batch
        ]

    # wrapper for acummulating results from batch_embed
    async def embed(self, texts: list, model_name: str = "text-embedding-ada-002"):
        return [
            embed
            async for embed_batch in tqdm(
                self.batch_embed(iter(texts), model_name), total=ceil(len(texts) / 2500)
            )
            for embed in embed_batch
        ]
