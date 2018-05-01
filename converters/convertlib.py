from collections import OrderedDict
from typing import Dict, List, Union

def is_null(x, key=None) -> bool:
    if key is not None:
        if not isinstance(x, dict) or key not in x:
            return True
        else:
            # actually want to check x[key]
            x = x[key]
    return (x is None or x == "null"
            or (isinstance(x, (list, dict)) and len(x) < 1)
            or x in ["(Information not available)",
                     "no applicable service exists",
                     ])


def ensure_list(x) -> List:
    if isinstance(x, list):
        return x
    return [x]


def simplify_attr_list(data: Union[Dict, List], namekey: str) -> Dict:
    """
    Simplify
        [{namekey: "name1", "attr1": "val1", ...},
         {namekey: "name2", "attr1": "val1", ...}]}
    or, if there's only one,
        {namekey: "name1", "attr1": "val1", ...}
    to
      {"name1": {"attr1": "val1", ...},
       "name2": {"attr1": "val1", ...}}
    """
    new_data = {}
    for d in ensure_list(data):
        new_d = dict(d)
        name = new_d[namekey]
        del new_d[namekey]
        new_data[name] = new_d
    return new_data


def singleton_list_to_value(a_list):
    if len(a_list) == 1:
        return a_list[0]
    return a_list


def expand_attr_list_single(data: Dict, namekey:str, valuekey: str, name_first=True) -> Union[Dict, List]:
    """
    Expand
        {"name1": "val1",
         "name2": "val2"}
    to
        [{namekey: "name1", valuekey: "val1"},
         {namekey: "name2", valuekey: "val2"}]
    or, if there's only one,
        {namekey: "name1", valuekey: "val1"}
    """
    newdata = []
    for name, value in data.items():
        if name_first:
            newdata.append(OrderedDict([(namekey, name), (valuekey, value)]))
        else:
            newdata.append(OrderedDict([(valuekey, value), (namekey, name)]))
    return singleton_list_to_value(newdata)


def expand_attr_list(data: Dict, namekey: str, ordering: Union[List, None]) -> Union[Union[Dict, OrderedDict], List[Union[Dict, OrderedDict]]]:
    """
    Expand
        {"name1": {"attr1": "val1", ...},
         "name2": {"attr1": "val1", ...}}
    to
        [{namekey: "name1", "attr1": "val1", ...},
         {namekey: "name2", "attr1": "val1", ...}]}
    or, if there's only one,
        {namekey: "name1", "attr1": "val1", ...}
    If ``ordering`` is not None, instead of using a dict, use an OrderedDict with the keys in the order provided by
    ``ordering``.
    """
    newdata = []
    for name, value in data.items():
        if ordering:
            new_value = OrderedDict()
            for elem in ordering:
                if elem == namekey:
                    new_value[elem] = name
                elif elem in value:
                    new_value[elem] = value[elem]
                else:
                    new_value[elem] = None
        else:
            new_value = dict(value)
            new_value[namekey] = name
        newdata.append(new_value)
    return singleton_list_to_value(newdata)