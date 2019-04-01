
SYMBOLS = [ '[', ']', '.', ',', '_','+', '-', ':']
MNEM = [ "MOV", "ADD", "DEC", "CMP", "AND", "OR", "INC", "JGE", "MOVSW"]
DIRECTIVE =  [ "DB", "DW", "DD", "WORD", "PTR", "DWORD", "BYTE"]
REGISTER16 = [ 'AX', 'BX', 'CX', 'DX', 'SI']
REGISTER8 = ['AH', 'BH', 'CH', 'DH', 'AL', 'BL', 'CL', 'DL']
SEGMENT = [ "ENDS","SEGMENT",'END']
MACRO = [ "MACRO", "ENDM" ]
ID_SEGMENT = ["GS", "ES", "FS", "DS", "CS", "SS"]

table = list()
macro_buf = list()
macro_format = list()
macro_param = list()