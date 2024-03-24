import logging.config

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .boot import boot_seq
from .router.job import router as job_router
from .router.keys import router as keys_router
from .router.desktops import router as desktops_router
from .router.agents import router as agents_router
from .router.runtime import router as runtime_router
from .router.vnc import router as vnc_router
from .router.task import router as tasks_router

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)


boot_seq()

app = FastAPI()

access_logger = logging.getLogger("access")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    access_logger.info(f"Received request: {request.method} {request.url}")
    response = await call_next(request)
    access_logger.info(
        f"Returned response {request.method} {request.url}: {response.status_code}"
    )
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://surf.agentlabs.xyz",
        "https://surf.dev.agentlabs.xyz",
        "https://surf.deploy.agentlabs.xyz",
        "https://surf.stg.agentlabs.xyz",
        "https://surf.testing.agentlabs.xyz",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(job_router)
app.include_router(keys_router)
app.include_router(desktops_router)
app.include_router(runtime_router)
app.include_router(agents_router)
app.include_router(tasks_router)
app.include_router(vnc_router)


@app.get("/")
async def root():
    return {"message": "Agent in the shell"}


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8088)
