from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
import sqlalchemy
import os


class Base(DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = "account"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    role = sqlalchemy.Column(sqlalchemy.String(16), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(80), nullable=False, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String(1024), nullable=False)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    is_verified = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)


DATABASE_URL = os.getenv(
    "DATABASE_URL", "mysql+asyncmy://root:admin@localhost:3306/AUTH_DEMO"
)
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)



async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)