from komodo.models.framework.chat_message import ChatMessage
from komodo.models.framework.model_request import ModelRequest
from komodo.models.framework.model_response import ModelResponse
from komodo.models.openai.openai_completion import openai_client
from komodo.models.openai.openai_process_actions import process_actions_gpt_legacy_api


def openai_chat_response(request: ModelRequest) -> ModelResponse:
    return openai_chat_response_with_client(openai_client(), request)


def openai_chat_response_with_client(client, request: ModelRequest) -> ModelResponse:
    metadata = request.prepare_metadata()
    params = request.build_openai_params(stream=False)
    tools = request.agent.tools
    return openai_invoke(client, request.prompt, params=params, tools=tools, metadata=metadata)


def openai_invoke(client, prompt, *, tools=None, params=None, metadata=None) -> ModelResponse:
    messages = params['messages'] if 'messages' in params else []
    messages.append(ChatMessage(prompt, role='user'))

    done = False
    depth = 0
    while not done and depth < 5:
        completion = client.chat.completions.create(**params)
        response_message = completion.choices[0].message

        tool_calls = response_message.tool_calls
        if tool_calls:
            outputs = process_actions_gpt_legacy_api(tools, metadata, tool_calls)
            messages.append(response_message)
            for output in outputs:
                messages.append(output)

            depth += 1
        else:
            text = completion.choices[0].message.content
            status = completion.choices[0].finish_reason
            return ModelResponse(model=params['model'], status=status, output=completion, text=text)

    return ModelResponse(model=params['model'], status="error", output=None,
                         text="Error: max depth of tool calls reached")
