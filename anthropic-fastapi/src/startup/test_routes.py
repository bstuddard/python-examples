from src.startup.app import app
from src.startup.throttle import limiter
from fastapi import Request, Response
from fastapi.responses import StreamingResponse
from src.llm.anthropic_helpers import anthropic_stream_api_call
from src.llm.schemas import ChatInput


@app.get("/")
def read_root():
    return {"Hello": "World2"}


@app.get("/throttle")
@limiter.limit("10/minute")
def throttle_test(request: Request):
    return {"Hello": "World2-Throttle"}


@app.post("/stream")
async def stream_text(input: ChatInput):
    """FastAPI endpoint to stream AI-generated text"""
    return StreamingResponse(anthropic_stream_api_call(input.chat_input_list), media_type="text/event-stream")


""" # Enable if needed for database queries
from src.startup.database import run_query

@app.get("/db_test/")
async def test_db():
    result = await run_query('SELECT id FROM stg.tbl WHERE id=1')
    return result[0]
"""
