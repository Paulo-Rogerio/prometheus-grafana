import random
import uvicorn
import prometheus_client

from prometheus_client import Counter
from fastapi import FastAPI, HTTPException, Response, Request, Body
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

BOOKS = [ 
	{'id': 1, 'title': 'Titulo1', 'author': 'Author1', 'category': 'drama'},
    {'id': 2, 'title': 'Titulo2', 'author': 'Author2', 'category': 'drama'},
	{'id': 3, 'title': 'Titulo3', 'author': 'Author3', 'category': 'terror'},
	{'id': 4, 'title': 'Titulo4', 'author': 'Author4', 'category': 'misterio'},
	{'id': 5, 'title': 'Titulo4', 'author': 'Author5', 'category': 'comedia'}
]

REQUESTS = Counter('http_request_total',
                   'Total number of requests')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(path="/")
async def index():
    REQUESTS.inc()
    return "Home"

@app.get('/books')
async def books():
    REQUESTS.inc()
    return BOOKS

@app.get('/books/')
async def category(search: str):
    REQUESTS.inc()
    book_search = []
    for book in BOOKS:
    	if book.get('category').casefold() == search.casefold() or \
           book.get('title').casefold()    == search.casefold() or \
           book.get('author').casefold()   == search.casefold():
           book_search.append(book)
    return book_search 

@app.get('/book/{id}') 
async def book(id: int):
    REQUESTS.inc()
    for book in BOOKS:
    	if book.get('id') == id:
           return book

@app.post('/book/create')
async def create(book=Body()):
    REQUESTS.inc()
    BOOKS.append(book)

@app.put('/book/update')
async def update(update=Body()):
    REQUESTS.inc()
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == update.get('title').casefold():
           BOOKS[i] = update

@app.delete('/book/delete')
async def delete(id: int):
    REQUESTS.inc()
    for i in range(len(BOOKS)):
    	if BOOKS[i].get('id') == id:
           BOOKS.pop(i)
           break

@app.get("/metrics")
async def get_metrics():
    return Response(
        content=prometheus_client.generate_latest(),
        media_type="text/plain"
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3002)    
