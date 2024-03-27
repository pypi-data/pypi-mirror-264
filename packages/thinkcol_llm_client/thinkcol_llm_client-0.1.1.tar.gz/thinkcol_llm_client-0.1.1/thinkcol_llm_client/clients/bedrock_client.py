from dotenv import load_dotenv
import boto3
import os
import asyncio
import json
from math import ceil
from typing import Iterator, AsyncGenerator
from tqdm.asyncio import tqdm
from ..chat_client import ChatClient
from ..constants import SYSTEM_PROMPT, MSG_PROMPT, TEXTS_PER_REQUEST


class BedrockClient(ChatClient):
    def __init__(self, region="us-east-1"):
        load_dotenv()
        self.client = boto3.client(
            service_name="bedrock-runtime",
            region_name=region,
            aws_access_key_id=os.environ["BEDROCK_ACCESS_KEY"],
            aws_secret_access_key=os.environ["BEDROCK_SECRET_KEY"],
        )
        self.default_params = {
            "request_params": {
                "accept": "application/json",
                "contentType": "application/json",
            },
            "embed_params": {"truncate": "NONE", "input_type": "clustering"},
            "invoke_params": {
                "max_tokens": 512,
                "top_p": 0.8,
                "temperature": 0,
            },
        }

    # makes batched requests to bedrock
    async def batch_request(
        self,
        data: Iterator,
        request_params: dict = {},
        batch_size: int = 20,
        transform_fn=lambda x: x,
        **args,
    ) -> AsyncGenerator:
        request_params = request_params | self.default_params["request_params"]
        for chunk in self._chunk(data, batch_size, transform_fn, **args):
            aws = [
                asyncio.to_thread(
                    lambda p: self.client.invoke_model(body=p, **request_params),
                    payload,
                )
                for payload in chunk
            ]
            yield await asyncio.gather(*aws)

    async def batch_invoke(
        self,
        msgs: Iterator,
        model_name: str,
        batch_size: int = 20,
    ):
        async for response_batch in self.batch_request(
            msgs,
            {"modelId": model_name},
            batch_size=batch_size,
            transform_fn=lambda msg: json.dumps(
                {
                    "prompt": SYSTEM_PROMPT
                    + "\n\n"
                    + f"<context>{msg.get('context', '')}</context>\n\n"
                    + MSG_PROMPT.format(content=msg["content"]),
                }
                | self.default_params["invoke_params"]
            ),
        ):
            yield [
                json.loads(response["body"].read())["outputs"][0]["text"]
                for response in response_batch
            ]

    async def batch_embed(
        self,
        texts: Iterator,
        model_name: str,
        batch_size: int = 20,
        texts_per_request: int = TEXTS_PER_REQUEST,
    ) -> AsyncGenerator:
        texts_splits = self._chunk(texts, texts_per_request)
        async for response_batch in self.batch_request(
            texts_splits,
            {"modelId": model_name},
            batch_size=batch_size,
            transform_fn=lambda texts: json.dumps(
                {"texts": texts} | self.default_params["embed_params"]
            ),
        ):
            yield [
                embed
                for embed_split in [
                    json.loads(response["body"].read().decode())["embeddings"]
                    for response in response_batch
                ]
                for embed in embed_split
            ]

    async def embed(
        self,
        texts: list,
        model_name: str = "cohere.embed-multilingual-v3",
        batch_size=20,
        texts_per_request=TEXTS_PER_REQUEST,
    ) -> list:
        return [
            embed
            async for embed_batch in tqdm(
                self.batch_embed(
                    iter(texts), model_name, batch_size, texts_per_request
                ),
                total=ceil(len(texts) / (batch_size * texts_per_request)),
            )
            for embed in embed_batch
        ]

    async def invoke(
        self,
        texts: list,
        model_name: str = "mistral.mixtral-8x7b-instruct-v0:1",
        batch_size=20,
    ) -> list:
        return [
            output
            async for batch_output in tqdm(
                self.batch_invoke(iter(texts), model_name, batch_size),
                total=ceil(len(texts) / batch_size),
            )
            for output in batch_output
        ]
