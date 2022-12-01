import json, datetime as dt


def get_json(file: str) -> dict:
    with open(file, "r", encoding='utf-8') as f:
        file_content : dict = json.loads(f.read())
    return file_content

def dump_json(file: str, dump_content: dict):
    with open(file, "w+", encoding='utf-8') as f:
        json.dump(obj = dump_content, fp = f, indent = 4)

def log_error(error):
    print(f"\x1b[31m[{dt.datetime.now()}] -- {error}\n\x1b[0m")