---
title: "Run FastAPI Server as a Package"
categories: [Dev, FastAPI]
math: true
---

## Introduction

When you try to start your FastAPI server, you've probably used `uvicorn` pointing to the FastAPI `app`:

```bash
uvicorn main:app --reload
```

While it works fine, it has some rooms for improvement.

First, when you restructure your server, you must enter the adjusted path to `app` every time you start the server.

Suppose you put FastAPI app in `src.main` then you would have to type. Even if it looked trivial, I hated typing it every time I start the server.

```bash
uvicorn src.main:app --reload
```

Also, with the typical approach, since the entry point of starting the server is `app`, it's hard to perform preliminary setups cleanly.

To make our server more modularized and easier to maintain, let's make the server as a package.

## Treat FastAPI Server as a Package

Instead of typing the command in a shell, we can programmatically start the FastAPI server with uvicorn by passing the FastAPI app path as a parameter.

```python
uvicorn.run(app="src.main:app", host="127.0.0.1", port=8080)
```

With this in mind, let's create a new project called `dummy`.

```bash
.
├── dummy
│   ├── __main__.py
│   └── server.py
├── poetry.lock
└── pyproject.toml
```

All the server application codes would go inside `dummy/` directory.

You notice that we have `__main__.py` right under `dummy/`. This file is a special module that enables you to treat a Python package as a <span class="hl">executable script</span>. So you would be able to "run" the Python package from the command line:

```bash
python -m dummy
```

Then, it would look at `__main__.py` and execute the code in that package.

Hence, we must put the code to start the FastAPI app inside `__main__.py`.

Now, let's look at the code.

## Implementation

* `server.py`

```python
from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="dummy server",
        version="0.1.0",
    )
    
    @app.get("/")
    def health_check():
        return {"message": "I'm doing fine. Thanks for asking."}
    
    return app


app = create_app()
```

* `__main__.py`

```python
import argparse
import os

import uvicorn


def extract_args() -> dict:
    argParser = argparse.ArgumentParser()
    argParser.add_argument(
        "-e",
        "--env",
        type=str,
        help='Server environment. Either "local", "dev", or "prod".',
        choices=["dev", "local", "prod"],
        default="local",
    )
    args = argParser.parse_args()
    return {"env": args.env}


def main(env: str) -> None:
    print(f"- Running server in {env} environment...")
    uvicorn.run(
        app="dummy.server:app",
        host="127.0.0.1",
        port=8080,
        reload=True if env == "local" else False,
    )
    
    
if __name__ == "__main__":
    args = extract_args()
    main(env=args["env"])
```

In `server.py`, we instantiate a FastAPI app. Then, in `__main__.py`, we call `uvicorn.run()` method to start the server, passing the FastAPI app path as a parameter.

```python
uvicorn.run(app="dummy.server:app")
```

> We can actually pass a FastAPI app instance as a parameter.
> 
> But then, we wouldn't be able to use `--reload` option.
> ![Alt text](/assets/img/fastapi/startserver1.png)
{: .prompt-info}

Another advantage is that we can pass any arguments when we start the server. In this example, the `dummy` package accepts `--env` argument to specify the development environment: `local`, `dev`, or `prod`.

Now, let's run the server with

```bash
python -m dummy --env local
```

![Alt text](/assets/img/fastapi/startserver2.png)

When we go to `localhost:8080` we can see that the server is successfully running.


![Alt text](/assets/img/fastapi/startserver3.png)

We've looked at how to treat our FastAPI server as a package. It helps us to keep our code clean and also perform preliminary steps before running the server.
