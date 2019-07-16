import Common as Com
import math

def shift_count(word, sh):
    '''
    Function counts a shift for listing without determing them exactly 
    '''
    #in the beginnig of macro index
    if len(word) == 1:
        if not(word[0][1].upper() != "SEGMENT" or word[0][0].upper() != "MOVSW" or  word[0][0].upper() != "ENDM" or  word[0][1] != "USER_MACRO"): # in case there is one word in a row and it is not allowed 
            Com.error_flags.append(sh)
    if len(word) == 1 and word[0][1] == "USER" or len(word) == 1 and  word[0][1] == "UNDEFINED":
        Com.error_flags.append(sh)
    if len(word) == 1 and word[0][1] == "USER_MACRO" or len(word) == 2 and word[0][1] == "USER_MACRO":
        for i in range(len(Com.macro_user)):
            if word[0][0] == Com.macro_user[i][0]:
                Com.count = i
        for i in range(len(Com.macro_buf[Com.count])):
            Com.macro_call.append(sh+i+1)

    if len(word) <= 3 and len(word) >= 2:            #when macro starts
        if word[1][0] == "MACRO":
            for macro in Com.macro_user: 
                if word[0][0] == macro[0]:
                    Com.start_macro = True
                    break
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
            Com.label_id.append(word[0][0])
            Com.label_dict.update({word[0][0]: Com.shift})
            Com.label_berofe_assigm = True
    for i in range(len(word)):
        if word and not Com.start_macro:
            if word[i][1].upper() == "SEGMENT_USER": 
                Com.shift = 0
                Com.active_seg += 1
            if Com.active_seg == 1 and len(word) != 1:
                if len(word) != 3 and word[1][1] != "SEGMENT":
                    Com.error_flags.append(sh)
                elif i == 0 and word[i][1] != "USER" and word[i+1][1] != "SEGMENT" or i == 1 and word[i][1] != "DIRECTIVE" and word[i][1] != "SEGMENT":
                    Com.error_flags.append(sh)
            if word[i][1].upper() == "DIRECTIVE":
                if len(word) == 3:
                    text_sh = 1
                    Com.data_user.append(word[0][0])
                    Com.user_dict.update({word[0][0]:hex(Com.shift)[2:].rjust(4, "0")})
                    Com.user_type_dict.update({word[0][0]:word[1][0]})
                    Com.data.append(word)
                    Com.user_type_dict.update({word[0][0]: word[1][0]})
                    if word[i+1][1] == "TEXTCONST":
                        if word[i][0] == "DB":
                            text_sh = len(word[i+1][0])-2
                            Com.shift+= text_sh
                        else:
                            Com.error_flags.append(sh)
                    elif word[i][0].upper() == "DB":
                        Com.shift += 1*text_sh
                    elif word[i][0].upper() == "DW":
                        Com.shift += 2*text_sh
                    elif word[i][0].upper() == "DD":
                        Com.shift += 4*text_sh
                    else:
                        Com.error_flags.append(sh)
            if word[i][1].upper() == "MNEM":
                if word[i][0].upper() == "MOV": #reg - imm 
                    if Com.operands[sh][0][0][0] and Com.operands[sh][1][0][5]:   
                        if Com.operands[sh][0][1][0] == 8:
                            Com.shift += 1                     
                        elif Com.operands[sh][0][1][0] == 16:
                                Com.shift += 2                    
                        else:
                            Com.error_flags.append(sh)
                            continue
                        if Com.operands[sh][1][1][5].endswith("h"):
                            if int(str(Com.operands[sh][1][1][5][:len(Com.operands[sh][1][1][5])-1]).upper(), 16) < 255:
                                Com.shift += 1
                            elif int(str(Com.operands[sh][1][1][5][:len(Com.operands[sh][1][1][5])-1]).upper(), 16) >= 255 and Com.operands[sh][0][1][0] != 8:
                                Com.shift += 2
                            else:
                                Com.shift += 1
                        elif Com.operands[sh][1][1][5].endswith("b"):
                            if int(str(Com.operands[sh][1][1][5][:len(Com.operands[sh][1][1][5])-1]).upper(), 2) < 255:
                                Com.shift += 1
                            elif int(str(Com.operands[sh][1][1][5][:len(Com.operands[sh][1][1][5])-1]).upper(), 2) >= 255 and Com.operands[sh][0][1][0] != 8:
                                Com.shift += 2
                            else:
                                Com.shift += 1              #in case oveflow eith 8-rigister
                        elif int(Com.operands[sh][1][1][5]) < 255:
                            Com.shift += 1
                        elif int(Com.operands[sh][1][1][5]) >= 255:
                            Com.shift += 2   
                    else:
                        Com.error_flags.append(sh)
                        continue
                if word[i][0].upper() == "CMP" : # cmp reg, mem 
                    # the first register                the second user_id                                      segment id                                                  operand has ptr                                                          
                    if Com.operands[sh][0][0][0] and    Com.operands[sh][1][0][3] or Com.operands[sh][0][0][0] and Com.operands[sh][1][0][2] or Com.operands[sh][0][0][0] and Com.operands[sh][1][0][1] or Com.operands[sh][0][0][0] and Com.operands[sh][1][0][4]: 
                        #Com.shift += 1
                        if Com.operands[sh][1][0][3]: # user id
                            Com.shift += 3
                        if  Com.operands[sh][1][0][2]:# id segment 
                            if Com.operands[sh][1][1][2] == "3Eh" and Com.operands[sh][1][1][4] == 6:
                                Com.shift-=1
                            if Com.operands[sh][1][1][2] == "36h" and Com.operands[sh][1][1][4] == 5:
                                Com.shift -= 1
                            Com.shift+=1
                        if Com.operands[sh][1][0][4]:
                            Com.shift += 1
                            if word[len(word)-2][1] == "NUMBER":
                                if int(word[len(word)-2][0]) <= 255:
                                    Com.shift +=1
                                else: 
                                    Com.shift += 2
                        if Com.operands[sh][0][1][0] == 8 or Com.operands[sh][0][1][0] == 16:# in case register
                                Com.shift += 1
                        else: 
                            Com.error_flags.append(sh)
                    elif Com.operands[sh][1][0][0] and    Com.operands[sh][0][0][3] or Com.operands[sh][1][0][0] and Com.operands[sh][0][0][2] or Com.operands[sh][1][0][0] and Com.operands[sh][0][0][1] or Com.operands[sh][1][0][0] and Com.operands[sh][0][0][4]: 
                        if Com.operands[sh][0][0][3]: # user id
                            Com.shift += 3
                        if  Com.operands[sh][0][0][2]:# id segment 
                            if Com.operands[sh][0][1][2] == "3Eh" and Com.operands[sh][0][1][4] == 6:
                                Com.shift-=1
                            if Com.operands[sh][0][1][2] == "36h" and Com.operands[sh][0][1][4] == 5:
                                Com.shift -= 1
                            Com.shift+=1
                        if Com.operands[sh][0][0][4]:
                            Com.shift += 1
                            if word[len(word)-2][1] == "NUMBER":
                                if int(word[len(word)-2][0]) <= 255:
                                    Com.shift +=1
                                else: 
                                    Com.shift += 2
                        if Com.operands[sh][1][1][0] == 8 or Com.operands[sh][1][1][0] == 16:# in case register
                                Com.shift += 1
                        else: 
                            Com.error_flags.append(sh)
                    else:
                        Com.error_flags.append(sh)
                if word[i][0].upper() == "JGE":
                    if len(word) == 2:
                        if Com.label_berofe_assigm:
                            for label in Com.label_id:
                                if label == word[i+1][0]:
                                    Com.shift +=2
                                    Com.label_berofe_assigm = False
                                    break
                        else:
                            Com.shift += 2  
                    else:
                        Com.error_flags.append(sh)
                if word[i][0].upper() == "AND": #mem - reg
                                                        #user id                                                             segment id                                                    
                    if Com.operands[sh][1][0][0] and Com.operands[sh][0][0][3] or Com.operands[sh][1][0][0] and Com.operands[sh][0][0][2] or Com.operands[sh][1][0][0] and Com.operands[sh][0][0][1] or Com.operands[sh][1][0][0] and Com.operands[sh][0][0][4]: 
                        Com.shift += 1
                        if Com.operands[sh][0][0][3]: # user id
                            Com.shift += 3
                        if  Com.operands[sh][0][0][2]:# id segment 
                            if Com.operands[sh][0][1][2] == "3Eh" and Com.operands[sh][0][1][4] != 5:
                                Com.shift-=1
                            if Com.operands[sh][0][1][2] == "36h" and Com.operands[sh][0][1][4] == 5:
                                Com.shift -= 1
                            Com.shift+=1
                            for i in range(len(word)):
                                if word[i][1] == "NUMBER":
                                    Com.shift += 1
                        if Com.operands[sh][0][0][4]:#add reg
                            Com.shift += 1
                    else:
                        Com.error_flags.append(sh) #  the second one is number
                if word[i][0].upper() == "OR" and Com.operands[sh][1][0][5]: # mem-imm
                    Com.shift += 2
                    if Com.operands[sh][0][0][3]: #user id 
                        Com.shift += 2
                    if  Com.operands[sh][0][0][2]: # id segment 
                        if Com.operands[sh][0][1][2] == "3Eh" and Com.operands[sh][0][1][4] != 5:
                                Com.shift-=1
                        if Com.operands[sh][0][1][2] == "36h" and Com.operands[sh][0][1][4] == 5:
                                Com.shift -= 1
                        Com.shift+=1
                    if Com.operands[sh][0][0][4]:
                        if word[len(word)-4][1] == "NUMBER":
                            if int(word[len(word)-4][0]) <= 255:
                                Com.shift +=1
                            else: 
                                Com.shift += 2
                    if Com.operands[sh][1][0][5]:
                        if Com.operands[sh][1][1][5].endswith("h"):
                           if int(Com.operands[sh][1][1][5][:-1], 16) > 255:
                                Com.shift +=1
                        elif Com.operands[sh][1][1][5].endswith("b"):
                            if int(Com.operands[sh][1][1][5][:-1], 2) > 255:
                                Com.shift +=1
                        elif Com.operands[sh][1][1][5].endswith("d"):
                            if int(Com.operands[sh][1][1][5][:-1], 2) > 255:
                                Com.shift +=1
                        elif int(Com.operands[sh][1][1][5]) > 255:
                            Com.shift +=1
                        Com.shift += 1
                if word[i][0].upper() == "DEC" and Com.operands[sh][0][0][3] or word[i][0].upper() == "DEC" and  Com.operands[sh][0][0][2] or  word[i][0].upper() == "DEC" and Com.operands[sh][0][0][4] or   word[i][0].upper() == "DEC" and Com.operands[sh][0][0][5] :
                    Com.shift += 1
                    if Com.operands[sh][0][0][3]: # user id
                        Com.shift += 3
                    if  Com.operands[sh][0][0][2]:# id segment 
                        Com.shift += 1
                    if Com.operands[sh][0][0][4]:# in case register
                        Com.shift += 1
                        if word[len(word)-2][1] == "NUMBER":
                            if int(word[len(word)-2][0]) <= 255:
                                Com.shift +=1
                            else: 
                                Com.shift += 2
                if word[i][0].upper() == "ADD" and Com.operands[sh][1][0][0] and Com.operands[sh][0][0][0]:
                    if len(word) == 4:
                        if word[i+1][1] == "USER_MACRO_PARAM" or word[i+2][1] == "USER_MACRO_PARAM":
                            if (word[i+1][0].endswith("H") or word[i+1][0].endswith("L")) or (word[i+2][0].endswith("H") or word[i+2][0].endswith("L")):
                                Com.shift += 2
                            if word[i+1][0].endswith("X") or word[i+2][0].endswith("X"):
                                Com.shift += 1
                            else: 
                                Com.error_flags.append(sh)
                                continue
                    Com.shift += 2
                if word[i][0].upper() == "INC" and  Com.operands[sh][0][0][0]:
                    if Com.operands[sh][0][1][0] == 8:
                        Com.shift += 2
                    elif Com.operands[sh][0][1][0] == 16:
                        Com.shift += 1
                    elif word[i+1][1] == "USER_MACRO_PARAM":
                        if word[i+1][0].endswith("H") or word[i+1][0].endswith("L") :
                            Com.shift += 2
                        if word[i+1][0].endswith("X"):
                            Com.shift += 1
                        else: 
                            Com.error_flags.append(sh)
                            continue
                if word[i][0].upper() == "MOVSW":
                    Com.shift += 1
                    if len(word) != 1:
                        Com.error_flags.append(sh)
    if word[0][1] != "SEGMENT_USER":
        number = '00' + format(Com.shift, '02x').upper()
    else: 
        number = "0000"
    Com.shift_array.append(number)
    Com.start_macrol.append(Com.start_macro)
    Com.active_segl.append(Com.active_seg)

