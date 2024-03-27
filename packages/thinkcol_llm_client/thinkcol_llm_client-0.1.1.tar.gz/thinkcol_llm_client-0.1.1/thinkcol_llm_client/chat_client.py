from abc import ABC, abstractmethod
from typing import Iterable


class ChatClient(ABC):

    @abstractmethod
    def invoke(self, msgs: list, model_name: str, batch_size: int):
        pass

    @abstractmethod
    def embed(
        self, texts: list, model_name: str, batch_size: int, texts_per_request: int
    ):
        pass

    # helper generator for chunking iterables into {chunk_size}-sized chunks
    def _chunk(
        self, iter: Iterable, chunk_size: int = 50, transform_fn=lambda x: x, **args
    ):
        chunk: list = []
        while True:
            el = next(iter, None)
            # check if iterator is empty
            if el is None:
                if chunk:
                    yield chunk
                break
            chunk.append(transform_fn(el, **args))
            if len(chunk) == chunk_size:
                yield chunk
                chunk = []
