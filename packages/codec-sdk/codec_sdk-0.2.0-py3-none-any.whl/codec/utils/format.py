class ResponseObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, dict):
                value = ResponseObject(**value)
            setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        if isinstance(value, dict):
            value = ResponseObject(**value)
        setattr(self, key, value)

    def __delitem__(self, key):
        delattr(self, key)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def json(self):
        d = {}
        for key, value in self.__dict__.items():
            if isinstance(value, ResponseObject):
                d[key] = value.json()
            elif isinstance(value, list):
                list_items = []
                for item in value:
                    if isinstance(item, ResponseObject):
                        list_items.append(item.json())
                    else:
                        list_items.append(item)
                d[key] = list_items
            else:
                d[key] = value
        return d


def format_api_response(data):
    if isinstance(data, dict):
        return ResponseObject(**{k: format_api_response(v) for k, v in data.items()})
    elif isinstance(data, list):
        return [format_api_response(item) for item in data]
    else:
        return data
