from model import *
import asyncio
from controller import WEBHOOK_PORT
import uvicorn
from datetime import datetime

from handlers import project_router, shelf_router, product_router, convert_router



async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
# asyncio.run(init_models())



# from handlers import app
from controller import app


@app.on_event("startup")
async def startup():
    # await init_models()
    print("startup ended")


routers = [convert_router, shelf_router, project_router, product_router]

for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы с любого происхождения
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
    
)
    uvicorn.run("wsgi:app", host="0.0.0.0", port=int(WEBHOOK_PORT), workers=2)
    print(f'START {datetime.now()}')
