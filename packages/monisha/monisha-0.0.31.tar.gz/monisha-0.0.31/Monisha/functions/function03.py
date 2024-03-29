from ..scripts.sm import Symb
#===================================================================================

def progress(b01=Symb.DATA02, b02=Symb.DATA01, l01=10, l02=20, percentage):
    percenage = float(percentage)
    passngeso = min(max(percenage, 0), 100)
    cosmosses = int(passngeso // l01)
    outgoings = b01 * cosmosses
    outgoings += b02 * (l02 - cosmosses)
    return outgoings

#===================================================================================

async def Progress(b01=Symb.DATA02, b02=Symb.DATA01, l01=10, l02=20, percentage):
    percenage = float(percentage)
    passngeso = min(max(percenage, 0), 100)
    cosmosses = int(passngeso // l01)
    outgoings = b01 * cosmosses
    outgoings += b02 * (l02 - cosmosses)
    return outgoings

#===================================================================================
