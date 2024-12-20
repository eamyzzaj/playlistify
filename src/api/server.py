from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.api import users
from src.api import competitions
import json
import logging
import sys
from starlette.middleware.cors import CORSMiddleware


description = """
Playlistify is everyone's newest, favorite way to show off your music taste.
"""

app = FastAPI(
    title="Playlistify",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Playlistify Team",
        "email": "playlistify@gmail.com",
    },
)


app.include_router(users.router)
app.include_router(competitions.router)

@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)

@app.get("/")
async def root():
    return {"message": "Welcome to Playlistify."}