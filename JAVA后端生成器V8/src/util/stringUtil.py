import re


def low_str_first(string: str) -> str:
    if string is None or len(string) < 1:
        return ""
    if len(string) == 1:
        return string.lower()
    f1 = string[0].lower()
    f2 = string[1:]
    return f1 + f2


def upper_str_first(string: str) -> str:
    if string is None or len(string) < 1:
        return ""
    if len(string) == 1:
        return string.upper()
    f1 = string[0].upper()
    f2 = string[1:]
    return f1 + f2


def get_java_type(type_str) -> str:
    if "int" in type_str:
        return "Integer"
    if "date" in type_str:
        return "Date"
    if "time" in type_str:
        return "Date"
    if "float" in type_str:
        return "Double"
    if "double" in type_str:
        return "Double"
    return "String"


def underscore_to_small_hump(name: str) -> str:
    name = name.strip("_")
    new_str = ""
    first = True
    for i in name.split("_"):
        if first:
            new_str += low_str_first(i)
            first = False
        else:
            new_str += upper_str_first(i)
    return new_str


def underscore_to_big_hump(name: str) -> str:
    name = name.strip("_")
    new_str = ""
    for i in name.split("_"):
        new_str += upper_str_first(i)
    return new_str


def hump_to_underscore(name: str) -> str:
    new_str = ""
    first = False
    for i in name:
        if re.match("[A-Z]", i) and first:
            new_str += "_"
        new_str += low_str_first(i)
        first = True
    return new_str


def remove_prefix(string: str, prefix: str) -> str:
    if prefix == string[:len(prefix)]:
        string = string[len(prefix):]
    return string


def remove_prefix_not_case(string: str, prefix: str) -> str:
    if prefix.lower() == string[:len(prefix)].lower():
        string = string[len(prefix):]
    return string


def equal_str_tail(string: str, prefix) -> bool:
    s_len, p_len = len(string), len(prefix)
    if s_len == 0 or p_len == 0 or p_len > s_len:
        return False
    return prefix == string[s_len - p_len:]


def equal_str_tail_not_case(string: str, prefix) -> bool:
    string, prefix = string.lower(), prefix.lower()
    return equal_str_tail(string, prefix)
