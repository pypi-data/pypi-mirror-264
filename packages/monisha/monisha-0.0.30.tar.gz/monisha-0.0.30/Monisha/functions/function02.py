from ..scripts.uo import Humon
from ..scripts.en import Scripted
#=============================================================================

def Dbytes(sizes, bieses=Scripted.DATA01):
    if not sizes or (sizes == Scripted.DATA02):
        outgoing = "0 B"
        return outgoing
    nomos = 0
    POWEO = 2**10
    POWER = Humon.DATA01
    while sizes > POWEO:
        sizes /= POWEO
        nomos += 1
    ouing = str(round(sizes, 2)) + Scripted.DATA02 + POWER[nomos] + bieses
    return ouing

#=============================================================================

def Hbytes(sizes, bieses=Scripted.DATA01):
    if not sizes or (sizes == Scripted.DATA02):
        outgoing = "0 𝙱"
        return outgoing
    nomos = 0
    POWEO = 2**10
    POWER = Humon.DATA02
    while sizes > POWEO:
        sizes /= POWEO
        nomos += 1
    ouing = str(round(sizes, 2)) + Scripted.DATA02 + POWER[nomos] + bieses
    return ouing

#=============================================================================
