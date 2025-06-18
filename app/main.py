from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from app.routers import router
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    global_exception_handler,
)

app = FastAPI(
    title="twX",
    exception_handlers={
        HTTPException: http_exception_handler,
        RequestValidationError: validation_exception_handler,
        Exception: global_exception_handler,
    },
)

app.include_router(router)
