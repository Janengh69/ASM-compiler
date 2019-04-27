import Common as Com
#ask about macro parametr
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
                Com.error_flags.append(pos+1)         #in case we meet underfined world
                print("underfined")
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
                Com.error_flags.append(pos+1)
              #  print("meh")
                break
            count += 1
       #list_print(i)
       #row_print(table[pos], lex_list, pos)
       pos += 1 
    return table
    #sentences_syntax_print(table)
   
def sentences_syntax_print(table):
        print('\n')
        print('LABELS,ID        MNEM             1 OPERAND            2 OPERAND      ')
        print('----------------------------------------------------------------------------')
        print('   №LEX    1st  lex        №       1st lex       №       1st lex        №')
        print('----------------------------------------------------------------------------')
        for i in table:
            for j in i:
                if(j == []):
                    print('     -     ', end ='')
                for k in j:
                    print('     %d     ' % (k), sep ='', end ='')
            print()
        
        print('Error flags:', Com.error_flags)

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
def list_print(i):
    for j in i:
        if not j: 
            continue
        print (j[0], " ", end ='')
    print()

def instruction_analysis(lst, i, syn): #lst - one row from list in lexical analysis
    # 1 - reg
    # 2 - ptr
    # 3 - segment id
    # 4 - user id, label
    # 5 - addr reg
    # 6 - const
    #print(lst)
    Com.operands.append([[],[]])
    Com.operands[i][0].append([False, False, False, False, False, False])
    Com.operands[i][0].append(['', '', '', '', '',''])
    Com.operands[i][0].append(['', '', '', '', '',''])
    Com.operands[i][1].append([False, False, False, False, False, False])
    Com.operands[i][1].append(['', '', '', '', '',''])
    Com.operands[i][1].append(['', '', '', '', '',''])
    error_flag = True
    if len(syn) >= 2: 
        if lst[0][1] == "MNEM":
            count = 0                       #to control shift in operands table
            for j in range(1, len(syn)):
                place = syn[j][0]
                if place >= len(lst):
                    place-=1
                if lst[place][1] == "SYMBOL":
                    continue
                #if it contains register (1 row)
                count += 1

                if lst[place][1] == "REGISTER16" and lst[place-1][0] != "[":
                     Com.operands[i][j-count][0][0] = True
                     Com.operands[i][j-count][1][0] = 16
                     for com in range(len(Com.REGISTER16)):
                         if lst[place][0] == Com.REGISTER16[com]:
                             Com.operands[i][j-count][2][0] = com
                             error_flag = False
                             break
                     if error_flag:                         #to check
                         Com.error_flags.append(i)
                         return
                elif lst[place][1] == "REGISTER8":
                     Com.operands[i][j-count][0][0] = True
                     Com.operands[i][j-count][1][0] = 8
                     for com in range(len(Com.REGISTER8)):
                         if lst[place][0] == Com.REGISTER8[com]:
                             Com.operands[i][j-count][2][0] = com
                             error_flag = False
                             break
                     if error_flag:                 
                         Com.error_flags.append(i)
                         print("not register")
                         return
                #if it contains label or user id (4 column)
                elif lst[place][1] == "USER" or lst[place][1] == "USER_MACRO_PARAM":
                    for k in range(len(Com.user_list)):
                        if Com.user_list[k].upper() == lst[place][0]:
                            Com.operands[i][j-count][0][3] = True
                            Com.operands[i][j-count][1][3] = k
                            break
                    for k in range(len(Com.macro_fact_param)):
                        if Com.macro_fact_param[k][1].upper() == lst[place][0]:
                            Com.operands[i][j-count][0][0] = True
                            Com.operands[i][j-count][1][0] = k
                            break   
                elif syn[j][1] > 1: 
                    #if it contains ptr (2 column) 
                    if lst[place][0] == "PTR":#to check
                        for k in range(4,len(Com.DIRECTIVE)):
                            if lst[place-1][0] == Com.DIRECTIVE[k]:
                                Com.operands[i][j-count][0][1] = True
                                Com.operands[i][j-count][1][1] = Com.DIRECTIVE[k]
                    #if it contains segment prefix (3 column)
                    for k in range(len(Com.ID_SEGMENT)):
                        if Com.DIRECTIVE[k] == lst[place][0]:
                            Com.operands[i][j-count][0][2] = True
                            Com.operands[i][j-count][1][2] = Com.NUMBERS_FOR_REG[k]
                            break
                    left = 0
                    right = 0
                    for k in range(len(syn)-1, len(lst)):
                        if lst[k][0] == "[":
                            left +=1
                        if lst[k][1] == "REGISTER16" and left>0: #TOOOOOOOOOOOOOOOOOOOOOOOOOO DOOOOOOOOOOOOOOOOOOOOOOOOOOOO CMP BL, [SI+1]
                            Com.operands[i][j-count][0][4] = True
                            Com.operands[i][j-count][1][4] = Com.REGISTER16.index(lst[k][0])
                        if lst[k][0] == "]" and left >= right:
                            right+=1
                    if left != right:
                        Com.error_flags.append(i)
                        print("brackets")
                        return
                    counter = 0
                    for k in range(len(syn), syn[2][1]):
                        if lst[k][1] == "REGISTER16":
                            if syn[2][1] >= 5:
                                count -= 1
                             #cause count increments two times because of ig_segment and ptr
                            Com.operands[i][j-count][0][4] = True
                            Com.operands[i][j-count][1][4] = Com.NUMBERS_FOR_REG[counter]
                        elif lst[k][1] == "REGISTER8":
                            Com.operands[i][j-count][0][4] = True
                            Com.operands[i][j-count][1][4] = Com.NUMBERS_FOR_REG[counter]
                        elif lst[k][1] == "NUMBER":
                            Com.operands[i][j-count][0][5] = True
                            Com.operands[i][j-count][1][5] = lst[k][0]
                        counter +=1
                #if it has const (6 column)
                elif lst[place][1] == "NUMBER":
                    Com.operands[i][j-count][0][5] = True
                    Com.operands[i][j-count][1][5] = lst[place][0]
                    if place == 1:
                        print("Error")
                        Com.error_flags.append(i)               #to do twice if there is no user id/label
                        print("number")
                        continue
                
#    print(Com.operands[i])


def print_operands():
    for row in Com.operands:
        for word in row:
            print(word)