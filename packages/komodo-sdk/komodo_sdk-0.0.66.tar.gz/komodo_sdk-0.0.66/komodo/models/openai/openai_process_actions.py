import json
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from time import time

from komodo.framework.komodo_tool_registry import KomodoToolRegistry
from komodo.models.framework.chat_metadata import ChatMetaData
from komodo.shared.documents.text_extract import to_clean_text
from komodo.shared.utils.sentry_utils import sentry_trace
from komodo.shared.utils.term_colors import print_info, print_error, print_header, print_gray, print_warning
from komodo.shared.utils.timebox import time_print_simple, time_print

TOOLS_TIMEOUT = 60


@sentry_trace
def process_actions_gpt_legacy_api(tools, metadata, tool_calls) -> list:
    outputs = get_tools_outputs(tools, metadata, tool_calls)
    for output in outputs:
        output['role'] = "tool"
        output['content'] = output['output']
        del output['output']

    print_gray("Outputs: ", json.dumps(outputs, default=vars))
    return outputs


@sentry_trace
def process_actions_gpt_streaming(tools, metadata, tool_calls) -> list:
    outputs = get_tools_outputs(tools, metadata, tool_calls)
    for output in outputs:
        output['role'] = "function"
        output['content'] = output['output']
        del output['output']

    print_gray("Outputs: ", json.dumps(outputs, default=vars))
    return outputs


def get_tools_outputs(tools, metadata, tool_calls, timeout=TOOLS_TIMEOUT):
    parallel = len(tool_calls) > 1
    start = time()
    try:
        if parallel:
            return get_tools_outputs_parallel(tools, metadata, tool_calls, timeout)
        else:
            return get_tools_outputs_sequential(tools, metadata, tool_calls)
    except TimeoutError:
        if parallel:
            print_gray(f'timeout: {timeout} waiting time: {time() - start}')
            print_warning("Timed out parallel, trying sequential execution...")
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
    with ThreadPoolExecutor() as executor:
        for output in executor.map(process_tool_call, repeat(tools), tool_calls, repeat(metadata), timeout=timeout):
            outputs.append(output)
    return outputs


def process_tool_call(tools, call, metadata: ChatMetaData):
    message = f"Processing tool call: {call.id} Type: {call.type} Function: {call.function.name} Arguments: {call.function.arguments}"
    print_info(message)
    shortcode = call.function.name
    arguments = call.function.arguments
    tool = KomodoToolRegistry.find_tool_by_shortcode(shortcode, tools)
    output = generate_tool_output(shortcode, tool, arguments, metadata)
    return {"tool_call_id": call.id, "name": shortcode, "output": output}


@time_print
def generate_tool_output(shortcode, tool, arguments, metadata):
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
