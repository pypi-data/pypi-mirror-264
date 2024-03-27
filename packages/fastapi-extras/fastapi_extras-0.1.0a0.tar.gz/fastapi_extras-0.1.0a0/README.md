# FastAPI Extras

This package provides some extra utilities for FastAPI.

## Installation

```bash
pip install fastapi-extras
```

## Usage

### Error Handling

```python
from fastapi import FastAPI
from fastapi_extras.errors import configure_error_handlers, BadRequestError

app = FastAPI()
configure_error_handlers(app)

@app.get("/error")
def error():
    raise BadRequestError("This is a bad request", detail={"reason": "You did something wrong"})
    """
    {
        "status": 400,
        "title": "BadRequest",
        "message": "This is a bad request",
        "detail": {
            "reason": "You did something wrong"
        },
    }
    """
```
