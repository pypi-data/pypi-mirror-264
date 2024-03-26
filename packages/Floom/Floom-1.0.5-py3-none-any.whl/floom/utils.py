from typing import get_origin, get_args, Union, Dict, Any, List, Type


def convert_response(data: Union[Dict[str, Any], List[Dict[str, Any]]], response_type: Union[Type, List[Type]]) -> Union[object, List[object]]:
    # Determine if response_type is a list or a single type
    if get_origin(response_type) is list:
        # Extract the class type from the list
        cls = get_args(response_type)[0]
        if isinstance(data, list):
            return [cls(**item) for item in data]
        else:
            return cls(**data)
    else:
        if isinstance(data, list):
            return [response_type(**item) for item in data]
        else:
            return response_type(**data)