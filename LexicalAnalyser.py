import re
import Common as Com
import sys

def AsmFileToList(filename): #strip 
    file = open(filename, "r")
    programm = list()
    for line in file:
        match = ''.join(re.findall("[a-zA-Z0-9:;+\" ' ',. \-'\t' \[ \]]", line))
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
    for word in programm: # deleting extra empty lists
        for i in word:
            if i == '':
                word.remove(i)
    macro_search(programm) 
    return programm

def macro_search(lst):
    count = -1
    macro_flag = False
    for row in range(len(lst)):
        if any("MACRO" in s for s in lst[row]) : # checing if there are any MACRO in list
                # in case this is not "macro parametr"
            if len(lst[row]) == 2 and lst[row][0] != "MACRO" or len(lst[row]) == 3:
                Com.macro_buf.append([])
                count +=1
                macro_flag = True              # there is macro 
                Com.macro_user.append([lst[row][0], row])
                if len(lst[row]) > 2:                    # in case MACRO has parametrs
                    Com.macro_param.append(lst[row][2])
                #Com.macro_buf[count].append(row)
                continue
            elif len(lst[row]) == 2 and lst[row][0].upper() == "MACRO":
                Com.error_flags.append(row+1)
                #print("macro1")
                continue
            else:
                 Com.error_flags.append(row+1)
                 #print("macro")
                 continue

        if macro_flag:      #recording all the MACRO in macro_buf list
            if any("ENDM" in s for s in lst[row]):
                macro_flag = False 
        if macro_flag:
            Com.macro_buf[count].append(lst[row])  # end of macro 
    #print(Com.macro_buf)
   # print(Com.macro_user)
   # print(Com.macro_param)
        
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



# if data1 segment, but data ends TO DO: mistakes on all lines
# text between data and code segment

