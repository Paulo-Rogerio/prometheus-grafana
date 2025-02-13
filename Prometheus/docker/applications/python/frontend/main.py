import httpx
import logging
import os
import time
import uvicorn

from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from opentelemetry.propagate import inject
from typing import Optional
from utils import PrometheusMiddleware, metrics, setting_otlp

APP_NAME = os.environ.get("APP_NAME", "frontend")
EXPOSE_PORT = os.environ.get("EXPOSE_PORT", 3003)
OTLP_GRPC_ENDPOINT = os.environ.get("OTLP_GRPC_ENDPOINT", "http://tempo:4317")

app = FastAPI()

#-----------------------------
# Instrument Prometheus
#-----------------------------
app.add_middleware(
    PrometheusMiddleware, 
    app_name=APP_NAME
)

app.add_route("/metrics", metrics)

setting_otlp(app, APP_NAME, OTLP_GRPC_ENDPOINT)

class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1

logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

#-----------------------------
# Application
#-----------------------------

class BookIn(BaseModel):
    title: str
    author: str
    category: str

class BookOut(BookIn):
    id: int
    created_at: datetime

@app.get("/library/random_status")
async def random_status():
    async with httpx.AsyncClient() as client:
        response = await client.get(f'http://books:3002/book/random_status')
        logging.info("Ramdom Status Library {return_status}")
        return response.json()

@app.get('/library/book/{book_id}')
async def get_book(book_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'http://books:3002/book/{book_id}')
        logging.info("Get Book in Library - {book_id}")
        return response.json()

@app.get('/library/book')
async def search_book(search: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'http://books:3002/book?search={search}')
        logging.info("Get Book in Library by title: {title}")
        return response.json()

@app.get('/library/books')
async def get_books():
    async with httpx.AsyncClient() as client:
        response = await client.get('http://books:3002/books')
        logging.info("Get All Books in Library")    
    return response.json()

@app.post('/library/book', response_model=BookOut)
async def create_book(book: BookIn):
    async with httpx.AsyncClient() as client:
        response = await client.post('http://books:3002/book', json=book.model_dump())
        logging.info("Create Book in Library {book}")
        return response.json()

#-----------------------------
# Entrypoint Application
#-----------------------------
if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=EXPOSE_PORT, log_config=log_config)
