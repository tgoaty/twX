from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
