import re

SYMBOLS = [ '[', ']', '.', ',', '_', '@','+', '-', ':']
COMANDS = [ "MOV", "ADD", "DEC", "CMP", "AND", "OR", "INC", "JGE", "MOVSW"]
DIRECTIVE = ['END', "DATA", "SEGMENT", "MACRO", "ENDM", "DB", "DW", "DD", "CODE", "ENDS", "WORD", "PTR", "OFFSET"]
REGISTER16 = [ 'AX', 'BX', 'CX', 'DX']
REGISTER8 = ['AH', 'BH', 'CH', 'DH', 'AL', 'BL', 'CL', 'DL']

def error( msg):
    print ('Lexer error: ', msg)

def AsmFileToList(filename):
    file = open(filename, "r")
    programm = list()
    flag = False
    for line in file:
        match = ''.join(re.findall("[a-zA-Z0-9:;+\" ' ',. '\t' @ \[ \]]", line))
        if match.find(',') != -1:
            match = match.replace(match[match.find(',') ], ' ,')
        if match.find(':') != -1:
            match = match.replace(match[match.find(':') ], ' : ')
        if match.find(']') != -1:
            match = match.replace(match[match.find(']') ], ' ]')
        if match.find('[') != -1:
            match = match.replace(match[match.find('[') ], '[ ')
        if match.find('+') != -1:
            match = match.replace(match[match.find('+') ], ' + ')
        if match.find(';') != -1:
            match = match.replace(match[match.find(';') :], '')
        if match.find('\t') != -1:
            match = match.replace(match[match.find('\t') : match.find('\t')+1], ' ')
        programm.append(match.split(" "))
    for word in programm:
        for i in word:
            if i == '':
                word.remove(i)
    return programm

def check_is_comand(word):
    for temp in COMANDS:
        if word.upper() == temp:
            return True
    return False

def check_is_symbol(word):
    for temp in SYMBOLS:
        if word == temp:
            return True
    return False

def check_is_directive(word):
    for temp in DIRECTIVE:
        if word.upper() == temp:
            return True
    return False

def check_is_register8(word):
    for temp in REGISTER8:
        if word.upper() == temp:
            return True
    return False

def check_is_register16(word):
    for temp in REGISTER16:
        if word.upper() == temp:
            return True
    return False

def output(list1):
    for word in list1:
        print(word)

def list_to_table(lst):
    result = list()
    row = dict()
    flag = False
    for word in lst:
        for i in word: 
            row = dict()
            if check_is_comand(i):
                row = [i.upper(), "COMAND", len(i)]
                flag = True
            elif check_is_directive(i):
                row = [ i.upper(), "DIRECTIVE", len(i)]
                flag = True
            elif check_is_symbol(i):
                row = [ i, "SYMBOL", len(i)]
                flag = True
            elif check_is_register8(i):
                row = [ i.upper(), "REGISTER8", len(i)]
                flag = True
            elif check_is_register16(i):
                row = [ i.upper(), "REGISTER16", len(i)]
                flag = True
            elif i == '':
                continue
            elif i == ''.join(re.findall(r'0+[0-9a-fA-F]+[hH]', i)) or i == ''.join(re.findall(r'[01]+[bB]', i)) or i == ''.join(re.findall(r'[0-9]+[dD]?', i)):
                row = [ i, "NUMBER", len(i)]
            elif i == ''.join(re.findall(r'[A-Z|a-z?.\d+]{1,6}', i)) and not flag:
                    row = [ i.upper(), "USER", len(i)]
            elif i == ''.join(re.findall(r'[/"\w/"]+', i)):
                row = [ i, "TEXTCONST", len(i)] 
            elif i == ''.join(re.findall(r'[@][a-z]+[0-9]+', i)) and not flag:
                row = [ i, "MITKA", len(i)]
            elif(not row): continue
            result.append(row)
            flag = False
    #output(result)
    return(result)