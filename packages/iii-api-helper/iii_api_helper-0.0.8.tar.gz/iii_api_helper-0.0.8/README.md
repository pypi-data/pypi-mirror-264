<h1 align="center"><b>III API base</b></h1>
<p align="center">
  <img alt="Branding" width="128px" src="icons/logo.png" />
</p>
<div align="center">
<a href="https://github.com/pypa/hatch">
  <img alt="Hatch project" src="https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg">
</a>
<a href="https://pypi.org/project/iii-api-helper" target="_blank">
  <img src="https://img.shields.io/pypi/v/iii-api-helper?logo=pypi&logoColor=ffd242&label=PyPI" alt="Package version">
</a>
<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/iii-api-helper">
<br />
<a href="https://pepy.tech/project/iii-api-helper" >
  <img alt="Downloads" src="https://static.pepy.tech/badge/iii-api-helper"/>
</a>
<a href="https://pepy.tech/project/iii-api-helper" >
  <img alt="Weekly downloads" src="https://static.pepy.tech/badge/iii-api-helper/week"/>
</a>
<a href="https://pepy.tech/project/iii-api-helper" >
  <img alt="Monthly downloads" src="https://static.pepy.tech/badge/iii-api-helper/month"/>
</a>
<p align="center">
III FastAPI Common base
<br />
<a href="https://pypi.org/project/iii-api-helper/"><strong>Go to pypi now</strong></a>
</p>
</div>

---

## Usage

### Config

> The later config will override the previous one.

This table shows the predefined environment variables.

| Keyword    | Type    | Default     | Description                             |
|------------|---------|-------------|-----------------------------------------|
| `DEBUG`    | boolean | false       | To set the logging as `DEBUG` state.    |
| `RELOAD`   | boolean | false       | To auto reload the FastAPI application. |
| `APP_NAME` | string  | Backend API | The application name shows on Swagger.  |

```python
from pathlib import Path

from api_helper.config import load_config

# Load config
load_config(Path(__file__).parent / ".env")

# Load default config in the directory (.env)
load_config(Path(__file__).parent)
```

### FastAPI example

> To config the FastAPI by env, read the [Config](#config) section.

```python
from pathlib import Path

from api_helper import FastAPI, success_response

app: FastAPI = FastAPI(base_folder=Path(__file__).parent)
# Optional to setup sentry
app.setup_sentry("sentry_dsn")


@app.get("/")
def home():
    return success_response("Hello, World!")


# Start the app and enjoy
app.run("127.0.0.1", 5000)
```

## Build backend

hatch

- [version](https://hatch.pypa.io/1.9/version/)

```shell
hatch env create
hatch build
hatch publish -r test
```
