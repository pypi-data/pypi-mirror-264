import json

from komodo.framework.komodo_tool_registry import KomodoToolRegistry
from komodo.shared.documents.text_extract import to_clean_text


def debug_invoke(call, *, params=None, metadata=None, tools=None):
    message = debug_invoke_internal(call, params=params, metadata=metadata, tools=tools)
    return f"""```debug 
{message}``` 
"""


def debug_invoke_internal(call, *, params=None, metadata=None, tools=None):
    tool = KomodoToolRegistry.find_tool_by_shortcode(call.function.name, tools)
    try:
        arguments = json.loads(call.function.arguments)
        args_display = "\n".join([f"{k}: {to_display(str(arguments[k]))}" for k in arguments.keys()])
    except json.JSONDecodeError:
        args_display = call.function.arguments[:80]

    if not metadata.user.show_tool_progress or metadata.user.show_tool_progress.lower == 'none':
        return ""

    if metadata.user.show_tool_progress == 'details':
        return f"""Invoking {tool.name} with arguments:
{args_display}
"""

    return f"Invoking {tool.name} with arguments: {args_display}\n"


def debug_response(call, *, params=None, metadata=None, tools=None):
    message = debug_response_internal(call, params=params, metadata=metadata, tools=tools)
    return f"""```debug
{message}``` 
"""


def debug_response_internal(output, *, params=None, metadata=None, tools=None):
    tool = KomodoToolRegistry.find_tool_by_shortcode(output['name'], tools)
    contents = output['content']
    contents_display = to_display(contents)

    if not metadata.user.show_tool_progress or metadata.user.show_tool_progress.lower == 'none':
        return ""

    if metadata.user.show_tool_progress == 'details':
        return f"""Received response from {tool.name}.
{contents_display}
"""

    return f"Received response from {tool.name}: {contents_display}\n"


def to_display(contents, width=100, max_lines=5):
    import textwrap
    import re

    updated = ' '.join(contents.split("\n"))
    updated = ' '.join(updated.split("\\n"))
    updated = re.sub(r'\s+', ' ', updated)
    indent = "  "

    wrapped_lines = textwrap.wrap(updated, width=width, subsequent_indent=indent, max_lines=max_lines + 1)
    wrapped_lines = [line[:width + 10] for line in wrapped_lines]  # max 100 chars even w wrapping
    displayed_lines = wrapped_lines[:max_lines]

    if len(wrapped_lines) > max_lines:
        remaining_chars = sum(len(line) for line in wrapped_lines[max_lines:]) + len(
            wrapped_lines) - max_lines - 1  # account for newlines
        displayed_lines.append(indent + "... " + str(remaining_chars) + " more characters")

    display = "\n".join(displayed_lines)
    print(contents)
    print(display)
    return display


if __name__ == "__main__":
    text = """{'contents': 'CHAPTER 1\nInflation: Concepts, Evolution, and Correlates\nIn the
    past four to five decades, inflation has fallen around the world, with
    median\nannual global consumer price inflation down from a peak of 16.6 percent
    in 1974 to\n2.6  percent  in  2017.  This  decline  began  in advanced
    economies  in  the  mid-1980s\nand  in  emerging  market  and  developing"
    CHAPTER 1\nInflation: Concepts, Evolution, and Correlates\nIn the
    past four to five decades, inflation has fallen around the world, with
    median\nannual global consumer price inflation down from a peak of 16.6 percent
    in 1974 to\n2.6  percent  in  2017.  This  decline  began  in advanced
    economies  in  the  mid-1980s\nand  in  emerging  market  and  developing
    """
    d = to_display(text, width=100, max_lines=5)
    print(d)

    print(to_clean_text(d))
