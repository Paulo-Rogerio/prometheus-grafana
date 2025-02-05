import random
import prometheus_client
import psutil
import uvicorn
import time

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST, REGISTRY
from fastapi import FastAPI, HTTPException, Response, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
from pydantic import BaseModel

app = FastAPI()

#-----------------------------
# Instrument Prometheus Client
#-----------------------------
#
# Custom metrics
REQUEST_COUNT = Counter('http_request_total', 'Total HTTP Requests', ['method', 'status', 'path'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP Request Duration', ['method', 'status', 'path'])
REQUEST_IN_PROGRESS = Gauge('http_requests_in_progress', 'HTTP Requests in progress', ['method', 'path'])
#
# System metrics
CPU_USAGE = Gauge('process_cpu_usage', 'Current CPU usage in percent')
MEMORY_USAGE = Gauge('process_memory_usage_bytes', 'Current memory usage in bytes')

def update_system_metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.Process().memory_info().rss)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    method = request.method
    path = request.url.path

    REQUEST_IN_PROGRESS.labels(method=method, path=path).inc()
    
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    status = response.status_code
    REQUEST_COUNT.labels(method=method, status=status, path=path).inc()
    REQUEST_LATENCY.labels(method=method, status=status, path=path).observe(duration)
    REQUEST_IN_PROGRESS.labels(method=method, path=path).dec()

    return response

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
    return "Home"

@app.get('/books')
async def books():
    return BOOKS

@app.get('/books/')
async def category(search: str):
    book_search = []
    for book in BOOKS:
    	if book.get('category').casefold() == search.casefold() or \
           book.get('title').casefold()    == search.casefold() or \
           book.get('author').casefold()   == search.casefold():
           book_search.append(book)
    return book_search 

@app.get('/book/{id}') 
async def book(id: int):
    for book in BOOKS:
    	if book.get('id') == id:
           return book

@app.post('/book/create')
async def create(book=Body()):
    BOOKS.append(book)

@app.put('/book/update')
async def update(update=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == update.get('title').casefold():
           BOOKS[i] = update

@app.delete('/book/delete')
async def delete(id: int):
    for i in range(len(BOOKS)):
    	if BOOKS[i].get('id') == id:
           BOOKS.pop(i)
           break

@app.get("/metrics")
async def metrics():
    update_system_metrics()
    return Response(
        generate_latest(REGISTRY), 
        media_type=CONTENT_TYPE_LATEST
    )

#-----------------------------
# Entrypoint Application
#-----------------------------

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3002)    
