
SYMBOLS = [ '[', ']', '.', ',', '_','+', '-', ':']
MNEM = [ "MOV", "ADD", "DEC", "CMP", "AND", "OR", "INC", "JGE", "MOVSW"]
#OPER = ["reg-imm", "reg-reg", "mem", "reg-mem", "mem-reg", "mem-imm", "reg", " ", " " ]
DIRECTIVE =  [ "DB", "DW", "DD", "PTR", "WORD", "DWORD", "BYTE"]
REGISTER16 = [ 'AX', 'CX', 'DX', 'BX', 'SP', 'BP', 'SI', 'DI']
REGISTER8 = [ 'AL','CL', 'DL', 'BL','AH',  'CH', 'DH', 'BH']
SEGMENT = [ "ENDS","SEGMENT",'END']
MACRO = [ "MACRO", "ENDM" ]
ID_SEGMENT = ["ES", "CS", "SS", "DS", "FS", "GS"]
NUMBERS_FOR_REG = [ "26h", "2Eh", "6h", "3Eh", "64h", "65h" ]

lex_table = list()          # for lexical analisys
error_flags = list()        # for indexes of rows in program with error
macro_buf = list()          # text in macro 
macro_user = list()         # list of user identifiers using macro
macro_param = list()        # paraments when calling macro
operands = list()           # table with information about operands
user_list = list()          # list for user identifiers in program
segment_user = list()       # list of user segment identifiers 
table_segment = list()

active_seg = 0            # for counting segments and check if it opened
segment_flag = False
shift = 0 
