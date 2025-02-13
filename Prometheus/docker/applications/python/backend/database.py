from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

engine = create_async_engine(
    'postgresql+psycopg://books:123456@postgres:5432/books'
)


async def get_session():
    async with AsyncSession(engine) as session:
        yield session

