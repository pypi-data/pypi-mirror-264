from abc import ABC, abstractmethod
from typing import Iterable


class ChatClient(ABC):

    @abstractmethod
    def batch_invoke(messages: list[str]):
        pass

    @abstractmethod
    def batch_embed(messages: list[str]):
        pass

    @abstractmethod
    def invoke(self, data: list):
        pass

    @abstractmethod
    def embed(self, data: list):
        pass

    # helper generator for chunking iterables into {chunk_size}-sized chunks
    def _chunk(self, iter: Iterable, transform_fn, chunk_size: int = 50, **args):
        chunk = []
        while True:
            el = next(iter, None)
            # check if iterator is empty
            if el == None:
                if chunk:
                    yield chunk
                break
            chunk.append(transform_fn(el, **args))
            if len(chunk) == chunk_size:
                yield chunk
                chunk = []
