import json
import uuid
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from time import time

from komodo.framework.komodo_tool_registry import KomodoToolRegistry
from komodo.models.framework.chat_metadata import ChatMetaData
from komodo.shared.documents.text_extract import to_clean_text
from komodo.shared.utils.sentry_utils import sentry_trace
from komodo.shared.utils.term_colors import print_info, print_error, print_header, print_gray
from komodo.shared.utils.timebox import time_limit, TimeoutException, time_print_simple

TOOLS_TIMEOUT = 15


@sentry_trace
def process_actions_gpt_preview(tools, run) -> list:
    outputs = get_tools_output_preview(tools, run)
    for output in outputs:
        del output['name']

    print_gray("Outputs: ", json.dumps(outputs, default=vars))
    return outputs


def get_tools_output_preview(tools, run):
    assert run.required_action.type == 'submit_tool_outputs'
    print("Processing actions. Run Id: " + run.id + " Thread Id: " + run.thread_id)
    tool_calls = run.required_action.submit_tool_outputs.tool_calls
    metadata = run.metadata or {}
    print("Metadata: ", json.dumps(metadata, default=vars))
    metadata['run_id'] = run.id
    outputs = get_tools_outputs(tools=tools, metadata=metadata, tool_calls=tool_calls)
    return outputs


@sentry_trace
def process_actions_gpt_legacy_api(tools, metadata, tool_calls) -> list:
    outputs = get_tools_output_legacy(tools, metadata, tool_calls)
    for output in outputs:
        output['role'] = "tool"
        output['content'] = output['output']
        del output['output']

    print_gray("Outputs: ", json.dumps(outputs, default=vars))
    return outputs


@sentry_trace
def process_actions_gpt_streaming(tools, metadata, tool_calls) -> list:
    outputs = get_tools_output_legacy(tools, metadata, tool_calls)
    for output in outputs:
        output['role'] = "function"
        output['content'] = output['output']
        del output['output']

    print_gray("Outputs: ", json.dumps(outputs, default=vars))
    return outputs


def get_tools_output_legacy(tools, metadata, tool_calls):
    outputs = get_tools_outputs(tools=tools, metadata=metadata, tool_calls=tool_calls)
    return outputs


def get_tools_outputs(tools, metadata, tool_calls, timeout=TOOLS_TIMEOUT):
    parallel = len(tool_calls) > 1
    try:
        if parallel:
            return get_tools_outputs_parallel(tools, metadata, tool_calls, timeout)
        else:
            return get_tools_outputs_sequential(tools, metadata, tool_calls)
    except TimeoutError:
        if parallel:
            print("Timed out processing tool calls in parallel, trying sequential execution to collect outputs")
            return get_tools_outputs_sequential(tools, metadata, tool_calls)


@time_print_simple
def get_tools_outputs_sequential(tools, metadata, tool_calls):
    outputs = []
    for call in tool_calls:
        output = process_tool_call(tools, call, metadata)
        outputs.append(output)
    return outputs


@time_print_simple
def get_tools_outputs_parallel(tools, metadata, tool_calls, timeout=TOOLS_TIMEOUT):
    outputs = list()
    start = time()
    with ThreadPoolExecutor() as executor:
        for output in executor.map(process_tool_call, repeat(tools), tool_calls, repeat(metadata), timeout=timeout):
            outputs.append(output)
    finish = time()
    print_gray(f'wall time to execute: {finish - start}')
    return outputs


def process_tool_call_with_time_limit(tools, call, metadata=None, timeout=TOOLS_TIMEOUT):
    # signal approach to timeouot only works in main thread
    if metadata is None:
        metadata = {'run_id': str(uuid.uuid4())}

    try:
        with time_limit(timeout):
            print("Processing tool call: " + call.id)
            result = process_tool_call(tools, call, metadata)
            print("Completed tool call: " + call.id)
            return result
    except TimeoutException:
        print("Timed out processing tool call: " + call.id)
        return json.dumps({"tool_call_id": call.id, "name": call.function.name,
                           "output": "Timed out processing tool call: " + call.id})


def process_tool_call(tools, call, metadata: ChatMetaData):
    print_call_info(call)
    output = generate_tool_output(call.function.name, call.function.arguments, metadata, tools)
    return {"tool_call_id": call.id, "name": call.function.name, "output": output}


def print_call_info(call):
    message = f"Processing tool call: {call.id} Type: {call.type} Function: {call.function.name} Arguments: {call.function.arguments}"
    print_info(message)


def generate_tool_output(shortcode, arguments, metadata, tools):
    tool = KomodoToolRegistry.find_tool_by_shortcode(shortcode, tools)
    if tool:
        print_header("Invoking tool object: " + tool.name)
        try:
            args = json.loads(arguments)
            output = str(tool.action(args))
            output = to_clean_text(output)
        except Exception as e:
            print_error(f"Error invoking tool {shortcode}: {e}")
            output = f"Error invoking tool {shortcode}"
    else:
        print_error(f"Requested tool {shortcode} is not available")
        output = f"Requested tool {shortcode} is not available"

    max_output_len = metadata.max_function_output_len()
    if len(output) > max_output_len:
        output = output[:max_output_len] + " ... (truncated)"
    return output
