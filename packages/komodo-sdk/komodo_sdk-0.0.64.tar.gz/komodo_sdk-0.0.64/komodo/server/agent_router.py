import asyncio
import base64
from typing import AsyncGenerator

from fastapi import Depends, APIRouter, HTTPException, Body
from starlette.responses import StreamingResponse

from komodo.models.framework.appliance_runtime import ApplianceRuntime
from komodo.models.framework.chat_message import ChatMessage
from komodo.models.framework.runner_factory import RunnerFactory
from komodo.server.globals import get_appliance, get_email_from_header
from komodo.store.conversations_store import ConversationStore

router = APIRouter(
    prefix='/api/v1/agent',
    tags=['Agent']
)


@router.get('/conversations/{agent_shortcode}')
async def get_conversations(agent_shortcode, email=Depends(get_email_from_header)):
    conversation_store = ConversationStore()
    conversations = conversation_store.get_conversation_headers(email, agent_shortcode)
    return conversations


@router.post('/ask/{agent_shortcode}')
async def ask_agent(agent_shortcode, message=Body(), guid=Body(),
                    email=Depends(get_email_from_header), appliance=Depends(get_appliance)):
    # Get Agent Info based on short code
    runtime = ApplianceRuntime(appliance)
    agent = runtime.get_agent(agent_shortcode)
    if agent is None:
        raise HTTPException(status_code=400, detail=f"Agent {agent_shortcode} is not available")

    store = ConversationStore()
    conversation = store.get_or_create_conversation(guid, agent_shortcode, email, message)

    messages = store.get_messages(conversation.guid)
    history = ChatMessage.convert_from_proto_messages(messages)

    store.add_user_message(guid=conversation.guid, sender=email, text=message)

    try:
        user = runtime.get_user(email)
        runner = RunnerFactory.create_runner(agent, user=user)
        reply = runner.run(message, history=history)
        store.add_agent_message(guid=conversation.guid, sender=agent_shortcode, text=reply.text)
        return {"reply": reply.text, "message": message}
    except Exception as e:
        print("Error while asking agent: ", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ask-streamed")
async def ask_agent_streamed(email: str, agent_shortcode: str, prompt: str, guid: str = None,
                             appliance=Depends(get_appliance)):
    print("email: ", email, "agent_shortcode: ", agent_shortcode, "prompt: ", prompt)

    # Get Agent Info based on short code
    runtime = ApplianceRuntime(appliance)
    agent = runtime.get_agent(agent_shortcode)
    if agent is None:
        raise HTTPException(status_code=400, detail="Respective Agent is not available")

    store = ConversationStore()
    conversation = store.get_or_create_conversation(guid, agent_shortcode, email, prompt)
    messages = store.get_messages(conversation.guid)
    history = ChatMessage.convert_from_proto_messages(messages)

    store.add_user_message(guid=conversation.guid, sender=email, text=prompt)

    def stream_callback():
        try:
            user = runtime.get_user(email)
            runner = RunnerFactory.create_runner(agent, user=user)
            return runner.run_streamed(prompt, history=history)
        except Exception as e:
            print("Error while asking agent: ", e)
            raise HTTPException(status_code=500, detail=str(e))

    def store_callback(reply):
        store.add_agent_message(conversation.guid, sender=agent_shortcode, text=reply)

    return StreamingResponse(komodo_async_generator(stream_callback, store_callback),
                             media_type='text/event-stream')


async def komodo_async_generator(stream_callback, store_callback) -> AsyncGenerator[str, None]:
    reply = ""
    exception_occurred = False  # Flag to indicate an exception occurred during yield
    exception_message = ""  # To store the exception message
    for part in stream_callback():
        reply += part
        if exception_occurred:
            break  # Stop processing if an exception has occurred

        try:
            encoded = base64.b64encode(part.encode('utf-8')).decode('utf-8')
            yield f"data: {encoded}\n\n"
            await asyncio.sleep(0)

        except Exception as e:
            exception_occurred = True
            exception_message = str(e)

    store_callback(reply)

    if exception_occurred:
        print("Error while streaming: " + exception_message)
    else:
        print("stream complete")
        yield "event: stream-complete\ndata: {}\n\n"
