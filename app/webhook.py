from fastapi import APIRouter
from app.etl import run_etl

router = APIRouter()


@router.post("/webhook/process-emails")
def process_emails():
    return run_etl(limit=10)