def list_to_table(lst):
    result = list() 
    user_list = set()
    pos = 0
    count_macro = 0             # to skip macros in determining error position
    count = 0                   # for controlling segments 
    user_macro = False
    flag = False
    param_flag = True
    program_works = True
    
    for word in lst:
        if word:
            result.append([])
        else: 
            continue
        for i in range(len(word)):      #describing every word (lexical analysis)
            if program_works:
                row = list()
                if check_is_mnem(word[i]):
                    row = [word[i].upper(), "MNEM", len(word[i])]
                    flag = True
                    param_flag = True              
                elif check_is_macro(word[i]) and Com.segment_flag:
                    row = [ word[i].upper(), "MACRO", len(word[i])]
                    flag = True
                elif check_is_segment_id(word[i])and Com.segment_flag:
                    row = [ word[i].upper(), "ID_SEGMENT", len(word[i])]
                    flag = True
                elif check_is_directive(word[i])and Com.segment_flag:
                    row = [ word[i].upper(), "DIRECTIVE", len(word[i])]
                    flag = True
                elif check_is_segment(word[i]):
                    row = [word[i].upper(), "SEGMENT", len(word[i])]
                    Com.active_seg+=1
                    if len(word) == 2 and word[i].upper() == "SEGMENT": #to doo
                        Com.segment_flag = True
                        if word[i-1] == ''.join(re.findall(r'[A-Z|a-z?.\d+]', word[i-1])) and len(word[i-1]) <= 6:
                            row = [word[i-1].upper(), "SEGMENT_USER", len(word[i-1])]
                            Com.error_flags = Com.error_flags[:-1]              # cause at the start of segment we dont have 
                            if word[i-1].upper() in Com.segment_user:
                                Com.error_flags.append(pos)
                            Com.segment_user.append(word[i-1])                 # to differentiate name of segments later

                            result[pos].append(row)
                            row = [word[i].upper(), "SEGMENT", len(word[i])]
                    if len(word) == 1 and word[i].upper() != "END":        # in case user forgot to name segment
                        Com.error_flags.append(pos - count_macro+1)
                        Com.segment_flag = False   
                        #print("end")

                    elif Com.active_seg%2 == 0 and word[i].upper() == "END" or Com.active_seg%2 == 0 and word[i].upper() != "ENDS": #in case user forgot to close segment
                        Com.error_flags.append(pos-count_macro+1)
                        Com.segment_flag = False
                        Com.active_seg +=1
                        #print("ends")

                    elif Com.active_seg%2 == 0 and word[i].upper() == "ENDS":        #if segment ends
                        for usr in Com.segment_user:
                            if usr == word[i-1]:
                                Com.segment_flag = False
                                row = [word[i].upper(), "SEGMENT", len(word[i])]
                                result[pos].append(row)
                        if Com.segment_flag:
                            Com.error_flags.append(pos-count_macro+1)
                            #print("data1 != data")
                            continue
                    if len(word) == 1 and word[i].upper() == "END": #all segments are closed but we should append end
                        Com.segment_flag = True   
                        program_works = False    
                    flag = True

                elif check_is_symbol(word[i])and Com.segment_flag:
                    row = [ word[i], "SYMBOL", len(word[i])]
                    if len(word) == 1:
                        Com.error_flags.append(pos-count_macro+1)
                    if word[i] == ',' and word[i-1] == ',':
                        Com.error_flags.append(pos-count_macro+1)
                    if i == len(word)-1 and word[i] != ']' and  word[i] != ':':
                        Com.error_flags.append(pos-count_macro+1)
                    flag = True
                elif check_is_register8(word[i])and Com.segment_flag:
                    row = [ word[i].upper(), "REGISTER8", len(word[i])]
                    flag = True
                elif check_is_register16(word[i])and Com.segment_flag:
                    row = [ word[i].upper(), "REGISTER16", len(word[i])]
                    flag = True
                elif word[i] == '':
                    continue
                elif word[i] == ''.join(re.findall(r'[0-9a-fA-F]+[hH]', word[i])) or word[i] == ''.join(re.findall(r'[-]+[0-9a-fA-F]+[hH]', word[i])) or word[i] == ''.join(re.findall(r'[01]+[bB]', word[i])) or word[i] == ''.join(re.findall(r'[0-9]+[dD]?', word[i])) and Com.segment_flag or word[i] == ''.join(re.findall(r'[-]+[0-9]+[dD]?', word[i])) and Com.segment_flag or word[i] == ''.join(re.findall(r'[-]+[01]+[bB]?', word[i])) and Com.segment_flag:
                    row = [ word[i], "NUMBER", len(word[i])]
                    flag = True
                elif word[i] == ''.join(re.findall(r'[@][a-z]+[0-9]+', word[i])) and Com.segment_flag and not flag:
                    row = [ word[i], "LABLE", len(word[i])]
                elif word[i] == ''.join(re.findall(r'[A-Z|a-z?.\d+]', word[i])) and Com.segment_flag and len(word[i]) <= 6 and not flag:
                    for k in range(len(Com.macro_user)):
                        if Com.macro_user[k][0] == word[i] and lst.index(word) > Com.macro_user[k][1]:
                            if len(word) == 1 or (len(word) == 2 and word[1] != "MACRO"):   #in case we call macro in program 
                                if len(word) == 2:
                                        row = macro_to_lex(word)
                                        result.append(row)
                                        pos+=1
                                else:
                                    row.append([word[0].upper(), "USER_MACRO", len(word[0])])
                                    result.append(row)
                                    pos+=1
                                ###########################################################
                                if len(word) == 2:
                                    param = word[1]
                                    Com.macro_fact_param.append([word[0], param])      #for grammar analysis
                                param_flag = False
                                for x in Com.macro_buf[k]:
                                    #Com.macro_call.append(pos)                                      
                                    row = macro_to_lex(x)               #lexical analysis for macro 
                                    if row != None:
                                        for rw in row:                  #replacing formal parametr into actual one
                                            if rw[1] == "USER_MACRO_PARAM":
                                                rw[0] = param.upper()
                                        result.append(row)
                                        pos+=1
                                        count_macro +=1
                                break
                            row = [word[i].upper(), "USER_MACRO", len(word[i])]
                            user_marco = True
                            break
                    if not user_macro:
                        if Com.macro_param:
                            for param in Com.macro_param:
                                if word[i].upper() == param:
                                    row = [ word[i].upper(), "USER_MACRO_PARAM", len(word[i])]
                                    break
                                else:
                                    row = [word[i].upper(), "USER", len(word[i])]
                                    user_list.add(word[i])      #set not to allow names repeating
                                    user_macro = False
                        else:
                            row = [word[i].upper(), "USER", len(word[i])]
                            user_list.add(word[i])      #set not to allow names repeating
                            user_macro = False
                elif word[i][0] == '"'  and not flag and Com.segment_flag : 
                    if word[i][len(word[i])-1] == '"':
                        word[i] = ''.join(re.findall(r'[\"A-Z|a-z|\d+\"]', word[i]))
                        row = [ word[i], "TEXTCONST", len(word[i])]
                    else: 
                        Com.error_flags.append(pos - count_macro +1)
                        continue                                                                                    ##HZ NADO LI SKIPAT
                elif word[i][len(word[i])-1] == '"'  and not flag and Com.segment_flag : 
                    if word[i][0] == '"':
                        word[i] = ''.join(re.findall(r'[\"A-Z|a-z|\d+\"]', word[i]))
                        row = [ word[i], "TEXTCONST", len(word[i])]
                    else: 
                        Com.error_flags.append(pos - count_macro +1)
                        continue                                            
                elif word[i] == ''.join(re.findall(r'[A-Z|a-z|\d+]', word[i])) and not flag and Com.segment_flag:

                    if len(word[i]) > 6:
                        row = [ word[i].upper(), "UNDERFINED", len(word[i])]
                elif not Com.segment_flag: # and Com.active_seg != 0:
                        Com.error_flags.append(pos - count_macro +1)
                if param_flag and row != None and Com.segment_flag:
                    result[pos].append(row)
                flag = False
                user_macro = False
                

            else:
                Com.error_flags.append(pos - count_macro +1)
                #print("end of programm")
        pos +=1
    result = [x for x in result if x != []] #clearing empty lists 
    Com.user_list = list(user_list)
    return(result)


