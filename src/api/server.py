from fastapi import FastAPI, exceptions, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.api import users
from src.api import competitions
import json
import logging
import time
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("performance")

# Add CORS middleware
origins = ["https://potion-exchange.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

# Middleware to log execution time for all endpoints
@app.middleware("http")
async def log_execution_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    execution_time = (end_time - start_time) * 1000
    logger.info(f"Endpoint: {request.url.path} | Time: {execution_time:.2f} ms")
    return response

# Include routers
app.include_router(users.router)
app.include_router(competitions.router)

# Custom exception handler
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
