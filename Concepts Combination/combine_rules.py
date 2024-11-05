from cocos import combine_two
from parse_gtzan import get_rules_list, get_genres_dict
import itertools
from tqdm import tqdm

file = 'music_rules.txt'
if __name__ == '__main__':
    
    rl = get_rules_list(file)
    rd = get_genres_dict(rl)

    k = list(rd.keys())
    h, m = 'pop', k[1]

    combinazioni = list(itertools.permutations(k, 2))
    print(combinazioni,len(combinazioni),len(k))
    
    for h,m in tqdm(combinazioni):
        s = combine_two(rd[h]['r']+rd[h]['t'],rd[m]['r']+rd[m]['t'])

        #print([r for r in zip(s[0], s[1])])


        with open(f'scenarios/{h}_{m}_scenario.txt', 'w') as f:
            f.write(str(s[0])+'\n')
            f.write(str(s[1])+'\n')
            f.write(str(s[2]))
        