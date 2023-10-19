from finanzenpy.stocks import identify_security
from finanzenpy.sel import get_historic



instr = identify_security('IE00B4KBBD01')
#instr = identify_security('DE0005190003')


get_historic(instr)
