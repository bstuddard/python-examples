from src.startup.app import app
from src.startup.throttle import limiter
from fastapi import Request, Response
from fastapi.responses import StreamingResponse
from src.llm.anthropic_test import test_anthropic_stream_api_call


@app.get("/")
def read_root():
    return {"Hello": "World2"}


@app.get("/throttle")
@limiter.limit("10/minute")
def throttle_test(request: Request):
    return {"Hello": "World2-Throttle"}


@app.get("/stream")
async def stream_text(query: str):
    return StreamingResponse(test_anthropic_stream_api_call(query), media_type="text/plain")


""" # Enable if needed for database queries
from src.startup.database import run_query

@app.get("/db_test/")
async def test_db():
    result = await run_query('SELECT id FROM stg.tbl WHERE id=1')
    return result[0]
"""
