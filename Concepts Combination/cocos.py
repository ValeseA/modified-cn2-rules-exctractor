
from prop import Prop, TProp
import itertools
import numpy as np
from manage_ontology import ManageOntology


def conflicts(cx : list[Prop], cy: list[Prop]):
    confl = {r.var : r for r in cx}
    confl = {r.var : [confl[r.var],r] for r in cy if r.var in confl}

    for _,[rx,ry] in confl.items() :
        m = ry if not ry.head else rx
        h = rx if rx.head else ry
        if h.is_t() and m.is_t():
            #unify t values?
            if h.val == m.val:
                h.t_val = (h.t_val + m.t_val) / 2

            m.always_off = True
            
        elif (not h.is_t()) and (not m.is_t()):
            if h.val == m.val:
                m.always_off = True
            else:
                raise Exception(f"Can't combine the concepts. \nTwo rigid properties in conflict: < {h} > and < {m} >")
        else:
            if h.is_t():
                h.always_off = True
            else: m.always_off = True

def calc_prob(s,sp_t):
    # somma probabilistica limitata
    # o altre...
    # somma
    return sum([sp_t[i].t_val for i in range(len(s)) if s[i]])

def create_scenarios(cx, cy, max_prop = -1):
    sp_t,sp_r = [],[]
    for r in cx+cy:
        if not r.is_always_off():
            if r.is_t(): sp_t.append(r)
            else: sp_r.append(r)
    scenarios = list(map(list, itertools.product([0, 1], repeat=len(sp_t))))
    for s in scenarios[::-1]:
        if max_prop != -1 and sum(s) + len(sp_r) > max_prop:
            scenarios.remove(s)
        p = calc_prob(s,sp_t)
        s.append(p)
    scenarios = sorted(scenarios, key=lambda x: x[-1], reverse=True)
    #print(scenarios)
    return scenarios, sp_t, sp_r



def combine_two(cx,cy):
    #print(cx,cy)
    for c in cx: c.head = True
    for c in cy: c.head = False
    conflicts(cx,cy)
    s, sp_t, sp_r = create_scenarios(cx,cy,len(cx))
    # Check Consistency
    #onto = ManageOntology(s,sp_r,sp_t)
    for scenario in s:
        onto = ManageOntology(scenario,sp_r,sp_t)
        if (onto.check_consistency()):

            print('OK!')
            print(f'{scenario},{sp_t},{sp_r}')
            return scenario, sp_t, sp_r
            break
        else:
            print('NO')

if __name__ == '__main__':
    h = []
    h.append(Prop('head','a == 10'))
    h.append(Prop('head','b == 5'))
    h.append(TProp('head','c == 10',0.8))
    h.append(TProp('head','d == 5',0.7))
    h.append(TProp('head','e == 7',0.7))


    m = []
    #m.append(Prop('modifier','a == 7'))
    m.append(Prop('modifier','b == 5'))
    m.append(Prop('modifier','c == 5'))
    m.append(TProp('modifier','d == 9',0.9))
    m.append(TProp('modifier','e == 7',0.9))
    m.append(TProp('modifier','k == 7',0.9))


    combine_two(h,m)


