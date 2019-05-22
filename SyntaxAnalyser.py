import Common as Com
def syntax_check(lex_list):
    table = list()
    pos = 0
    for i in lex_list:
       count = 1
       fl = 2     
       table.append([])
       table[pos].append([])
       table[pos].append([])
       for j in range(len(i)):
            if not i[j]:
                continue
            if(i[j] and'UNDEFINED' in i[j][1] ):
                Com.error_flags.append(pos)         #in case we meet underfined world
                #print("underfined")
                pos += 1
                continue
            if((j == 0 and i[j][1] == 'USER') or (j == 0 and i[j][1] == 'USER_MACRO') or i[j][1] == 'SEGMENT_USER' or (j != len(i)-1 and i[j][1] == 'USER' and i[j+1][0] == ':')): 
                table[pos][0] = [count] 
            elif(len(table[pos]) != 3 and table[pos][1] == [] and (i[j][1] == 'MACRO' or i[j][1] == 'MNEM' or i[j][1] == 'SEGMENT' or i[j][1] == 'DIRECTIVE')):
                table[pos][1] = [count, 1]
            elif( i[j][1] == 'DIRECTIVE' or i[j][1] == 'SYMBOL' or i[j][1] == 'USER' or i[j][1] == 'USER_MACRO' or i[j][1] == 'USER_MACRO_PARAM' or i[j][1] == 'ID_SEGMENT' or i[j][1] == 'SEGMENT_USER' or i[j][1] == 'REGISTER16' or i[j][1] == 'REGISTER8' or i[j][1] == 'TEXTCONST' or i[j][1] == 'NUMBER'):
                if((i[j][0] == ':' and table[pos][0] != []) or i[j][0] == ','):
                    count += 1
                    continue
                elif(table[pos][0] == [] and table[pos][1] == []):
                    Com.error_flags.append(pos+1)
                    print("empty")
                    break
                elif(len(table[pos]) == 2):
                    table[pos].append([count, 0])
                elif(len(table[pos]) == 3 and i[j-1][0] == ','):
                    table[pos].append([count, 0])
                    fl = 3
                table[pos][fl][1] += 1
            else:
                Com.error_flags.append(pos)
                #print("meh")
                break
            count += 1
       pos += 1 
    return table

def row_print(i, lex_list, pos):
    print(lex_list[pos])
    print('LABELS,ID           MNEM                  1 OPERAND              2 OPERAND      ')
    print('----------------------------------------------------------------------------')
    print('   №LEX      1st  lex    quantity    1st lex   quantity     1st lex   quantity')
    print('----------------------------------------------------------------------------')
    for j in i:
        if(j == []):
            print('     -     ', end ='')
        for k in j:
            print('     %d     ' % (k), sep ='', end ='')
    print()


