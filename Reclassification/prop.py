'''
TODO:
    - Add NOT to the properties
'''

class Prop:
    def __init__(self, label, cond, neg = False, head = False):
        self.label = label
        self.cond = cond
        self.neg = neg
        self.on = None
        
        self.always_off = False
        self.head = head

        if ('==' in self.cond):
            self.var, self.b, self.val = self.parse_cond()
        else : self.var, self.b, self.val = cond, None, None

    def __str__(self):
        return f"{self.label} -> {self.cond}"

    def __repr__(self):
        return f"<{self.__str__()}>"

    def is_t(self):
        return False
    
    def is_on(self):
        return self.on
    
    def parse_cond(self):
        r = self.cond.split(' == ')
        return r[0], ['=='], r[1]
    
    def is_always_off(self):
        return self.always_off
    
class TProp(Prop):
    def __init__(self, label, cond, t_val, neg = False, head = False):
        super().__init__(label, cond, neg, head)
        self.t_val = float(t_val)

    def __str__(self):
        return f"T({self.label}) -> {self.cond} : {self.t_val}"

    def is_t(self):
        return True
    