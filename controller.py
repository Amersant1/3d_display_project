from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from config import DATABASE_CONNECTION_URL, WEBHOOK_PORT

connection_string = DATABASE_CONNECTION_URL
engine = create_async_engine(connection_string, echo=False,
    # pool_size=20,  # Increase the pool size
    # max_overflow=30,  # Increase the overflow limit
    # pool_timeout=60  # Increase the timeout
)


Session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()



try:
    app = FastAPI()

    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы с любого происхождения
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
    
)
    # Base.metadata.create_all(engine)
except Exception as e:
    print(e)
