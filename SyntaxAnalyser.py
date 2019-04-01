import Common as Com
error_flags = list()
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
                error_flags.append([pos+1, (i[j][1].index('UNDEFINED'))+1])
                pos += 1
                continue
            if((j == 0 and i[j][1] == 'USER') or (j == 0 and i[j][1] == 'USER_MACRO') or (j != len(i)-1 and i[j][1] == 'USER' and i[j+1][0] == ':')):
                #if j == 0 and i[j][1] == 'USER_MACRO':
                #    if len(i) == 1 :
                #        i[j]    .insert(j, Com.macro_buf)
                table[pos][0] = [count] 
            elif(len(table[pos]) != 3 and table[pos][1] == [] and (i[j][1] == 'MACRO' or i[j][1] == 'MNEM' or i[j][1] == 'SEGMENT' or i[j][1] == 'DIRECTIVE')):
                table[pos][1] = [count, 1]
            elif( i[j][1] == 'DIRECTIVE' or i[j][1] == 'SYMBOL' or i[j][1] == 'USER' or i[j][1] == 'USER_MACRO' or i[j][1] == 'USER_MACRO_PARAM' or i[j][1] == 'ID_SEGMENT' or i[j][1] == 'REGISTER16' or i[j][1] == 'REGISTER8' or i[j][1] == 'TEXTCONST' or i[j][1] == 'NUMBER'):
                if((i[j][0] == ':' and table[pos][0] != []) or i[j][0] == ','):
                    count += 1
                    continue
                elif(table[pos][0] == [] and table[pos][1] == []):
                    error_flags.append([pos+1, j+1])
                    break
                elif(len(table[pos]) == 2):
                    table[pos].append([count, 0])
                elif(len(table[pos]) == 3 and i[j-1][0] == ','):
                    table[pos].append([count, 0])
                    fl = 3
                table[pos][fl][1] += 1
            else:
                error_flags.append([pos+1, j+1])
                break
            count += 1
       list_print(i)
       row_print(table[pos], lex_list, pos)
       pos += 1  

      # print(table[pos])
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
        
        print('Error flags:', error_flags)

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

def instruction_analysis():
#    operand_lexem = list()
#    pos = abs
#    for row in Com.table:
#        if row[0][1] == "MNEM":
#            for i in range(1, len(row)):
#                operand_lexem.append([])
#                if row[i][1] == "REGISTER16":

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


