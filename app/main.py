from fastapi import FastAPI, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from lib.db import get_session
from lib.viewmodel import MainModel
from fastapi.middleware.cors import CORSMiddleware
from lib.schemas import TemplateSchema, DeviceSchema


app = FastAPI(root_path="/api/")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/path/")
async def templates(
    last_id: None|int=Query(None, description='Последний ID'),
    q: str=Query('', description='Строка поиска'),
    session: AsyncSession=Depends(get_session)
) -> list[dict]:
    model = MainModel(session)
    return await model.path(q, last_id)
