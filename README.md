# CoffiFilter

☕️ CoffiFilter is a tool to help manage your LLM agents' outbound tool usage.

[![PyPI](https://img.shields.io/pypi/v/coffifilter.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/coffifilter.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/coffifilter)][pypi status]
[![License](https://img.shields.io/pypi/l/coffifilter)][license]

[![Tests](https://github.com/sjakati98/coffifilter/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/sjakati98/coffifilter/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi status]: https://pypi.org/project/coffifilter/
[read the docs]: https://coffifilter.readthedocs.io/
[tests]: https://github.com/sjakati98/coffifilter/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/sjakati98/coffifilter
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## What is CoffiFilter?

- A tool to help manage your LLM agents' outbound tool usage.
- Track and manage the tools that your agents are using.
- Switch tools on and off for your agents without having to redeploy them.

## Features

- Connect to your own redis server.
- Drop in decorator for langchain functions.

## Requirements

- Python 3.6 or later
- Redis server

## Installation

You can install _CoffiFilter_ via [pip] from [PyPI]:

```console
$ pip install coffifilter
```

## Usage

CoffiFilter can wrap your Langchain tools to help manage their usage.

```python
import coffifilter
from langchain_community.tools import YouTubeSearchTool

coffifilter.init(
    redis_host="your-redishost.redis-cloud.com",
    redis_port=11552,
    redis_db=0,
    redis_password="your-redispassword",
)

youtube_tool = coffifilter.wrap_langchain_tool(YouTubeSearchTool())

...

tools = [..., youtube_tool]

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
agent_executor.invoke({"input": "can you find videos on langchain"})
```


CoffiFilter can also be used as a decorator for your langchain functions.

```python
import coffifilter

coffifilter.init(
    redis_host="your-redishost.redis-cloud.com",
    redis_port=11552,
    redis_db=0,
    redis_password="your-redispassword",
)

@tool
@coffifilter.coffi_filter("summarize_tool")
def summarize_tool(url: str, callbacks: Callbacks = None):
    """Summarize a website."""
    text = requests.get(url).text
    summary_chain = (
        ChatPromptTemplate.from_template(
            "Summarize the following text:\n<TEXT {uid}>\n" "{text}" "\n</TEXT {uid}>"
        ).partial(uid=lambda: uuid.uuid4())
        | ChatOpenAI(model="gpt-4o")
        | StrOutputParser()
    ).with_config(run_name="Summarize Text")
    return summary_chain.invoke(
        {"text": text},
        {"callbacks": callbacks},
    )
```

The current design is to check the redis server for the tool status before executing the function. It literally checks if the tool is on or off by checking the value of the key in the redis server. If the key is not found, it will default to off. If the key is found, it will check if the value is "true" or "false".

The decorator will raise a ValueError if the tool is off.

Eg. If the tool is off, the following error will be raised:
```python
ValueError(f"Tool '{filter_string}' is not enabled")
```

## Coming Soon

- Better documentation.
- Better langchain integration.
- Better error handling.
- Local first approach; avoiding redis server if not needed.
- User tracking and IFTTT tool usage.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [GPL 3.0 license][license],
_CoffiFilter_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

### Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/sjakati98/coffifilter/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/sjakati98/coffifilter/blob/main/LICENSE
[contributor guide]: https://github.com/sjakati98/coffifilter/blob/main/CONTRIBUTING.md
[command-line reference]: https://coffifilter.readthedocs.io/en/latest/usage.html
