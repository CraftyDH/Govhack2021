#this file might be unecersarry but it gives me peace of mind of mind

import json

def is_object(o):
    return hasattr(o, '__dict__')
    
def convert_data(data):
    if is_object(data): return convert_data(data.__dict__)
    elif type(data) is dict: return {k: convert_data(v) for k, v in data.items()}
    elif type(data) is list or type(data) is tuple: return [convert_data(n) for n in data]
    else: return data

def safe_str(data):
    d = convert_data(data)
    return json.dumps(d)

def safe_dump(data, file):
    return json.dump(convert_data(data), file)