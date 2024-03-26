# Dta Utils
=======

**Connect your app to DTA Services**


### What are DTA Services?

A collection of services to ease and speed up the development and monitoring of Applications, focused on gen AI apps.


## Introduction

You can use this package to easily integrate your application with the following services:
- DTA Proxy (manage and control access to LLM models)
- DTA Logs (monitor app usage and user feedback)

Any integration rely on having a service key generated on DTA to use its services.


## Dependencies

- [Python](https://www.python.org/) >= 3.10
- [Langfuse](https://github.com/langfuse/langfuse-python) >= 2


## Installation

You can install it using pip:

```bash
pip install dta-utils
```


## Basic usage

1. Install this package into your app

2. Add to your environment variables the following keys:

```bash
DTA_PROXY_KEY="sk..."
DTA_LOGS_PUBLIC_KEY="pk..."
DTA_LOGS_SECRET_KEY="sk-..."
```

3. Make calls to LLM models using *DTA Proxy*:

```python
from dta_utils import DtaProxy

client = DtaProxy.openai_client()

response = client.chat.completions.create(model="gpt-3.5-turbo", messages = [
    {
        "role": "user",
        "content": "tell me a random city of the world and its country"
    }
])

print(response)
```


4. Send logs to *Dta Logs*:


    4.1. Sending logs with a `DtaTracer` instance:


```python
from dta_utils import DtaTracer
import uuid

trace_id = f"trace_{uuid.uuid4()}"

tracer = DtaTracer(name="app-test")

# trace is a thread that will aggreagate events and scores
tracer.trace(
    id=trace_id,
    input={"data": "input"},
)

# event can be emitted anytime with anything relevant to track
tracer.event(
    name="event registered",
    input={"event-data": "event-input"},
    output={"event-data": "event-output"},
)

# traces can be updated at any time
tracer.trace(
    output={"data": "output"},
    tags=["example", "event", "tracer"],
)

# score is how to register any evaluation over a trace
tracer.score(
    name="user-feedback",
    # value can be any number
    value=5,
    comment="optional comments",
)
```


    4.2. Sending logs without an instance:


 Note: the `trace_id` have to be informed on each call


```python
from dta_utils import DtaLog
import uuid

trace_id = f"trace_{uuid.uuid4()}"

# trace is a thread that will aggreagate events
DtaLog.trace(
    id=trace_id,
    name="app-test",
    input={"data": "input"},
)

# event can be emitted anytime with anything relevant to track
DtaLog.event(
    trace_id=trace_id,
    name="event registered",
    input={"event-data": "event-input"},
    output={"event-data": "event-output"},
)

# traces can be updated at any time
DtaLog.trace(
    id=trace_id,
    output={"data": "output"},
    tags=["example", "event", "logs"],
)

# score is how to register any evaluation over a trace
DtaLog.score(
    trace_id=trace_id,
    name="user-feedback",
    # value can be any number
    value=-5,
    comment="optional comments",
)
```


    4.3. Log Model generation:

To log model generation, the most commom uses are either through openai lib (using Dta wrapper), or with Langchain, adding a set of callbacks provided.


        4.3.1. Using Openai lib wrapper:

```python
from dta_utils import DtaLog, DtaProxy
import uuid

trace_id = f"trace_{uuid.uuid4()}"

# get openai lib ready to log into DtaLog
# create the openai client using DtaProxy
client = DtaProxy.openai_client(openai=DtaLog.openai())

# example of using OpenAI functions
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
    }
]

# calling the model
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "how is the wheather in Reykjavik Iceland?",
        },
    ],
    tools=tools,
    # parameters for DTA log
    name="log-gen-name",
    trace_id=trace_id,
)

print(response)

# for performance improvement, the logs can be not immediately emitted
# so the following can be important if running the app in a mode that can be abruptly closed (like from command line)
# usually not important if running on a webserver where the app is not immediatelly closed
DtaLog.openai_flush(dta_openai)
```


        4.3.2. Using Langchain callbacks:

```python
from dta_utils import DtaLog, DtaProxy
from langchain_openai import ChatOpenAI

dta_handler = DtaLog.langchain_handler()

model = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo",
    openai_api_base=DtaProxy.url(),
    openai_api_key=DtaProxy.key(),
    callbacks=[dta_handler],
)

response = model.invoke(
    [
        {
            "role": "user",
            "content": "tell me a random city of the world and its country",
        }
    ]
)

print(response)

```

