import json

def readtext(file):
    with open(file, 'r', encoding='utf-8') as f:
        return f.read()

def savefile(file, info):
    with open(file, 'w') as f:
        json.dump(info, f)

def readfile(file):
    with open(file, 'r') as f:
        return json.load(f)

def save(**args):
    for k, v in args.items():
        savefile(str(k) + '.json', v)

def read(*args):
    return tuple(map(readfile, args))