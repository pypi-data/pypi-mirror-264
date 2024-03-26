import os,sys

NON = None
TLA_=[globals(),locals()]

#exptNon = lambda _or, *cfg, **tfg: try: return _or(*cfg, **tfg); except: return None
def dddfOut_cfc(_or_, fc,*cfg,**tfg): return       _or_[fc](     *cfg,**tfg)
def dddfOut_afc(_or_,afc,*cfg,**tfg): return {fc : _or_[fc](     *cfg,**tfg) for fc     in afc                 } 
def dddfOut_tfc(_or_,tfc,*cfg,**tfg): return {fc : _or_[fc]( jc ,*cfg,**tfg) for fc, jc in tfc.items(         )}
def dddfOut_nfc(_or_,nfc,*cfg,**tfg): return {fc : _or_[fc]( jc ,*cfg,**tfg) for fc, jc in nfc.__dict__.items()}
def dddfOut_mfc(_or_,nfc,*cfg,**tfg): raise  NotImplementedError
dddfOut_ = {
   'str' :  dddfOut_cfc,
   'lis' :  dddfOut_afc,
   'tup' :  dddfOut_afc,
   'dic' :  dddfOut_tfc,
   'Nym' :  dddfOut_nfc}
# FIXME tuple, namespace: parallel
def dddfOut(    _or_,_fc,*cfg,**tfg): return dddfOut_[type(_fc).__name__[:3]](_or_,_fc,*cfg,**tfg)
def dntfOut(    _or_,_fc,*cfg,**tfg): # HERE-4 # for DEBUG
  try    :                                   return dddfOut_[type(_fc).__name__[:3]](_or_,_fc,*cfg,**tfg)
  except :                                   return     None
# pass: not do any work here. FIXME tuple, namespace: parallel
def dptfOut(    _or_,_fc,*cfg,**tfg):
  if   isinstance(_fc, str):
    try     :return      _or_[_fc](     *cfg,**tfg)  # FIXME HERE-4
    except  :return      None
  elif isinstance(_fc, dict):
    tfg_ret = {}    # events-like, return not nessary
    for   fc,jc in  _fc.items() :
      try   :tfg_ret[fc]=_or_[ fc]( jc ,*cfg,**tfg)
      except:pass
    return tfg_ret
  elif isinstance(_fc,(list ,tuple)):
    tfg_ret = {}    # events-like, return not nessary
    for   fc    in  _fc:
      try   :tfg_ret[fc]=_or_[ fc](     *cfg,**tfg)
      except:pass
    return tfg_ret  # get 方法..

# [HERE-5] MODD [ARES] 
def dddd(_or_):
  return lambda fc, *cfg, **tfg: dddfOut(_or_, fc ,*cfg, **tfg)

def dptfOnt(    _or_,_fc,*cfg,**tfg):
  # not do any work here
  if   isinstance(  _fc, dict):
    tfg_ret = {}    # events-like, return not nessary
    for   fc,jc in  _fc.items() :
      try   :tfg_ret[fc]=_or_[ fc]( jc, *cfg, tfg[ jc])
      except:pass
    return tfg_ret
  elif isinstance(  _fc,(list ,tuple)):
    tfg_ret = {}    # events-like, return not nessary
    for   fc    in  _fc:
      try   :tfg_ret[fc]=_or_[ fc](     *cfg,  tfg[ fc])
      except:pass
    return tfg_ret  # get 方法..
  else:
    try     :return      _or_[_fc](     *cfg,  tfg[_fc])
    except  :return      None