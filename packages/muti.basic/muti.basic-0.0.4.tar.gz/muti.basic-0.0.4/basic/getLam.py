"""
 #  取得函集 get-lams
 @  E.C.Ares
 !  MIT LICENSE
 `  built in pkp for basic-python mio
"""
# r(import-refs)
#       r.. im
from .depLam         import *
from .parLam         import Imp
from threading       import Thread
#       r.. as
import      numpy        as _np
import      torch        as _tc
import  itertools        as _it
# s
_JC_NYM = 'lam_get'




_KY_ = ['dtype','device']

def isn_Lis( ox, ex): return ex in ox
def ism_Lis( ox,aex): return [ex in ox for ex in aex]
def ish_Lis( ox,aex): return all(ish_Lis( ox,aex))
def isx_Lis( ox,aex): return any(ish_Lis( ox,aex))

_JP_IS_ = ['n','m','h','x']
_JP_ISD = _JP_IS_ + ['e']
#_JP_DIC= ['_','K','V']
_JP_DIC = {'_':'items','K':'keys','V':'values'}
_JP_DI_ = list(_JP_DIC.keys())
_FC_AT_ = ['_','E','1']
def Lis_Dic( ox, fc='_'):
  if  fc == '_': return list(ox.items())
  if  fc == 'K': return list(ox.keys())
  if  fc == 'V': return list(ox.values())
  return   [ list(ox.keys()), list(ox.values())]


# FIXME PARALL #TLA_[0][ 'is'+_jk[0]+_jk[1]+'Dic']=lambda ox, ex:TLA_[0]['is'+_jk[0]+'_Lis'](Lis_Dic( ox, _jk[1]), ex)
for _jk  in _it.product(_JP_IS_,_JP_DI_):
    _fc_hea  =  'is'   +_jk[0]
    _fcMhea  =  _fc_hea+_jk[1]
    _fc_hea +=  '_'
    TLA_[0][_fcMhea+'Dic']= lambda ox,ex: TLA_[0][_fc_hea+'Lis'](getattr(ox,_JP_DIC(_jk[1]))(), ex)
    TLA_[0][_fcMhea+'Las']= lambda ox,ex: TLA_[0][_fcMhea+'Dic'](        ox.__dict__,           ex)

def iseKDic( ox, ex)      : return  True  if ex in ox.keys() and ox[ex] is not NON else False
iseKLas                   = lambda ox,ex:              iseKDic(          ox.__dict__,           ex)

def Var_DiK( ox, fc, ar=NON):
    if      ist( fc,TYP[41]):
        if  ist( ar,TYP[42]):
            return [Var_DiK( ox,_fc, ar.get(_fc,NON)) for _fc in  fc]
        return     [Var_DiK( ox,_fc, ar)              for _fc in  fc]
    return           ox.get(     fc, ar)
# 
def VarEDiK( ox, fc, ar= 0 ):
    if      ist( fc,TYP[41]):
        if  ist( ar,TYP[42]):
            return [Var_DiK( ox,_fc, ar.get(_fc,NON)) for _fc in  fc]
        return     [Var_DiK( ox,_fc, ar)              for _fc in  fc]
    var        =     ox.get(     fc, ar)
    return    ar if var is NON else var
# 
def Var1DiK( ox, fc, ar=NON):
    if      ist( fc,TYP[41]):
        _fc    = fc.pop(   )
        if  len( fc): return Var1DiK(
             ox, fc, ar=Var1DiK( ox, _fc, ar))
    fc        = _fc
    return   ox.get( fc, ar)

# FIXME PARALL
for _fc in _FC_AT_: TLA_[0][ 'Var'+_fc+'LaK'] =lambda ox, ex:TLA_[0]['Var'+_fc+'DiK'](ox.__dict__, ex)




_LC_HER = os.getcwd()
# input configs
def Inp( jc, lc=_LC_HER, fb_deb=True):
    _lc  =   os.path.join(   lc, jc)
    _jh  =   os.path.splitext(   jc)
    _jc  =  _jh[ 0]
    _fc  =  _jh[-1][ 1]
    if fb_deb:print(_lc)
    return  Imp(_lc,_fc)

def Him(imp):
    print('pause')
    pass

#if __name__ == "__main__":
if  Her('n'):
    #him()
    Him(Inp('tests.yml'))