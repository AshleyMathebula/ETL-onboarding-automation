import asyncio
from fastapi import FastAPI

from app.webhook import router
from app.etl import run_etl
from app.config import CHECK_INTERVAL_SECONDS


app = FastAPI(
    title="Email ETL Onboarding Automation",
    description="Reads onboarding emails and generates whitelist upload files.",
    version="1.0.0"
)


@app.get("/")
def health_check():
    return {
        "status": "running",
        "message": "Email ETL Automation API is live"
    }


async def polling_worker():
    while True:
        try:
            print("Checking inbox for unread emails...")
            result = run_etl(limit=10)
            print(result)
        except Exception as error:
            print(f"Polling error: {error}")

        await asyncio.sleep(CHECK_INTERVAL_SECONDS)


@app.on_event("startup")
async def start_polling():
    asyncio.create_task(polling_worker())


app.include_router(router)