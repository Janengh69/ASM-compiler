import Common as Com

def segm_table(word, sh):
    if len(word) == 1 and word[0][0] in Com.macro_user or len(word) == 2 and word[0][0] in Com.macro_user and word[1][0] != "MACRO":# mark next to macro call
        print("1    ", word[0][0])
    #in the beginnig of macro index
    if len(word) == 1:
        if not (word[0][1] != "SEGMENT" or word[0][0].upper() != "MOVSW" or  word[0][0] != "ENDM" or  word[0][1] != "USER_MACRO"): # in case there is one word in a row and it is not allowed 
            Com.error_flags.append(sh)
    if len(word) == 1 and word[0][0] == "END":
        Com.start_macro = True
    if len(word) <= 3 and len(word) >= 2:            #when macro starts
        if word[1][0] == "MACRO":
            for macro in Com.macro_user:  
                if word[0][0] == macro:
                    Com.start_macro = True
                    break
    number = '00' + format(Com.shift, '02x').upper()
    listing(word, number)
    if word[0][0] == "ENDM":                        # the end of macro 
        if len(word) == 1:
            Com.start_macro = False
        else:
            Com.operands.append([sh, 1])
    if len(word) == 2 and word[1][0] == "ENDS":     #if segment closes
        Com.shift = 0 
    text_sh = 1
    if len(word) == 2:
        if word[0][1] == "USER" and word[1][0] == ":":# in case labelid
            Com.lable_id.append(word[0][0])
            Com.label_berofe_assigm = True
    for i in range(len(word)):
        if word and not Com.start_macro:
            #table_segment.append([])
            if word[i][1].upper() == "SEGMENT_USER": 
                Com.shift = 0
                Com.active_seg += 1
            if Com.active_seg == 1 and len(word) != 1:
                if len(word) != 3 and word[1][1] != "SEGMENT":
                    Com.error_flags.append(sh+1)
                elif i == 0 and word[i][1] != "USER" and word[i+1][1] != "SEGMENT" or i == 1 and word[i][1] != "DIRECTIVE" and word[i][1] != "SEGMENT":
                    Com.error_flags.append(sh+1)
            if word[i][1].upper() == "DIRECTIVE":
                if len(word) == 3:
                    if word[i+1][1] == "TEXTCONST":
                        text_sh = len(word[i+1][0])-2
                        if word[i][0].upper() == "DB":
                            Com.shift += 1*text_sh
                        if word[i][0].upper() == "DW":
                            Com.shift += 2*text_sh
                        if word[i][0].upper() == "DD":
                            Com.shift += 4*text_sh
                # else:
                #     Com.error_flags.append([sh+1, i])
                #     print("not variable")
            if word[i][1].upper() == "MNEM":
                if word[i][0].upper() == "MOV": #reg - imm 
                    if Com.operands[sh][0][0][0] and Com.operands[sh][1][0][5]:   
                        if Com.operands[sh][0][1][0] == 8:
                            Com.shift += 1                          #Com.REGISTER8.index(word[i+1][0]) 
                        elif Com.operands[sh][0][1][0] == 16:
                             Com.shift += 2                         # Com.REGISTER16.index(word[i+1][0])
                        else:
                            Com.error_flags.append(sh+1)
                            print("not right operand")
                            continue
                        if Com.operands[sh][1][1][5].endswith("h"):
                            if int(str(Com.operands[sh][1][1][5][:len(Com.operands[sh][1][1][5])-1]).upper(), 16) < 255:
                                Com.shift += 1
                            if int(str(Com.operands[sh][1][1][5][:len(Com.operands[sh][1][1][5])-1]).upper(), 16) >= 255:
                                Com.shift += 2
                        elif Com.operands[sh][1][1][5].endswith("b"):
                            if int(str(Com.operands[sh][1][1][5][:len(Com.operands[sh][1][1][5])-1]).upper(), 2) < 255:
                                Com.shift += 1
                            if int(str(Com.operands[sh][1][1][5][:len(Com.operands[sh][1][1][5])-1]).upper(), 2) >= 255:
                                Com.shift += 2
                        elif int(Com.operands[sh][1][1][5]) < 256:
                            Com.shift += 1
                        elif int(Com.operands[sh][1][1][5]) >= 256:
                            Com.shift += 2   

                    else:
                        Com.error_flags.append(sh+1)
                        print("not right const")
                        continue
                if word[i][0].upper() == "CMP" : # cmp reg, mem 
                    # the first register                the second user_id                                      segment id                                                  operand has ptr                                                          
                    if Com.operands[sh][0][0][0] and Com.operands[sh][1][0][3] or Com.operands[sh][0][0][0] and Com.operands[sh][1][0][2] or Com.operands[sh][0][0][0] and Com.operands[sh][1][0][1] or Com.operands[sh][0][0][0] and Com.operands[sh][1][0][4]: 
                        Com.shift += 1
                        if Com.operands[sh][1][0][3]: # user id
                            Com.shift += 2
                        if  Com.operands[sh][1][0][2]:# id segment 
                            Com.shift += 1
                        if Com.operands[sh][1][0][5]:
                            Com.shift += 1
                        if Com.operands[sh][1][0][4]:
                            Com.shift += 1
                        if Com.operands[sh][0][1][0] == 8 or Com.operands[sh][0][1][0] == 16:
                             Com.shift += 1
                        else: 
                            Com.error_flags.append(sh+1)
                            print("not right reg")
                    else:
                        Com.error_flags.append(sh+1)
                        print("not right operand")
                if word[i][0].upper() == "JGE":
                    if Com.label_berofe_assigm:
                     #   print(word)
                        for lable in Com.lable_id:
                            if lable == word[i+1][0]:
                                Com.shift +=2
                                Com.label_berofe_assigm = False
                                break
                    else:
                        Com.shift += 2    
                if word[i][0].upper() == "AND": #mem - reg
                    print(Com.operands[sh][1][0][0])
                    if Com.operands[sh][1][0][0] and Com.operands[sh][0][0][3] or Com.operands[sh][1][0][0] and Com.operands[sh][0][0][2] or Com.operands[sh][1][0][0] and Com.operands[sh][0][0][1]: 
                        Com.shift += 1
                        if Com.operands[sh][0][0][3]: # user id
                            Com.shift += 3
                        if  Com.operands[sh][0][0][2]:# id segment 
                            Com.shift += 1
                        if Com.operands[sh][0][0][5]:#number
                            Com.shift += 1
                        if Com.operands[sh][0][0][4]:#add reg
                            Com.shift += 1
                    else:
                        Com.error_flags.append(sh+1)
                        print("not right reg")
                                                  #  the second one is number
                if word[i][0].upper() == "OR" and Com.operands[sh][1][0][5]: # mem-imm
                    Com.shift += 1
                    if Com.operands[sh][0][0][3]: 
                        Com.shift += 3
                    if  Com.operands[sh][0][0][2]:
                        Com.shift += 1
                    if Com.operands[sh][0][0][4]:
                        Com.shift += 1
                    if Com.operands[sh][1][0][5]:
                        Com.shift += 1
                if word[i][0].upper() == "DEC" and Com.operands[sh][0][0][3] or word[i][0].upper() == "DEC" and  Com.operands[sh][0][0][2] or  word[i][0].upper() == "DEC" and Com.operands[sh][0][0][4] or   word[i][0].upper() == "DEC" and Com.operands[sh][0][0][5] :
                    Com.shift += 1
                    if Com.operands[sh][0][0][3]: # user id
                        Com.shift += 3
                    if  Com.operands[sh][0][0][2]:# id segment 
                        Com.shift += 1
                    if Com.operands[sh][0][0][4]:# in case register
                        Com.shift += 1
                    if Com.operands[sh][0][0][5]:# in case number
                        Com.shift += 1
                if word[i][0].upper() == "ADD" and Com.operands[sh][1][0][0] and Com.operands[sh][0][0][0]:
                    if len(word) == 4:
                        if word[i+1][1] == "USER_MACRO_PARAM" or word[i+2][1] == "USER_MACRO_PARAM":
                            if (word[i+1][0].endswith("H") or word[i+1][0].endswith("L")) or (word[i+2][0].endswith("H") or word[i+2][0].endswith("L")):
                              Com.shift += 2
                            if word[i+1][0].endswith("X") or word[i+2][0].endswith("X"):
                                Com.shift += 1
                            else: 
                                Com.error_flags.append(sh+1)
                                print("inproper parametr")
                                continue
                    Com.shift += 2
                if word[i][0].upper() == "INC" and  Com.operands[sh][0][0][0]:
                    if Com.operands[sh][0][1][0] == 8:
                        Com.shift += 2
                    if Com.operands[sh][0][1][0] == 16:
                        Com.shift += 1
                    if word[i+1][1] == "USER_MACRO_PARAM":
                        if word[i+1][0].endswith("H") or word[i+1][0].endswith("L") :
                            Com.shift += 2
                        if word[i+1][0].endswith("X"):
                            Com.shift += 1
                        else: 
                            Com.error_flags.append(sh+1)
                            print("inproper parametr")
                            continue
                if word[i][0].upper() == "MOVSW":
                    Com.shift += 1
                    if len(word) != 1:
                        Com.error_flags.append(sh+1)
                        print("movws doesnt accept parametrs")
    

def listing(word, number):
    if not Com.start_macro:
        print(number, end = "       ")
    else:
        print(" ", end = "     ")
    for i in range(len(word)):
        print(word[i][0], end=' ')
    print()
