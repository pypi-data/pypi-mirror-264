import json


def json_load(path):
    with open(path, "r", encoding="utf8") as file:
        data_dict = json.load(file)
    return data_dict


def json_dump(path, data_dict):
    with open(path, "w", encoding="utf8") as file:
        json.dump(data_dict, file, indent=2, ensure_ascii=False)
