# LLM Client 
Internal package for making calls to LLMs.

## Install
```
pip install thinkcol_llm_client
```

## Usage: 
### Normal Usage
```
import asyncio
from clients.openai_client import OpenAIClient

texts = ["Hello", "Text 1", "ThinkCol"]

client = OpenAIClient()
asyncio.run(client.embed(texts))

questions = ["How do I implement best practices in data science projects" for _ in range(500)]
asyncio.run(client.invoke(questions))
```

### Jupyter Notebook

An event loop is created and run automatically by Jupyter. Replace asyncio.run with await.
```
await client.embed(texts)
```