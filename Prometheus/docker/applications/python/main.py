import httpx
import logging
import os
import random
import time
import uvicorn

from fastapi import FastAPI, HTTPException, Response, Request, Body
from opentelemetry.propagate import inject
from typing import Optional
from utils import PrometheusMiddleware, metrics, setting_otlp

APP_NAME = os.environ.get("APP_NAME", "app-books")
EXPOSE_PORT = os.environ.get("EXPOSE_PORT", 3002)
OTLP_GRPC_ENDPOINT = os.environ.get("OTLP_GRPC_ENDPOINT", "http://tempo:4317")

app = FastAPI()

#-----------------------------
# Instrument Prometheus
#-----------------------------
app.add_middleware(PrometheusMiddleware, app_name=APP_NAME)

app.add_route("/metrics", metrics)

setting_otlp(app, APP_NAME, OTLP_GRPC_ENDPOINT)

class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1

logging.getLogger("uvicorn.access").addFilter(EndpointFilter())


#-----------------------------
# Dynamic Database
#-----------------------------
BOOKS = [ 
	{'id': 1, 'title': 'Titulo1', 'author': 'Author1', 'category': 'aventura'},
    {'id': 2, 'title': 'Titulo2', 'author': 'Author2', 'category': 'drama'},
	{'id': 3, 'title': 'Titulo3', 'author': 'Author3', 'category': 'terror'},
	{'id': 4, 'title': 'Titulo4', 'author': 'Author4', 'category': 'misterio'},
	{'id': 5, 'title': 'Titulo4', 'author': 'Author5', 'category': 'comedia'}
]

#-----------------------------
# Application
#-----------------------------
@app.get(path="/")
async def index():
    logging.info("Home Index")
    return "Home"

@app.get('/books')
async def books():
    logging.info("Read all books")
    return BOOKS

@app.get('/books/')
async def category(search: str):
    book_search = []
    for book in BOOKS:
    	if book.get('category').casefold() == search.casefold() or \
           book.get('title').casefold()    == search.casefold() or \
           book.get('author').casefold()   == search.casefold():
           book_search.append(book)
    logging.info("Read book {book_search}")
    return book_search 

@app.get('/book/{id}') 
async def book(id: int):
    for book in BOOKS:
        # Force Error 500
        if id >= 1000:
            raise HTTPException(status_code=500, detail="Internal Server Error")
            return {"status": "Internal Server Error"}
            logging.error("Error Id greater than 1000 !!!!")
            break

        if book.get('id') == id:
            logging.info("Read book with Id {book}")
            return book

@app.post('/book/create')
async def create(book=Body()):
    BOOKS.append(book)
    logging.info("Create book {book}")
    return book

@app.put('/book/update')
async def update(book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book.get('title').casefold():
           BOOKS[i] = book
           logging.info("Update book {book}")
           return book

@app.delete('/book/delete')
async def delete(id: int):
    for i in range(len(BOOKS)):
    	if BOOKS[i].get('id') == id:
           BOOKS.pop(i)
           logging.info("Delete book {BOOKS[i]}")
           return {}           

#-----------------------------
# Entrypoint Application
#-----------------------------

if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=EXPOSE_PORT, log_config=log_config)
