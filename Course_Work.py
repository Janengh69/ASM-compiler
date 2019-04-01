import LexicalAnalyser as Lex
import Common as Com
import SyntaxAnalyser as Syn

def main():

    Com.table = Lex.list_to_table(Lex.AsmFileToList("test_programm.asm"))
    print(Com.table)
    #Com.table = Lex.AsmFileToList("test_programm.asm")
    #Lex.macro_search(Com.table)
    #Lex.insert_macro(Com.table)
   # for row in Com.table:
    #    Lex.list_to_table(row)    
    #Lex.output(table)
    Syn.syntax_check(Com.table)
main()