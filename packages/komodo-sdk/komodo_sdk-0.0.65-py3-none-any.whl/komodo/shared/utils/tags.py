import re


def with_tag(message, tag="debug"):
    return f"<{tag}>{message}</{tag}>" if message else ""


def remove_tag(input_string, tag="debug"):
    # Define regex pattern to match <debug>...</debug> content
    pattern = rf'<{tag}>.*?</{tag}>'
    # Use re.sub to replace matched patterns with an empty string
    output_string = re.sub(pattern, '', input_string)
    output_string = ' '.join(output_string.split())
    return output_string


def remove_triple_quotes(input_string, tag="debug"):
    # Define regex pattern to match <debug>...</debug> content
    pattern = rf'```{tag}.*?```'
    # Use re.sub to replace matched patterns with an empty string
    output_string = re.sub(pattern, '', input_string)
    output_string = ' '.join(output_string.split())
    return output_string


if __name__ == "__main__":
    # Test the add_tags function
    message = "This is a test message"
    tagged_message = with_tag(message)
    print(tagged_message)

    # Test the remove_tags function
    input_string = "This is a <debug>debug</debug> string with <debug>some debug content</debug>."
    output_string = remove_tag(input_string)
    print(output_string)

    # Test the remove_quotes function
    input_string = "This is a ```debug string``` with ```debugsome debug content```."
    output_string = remove_triple_quotes(input_string)
    print(output_string)
