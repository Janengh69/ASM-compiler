
SYMBOLS = [ '[', ']', '.', ',', '_','+', '-', ':']
MNEM = [ "MOV", "ADD", "DEC", "CMP", "AND", "OR", "INC", "JGE", "MOVSW"]
DIRECTIVE =  [ "DB", "DW", "DD", "PTR", "WORD", "DWORD", "BYTE"]
REGISTER16 = [ 'AX', 'CX', 'DX', 'BX', 'SP', 'BP', 'SI', 'DI']
REGISTER8 = [ 'AL','CL', 'DL', 'BL','AH',  'CH', 'DH', 'BH']
SEGMENT = [ "ENDS","SEGMENT",'END']
MACRO = [ "MACRO", "ENDM" ]
ID_SEGMENT = ["ES", "CS", "SS", "DS", "FS", "GS"]
NUMBERS_FOR_REG = [ "26h", "2Eh", "6h", "3Eh", "64h", "65h" ]

lex_table = list()
error_flags = list()
macro_buf = list()
macro_format = list()
macro_param = list()
operands = list()
user_list = list()