import httpx
import logging
import os
import random
import time
import uvicorn

from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import Depends, FastAPI, Query, Response
from pydantic import BaseModel
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine, get_session
from models import Book, reg

from opentelemetry.propagate import inject
from typing import Optional
from utils import PrometheusMiddleware, metrics, setting_otlp

APP_NAME = os.environ.get("APP_NAME", "app-books")
EXPOSE_PORT = os.environ.get("EXPOSE_PORT", 3002)
OTLP_GRPC_ENDPOINT = os.environ.get("OTLP_GRPC_ENDPOINT", "http://tempo:4317")

@asynccontextmanager
async def lifespan(app):
    async with engine.begin() as conn:
        await conn.run_sync(reg.metadata.drop_all)
        await conn.run_sync(reg.metadata.create_all)

    yield

app = FastAPI(lifespan=lifespan)

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


@app.get(path="/")
async def index():
    logging.info("Home Index Books")
    return "Home"

@app.get("/book/random_status")
async def random_status(response: Response):
    return_status = random.choice([404, 405, 422, 500, 503])
    logging.info("Ramdom Status Books-Backend {return_status}")
    response.status_code = return_status
    return {"path": "/book/random_status"}

@app.get('/book/{book_id}', response_model=BookOut)
async def get_book(book_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.get(Book, book_id)
    logging.info("Get Book in Books-Backend - {book_id}")
    return result

@app.get('/book')
async def search_book(search: str, session: AsyncSession = Depends(get_session)):
    query = await session.execute(select(Book).where(Book.title == search))
    result = query.scalars().all()
    logging.info("Get Book in Books-Backend by title: {title}")
    return result

@app.get('/books', response_model=list[BookOut])
async def get_books(
    limit: int = Query(default=50),
    offset: int = Query(default=0),
    session: AsyncSession = Depends(get_session)
):
    result = await session.scalars(select(Book).limit(limit).offset(offset))
    logging.info("Get All Books in Books-Backend")
    return result.all()

@app.post('/book', response_model=BookOut)
async def create_book(
    book: BookIn, session: AsyncSession = Depends(get_session)
):
    logging.info("Create Book in Books-Backend {book}")
    dump = book.model_dump()
    book_db = Book(**dump)
    session.add(book_db)
    await session.commit()
    await session.refresh(book_db)
    return book_db

@app.put('/book/{book_id}', response_model=BookOut)
async def update_book(book_id: int, payload: BookIn, session: AsyncSession = Depends(get_session)):
    query = await session.execute(select(Book).filter(Book.id == book_id))
    result = query.scalars().first()
    logging.info("Update Book in Books-Backend {payload}")
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")    
    result.title = payload.title
    result.author = payload.author
    result.category = payload.category
    await session.commit()
    await session.refresh(result)
    return result

@app.delete('/book/{book_id}', response_model=list[BookOut])
async def delete_book(book_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(delete(Book).where(Book.id == book_id))
    await session.commit()
    logging.info("Delete Book in Books-Backend {book_id}")
    return []

#-----------------------------
# Entrypoint Application
#-----------------------------
if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=EXPOSE_PORT, log_config=log_config)
