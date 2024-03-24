import openai

from komodo.models.framework.model_request import ModelRequest
from komodo.models.framework.models import OPENAI_GPT4_MODEL
from komodo.models.openai.openai_api_streamed_tool_call import StreamingToolCallBuilder
from komodo.models.openai.openai_completion import openai_client
from komodo.models.openai.openai_process_actions import process_actions_gpt_streaming
from komodo.shared.utils.sentry_utils import sentry_trace


def openai_chat_response_streamed(request: ModelRequest):
    client = openai_client()
    model = request.agent.model
    metadata = request.prepare_metadata()
    params = request.build_openai_params(stream=True)
    tools = request.agent.tools

    try:
        for token in openai_invoke_streamed(client, request.prompt, params=params, metadata=metadata, tools=tools):
            yield token

    except openai.BadRequestError as e:
        if e.code == "context_length_exceeded" and model != OPENAI_GPT4_MODEL:
            metadata.model = OPENAI_GPT4_MODEL
            params['model'] = OPENAI_GPT4_MODEL
            for token in openai_invoke_streamed(client, request.prompt, params=params, metadata=metadata, tools=tools):
                yield token
        else:
            raise e

    except Exception as e:
        print(e)
        yield "Encountered error retrieving results: " + str(e)


@sentry_trace
def openai_invoke_streamed(client, prompt, *, params=None, metadata=None, tools=None):
    messages = params['messages'] if 'messages' in params else []
    messages.append({'role': 'user', "content": prompt})

    done = False
    depth = 0
    while not done and depth < 5:
        completion = client.chat.completions.create(**params)
        streamed_role = None
        tool_call_builder = StreamingToolCallBuilder()
        for chunk in completion:
            delta = chunk.choices[0].delta
            if delta is not None:
                if delta.role is not None and delta.role != streamed_role:
                    streamed_role = delta.role
                if delta.content is not None:
                    yield delta.content
                if delta.tool_calls is not None:
                    tool_call_builder.process(delta.tool_calls)

        tool_calls = tool_call_builder.get_tool_calls()
        if tool_calls:
            outputs = process_actions_gpt_streaming(tools, metadata, tool_calls)
            for output in outputs:
                messages.append(output)

            params['messages'] = messages
            depth += 1
        else:
            done = True
