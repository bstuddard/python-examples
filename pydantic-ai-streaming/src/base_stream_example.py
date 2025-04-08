import os
from typing import AsyncGenerator
from anthropic import AsyncAnthropic

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')


def build_anthropic_message_input(chat_input_list: list) -> list:
    """Builds anthropic message input.

    Args:
        chat_input_list (list): List of chat inputs to send to the API.

    Returns:
        list: List of anthropic message input.
    """
    message_input = []
    for chat_instance in chat_input_list:        
        message_input.append({
            'role': chat_instance['role'], 
            "content": [
                {
                    "type": "text",
                    "text": chat_instance['message']
                }
            ]
        })
    return message_input


async def anthropic_stream_api_call(chat_input_list: list) -> AsyncGenerator[str, None]:
    """Streams anthropic response.

    Args:
        chat_input_list (list): List of chat inputs to send to the API.

    Yields:
        AsyncGenerator[str, None]: Stream of anthropic response.
    """

    # Build message list
    message_input = build_anthropic_message_input(chat_input_list=chat_input_list)

    # Setup and make api call.
    client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    stream = await client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        temperature=0.2,
        system='You are a helpful assistant that can answer questions and help with tasks.',
        messages=message_input,
        stream=True
    )

    async for event in stream:
        if event.type in ['message_start', 'message_delta', 'message_stop', 'content_block_start', 'content_block_stop']:
            pass
        elif event.type == 'content_block_delta':
            yield event.delta.text
        else:
            yield event.type


async def anthropic_full_api_call(chat_input_list: list, system_prompt: str) -> str:
    """
    Makes a non-streaming call to the Anthropic API and returns the full response.
    
    Args:
        chat_input_list (list): List of chat inputs containing role and message
        system_prompt (str): System prompt to use for the API call
    
    Returns:
        str: Complete response from the API
    """
    message_input = build_anthropic_message_input(chat_input_list)
    
    client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    message = await client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=4096,
        temperature=0.2,
        system=system_prompt,
        messages=message_input
    )

    # Extract and return the full response text
    output_text = message.content[0].text
    return str(output_text)