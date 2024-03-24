"""
Asynchronous client implementation for communicating with the [Nebula REST API](/api-ref/rest-api/).

Explore the client by communicating with an in-memory webserver - no setup required:

<div class="termy">
```
$ # start python REPL with native await functionality
$ python -m asyncio
>>> from nebula.client.orchestration import get_client
>>> async with get_client() as client:
...     response = await client.hello()
...     print(response.json())
👋
```
</div>
"""
