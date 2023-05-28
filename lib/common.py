import json

def write_result(filename,ans,fr,strain,stress):
    w = {
        "U":ans,
        "Fr":fr,
        "strain":strain,
        "stress":stress
    }
    with open(filename,"w") as f:
        json.dump(w,f)

def load_result(filename):
    with open(filename,"w") as f:
        r = json.load(f)
    return r["U"],r["Fr"],r["strain"],r["stress"]

def load_input(filename):
    with open(filename,"r") as f:
        r = json.load(f)
    return r

def write_input(filename,d):
    with open(filename,"w") as f:
        json.dump(d,f)