def listing(word, sh):
    temp = ""
    if sh in Com.macro_call:
        temp = " 1"
    if not Com.start_macrol[sh] and word[0][0] != "ENDM":
        temp += "  " + Com.shift_array[sh-1] + " " + Com.bytes[sh] + "      "
    else:
         temp ="     "
    if len(word) == 1 or len(word) == 2 and word[1][0] != "MACRO":# mark next to macro call
        for i in range(len(Com.macro_user)):
            if word[0][0] == Com.macro_user[i][0]:
                if not Com.start_macrol[sh]:# in case we call macro in macro 
                    temp = "      "

    if sh in Com.error_flags:
        temp = " error"
    print(temp, end=' ')
    for i in range(len(word)):
        print(word[i][0], end=' ')
    print()


def second_pass(row, sh):
    '''
    Function "second pass" determines bytes that will be showed in listing and detects 
    different common mistakes
    '''
    number = ""
    byte_number = ""
    if Com.active_segl[sh] == 1 and len(row) == 3:   # counting bytes in data segment 
            byte_number = row[2][0]
            if byte_number.endswith("b") :              #in case binary
                temp_byte = int(byte_number[:-1],2)
                if temp_byte < 255 and row[1][0] == "DB" or temp_byte < 65535 and row[1][0] == "DW" :
                    byte_number = hex(int(byte_number[:-1],2))[2:].upper()
                else:
                    Com.error_flags.append(sh)
            elif byte_number.endswith("h"):                # in case hex
                temp_byte = int(byte_number[:-1],16)
                if (temp_byte < 255 and row[1][0] == "DB") or (temp_byte < 65535 and row[1][0] == "DW"):
                    byte_number = hex(int(byte_number[:-1],16))[2:].upper()
                else:
                    Com.error_flags.append(sh)
            elif byte_number.endswith("d"):                # in case demical 
                temp_byte = int(byte_number[:-1], 10)
                if temp_byte < 255 and row[1][0] == "DB" or temp_byte < 65535 and row[1][0] == "DW":
                    byte_number = hex(int(byte_number[:-1], 10))[2:].upper()
                else:
                    Com.error_flags.append(sh)
            if row[1][0] == "DB":
                byte_number.rjust(2,'0')
            elif row[1][0].upper() == "DW":
                byte_number = byte_number.rjust(4,"0") 
            if byte_number.startswith("\"") and byte_number.endswith("\""):   #in case textconst
                textconst = byte_number 
                byte_number = " "
                for i in range(1,len(textconst)-1):
                    byte_number += hex(ord(textconst[i]))[-2:].upper() + " "

    elif Com.active_segl[sh] == 2:
        if Com.start_macrol[sh]:
            Com.bytes.append(" ")
            return
        if row[0][0] == "MOV":
            for i in range(len(Com.MNEM)):
                if Com.MNEM[i] == "MOV":
                    byte_number = int(Com.OPCODE[i], 16)                                #getting opcode 
            if Com.operands[sh][0][0][0] and Com.operands[sh][1][0][5]:                 #if first is register and the second is the const
                byte_number += Com.operands[sh][0][2][0]                                #including the register byte_number
                temp = Com.operands[sh][1][1][5]   
                max = 65536
                if temp.rfind('-') != -1:
                    if Com.operands[sh][0][1][0] == 8:
                        max = 256
                    if Com.operands[sh][0][1][0] == 16:
                        max = 65536
                    if temp.endswith("h") or temp.endswith("H"):
                        temp = int(temp[1:][:-1],16)
                        if max == 256 and temp < max or max == 65536 and temp < max:
                            temp = hex(max - temp)[2:]
                        else:
                            Com.error_flags.append(sh)
                    elif temp.endswith("b"):
                        temp = int(temp[1:][:-1], 2)
                        if max == 256 and temp < max or max == 65536 and temp < max:
                            temp = hex(max - temp)[2:]
                        else:
                            Com.error_flags.append(sh)
                    elif temp.endswith("d"):
                        temp = int(temp[:-1], 10)
                        if max == 256 and temp < max or max == 65536 and temp < max:
                            temp = hex(max + temp)[2:]
                        else:
                            Com.error_flags.append(sh)
                    elif temp.isdigit():
                        temp = hex(max - int(temp[:-1], 10))[2:]
                elif temp.endswith("h") or temp.endswith("H"):
                    temp = temp[:-1]
                elif temp.endswith("b"):
                    temp = hex(int(temp[:-1], 2))[2:]
                elif temp.endswith("d"):
                    temp = hex(int(temp[:-1], 10))[2:]
                elif temp.startswith("0"):
                    temp = temp[1:]

                if Com.operands[sh][0][1][0] == 16:                                 #in case 16 register 
                    byte_number += 8
                    if len(str(temp)) > 4:
                        Com.error_flags.append(sh)                                #in case overflow
                    else:
                        byte_number = str(hex(byte_number)[2:])
                        number  = temp.rjust(4,'0').upper()   
                elif Com.operands[sh][0][1][0] == 8:                                #in case 8register
                    if len(str(temp)) > 2:
                        Com.error_flags.append(sh)                                #in case overflow
                    else:
                        byte_number = str(hex(byte_number)[2:])
                        number  = temp.rjust(2,'0').upper()
                else:
                    Com.error_flags.append(sh)
                    return
        if row[0][0] == "ADD":
            for i in range(len(Com.MNEM)):
                if Com.MNEM[i] == "ADD":
                    byte_number = int(Com.OPCODE[i], 16)  #getting opcode
            if Com.operands[sh][0][0][0] and Com.operands[sh][1][0][0] :
                if Com.operands[sh][0][1][0] == Com.operands[sh][1][1][0]:
                    if Com.operands[sh][0][1][0] == 16:
                        byte_number += 1
                else:
                    Com.error_flags.append(sh)
                byte_number = str(byte_number).rjust(2, '0')
            else:
                Com.error_flags.append(sh)
        if row[0][0] == "CMP":
            mod = reg = rm = segm_id = numb = type = ""
            for i in range(len(Com.MNEM)):
                if Com.MNEM[i] == "CMP":
                    byte_number = int(Com.OPCODE[i], 16)
            if Com.operands[sh][0][0][0] and Com.operands[sh][1][0][4] or Com.operands[sh][0][0][0] and Com.operands[sh][1][0][3] and row[3][0] in Com.data_user:  
                if Com.operands[sh][1][0][3]:# in case user id 
                    type = Com.user_type_dict.get(Com.data_user[Com.operands[sh][1][1][3]])
                    mod = "00"
                    rm = "110"
                    reg = str(bin(Com.operands[sh][0][2][0]))[2:].rjust(3,'0')
                    numb = Com.user_dict.get(Com.data_user[Com.operands[sh][1][1][3]]) + "r"
                    if Com.operands[sh][0][1][0] == 8 and type != "DB":
                        Com.error_flags.append(sh)
                    if Com.operands[sh][0][1][0] == 16 and type != "DW":
                        Com.error_flags.append(sh)
                if Com.operands[sh][0][1][0] == 16:
                        byte_number += 1
                if Com.operands[sh][1][0][2]:
                    if Com.operands[sh][1][1][2] != "3Eh":# and Com.operands[sh][1][1][4] == 5:
                        segm_id = Com.NUMBERS_FOR_REG[Com.NUMBERS_FOR_REG.index(Com.operands[sh][1][1][2])][:-1] + ":"
                    if Com.operands[sh][1][1][2] == "3Eh" and Com.operands[sh][1][1][4] == 5:
                        segm_id = "3E:"
                    elif Com.operands[sh][1][1][2] == "36h" and Com.operands[sh][1][1][4] == 5:
                        segm_id = ""
                if Com.operands[sh][1][0][4]:# in case addr reg
                    mod = "01"
                    reg = str(bin(Com.operands[sh][0][2][0]))[2:].rjust(3,"0")
                    for word in row:            # if we have number offset
                        if word[1] == "NUMBER":
                            numb = hex(int(word[0]))[2:]
                            if(len(numb) <= 2):
                                numb = numb.rjust(2, '0')
                            elif(len(numb) <= 4):
                                numb = numb.rjust(4, '0')
                    if Com.operands[sh][1][1][4] == 6: # in case si
                        rm = "100"
                    elif Com.operands[sh][1][1][4] == 7: #in case di
                        rm = "101"
                    elif Com.operands[sh][1][1][4] == 5: # in case bp
                        rm = "110"
                    elif Com.operands[sh][1][1][4] == 3: # in case bx
                        rm = "111"
                    else:                   #in case wrong adress register
                        Com.error_flags.append(sh)
                byte_number = segm_id + hex(byte_number)[2:]
                number = hex(int(mod + reg + rm, 2))[2:].rjust(2,'0').upper() + " "+ numb

            elif Com.operands[sh][1][0][0] and Com.operands[sh][0][0][4] or Com.operands[sh][1][0][0] and Com.operands[sh][0][0][3] and row[1][0] in Com.data_user:  
                if Com.operands[sh][0][0][3]:# in case user id 
                    type = Com.user_type_dict.get(Com.data_user[Com.operands[sh][0][1][3]])
                    mod = "00"
                    rm = "110"
                    reg = str(bin(Com.operands[sh][1][2][0]))[2:].rjust(3,'0')
                    numb = Com.user_dict.get(Com.data_user[Com.operands[sh][0][1][3]]) + "r"
                    if Com.operands[sh][1][1][0] == 8 and type != "DB":
                        Com.error_flags.append(sh)
                    if Com.operands[sh][1][1][0] == 16 and type != "DW":
                        Com.error_flags.append(sh)
                if Com.operands[sh][1][1][0] == 16:
                        byte_number += 1
                if Com.operands[sh][0][0][2]:
                    if Com.operands[sh][0][1][2] != "3Eh":# and Com.operands[sh][1][1][4] == 5:
                        segm_id = Com.NUMBERS_FOR_REG[Com.NUMBERS_FOR_REG.index(Com.operands[sh][0][1][2])][:-1] + ":"
                    if Com.operands[sh][0][1][2] == "3Eh" and Com.operands[sh][0][1][4] == 5:
                        segm_id = "3E:"
                    elif Com.operands[sh][0][1][2] == "36h" and Com.operands[sh][0][1][4] == 5:
                        segm_id = ""
                if Com.operands[sh][0][0][4]:# in case addr reg
                    mod = "01"
                    reg = str(bin(Com.operands[sh][1][2][0]))[2:].rjust(3,"0")
                    for word in row:            # if we have number offset
                        if word[1] == "NUMBER":
                            numb = hex(int(word[0]))[2:]
                            if(len(numb) <= 2):
                                numb = numb.rjust(2, '0')
                            elif(len(numb) <= 4):
                                numb = numb.rjust(4, '0')
                    if Com.operands[sh][0][1][4] == 6: # in case si
                        rm = "100"
                    elif Com.operands[sh][0][1][4] == 7: #in case di
                        rm = "101"
                    elif Com.operands[sh][0][1][4] == 5: # in case bp
                        rm = "110"
                    elif Com.operands[sh][0][1][4] == 3: # in case bx
                        rm = "111"
                    else:                   #in case wrong adress register
                        Com.error_flags.append(sh)
                byte_number = segm_id + hex(byte_number)[2:]
                number = hex(int(mod + reg + rm, 2))[2:].rjust(2,'0').upper() + " "+ numb
            else:
                Com.error_flags.append(sh)
        if row[0][0] == "INC":
            mod = reg = rm = ""
            number = ""
            if Com.operands[sh][0][0][0]:
                if Com.operands[sh][0][1][0] == 16:
                    byte_number = int("40", 16)
                    byte_number += Com.operands[sh][0][2][0]
                if Com.operands[sh][0][1][0] == 8:
                    for i in range(len(Com.MNEM)):
                        if Com.MNEM[i] == "INC":
                            byte_number = int(Com.OPCODE[i], 16)
                            mod = "11"
                            reg = "000"
                            rm = str(bin(Com.REGISTER8.index(row[1][0]))[2:]).rjust(3,"0")
                            number = hex(int(mod + reg + rm, 2))[2:].rjust(2,'0').upper() + " "
            else: 
                Com.error_flags.append(sh)
            if byte_number:
                byte_number = hex(byte_number)[2:]
        if row[0][0] == "MOVSW":
            for i in range(len(Com.MNEM)):
                if Com.MNEM[i] == "MOVSW":
                    byte_number = Com.OPCODE[i]
        if row[0][0] == "JGE":
            for i in range(len(Com.MNEM)):
                if Com.MNEM[i] == "JGE":
                    byte_number = Com.OPCODE[i]
                    if len(row) == 2:
                        min = False
                        temp = int(Com.label_dict.get(row[1][0],0)) 
                        if temp == 0:
                            Com.error_flags.append(sh)
                        temp -= int((Com.shift_array[sh]).lstrip("0"), 16)
                        if temp < 0:                                # in case label was called after description
                            min = True
                            temp = 256 + temp
                        if temp < 127 or min:
                            number = hex(temp)[2:].rjust(2, "0").upper()
                        else:
                            number = "00"
        if row[0][0] == "DEC":
            mod = reg = rm = numb = segm_id = ""
            for i in range(len(Com.MNEM)):
                if Com.MNEM[i] == "DEC":
                    byte_number = int(Com.OPCODE[i], 16) 
            if Com.operands[sh][0][0][2]:
                    segm_id = Com.NUMBERS_FOR_REG[Com.NUMBERS_FOR_REG.index(Com.operands[sh][0][1][2])][:-1] + ":"
            if Com.operands[sh][0][0][4]:  #in case addr reg
                byte_number += 1
                mod = "01"
                reg = "001"
                for word in row:            # if we have number offset
                        if word[1] == "NUMBER":
                            numb = hex(int(word[0]))[2:]
                            if(len(numb) <= 2):
                                numb = numb.rjust(2, '0').upper()
                            elif(len(numb) <= 4):
                                numb = numb.rjust(4, '0').upper()
                if Com.operands[sh][0][1][4] == 6: # in case si
                    rm = "100"
                elif Com.operands[sh][0][1][4] == 7: #in case di
                    rm = "101"
                elif Com.operands[sh][0][1][4] == 5: # in case bp
                    rm = "110"
                elif Com.operands[sh][0][1][4] == 3: # in case bx
                    rm = "111"
                else:                   #in case wrong adress register
                    Com.error_flags.append(sh)
            elif  Com.operands[sh][0][0][3]:# in case user id 
                if Com.data[Com.operands[sh][0][1][3]][1][0] == "DD":
                        Com.error_flags.append(sh)
                mod = "00"
                rm = "110"
                reg = "001"
                if Com.user_type_dict.get(row[1][0]) == "DW" or Com.user_type_dict.get(row[1][0]) == "DD":
                    byte_number += 1
                if row[len(row)-1][0] in Com.data_user:
                    numb = Com.user_dict.get(Com.data_user[Com.operands[sh][0][1][3]]).upper() + "r"
                else:
                    Com.error_flags.append(sh)
            else:
                Com.error_flags.append(sh)
            byte_number = segm_id + " " + hex(byte_number)[2:]
            if mod and reg and rm:
                number = hex(int(mod + reg + rm, 2))[2:].rjust(2,'0').upper() + " " + numb
        if row[0][0] == "AND": # and mem reg
            mod = type = reg = rm = segm_id = numb = ""
            for i in range(len(Com.MNEM)):
                if Com.MNEM[i] == "AND":
                    byte_number = int(Com.OPCODE[i], 16)
                    # reg                                    addr reg               reg                             user id                 
            if Com.operands[sh][1][0][0] and Com.operands[sh][0][0][4] or Com.operands[sh][1][0][0] and Com.operands[sh][0][0][3]:  
                # reg = 16
                if Com.operands[sh][1][1][0] == 16:
                    byte_number += 1
                if Com.operands[sh][0][0][3]:# in case user id 
                    if Com.data[Com.operands[sh][0][1][3]][1][0] == "DD":
                        Com.error_flags.append(sh)
                    if Com.operands[sh][0][1][3] or Com.operands[sh][0][1][3] == 0 :
                        mod = "00"
                        rm = "110"
                        type = Com.user_type_dict.get(Com.data_user[Com.operands[sh][0][1][3]])
                        reg = str(bin(Com.operands[sh][1][2][0]))[2:].rjust(3,'0')
                        numb = Com.user_dict.get(Com.data_user[Com.operands[sh][0][1][3]]).upper() + "r"
                        if Com.operands[sh][1][1][0] == 8 and type != "DB":
                            Com.error_flags.append(sh)
                        if Com.operands[sh][1][1][0] == 16 and type != "DW":
                            Com.error_flags.append(sh)
                    else: 
                        Com.error_flags.append(sh)
                if Com.operands[sh][0][0][2]:
                    if Com.operands[sh][0][1][2] != "3Eh":# and Com.operands[sh][1][1][4] == 5:
                        segm_id = Com.NUMBERS_FOR_REG[Com.NUMBERS_FOR_REG.index(Com.operands[sh][0][1][2])][:-1] + ":"
                    if Com.operands[sh][0][1][2] == "3Eh" and Com.operands[sh][0][1][4] == 5:
                        segm_id = "3E:"
                    elif Com.operands[sh][0][1][2] == "36h" and Com.operands[sh][0][1][4] == 5:
                        segm_id = ""
                if Com.operands[sh][0][0][4]:# in case addr reg
                    mod = "01"
                    reg = str(bin(Com.operands[sh][1][2][0]))[2:].rjust(3,"0").upper()
                    for word in row:            # if we have number offset
                        if word[1] == "NUMBER":
                            numb = hex(int(word[0]))[2:]
                            if(len(numb) <= 2):
                                numb = numb.rjust(2, '0').upper()
                            elif(len(numb) <= 4):
                                numb = numb.rjust(4, '0').upper()
                    if Com.operands[sh][0][1][4] == 6: # in case si
                        rm = "100"
                    elif Com.operands[sh][0][1][4] == 7: #in case di
                        rm = "101"
                    elif Com.operands[sh][0][1][4] == 5: # in case bp
                        rm = "110"
                    elif Com.operands[sh][0][1][4] == 3: # in case bx
                        rm = "111"
                    else:                   #in case wrong adress register
                        Com.error_flags.append(sh)
                if byte_number:
                    byte_number = segm_id + hex(byte_number)[2:]
                    number = hex(int(mod + reg + rm, 2))[2:].rjust(2,'0').upper() + " "+ numb
        if row[0][0] == "OR": # and mem imm
            mod = reg = rm = segm_id = numb = temp = ""
            for i in range(len(Com.MNEM)):
                if Com.MNEM[i] == "OR":
                    byte_number = int(Com.OPCODE[i], 16)
                    # imm                                    addr reg               imm                             user id                 
            if Com.operands[sh][1][0][5] and Com.operands[sh][0][0][4] or Com.operands[sh][1][0][5] and Com.operands[sh][0][0][3]:  
                reg = "001"
                if Com.operands[sh][1][0][5]:
                    temp = str(Com.operands[sh][1][1][5])
                    max = 65536
                    if temp.rfind('-') != -1:
                        if Com.data[Com.operands[sh][0][1][3]][1][0] == "DB":
                            max = 256
                        if Com.data[Com.operands[sh][0][1][3]][1][0] == "DW":
                            max = 65536

                        if temp.endswith("h") or temp.endswith("H"):
                            temp = int(temp[1:][:-1],16)
                            if max == 256 and temp < max or max == 65536 and temp < max:
                                temp = max - temp
                            else:
                                Com.error_flags.append(sh)
                        elif temp.endswith("b"):
                            temp = int(temp[1:][:-1], 2)
                            if max == 256 and temp < max or max == 65536 and temp < max:
                                temp = max - temp
                            else:
                                Com.error_flags.append(sh)
                        elif temp.endswith("d"):
                            temp = int(temp[:-1], 10)
                            if max == 256 and temp < max or max == 65536 and temp < max:
                                temp = max + temp
                            else:
                                Com.error_flags.append(sh)
                        elif temp.isdigit():
                            temp = max - int(temp[:-1], 10)
                            
                    elif temp.endswith("h"):
                        temp = int(temp[:-1], 16)
                    elif temp.endswith("b"):
                        temp = int(temp[:-1], 2)
                    elif temp.endswith("d"):
                        temp = int(temp[:-1], 10)
                    elif temp.startswith("0"):
                        temp = temp[1:]
                    elif temp.isdigit():
                        temp = int(temp, 10)
                    if int(temp) < 127:
                        byte_number = 131                    
                if Com.operands[sh][0][0][3]:# in case user id 
                    if Com.operands[sh][0][1][3] or Com.operands[sh][0][1][3] == 0:# in case there is no user id in data segment
                        if Com.data[Com.operands[sh][0][1][3]][1][0] == "DW": 
                            byte_number += 1
                        elif Com.data[Com.operands[sh][0][1][3]][1][0] == "DB":
                            byte_number = 128
                        else:
                            Com.error_flags.append(sh)
                        if temp > 255:
                            Com.error_flags.append(sh)
                        elif temp < 127 and Com.data[Com.operands[sh][0][1][3]][1][0] != "DB":
                            byte_number = 131
                        if Com.data[Com.operands[sh][0][1][3]][1][0] == "DB":
                            temp = hex(int(temp))[2:].rjust(2,"0").upper()
                        else:
                            temp = hex(int(temp))[2:].rjust(4,"0").upper()
                            
                        mod = "00"
                        rm = "110"
                        numb = Com.user_dict.get(Com.data_user[Com.operands[sh][0][1][3]]).upper() + "r" 
                    else: 
                        Com.error_flags.append(sh)
                if Com.operands[sh][0][0][1] and not Com.operands[sh][0][0][3]:
                    temp = hex(temp)[2:]
                    if Com.operands[sh][0][1][1].upper() == "WORD":
                        temp = temp.rjust(4, "0")
                    elif Com.operands[sh][0][1][1].upper() == "BYTE":
                        temp = temp.rjust(2, "0")
                if Com.operands[sh][0][0][2]:
                    if Com.operands[sh][0][1][2] != "3Eh":# and Com.operands[sh][1][1][4] == 5:
                        segm_id = Com.NUMBERS_FOR_REG[Com.NUMBERS_FOR_REG.index(Com.operands[sh][0][1][2])][:-1] + ":"
                    if Com.operands[sh][0][1][2] == "3Eh" and Com.operands[sh][0][1][4] == 5:
                        segm_id = "3E:"
                    elif Com.operands[sh][0][1][2] == "36h" and Com.operands[sh][0][1][4] == 5:
                        segm_id = ""
                if Com.operands[sh][0][0][4]:# in case addr reg
                    mod = "01"
                    for word in range(len(row)):            # if we have number offset
                        if row[word][1] == "NUMBER" and len(row)-1 > word:
                            numb = hex(int(row[word][0]))[2:]
                            if(len(numb) <= 2):
                                numb = numb.rjust(2, '0').upper()
                            elif(len(numb) <= 4):
                                numb = numb.rjust(4, '0').upper()
                    if not Com.operands[sh][0][0][1]:
                        temp = hex(temp)[2:]
                        if len(temp) <= 2:
                            temp = temp.rjust(2,"0")
                        elif len(temp) == 3 or len(temp) == 4:
                            temp = temp.rjust(4,"0")
                        else:
                            Com.error_flags.append(sh)
                    if Com.operands[sh][0][1][4] == 6: # in case si
                        rm = "100"
                    elif Com.operands[sh][0][1][4] == 7: #in case di
                        rm = "101"
                    elif Com.operands[sh][0][1][4] == 5: # in case bp
                        rm = "110"
                    elif Com.operands[sh][0][1][4] == 3: # in case bx
                        rm = "111"
                    else:                   #in case wrong adress register
                        Com.error_flags.append(sh)
            else:
                Com.error_flags.append(sh)
            #if byte_number and number:
            byte_number = segm_id + hex(byte_number)[2:]
            if mod and reg and rm:
                if not numb.endswith("r"):
                    numb = numb.upper()
                number = hex(int(mod + reg + rm, 2))[2:].rjust(2,'0').upper() + " "+ numb + " " + temp.upper()
    if sh in Com.error_flags:
        Com.bytes.append("error ")
    else:
        Com.bytes.append((str(byte_number).upper() + " " + number))
   