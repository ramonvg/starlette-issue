# What's going on
When an endpoint raises an exception that is handled with the `exception_handlers` feature the endpoint will return the correct response to the client but a few seconds later a `RuntimeError: No response returned.` exception will be raised. 

I've notice this **only happens** when Starlette is initialized with more than one middlewares that are a subclass of `BaseHTTPMiddleware`. If you remove one of the DummyMiddleware's it'll stop happening.

This started happening with version `0.15.0`. It doesn't happen in version `0.14.2`. I'm wondering if it could be related to the major change related to `AnyIO`.

# How to reproduce the issue
## Setup dependencies
Just install the requirements.txt. 

`pip install -r requirements.txt`

## Start server
`uvicorn app:app --reload`

## Trigger exception
Just query the timeout endpoint with curl or whatever you prefer:

`curl http://localhost:8000/timeout`

# Example trace
```
INFO:     Will watch for changes in these directories: ['/home/ramon/tmp/starlette-issue']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [170302] using statreload
INFO:     Started server process [170342]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:42846 - "GET /timeout HTTP/1.1" 408 Request Timeout
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "/home/ramon/.pyenv/versions/3.9.5/envs/starlette-issue/lib/python3.9/site-packages/anyio/streams/memory.py", line 81, in receive
    return self.receive_nowait()
  File "/home/ramon/.pyenv/versions/3.9.5/envs/starlette-issue/lib/python3.9/site-packages/anyio/streams/memory.py", line 76, in receive_nowait
    raise WouldBlock
anyio.WouldBlock

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/ramon/.pyenv/versions/3.9.5/envs/starlette-issue/lib/python3.9/site-packages/starlette/middleware/base.py", line 41, in call_next
    message = await recv_stream.receive()
  File "/home/ramon/.pyenv/versions/3.9.5/envs/starlette-issue/lib/python3.9/site-packages/anyio/streams/memory.py", line 101, in receive
    raise EndOfStream
anyio.EndOfStream

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/ramon/.pyenv/versions/3.9.5/envs/starlette-issue/lib/python3.9/site-packages/uvicorn/protocols/http/h11_impl.py", line 373, in run_asgi
    result = await app(self.scope, self.receive, self.send)
  File "/home/ramon/.pyenv/versions/3.9.5/envs/starlette-issue/lib/python3.9/site-packages/uvicorn/middleware/proxy_headers.py", line 75, in __call__
    return await self.app(scope, receive, send)
  File "/home/ramon/.pyenv/versions/3.9.5/envs/starlette-issue/lib/python3.9/site-packages/starlette/applications.py", line 112, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/home/ramon/.pyenv/versions/3.9.5/envs/starlette-issue/lib/python3.9/site-packages/starlette/middleware/errors.py", line 181, in __call__
    raise exc
  File "/home/ramon/.pyenv/versions/3.9.5/envs/starlette-issue/lib/python3.9/site-packages/starlette/middleware/errors.py", line 159, in __call__
    await self.app(scope, receive, _send)
  File "/home/ramon/.pyenv/versions/3.9.5/envs/starlette-issue/lib/python3.9/site-packages/starlette/middleware/base.py", line 63, in __call__
    response = await self.dispatch_func(request, call_next)
  File "/home/ramon/tmp/starlette-issue/./app.py", line 26, in dispatch
    return await call_next(request)
  File "/home/ramon/.pyenv/versions/3.9.5/envs/starlette-issue/lib/python3.9/site-packages/starlette/middleware/base.py", line 45, in call_next
    raise RuntimeError("No response returned.")
RuntimeError: No response returned.
```