from .annotation_string import get_annotation_string
from .options import INCLUDE_ANY_TYPE


def get_function_params(node):
    function_params = []
    for arg in node.args.args:
        function_param = {"name": arg.arg }
        if arg.annotation:
            function_param["type"] = get_annotation_string(arg.annotation)
        elif INCLUDE_ANY_TYPE:
            function_param["type"] = "Any"

        function_params.append(function_param)

    return function_params
