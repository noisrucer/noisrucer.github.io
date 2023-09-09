---
title: "Using Dev Container to run Python 3.8 on M1 chip."
categories: [Dev, Docker]
math: true
---

## Introduction

During my internship, one of my jobs was to develop a server-side Python SDK that collects user-assistant chatbot conversation data and send to ingestion server.

I decided to support the Python version `>= 3.8.0`.

The reason was the Python SDK will provide integrations with LangChain and OpenAI and they require `>= Python 3.7`.

![Alt text](/assets/img/python/devcontainer1.png).

However, since Python 3.7 is now in "end-of-life" status (as of Sep 2023), I chose to support from `3.8.0`.

## Problem

Then comes the problem..

I was trying to set up the Python environment with `pyenv` but soon faced the installation issue for `3.8.0`.

After a bit of research, I found out that Python `3.9.1` was the first version to support macOS 11 Big Sur, and in turn supporting **M1-powered Macbooks**.


## Using Dev Container on vscode

![Alt text](/assets/img/python/devcontainer6.png)

In order to use `3.8.0` on M1 architecture (arm64), I used <span class="hl">Dev Container</span>.

A Dev Container allows you to use a docker container as a **full-featured development environment**, hence making the setup process super easy.

Especially, VSCode supports Dev Container extension so that we can work inside the dev container with all the features and settings from the local environment.


## Install Related VSCode extensions

Install **Dev Containers** and **Remote Development** extensions on VSCode.

![Alt text](/assets/img/python/devcontainer2.png)

## Configure Dev Container Settings

![Alt text](/assets/img/python/devcontainer3.png)

* First, create `.devcontainer` folder in your project root directory.
* Create `Dockerfile` and `devcontainer.json` files under it.

Since we want to use Python version `3.8.10`, let's write a Dockerfile with the Python 3.8.0 base image.

```dockerfile
FROM python:3.8.0

# Other configs if you need
```

Then, write it in `devcontainer.json`

```json
{
    "name": "Python 3.8.0",
    "build": {
    "dockerfile": "Dockerfile",
    "context": ".."
  },
    "customizations": {
    // Configure properties specific to VS Code.
    "vscode": {
      // Set *default* container specific settings.json values on container create.
      "settings": { 
        "python.defaultInterpreterPath": "/usr/local/bin/python"
      },
      
      // Add the IDs of extensions you want installed when the container is created.
      "extensions": [
        "ms-python.python"
      ]
    }
  }
}
```

## Start the Dev Container

![Alt text](/assets/img/python/devcontainer4.png)

Enter `Commnad + Shift + P` to open up Command Palette and type **Dev Containers: Reopen in Container**.


![Alt text](/assets/img/python/devcontainer5.png)

Then, we can see that we jumped into the dev container.

Check the python version with `python --version` in the terminal. We can see that we're using Python 3.8.0!

### Automatic Workspace Mounting

One great thing about VSCode Dev Container is that it supports **automatic workspace mounting**. This means that you can work on either the local and inside the dev container, and all the workspace files are automatically synced, providing a seamless experience.
