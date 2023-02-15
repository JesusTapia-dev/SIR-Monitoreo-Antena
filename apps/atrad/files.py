import json

def read_json_file(fp):
    
    kwargs = {}
    
    json_data = fp
    data = json.load(json_data)
    json_data.close()
    
    topic = data["topic"][0][1]
    
    kwargs['topic'] = topic
    
    return kwargs


def write_json_file(filename):
    pass