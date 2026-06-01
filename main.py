import uuid

from fastapi import FastAPI, Request

from app.api.lifespan import lifespan
from app.api.routers.query_router import query_router
from app.core.context import request_id_contextvar

app = FastAPI(lifespan=lifespan)

app.include_router(query_router)

@app.middleware("http")
async def log_request(request: Request, call_next):
    # 请求被处理之前
    resquest_id = uuid.uuid4()
    request_id_contextvar.set(resquest_id)
    reponse = await call_next(request)
    # 请求被处理之后
    return reponse