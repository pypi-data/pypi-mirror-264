# LLM Client 
Internal package for making calls to LLMs.

## Install
```
pip install llm-client
```

## Usage: 
```
import asyncio
from clients.openai_client import OpenAIClient

texts = ["Hello", "Text 1", "ThinkCol"]

client = OpenAIClient()
asyncio.run(client.embed(texts))

questions = ["How do I implement best practices in data science projects" for _ in range(500)]
asyncio.run(client.invoke(questions))
```