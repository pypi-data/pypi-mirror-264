import ast


def get_annotation_string(annotation):
    annotation_map = {
        ast.Name: lambda a: a.id,
        ast.Subscript: lambda a: f"{get_annotation_string(a.value)}[{get_annotation_string(a.slice)}]",
        ast.Tuple: lambda a: f"({', '.join([get_annotation_string(elt) for elt in a.elts])})",
        ast.Attribute: lambda a: f"{get_annotation_string(a.value)}.{a.attr}",
        ast.List: lambda a: f"List[{get_annotation_string(a.elts[0]) if a.elts else 'Any'}]",
        ast.Dict: lambda a: f"Dict[{get_annotation_string(a.keys[0]) if a.keys else 'Any'}, {get_annotation_string(a.values[0]) if a.values else 'Any'}]",
        ast.Constant: lambda a: str(a.value)
    }
    return annotation_map.get(type(annotation), lambda a: "Any")(annotation)
