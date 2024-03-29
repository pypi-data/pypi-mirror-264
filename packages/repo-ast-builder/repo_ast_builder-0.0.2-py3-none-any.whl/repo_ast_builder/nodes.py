import ast

from .annotation_string import get_annotation_string
from .helper import get_function_params
from .options import INCLUDE_ANY_TYPE


def process_node(node, parent_node, file_path, directory):
    if isinstance(node, ast.FunctionDef):
        process_function_node(node, parent_node, file_path, directory)
    elif isinstance(node, ast.ClassDef):
        process_class_node(node, parent_node, file_path, directory)


def process_function_node(node, parent_node, file_path, directory):
    name = node.name
    info = {
        "relative_path": str(file_path.relative_to(directory)),
        "type": "function",
        "params": get_function_params(node),
    }

    if node.returns:
        info["return_type"] = get_annotation_string(node.returns)
    elif INCLUDE_ANY_TYPE:
        info["return_type"] = "Any"

    handle_children(node, info, file_path, directory)

    parent_node[name] = info


def handle_children(node, info, file_path, directory):
    children_info = {}
    for sub_node in node.body:
        process_node(sub_node, children_info, file_path, directory)
    if len(children_info) > 0:
        info["children"] = children_info


def process_class_node(node, parent_node, file_path, directory):
    class_name = node.name
    info = {
        "relative_path": str(file_path.relative_to(directory)),
        "type": "class",
    }
    handle_children(node, info, file_path, directory)
    parent_node[class_name] = info
