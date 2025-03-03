import os
import json
from typing import AsyncGenerator
from anthropic import AsyncAnthropic

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')


async def test_anthropic_stream_api_call(user_prompt_text) -> AsyncGenerator[str, None]:
    system_prompt_text = 'You are an AI agent.' # Change here as needed or do something like await get_system_prompt() if dynamic

    # Setup and make api call.
    client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    stream = await client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=2000,
        system=system_prompt_text,
        messages=[
            {
                "role": "user", 
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt_text
                    }
                ]
            }
        ],
        stream=True
    )

    async for event in stream:
        if event.type in ['message_start', 'message_delta', 'message_stop', 'content_block_start', 'content_block_stop']:
            pass
        elif event.type == 'content_block_delta':
            yield event.delta.text
        else:
            yield event.type

