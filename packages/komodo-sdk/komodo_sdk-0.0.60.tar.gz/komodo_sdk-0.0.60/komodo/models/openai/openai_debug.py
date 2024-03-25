import json

from komodo.framework.komodo_tool_registry import KomodoToolRegistry


def debug_invoke(call, *, params=None, metadata=None, tools=None):
    tool = KomodoToolRegistry.find_tool_by_shortcode(call.function.name, tools)
    try:
        arguments = json.loads(call.function.arguments)
        args_display = "\n".join([f"{k}: {str(arguments[k])[:80]}" for k in arguments.keys()])
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
    if len(contents) >= 400:
        contents = contents[:396] + "..."

    # split contents into strings of lenth 80
    contents_display = "\n".join([contents[i:i + 80] for i in range(0, len(contents), 80)])

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
