import types


def serialize_function(func):
    #   Serialize the function's code object to dictionary

    serialized_globals = {}
    for name, value in func.__globals__.items():
        if isinstance(value, (int, float, str)):  # primitive globals
            serialized_globals[name] = value
        elif name == func.__name__:  # recursive call will be changed to new instance of function
            serialized_globals[name] = ""
        elif isinstance(value, type) \
                and name in func.__code__.co_names:  # global classes that need to be serialized
            serialized_globals[name] = serialize_class(value)
        elif callable(value) and name in func.__code__.co_names:  # global functions that need to be serialized
            serialized_globals[name] = serialize_function(value)

    serialized_func = {
        '.type': "function",
        'name': func.__name__,  # name of function
        'argcount': func.__code__.co_argcount,  # number of arguments
        'posonlyargcount': func.__code__.co_posonlyargcount,  # number of positional arguments
        'kwonlyargcount': func.__code__.co_kwonlyargcount,  # number of key arguments
        'nlocals': func.__code__.co_nlocals,  # number of locals
        'stacksize': func.__code__.co_stacksize,  # potential used stack size (not useful)
        'flags': func.__code__.co_flags,  # code state flags
        'code': func.__code__.co_code,  # code of function as bytecode
        'consts': func.__code__.co_consts,  # values of consts
        'names': func.__code__.co_names,  # names of globals and attributes in function code (includes functions)
        'varnames': func.__code__.co_varnames,  # names of variables
        'filename': func.__code__.co_filename,  # name of file (not necessary)
        'firstlineno': func.__code__.co_firstlineno,  # position in code (not necessary)
        'lnotab': func.__code__.co_lnotab,  # offset info for bytecode
        'freevars': func.__code__.co_freevars,  # vars used in internal functions
        'cellvars': func.__code__.co_cellvars,  # vars used in internal functions

        'globals': serialized_globals,
        'argdefs': func.__defaults__,
        'closure': func.__closure__
    }

    return serialized_func


def deserialize_function(serialized_func):
    # Deserialize the function's code object from dictionary
    deserialized_code = types.CodeType(
        serialized_func['argcount'],
        serialized_func['posonlyargcount'],
        serialized_func['kwonlyargcount'],
        serialized_func['nlocals'],
        serialized_func['stacksize'],
        serialized_func['flags'],
        serialized_func['code'],
        serialized_func['consts'],
        serialized_func['names'],
        serialized_func['varnames'],
        serialized_func['filename'],
        serialized_func['name'],
        serialized_func['firstlineno'],
        serialized_func['lnotab'],
        serialized_func['freevars'],
        serialized_func['cellvars'],
    )

    recursive = False
    for name, value in serialized_func['globals'].items():  # editing non-primitive globals
        if name == serialized_func['name']:
            recursive = True
        elif not isinstance(value, (int, float, str)):  # deserialization of the rest objects
            if value['.type'] == "function":
                serialized_func['globals'][name] = deserialize_function(value)
            elif value['.type'] == "class":
                serialized_func['globals'][name] = deserialize_class(value)

    deserialized_func = types.FunctionType(
        deserialized_code,
        globals=serialized_func['globals'],
        name=serialized_func['name'],
        argdefs=serialized_func['argdefs'],
        closure=serialized_func['closure']
    )

    if recursive:
        deserialized_func.__globals__[serialized_func['name']] = deserialized_func

    return deserialized_func


def serialize_class(target):
    # Serialize the class object to dictionary

    serialized_attrs = {}         # serialize attributes
    for name, value in target.__dict__.items():
        if isinstance(value, (int, float, str)):
            serialized_attrs[name] = value
        elif isinstance(value, type):               # static class attributes
            serialized_attrs[name] = serialize_class(value)
        elif callable(value):
            serialized_attrs[name] = serialize_function(value)

    serialized_bases = []           # serialize base classes
    for value in target.__bases__:
        if value.__bases__ != ():        # exclude 'object' class
            print("class", value)
            serialized_bases.append(serialize_class(value))

    serialized_class = {
        '.type': "class",
        "name": target.__name__,
        "attrs": serialized_attrs,
        "bases": serialized_bases
    }
    return serialized_class


def deserialize_class(serialized_target):
    # Deserialize the class object from dictionary
    for name, value in serialized_target["attrs"].items():
        if not isinstance(value, (int, float, str)):
            if value['.type'] == "function":
                serialized_target["attrs"][name] = deserialize_function(value)
            elif value['.type'] == "class":
                serialized_target["attrs"][name] = deserialize_class(value)

    for i, value in enumerate(serialized_target["bases"]):
        serialized_target["bases"][i] = deserialize_class(value)

    deserialized_class = type(serialized_target["name"],
                              tuple(serialized_target["bases"]),
                              serialized_target["attrs"])

    return deserialized_class


def serialize_object(obj):
    # Serialize object (as class with data) to dictionary

    serialized_dict = {}
    for name, value in obj.__dict__.items():
        if isinstance(value, (int, float, str)):
            serialized_dict[name] = value
        elif isinstance(value, type):
            serialized_dict[name] = serialize_class(value)
        elif callable(value):
            serialized_dict[name] = serialize_function(value)
        else:
            serialized_dict[name] = serialize_object(value)

    serialized_obj = {
        ".type": 'object',
        "class": serialize_class(type(obj)),
        "dict": serialized_dict
    }
    return serialized_obj


def deserialize_object(serialized_obj):
    # Deserialize object from dictionary

    obj_class = deserialize_class(serialized_obj["class"])
    obj = obj_class.__new__(obj_class)

    for name, value in serialized_obj["dict"].items():
        setattr(obj, name, value)
    return obj
