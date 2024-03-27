
This is openai python client hacker, do something on the fly.

## Features:

* dumping LLM requests and responses into yaml or json files
* cache LLM responses

## Installation:

```
pip install openai-hacker
```

## Usage

Add the lines into your code:

```python
from openai_hacker import hack

hack()
```

available options:

* **dump_dir**, str, the location to dump LLM requests and responses. default `~/llm_dump_<timestamp>`
* **cache_dir**, str, the location to store cache files. default `~/llm_cache`
* **stage**, str, the prefix of dumped file names
* **suffix_completion**, str, the suffix of dumped file names for openai `Completion`. default `.yaml`
* **suffix_chat**, str, the suffix of dumped file names for openai `ChatCompletion`. default `_chat.yaml`
* **hack_chat**, bool,  hack openai `ChatCompletion` or not. default `True`
* **hack_completion**, bool, hack openai `Completion` or note. default `True`


