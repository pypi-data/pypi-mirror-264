from komodo.framework.komodo_tool_registry import KomodoToolRegistry


def debug_invoke(call, *, params=None, metadata=None, tools=None):
    tool = KomodoToolRegistry.find_tool_by_shortcode(call.function.name, tools)
    arguments = call.function.arguments
    if not metadata.user.show_tool_progress or metadata.user.show_tool_progress.lower == 'none':
        return ""

    if metadata.user.show_tool_progress == 'details':
        return f"""
```
Invoking {tool.name} with arguments: {arguments}
```
"""

    return f"Invoking {tool.name} with arguments: {arguments}\n"


def debug_response(output, *, params=None, metadata=None, tools=None):
    tool = KomodoToolRegistry.find_tool_by_shortcode(output['name'], tools)
    contents = output['content']
    if len(contents) > 100:
        contents = contents[:300] + "..."

    if not metadata.user.show_tool_progress or metadata.user.show_tool_progress.lower == 'none':
        return ""

    if metadata.user.show_tool_progress == 'details':
        return f"""
```
Received response from {tool.name}.
```
"""

    return f"Received response from {tool.name}: {contents}\n"
