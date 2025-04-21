from pydantic_ai import Agent
from pydantic_ai.messages import (
    AgentStreamEvent,
    FinalResultEvent,
    FunctionToolCallEvent,
    FunctionToolResultEvent,
    PartDeltaEvent,
    PartStartEvent,
    TextPartDelta,
    ToolCallPartDelta,
    ToolCallPart
)
from pydantic import BaseModel
from enum import Enum
from typing import AsyncIterator


class EventType(str, Enum):
    DISPLAY = "display"
    DEBUG = "debug"


class StreamEvent(BaseModel):
    event_type: EventType
    content: str

    def is_display(self) -> bool:
        return self.event_type == EventType.DISPLAY


def build_display_event(content: str) -> StreamEvent:
    """
    Build a display event from the provided content.

    Args:
        content (str): The content to include in the display event.

    Returns:
        StreamEvent: A validated event with display type and the provided content.
    """
    return StreamEvent(
        event_type=EventType.DISPLAY,
        content=content
    )


def build_debug_event(event: AgentStreamEvent) -> StreamEvent:
    """
    Build a debug event from an AgentStreamEvent.

    Args:
        event (AgentStreamEvent): The event to build the debug event from.

    Returns:
        StreamEvent: A validated event with debug type and the event details.
    """
    return StreamEvent(
        event_type=EventType.DEBUG,
        content=f'{type(event)}: {event}'
    )


def parse_event(event: AgentStreamEvent) -> StreamEvent:
    """
    Parse an AgentStreamEvent and return a StreamEvent.

    Args:
        event (AgentStreamEvent): The event to parse.

    Returns:
        StreamEvent: A validated event with display type and the provided content.
    """
    
    # Content we care about printing
    if isinstance(event, PartStartEvent) and hasattr(event.part, 'content'):
        return build_display_event(event.part.content)
    
    elif isinstance(event, PartDeltaEvent) and hasattr(event, 'delta') and isinstance(event.delta, TextPartDelta):
        return build_display_event(event.delta.content_delta)
    
    # Debug only (tool calls/results)
    elif isinstance(event, PartStartEvent) and isinstance(event.part, ToolCallPart):
        return build_debug_event(event)
    elif isinstance(event, PartDeltaEvent) and isinstance(event.delta, ToolCallPartDelta):
        return build_debug_event(event)
    elif isinstance(event, FinalResultEvent):
        return build_debug_event(event)
    elif isinstance(event, FunctionToolCallEvent):
        return build_debug_event(event)
    elif isinstance(event, FunctionToolResultEvent):
        return build_debug_event(event)
    else:
        return StreamEvent(
            event_type=EventType.DEBUG,
            content=f'UNKNOWN {type(event)}: {event}'
        )


async def handle_stream_events(stream: AsyncIterator[AgentStreamEvent], debug_messages: list[str]) -> AsyncIterator[str]:
    """
    Process stream events and handle display/debug routing.
    
    Args:
        stream: The event stream to process, yields AgentStreamEvent objects.
        debug_messages: List to collect debug messages. Modified in place.
        
    Yields:
        str: Content from display events
    """
    async for event in stream:
        parsed_event = parse_event(event)
        if parsed_event.is_display():
            yield parsed_event.content
        else:
            debug_messages.append(parsed_event.content)


async def main_stream(agent: Agent, user_prompt: str) -> AsyncIterator[str]:
    """
    Main function to handle the streaming of events from the agent based on the user prompt.

    This function manages the streaming of different types of nodes (user prompt, model request, tool calls, etc.)
    and processes the events generated during the stream. It yields the content of display events and collects
    debug messages for other types of events.

    Args:
        agent (Agent): The agent responsible for handling the user prompt and generating events.
        user_prompt (str): The user prompt to be processed by the agent.

    Yields:
        str: The content of display events generated during the stream.

    Collects:
        list: A list of debug messages generated during the stream and prints at the end.
    """
    debug_messages = []
    content_streamed = False
    async with agent.run_mcp_servers():
        async with agent.iter(user_prompt) as run:
            async for node in run:
                if Agent.is_user_prompt_node(node):
                    debug_messages.append(f'UserPromptNode: {node.user_prompt}')
                elif Agent.is_model_request_node(node):
                    debug_messages.append(f'ModelRequestNode: streaming partial request tokens')
                    async with node.stream(run.ctx) as request_stream:
                        async for content in handle_stream_events(request_stream, debug_messages):
                            if content:
                                content_streamed = True
                                yield content
                elif Agent.is_call_tools_node(node):
                    debug_messages.append(f'ToolCallNode: streaming tool calls and results (debug only)')
                    async with node.stream(run.ctx) as tool_request_stream:
                        async for _ in handle_stream_events(tool_request_stream, debug_messages):
                            pass
                elif Agent.is_end_node(node):
                    if content_streamed:
                        debug_messages.append(f'end_node: {run.result.data}')
                    else:
                        yield run.result.data
                else:
                    debug_messages.append(f'Unknown Node: {type(node)}: {node}')
                    
        print('\n\n\nDebug:')
        print('\n'.join(debug_messages))
        