def macro_to_lex(lst):
    result = list() 
    flag = False
    pos = 0
    user_macro = False
    for word in lst:
        if word:
            row = list()
            if check_is_mnem(word):
                row = [word.upper(), "MNEM", len(word)]
                flag = True
            elif check_is_macro(word):
                row = [ word.upper(), "MACRO", len(word)]
                flag = True
            elif check_is_segment_id(word):
                row = [ word.upper(), "ID_SEGMENT", len(word)]
                flag = True
            elif check_is_directive(word):
                row = [ word.upper(), "DIRECTIVE", len(word)]
                flag = True
            elif check_is_segment(word):
                row = [ word.upper(), "SEGMENT", len(word)]
                flag = True
            elif check_is_symbol(word):
                row = [ word, "SYMBOL", len(word)]
                flag = True
            elif check_is_register8(word):
                row = [ word.upper(), "REGISTER8", len(word)]
                flag = True
            elif check_is_register16(word):
                row = [ word.upper(), "REGISTER16", len(word)]
               # flag = True
            elif word == '':
                continue
            elif word == ''.join(re.findall(r'0+[0-9a-fA-F]+[hH]', word)) or word == ''.join(re.findall(r'[01]+[bB]', word)) or word == ''.join(re.findall(r'[-][0-9]+[dD]?', word)) or word == ''.join(re.findall(r'[0-9]+[dD]?', word)) :
                row = [ word, "NUMBER", len(word)]
            elif word == ''.join(re.findall(r'[@][a-z]+[0-9]+', word)) and not flag:
                row = [ word, "LABLE", len(word)]
            elif word == ''.join(re.findall(r'[A-Z|a-z?.\d+]', word)) and len(word) <= 6 and not flag:
                for k in range(len(Com.macro_user)):
                    if Com.macro_user[k][0] == word:
                        row = [word.upper(), "USER_MACRO", len(word)] 
                        user_marco = True
                        continue
                    if not user_macro:
                        for param in Com.macro_param:
                            if word.upper() == param:
                                row = [ word.upper(), "USER_MACRO_PARAM", len(word)]
                                break
                            else:
                                row = [ word.upper(), "USER", len(word)]
                                user_macro = False
            elif word[0] == '"' and word[len(word)-1] == '"' and not flag: 
                    word = ''.join(re.findall(r'[\"A-Z|a-z|\d+\"]', word))
                    row = [ word, "TEXTCONST", len(word)]
            elif word == ''.join(re.findall(r'[A-Z|a-z|\d+]', word)) and not flag:
                if len(word) > 6:
                    row = [ word.upper, "UNDERFINED", len(word)]
            result.append(row)
            pos+=1
            flag = False
        else: 
            continue
    return(result)