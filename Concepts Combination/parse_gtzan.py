from prop import Prop, TProp
from pprint import pprint

file = './music_rules.txt'

def get_rules_list(file):
    lines = []
    with open(file,'r') as f:
        lines = f.readlines()

    rules = [l.strip() for l in lines if l.startswith("Rule") and not "IF" in l]
    result = []
    for r in rules:
        r = r.split(': ')[1:]
        r = r[0].split('->') + r[1:]
        r = [x.strip() if not x.startswith("T(") else x[2:-2].strip() for x in r ]
        r = Prop(*r) if len(r) == 2 else TProp(*r)
        result.append(r)

    return result

def get_genres_dict(rules):
    genres = {}
    for r in rules:
        if r.label not in genres.keys():
            genres[r.label] = {'t':[], 'r':[]}
        if r.is_t():
            genres[r.label]['t'].append(r)
        else:
            genres[r.label]['r'].append(r)
    
    return genres

if __name__ == '__main__':
    rl = get_rules_list(file)
    rd = get_genres_dict(rl)
    pprint(rd)
