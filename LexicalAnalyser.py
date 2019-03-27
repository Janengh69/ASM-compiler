import re
import Common as Com

def error( msg):
    print ('Lexer error: ', msg)

def AsmFileToList(filename):
    file = open(filename, "r")
    programm = list()
    for line in file:
        match = ''.join(re.findall("[a-zA-Z0-9:;+\" ' ',. '\t' \[ \]]", line))
        # replacing all punktuals to find them easy later 
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
    for word in programm: # deleting extra empty lists
        for i in word:
            if i == '':
                word.remove(i)
    macro_search(programm) 
    return programm
def macro_search(lst):
    macro_flag = False
    for row in lst:
        if any("MACRO" in s for s in row):# checing if there are any MACRO in list
            macro_flag = True              # there is macro 
            Com.macro_format.append(row[0])
            if len(row) > 2:                    # in case MACRO has parametrs
                Com.macro_param.append(row[2])
            Com.macro_buf.append(row)
            continue
        if macro_flag:          #recording all the MACRO in macro_buf list
            Com.macro_buf.append(row)
            if any("ENDM" in s for s in row):
                macro_flag = False  # end of macro 
    #print(Com.macro_buf)
    #print(Com.macro_format)
        
def check_is_mnem(word):
    for temp in Com.MNEM:
        for temp in Com.MNEM:

            if word.upper() == temp:
                return True
        return False

def check_is_symbol(word):
    for temp in Com.SYMBOLS:
        for temp in Com.SYMBOLS:
            if word == temp:
                return True
        return False

def check_is_directive(word):
    for temp in Com.DIRECTIVE:
        for temp in Com.DIRECTIVE:
            if word.upper() == temp:
                return True
        return False

def check_is_register8(word):
    for temp in Com.REGISTER8:
        for temp in Com.REGISTER8:
            if word.upper() == temp:
                return True
        return False

def check_is_register16(word):
    for temp in Com.REGISTER16:
        for temp in Com.REGISTER16:
            if word.upper() == temp:
                return True
        return False
def check_is_macro(word):
    for temp in Com.MACRO:
        for temp in Com.MACRO:
            if word.upper() == temp:

                return True
        return False
def check_is_segment_id(word):
    for temp in Com.ID_SEGMENT:
        for temp in Com.ID_SEGMENT:
            if word.upper() == temp:
                return True
        return False
def check_is_segment(word):
    for temp in Com.SEGMENT:
        for temp in Com.SEGMENT:
            if word.upper() == temp:
                return True
        return False

def output(list1):
    for row in list1:
        print()
        for word in row:
            print("|  ", end = '')
            for i in range(len(word)):
                print(word[i], " ",end = '')
            print(" |", end = '')
        print()

def list_to_table(lst):
    result = list()
    pos = 0
    user_macro = False
    flag = False
    for word in lst:
        if word:
            result.append([])
        else: 
            continue
        for i in range(len(word)):      #describing every word (lexical analysis)
            row = list()
            if check_is_mnem(word[i]):
                row = [word[i].upper(), "MNEM", len(word[i])]
                flag = True
            elif check_is_macro(word[i]):
                row = [ word[i].upper(), "MACRO", len(word[i])]
                flag = True
            elif check_is_segment_id(word[i]):
                row = [ word[i].upper(), "ID_SEGMENT", len(word[i])]
                flag = True
            elif check_is_directive(word[i]):
                row = [ word[i].upper(), "DIRECTIVE", len(word[i])]
                flag = True
            elif check_is_segment(word[i]):
                row = [ word[i].upper(), "SEGMENT", len(word[i])]
                flag = True
            elif check_is_symbol(word[i]):
                row = [ word[i], "SYMBOL", len(word[i])]
                flag = True
            elif check_is_register8(word[i]):
                row = [ word[i].upper(), "REGISTER8", len(word[i])]
                flag = True
            elif check_is_register16(word[i]):
                row = [ word[i].upper(), "REGISTER16", len(word[i])]
                flag = True
            elif word[i] == '':
                continue
            elif word[i] == ''.join(re.findall(r'0+[0-9a-fA-F]+[hH]', word[i])) or word[i] == ''.join(re.findall(r'[01]+[bB]', word[i])) or word[i] == ''.join(re.findall(r'[0-9]+[dD]?', word[i])):
                row = [ word[i], "NUMBER", len(word[i])]
            elif word[i] == ''.join(re.findall(r'[@][a-z]+[0-9]+', word[i])) and not flag:
                row = [ word[i], "LABLE", len(word[i])]
            elif word[i] == ''.join(re.findall(r'[A-Z|a-z?.\d+]', word[i])) and len(word[i]) <= 6 and not flag:
                for k in range(len(Com.macro_format)):
                    if Com.macro_format[k] == word[i]:
                        row = [word[i].upper(), "USER_MACRO", len(word[i])] 
                        user_marco = True
                        break
                    if not user_macro:
                        row = [ word[i].upper(), "USER", len(word[i])]
                        user_macro = False
            elif word[i][0] == '"' and word[i][len(word[i])-1] == '"' and not flag: 
                 word[i] = ''.join(re.findall(r'[\"A-Z|a-z|\d+\"]', word[i]))
                 row = [ word[i], "TEXTCONST", len(word[i])]
            elif word[i] == ''.join(re.findall(r'[A-Z|a-z|\d+]', word[i])) and not flag:
                if len(word[i]) > 6:
                    row = [ word[i].upper, "UNDERFINED", len(word[i])]
            result[pos].append(row)
            flag = False
        pos +=1
    return(result)
def insert_macro(lst):
    for row in lst:
        for i in range(len(row)):
                if row[i][1] == 'USER_MACRO':
                    if len(row) == 1 :
                        row[i] = list_to_table(Com.macro_buf)
                        #row.insert(i, list_to_table(Com.macro_buf))
