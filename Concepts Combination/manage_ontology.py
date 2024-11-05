from owlready2 import *
from random import randint
from prop import Prop,TProp


class ManageOntology():
    def __init__(self, scenario, rigid_p, tipical_p):
        self.scenario = scenario
        self.rigid_p = rigid_p
        self.tipical_p = tipical_p
        self.cs = self.conflicts()

        onto_path.append(os.path.dirname(os.path.abspath(__file__)))
        self.world = World()
        self.onto = self.world.get_ontology("http://www.example.org/onto.owl#"+str(randint(0, 99)))
                
        self.head = self.create_class('head')
        self.modifier = self.create_class('modifier')
 
        self.add_tipical_attrs()
        self.add_rigid()
            
        self.combined = self.create_class('combined')
        self.combined.is_a.append(self.head & self.modifier)

        self.add_typical_combined_attrs()

        self.ind = self.combined("ind")
        #print(list(self.onto.classes()))
        #print(list(self.onto.properties()))
        
    
    def conflicts(self):
        # this method is to have only one valid rule per property
        cs = {}
        s = [1]*len(self.rigid_p) + self.scenario
        p = self.rigid_p+self.tipical_p
        for x,active_x in zip(p,s):
            for y,active_y in zip(p,s):
                if active_x and active_y and x.var == y.var and x.val != y.val and x.neg+y.neg != 1:
                    if x.var not in cs:
                        cs[x.var] = set()
                    cs[x.var] = cs[x.var].union(set((x.val,y.val)))
        #print(cs)
        return cs
        
    def add_rigid(self) :
        for p in self.rigid_p :
            
            tmp_attr = self.create_class(p.var)
            #print((p.var in self.cs and len(self.onto.search(iri=f"*{p.var}"))))
            if p.neg or (p.var in self.cs and len(self.onto.search(iri=f"*{p.var}"))): 
                tmp_attr = Not(tmp_attr)  


            if p.head:
                self.head.is_a.append(tmp_attr)
            else:
                self.modifier.is_a.append(tmp_attr) 

            #if p.val:
            #    self.create_instance(tmp_attr,p)

    def add_tipical_attrs(self) :
        for p in self.tipical_p:
            tmp_attr = self.create_class(p.var)
            #print((p.var in self.cs and len(self.onto.search(iri=f"*{p.var}"))))
            if p.neg or (p.var in self.cs and len(self.onto.search(iri=f"*{p.var}"))): 
                tmp_attr = Not(tmp_attr)  

            prefix = 'head' if p.head else 'modifier'
            el = self.head if p.head else self.modifier

            self.add_typical_logic(el,tmp_attr,prefix)

            #if p.val:
            #    self.create_instance(tmp_attr,p)


    def add_typical_combined_attrs(self):
        for p,active in zip(self.tipical_p,self.scenario):
            if active:
                attr_class = self.create_class(p.var)
                if p.neg:
                    attr_class = Not(attr_class)

                self.add_typical_logic(self.combined, attr_class, 'combined')

    def add_typical_logic(self, base_class, attr_class, prefix):
        class1 = self.create_class(f'{prefix}1')
        classes = self.create_class(f'{prefix}s')
        not_class1 = self.create_class(f'Not{prefix}1')

        classes.equivalent_to.append(base_class & class1)
        not_class1.equivalent_to.append(Not(class1))
        relation = self.create_property(f'{prefix.lower()}_R')

        classes.is_a.append(attr_class)
        class1.is_a.append(relation.only(Not(base_class) & class1))
        not_class1.is_a.append(relation.some(base_class & class1))

    def is_consistent(self):
        return self.check_consistency()

    def check_consistency(self):
        try:
            with self.onto:
                sync_reasoner(self.world)
        except Exception as e:
            print(e)
            return False
        return True

    def create_class(self, name, parent = Thing) :
        with self.onto :
            new_class = types.new_class(name, (parent,))
        return new_class
    
    def create_property(self, name) :
        with self.onto :
            new_prop = types.new_class(name, (ObjectProperty,))
        return new_prop


    def create_instance(self, attr_class,p):

        if p.head:
            instance = self.head(f"instance_{p.var}_{p.val}")
        else:
            instance = self.modifier(f"instance_{p.var}_{p.val}")

        instance[p.var] = p.val


if __name__ == "__main__" :
    r = []
    r.append(Prop('head','a == 5',False,True))
    r.append(Prop('head','b == 5',False,True))
 
    r.append(Prop('modifier','b == 5',False,False))
    r.append(Prop('modifier','c == 5',False,False))


    t = []
    t.append(TProp('head','c == 6',0.8,False,True))
    t.append(TProp('head','d == 5',0.7,False,True))
    t.append(TProp('head','e == 4',0.7,False,True))


    t.append(TProp('modifier','a == 5',0.9,False,False))
    t.append(TProp('modifier','e == 7',0.9,False,False))
    t.append(TProp('modifier','e == 6',0.9,False,False))


    x = ManageOntology([1,1,1,1,1,1],r,t)
    print(f'{x.is_consistent()}, {x.cs}\n')

    x = ManageOntology([0,1,1,1,1,1],r,t)
    print(f'{x.is_consistent()}, {x.cs}\n')

    x = ManageOntology([0,1,1,1,1,0],r,t)
    print(f'{x.is_consistent()}, {x.cs}\n')

    x = ManageOntology([0,0,0,0,0,0],r,t)
    print(f'{x.is_consistent()}, {x.cs}\n')