def instruction_analysis(lst, i, syn): #lst - one row from list in lexical analysis
    # 1 - reg
    # 2 - ptr
    # 3 - segment id
    # 4 - user id, label
    # 5 - addr reg
    # 6 - const
    Com.operands.append([[],[]])
    Com.operands[i][0].append([False, False, False, False, False, False])
    Com.operands[i][0].append(['', '', '', '', '',''])
    Com.operands[i][0].append(['', '', '', '', '',''])
    Com.operands[i][1].append([False, False, False, False, False, False])
    Com.operands[i][1].append(['', '', '', '', '',''])
    Com.operands[i][1].append(['', '', '', '', '',''])
    error_flag = True
    left = right = 0
    if len(syn) >= 2: 
        if lst[0][1] == "MNEM":
            count = 0                      #to control shift in operands table
            for place in range(1, len(lst)):
               
                if lst[place][0] == ",":
                    count+= 1
                if count > 1:
                    Com.error_flags.append(i)
                    #print("erroee")
                    return
                if lst[place][1] == "REGISTER16" and lst[place-1][0] != "[":
                     Com.operands[i][count][0][0] = True
                     Com.operands[i][count][1][0] = 16
                     for com in range(len(Com.REGISTER16)):
                         if lst[place][0] == Com.REGISTER16[com]:
                             Com.operands[i][count][2][0] = com
                             error_flag = False
                             break
                     #count += 1
                     if error_flag:                         #to check
                         Com.error_flags.append(i)
                        # print("jhghjhgdfgjdjgdj")
                         return
                elif lst[place][1] == "REGISTER8":
                     Com.operands[i][count][0][0] = True
                     Com.operands[i][count][1][0] = 8
                     for com in range(len(Com.REGISTER8)):
                         if lst[place][0] == Com.REGISTER8[com]:
                             Com.operands[i][count][2][0] = com
                             error_flag = False
                             break
                     #count += 1
                     if error_flag:                 
                         Com.error_flags.append(i)
                         #print("not register")
                         return
                #if it contains label or user id (4 column)
                elif lst[place][1] == "USER" or lst[place][1] == "USER_MACRO_PARAM":

                    if lst[place][1] == "USER":
                        for k in range(len(Com.data_user)):
                            if Com.data_user[k] == lst[place][0]:
                                Com.operands[i][count][0][3] = True
                                Com.operands[i][count][1][3] = k
                                break
                        if not Com.operands[i][count][0][3] and lst[place-1][0] != "JGE":
                            #Com.error_flags.append(i)
                            Com.operands[i][count][0][3] = True
                            print("kek")
                    else:
                        for k in range(len(Com.macro_fact_param)):
                            if Com.macro_fact_param[k][1].upper() == lst[place][0]:
                                for reg in Com.REGISTER16:
                                    if reg == lst[place][0]:
                                        Com.operands[i][count][0][0] = True
                                        Com.operands[i][count][1][0] = 16
                                        Com.operands[i][count][2][0] = Com.REGISTER16.index(lst[place][0])
                                        break
                                if not Com.operands[i][count][0][0]:
                                    Com.operands[i][count][0][3] = True
                                    Com.operands[i][count][1][3] = k
                                    break   
                                ########################################
                        for k in range(len(Com.macro_param)):
                            if Com.macro_param[k].upper() == lst[place][0]:
                                Com.operands[i][count][0][3] = True
                                Com.operands[i][count][1][3] = k
                                break
                    #if it contains ptr (2 column) 
                elif lst[place][0] == "PTR":#to check
                    for k in range(4,len(Com.DIRECTIVE)):
                        if lst[place-1][0] == Com.DIRECTIVE[k]:
                            Com.operands[i][count][0][1] = True
                            Com.operands[i][count][1][1] = Com.DIRECTIVE[k]
                #if it contains segment prefix (3 column)
                for k in range(len(Com.data_user)):# in case DEC WORD PTR VW
                    if Com.data_user[k] == lst[place][0]:
                        Com.operands[i][count][0][3] = True
                        Com.operands[i][count][1][3] = k
                        break
                            # in dec word ptr ES:[si+1] wrong second Com.operands
                for k in range(len(Com.ID_SEGMENT)):
                    if Com.ID_SEGMENT[k] == lst[place][0]:
                        Com.operands[i][count][0][2] = True
                        Com.operands[i][count][1][2] = Com.NUMBERS_FOR_REG[k]
                        break
       
                if lst[place][0] == "[":
                    left +=1
                    #left_in = k
                if lst[place][1] == "REGISTER16" and left>0 and left != right:
                        Com.operands[i][count][0][4] = True
                        Com.operands[i][count][1][4] = Com.REGISTER16.index(lst[place][0])
                if lst[place][0] == "]" and left >= right:
                    right+=1
                #if it has const (6 column)
                elif lst[place][1] == "NUMBER":
                    if place == len(lst)-1:
                        Com.operands[i][count][0][5] = True
                        Com.operands[i][count][1][5] = lst[place][0]
                        count +=1
                        if place == 1:
                           # print("Error")
                            Com.error_flags.append(i)               #to do twice if there is no user id/label
                            #print("number")
                            continue
            if left != right:
                    Com.error_flags.append(i)
                   # print("brackets")
                    return


def print_operands():
    for row in Com.operands:
        for word in row:
            print(word)
