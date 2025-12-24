from fastapi import FastAPI, Request
from datetime import datetime
import logging
import time
# import uvicorn
from pytz import timezone
from sqlalchemy.ext.asyncio import AsyncSession
from settings import (
    ENVIRONTMENT,
    TZ,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from core.mytask import run_scheduled_task_1
from contextlib import asynccontextmanager
from fastapi_utilities import repeat_at, repeat_every

from routes.auth import router as AuthRouter
from routes.file import router as FileRouter

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup ---
    # await scheduled_task()
    scheduled_task_1()
    # scheduled_task_2()
    scheduled_task_3()
    yield
    # --- shutdown ---


tittle="HRISKU"
if ENVIRONTMENT == 'dev':
    app = FastAPI(
        title=tittle,
        docs_url="/docs",
        redoc_url=None,
        openapi_url="/openapi.json",
        lifespan=lifespan,
        swagger_ui_oauth2_redirect_url="/docs/oauth2-redirect",
        swagger_ui_init_oauth={
            "clientId": "your-client-id",
            "authorizationUrl": "/auth/token",
            "tokenUrl": "/auth/token",
        },
    )
elif ENVIRONTMENT == 'prod':
        app = FastAPI(
        title=tittle,
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
        lifespan=lifespan,
        swagger_ui_oauth2_redirect_url="/docs/oauth2-redirect",
        swagger_ui_init_oauth={
            "clientId": "your-client-id",
            "authorizationUrl": "/auth/token",
            "tokenUrl": "/auth/token",
        },
    )
        
@repeat_at(cron="48 * * * *")
def scheduled_task_1():
    print("Start!")
    # Ambil waktu lokal sesuai TZ
    local_tz = timezone(TZ)
    now_local = datetime.now(local_tz)
    print(f"Local time ({TZ}):", now_local)
    # run_scheduled_task_1(func_name="generate_report")
    if now_local.hour == 22:
        print("Sudah pukul 23:58, memanggil fungsi generate_report untuk regenerate summary and report.")
        run_scheduled_task_1(func_name="generate_report")
    print("End")

@repeat_at(cron="*/30 * * * *") # every 15 minutes
def scheduled_task_3():
    print("Start!")
    # Ambil waktu lokal sesuai TZ
    local_tz = timezone(TZ)
    now_local = datetime.now(local_tz)
    print(f"Local time ({TZ}):", now_local)
    run_scheduled_task_1(func_name="generate_client_report_runner")
    print("End")

app.add_middleware(
    CORSMiddleware,
    # allow_origins=CORS_ALLOWED_ORIGINS,
    allow_origins=['*'],
    allow_credentials=True,
    # allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(HTTPSRedirectMiddleware) # Untuk batasi hanya https
# app.add_middleware(GZipMiddleware, minimum_size=500)  # Hanya mengompresi response di atas 500 byte

app.include_router(AuthRouter, prefix="/auth")
app.include_router(FileRouter, prefix="/file")

@app.get("/")
async def read_root():  # <-- Perbaikan di sini
    try:
        return {"message": "Hello welcome to hrisku"}
    except Exception as e:
        return {"error": str(e)}


logging.basicConfig(level=logging.INFO)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logging.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    duration = time.time() - start_time
    logging.info(f"Response: {response.status_code} in {duration:.2f} seconds")
    return response
# @app.on_event("startup")
# async def startup_event():
#     app.state.db_client = await get_db()

# @app.on_event("shutdown")
# async def shutdown_event():
#     await app.state.db_client.close()

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)


