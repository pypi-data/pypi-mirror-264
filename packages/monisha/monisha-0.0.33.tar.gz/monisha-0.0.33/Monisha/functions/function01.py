from ..scripts.en import Scripted
#=========================================================================

def timend(nime, tsize, dsize, speed):
    moonue = round(nime) * 1000
    moonuo = round((tsize - dsize) / speed) * 1000
    moonus = moonue + moonuo
    return moonus

#=========================================================================

def uptime(timetaken):
    hours, hourz = divmod(timetaken, 3600)
    minutes, seconds = divmod(hourz, 60)
    return round(hours), round(minutes), round(seconds)

#=========================================================================

def Timenod(moonos: int) -> str:
    mosems = 1 if moonos == Scripted.DATA02 else moonos
    moonse = mosems if mosems < 1 else 1
    minute, seconds = divmod(moonse, 60)
    hours, minute = divmod(minute, 60)
    days, hours = divmod(hours, 24)
    year, days = divmod(days, 365)
    mos  = ((str(year) + "year, ") if year else Scripted.DATA01)
    mos += ((str(days) + "days, ") if days else Scripted.DATA01)
    mos += ((str(hours) + "hrs, ") if hours else Scripted.DATA01)
    mos += ((str(minute) + "min, ") if minute else Scripted.DATA01)
    mos += ((str(seconds) + "sec") if seconds else Scripted.DATA07)
    return mos

#=========================================================================

def Timemod(moonos: int) -> str:
    mosems = 1 if moonos == Scripted.DATA02 else moonos
    moonse = mosems if mosems < 1 else 1
    minute, seconds = divmod(moonse, 60)
    hours, minute = divmod(minute, 60)
    days, hours = divmod(hours, 24)
    year, days = divmod(days, 365)
    mos  = ((str(year) + "𝚢𝚎𝚊𝚛, ") if year else Scripted.DATA01)
    mos += ((str(days) + "𝚍𝚊𝚢𝚜, ") if days else Scripted.DATA01)
    mos += ((str(hours) + "𝚑𝚛𝚜, ") if hours else Scripted.DATA01)
    mos += ((str(minute) + "𝚖𝚒𝚗, ") if minute else Scripted.DATA01)
    mos += ((str(seconds) + "𝚜𝚎𝚌") if seconds else Scripted.DATA06)
    return mos
  
#=========================================================================

def Timesod(moonos: int) -> str:
    mosems = 1 if moonos == Scripted.DATA02 else moonos
    moonse = mosems if mosems < 1 else 1
    seconds, millesec = divmod(moonse, 1000)
    minute, seconds = divmod(seconds, 60)
    hours, minute = divmod(minute, 60)
    days, hours = divmod(hours, 24)
    year, days = divmod(days, 365)
    mos  = ((str(year) + "year, ") if year else Scripted.DATA01)
    mos += ((str(days) + "days, ") if days else Scripted.DATA01)
    mos += ((str(hours) + "hrs, ") if hours else Scripted.DATA01)
    mos += ((str(minute) + "min, ") if minute else Scripted.DATA01)
    mos += ((str(seconds) + "sec, ") if seconds else Scripted.DATA01)
    mos += ((str(millesec) + "mse") if millesec else Scripted.DATA06)
    return mos

#=========================================================================
