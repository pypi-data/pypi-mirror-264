import json

from komodo.framework.komodo_tool_registry import KomodoToolRegistry


def debug_invoke(call, *, params=None, metadata=None, tools=None):
    tool = KomodoToolRegistry.find_tool_by_shortcode(call.function.name, tools)
    try:
        arguments = json.loads(call.function.arguments)
        args_display = "\n".join([f"{k}: {to_display(str(arguments[k]))}" for k in arguments.keys()])
    except json.JSONDecodeError:
        args_display = call.function.arguments[:80]

    if not metadata.user.show_tool_progress or metadata.user.show_tool_progress.lower == 'none':
        return ""

    if metadata.user.show_tool_progress == 'details':
        return f"""
```
Invoking {tool.name} with arguments:
{args_display}
```
"""

    return f"Invoking {tool.name} with arguments: {args_display}\n"


def debug_response(output, *, params=None, metadata=None, tools=None):
    tool = KomodoToolRegistry.find_tool_by_shortcode(output['name'], tools)
    contents = output['content']
    contents_display = to_display(contents)

    if not metadata.user.show_tool_progress or metadata.user.show_tool_progress.lower == 'none':
        return ""

    if metadata.user.show_tool_progress == 'details':
        return f"""
```
Received response from {tool.name}.
{contents_display}
```
"""

    return f"Received response from {tool.name}: {contents_display}\n"


import textwrap


def to_display(contents, n=80, lines=5):
    wrapped_lines = textwrap.wrap(contents, width=n)
    displayed_lines = wrapped_lines[:lines]

    if len(wrapped_lines) > lines:
        remaining_chars = sum(len(line) for line in wrapped_lines[lines:]) + len(
            wrapped_lines) - lines - 1  # account for newlines
        displayed_lines.append("... " + str(remaining_chars) + " more characters")

    return "\n".join(displayed_lines)
