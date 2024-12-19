from fastapi import FastAPI
from contextlib import asynccontextmanager
from example.router import auth
from example.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth, prefix="/auth", tags=["auth"])