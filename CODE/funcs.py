# Shared Arguments
SHARED_ARGS = ("allowed_stages", "color", "sound", "art_object","containers")

def block_maker(block_data):
    """
    Creates a YAML-compatible block from a dictionary of key-value pairs.

    Args:
        block_data (dict): A dictionary containing key-value pairs where keys are argument names 
                          and values are the corresponding values. Empty or None values are excluded.

    Returns:
        str: A formatted YAML block as a string with non-empty key-value pairs.
    """
    filtered_block = {key: value for key, value in block_data.items() if value or value == 0}
    block = "\n".join([f"{key}: {value}" for key, value in filtered_block.items()])
    return block.strip()

def block_auto_maker(kwargs):
    """
    Automatically creates a block dictionary from function inputs (passed as kwargs) 
    and processes it using block_maker.

    Args:
        kwargs (dict): All function inputs captured as key-value pairs.

    Returns:
        str: A formatted YAML block as a string with non-empty key-value pairs.
    """
    kwargs.pop('self', None)
    return block_maker(kwargs)

def merge_shared_args(base_args, kwargs):
    """
    Helper function to merge shared arguments into the main arguments.

    Args:
        base_args (dict): Main block arguments.
        kwargs (dict): Additional arguments passed to the block function.

    Returns:
        dict: Merged dictionary of arguments.
    """
    for arg in SHARED_ARGS:
        if arg in kwargs:
            base_args[arg] = kwargs[arg]
    return base_args

def timeModulator_node(FormEditorID="", magnitude="", **kwargs):
    """
    Creates a timeModulator block.

    Args:
        FormEditorID (str): The identifier for the form editor.
        magnitude (str): The magnitude value for the time modulation.
        **kwargs: Additional shared arguments such as 'allowed_stages', 'color', 'sound', and 'art_object'.

    Returns:
        str: A formatted YAML block for a timeModulator.
    """

    # if FormEditorID or magnitude is not provided, return an empty string
    if not FormEditorID or not magnitude:
        return ""

    block_args = {"FormEditorID": FormEditorID, "magnitude": magnitude}
    block_args = merge_shared_args(block_args, kwargs)
    return block_auto_maker(block_args)

def transformer_node(FormEditorID="", finalFormEditorID="", duration="", **kwargs):
    """
    Creates a transformer block.

    Args:
        FormEditorID (str): The identifier for the form editor.
        finalFormEditorID (str): The identifier for the final form editor.
        duration (str): The duration value for the transformation.
        **kwargs: Additional shared arguments such as 'allowed_stages', 'color', 'sound', 'art_object', 'containers'.

    Returns:
        str: A formatted YAML block for a transformer.
    """

    # if FormEditorID, finalFormEditorID, or duration is not provided, return an empty string
    if not FormEditorID or not finalFormEditorID or not duration:
        return ""

    block_args = {
        "FormEditorID": FormEditorID,
        "finalFormEditorID": finalFormEditorID,
        "duration": duration
    }
    block_args = merge_shared_args(block_args, kwargs)
    return block_auto_maker(block_args)

def owner_block(owner_title, owners):
    """
    Creates a block for owners with a title.

    Args:
        owner_title (str): Title of the owner block.
        owners (str): List or string of owner identifiers.

    Returns:
        str: A formatted YAML block for owners.
    """
    block = f"""
{owner_title}: {owners}
"""
    return block.strip()

def concatenate_nodes(*nodes,start="- "):
    """
    Concatenates multiple YAML nodes into a list format with proper indentation.

    Args:
        *nodes: Variable number of YAML node strings to concatenate.

    Returns:
        str: A concatenated YAML list block.

    Raises:
        ValueError: If any of the provided nodes are not strings.
    """
    wrapped_block = ""
    for i, node in enumerate(nodes):
        if not isinstance(node, str):
            raise ValueError(f"Invalid input: node {i} is not a string.")
        if i == 0:
            wrapped_block += f"{start}{node.replace('\n', '\n  ')}"
        else:
            wrapped_block += f"\n{start}{node.replace('\n', '\n  ')}"
    return wrapped_block

def block_wrapper(parent_block, child_blocks,start="- "):
    """
    Wraps child blocks under a parent block with proper YAML formatting.

    Args:
        parent_block (str): The parent block string.
        child_blocks (dict): A dictionary of titles and corresponding YAML child blocks.

    Returns:
        str: A formatted YAML block containing nested child blocks.
    """
    wrapped_block = f"{start}{parent_block}"
    for title, child_block in child_blocks.items():
        wrapped_block += f"\n{title}:\n  {child_block.replace('\n', '\n  ')}"
    return wrapped_block.strip()

def make_addon(forms_block, timeModulators, transformers):
    """
    Combines forms, timeModulators, and transformers into a complete YAML addon block.

    Args:
        forms_block (str): The forms block content.
        timeModulators (str): The timeModulators block content.
        transformers (str): The transformers block content.

    Returns:
        str: A fully formatted YAML addon block.
    """
    child_blocks = {
        'timeModulators': timeModulators,
        'transformers': transformers
    }
    wrapped_timeModulators_block = block_wrapper(forms_block, child_blocks)
    wrapped_block = f"formsLists:"
    wrapped_block += f"\n{wrapped_timeModulators_block.replace('\n', '\n  ')}"
    return wrapped_block.strip()

def add_comment_to_keys(block: str, comments: dict):
    """
    Adds comments to specified keys in a YAML block.

    Args:
        block (str): The original YAML block as a string.
        comments (dict): A dictionary mapping keys to their comments.

    Returns:
        str: The updated YAML block with comments added above specified keys.
    """
    lines = block.split("\n")
    updated_lines = []

    for line in lines:
        key = line.split(":")[0].strip()
        if key in comments:
            updated_lines.append(f"{line} # {comments[key]}")
        else: updated_lines.append(line)

    return "\n".join(updated_lines)