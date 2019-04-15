import Common as Com

table_segment = list()

#to do
# 	VW		D	5d
def segm_table(word, sh):
    #macro ignore to do 
    text_sh = 1
    for i in range(len(word)):
        if word:
            table_segment.append([])
            if word[i][1].upper() == "SEGMENT_USER": 
                Com.shift = 0
                #hex(dec).split('x')[-1]
            if word[i][1].upper() == "DIRECTIVE":
                if len(word) == 3 and word[i+1][1] == "TEXTCONST":
                    text_sh = len(word[i+1][0])-2
                elif word[i][0].upper() == "DB":
                    Com.shift += 1*text_sh
                elif word[i][0].upper() == "DW":
                    Com.shift += 2*text_sh
                elif word[i][0].upper() == "DD":
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
                            Com.error_flags.append([sh+1, i])
                            print("not right operand")
                            continue
                        if Com.operands[sh][1][1][5].endswith("h"):
                            if int(str(Com.operands[sh][1][1][5][:len(Com.operands[sh][1][1][5])-1]).upper(), 16) < 128:
                                Com.shift += 1
                            if int(str(Com.operands[sh][1][1][5][:len(Com.operands[sh][1][1][5])-1]).upper(), 16) >= 128:
                                Com.shift += 2
                        elif Com.operands[sh][1][1][5].endswith("b"):
                            if int(str(Com.operands[sh][1][1][5][:len(Com.operands[sh][1][1][5])-1]).upper(), 2) < 128:
                                Com.shift += 1
                            if int(str(Com.operands[sh][1][1][5][:len(Com.operands[sh][1][1][5])-1]).upper(), 2) >= 128:
                                Com.shift += 2
                        
                    else:
                        Com.error_flags.append([sh+1, i])
                        print("not right const")
                        continue
                if word[i][0].upper() == "CMP" : # cmp reg, mem 
                    if Com.operands[sh][0][0][0] and Com.operands[sh][1][0][3] or Com.operands[sh][0][0][0] and Com.operands[sh][1][0][2] or Com.operands[sh][0][0][0] and Com.operands[sh][1][0][1]: 
                        Com.shift += 3
                        if Com.operands[sh][0][1][0] == 8 or Com.operands[sh][0][1][0] == 16:
                             Com.shift += 1
                        else: 
                            Com.error_flags.append([sh+1, i])
                            print("not right reg")
                    else:
                        Com.error_flags.append([sh+1, i])
                        print("not right operand")
                if word[i][0].upper() == "JGE":
                    Com.shift += 2    
                if word[i][0].upper() == "AND": #mem - reg
                    if Com.operands[sh][1][0][0] and Com.operands[sh][0][0][3] or Com.operands[sh][1][0][0] and Com.operands[sh][0][0][2] or Com.operands[sh][1][0][0] and Com.operands[sh][0][0][1]: 
                        Com.shift += 4
                        # if  int(Com.operands[sh][1][1][5]) < 128:
                        #     Com.shift += 1
                        # elif int(Com.operands[sh][1][1][5]) >= 128:
                        #     Com.shift += 2

                        # else:
                        #     Com.error_flags.append([sh+1, i])
                        #     print("not right reg")
                    Com.shift += 4
                if word[i][0].upper() == "OR":
                    Com.shift += 5
                if word[i][0].upper() == "DEC" :
                    Com.shift += 4
                if word[i][0].upper() == "ADD" :
                    Com.shift += 4
                if word[i][0].upper() == "INC" :
                    Com.shift += 1
    print("00" + format(Com.shift, '02x'))