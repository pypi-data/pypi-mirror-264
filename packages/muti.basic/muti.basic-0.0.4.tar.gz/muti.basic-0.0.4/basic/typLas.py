from depLam import *


class   Dim(Namespace):
    def __init__(  self, **g):
        self.ox = dict(**g)
    pass

class   Dic(dict):
    pass


class   Dix(dict):
    def __init__(      self, *c,**g):
        self.upd_saf(**self.frm( *c))
        self.upd_saf(           **g)
    def __setattr__(   self, jc, ex):
        if   ist( ex,TYP[41],TYP[14]):
            ex = type(ex)(self.__class__(x) if isinstance(x, dict) else x for x in ex)
        elif ist( ex,TYP[42]) and not ist(ex, Dix):
            ex = Tic(ex)
        super().__setattr__(jc, ex)
        super().__setitem__(jc, ex)
    __setitem__ = __setattr__

    def frm(self, *c): return c[0] if c and ist(c[0],TYP[42]) else {}
    #def updtDix(self,**g): 
    def upd(    self,**g): 
        for _eh  in dict(**g).items() :  self.__setattr__(*_eh)
    def upd_saf(self,    **g):
        if   g :self.upd(**g)
    # poptItm
    def pop(self, k, *c):
        if self.__hasattr__(k): self.__delattr__(k)
        return   super().pop(k, *c)


if Her(__name__): h = Dix(ox=1, c=1)