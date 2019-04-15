import LexicalAnalyser as Lex
import Common as Com
import SyntaxAnalyser as Syn
import GrammarAnalysis as Gramm

def main():
    syntax_table = list()
    Com.lex_table = Lex.list_to_table(Lex.AsmFileToList("test_programm.asm"))
    print(Com.user_list)
    syntax_table = Syn.syntax_check(Com.lex_table)
    for i in range(len(Com.lex_table)):
        Syn.instruction_analysis(Com.lex_table[i], i, syntax_table[i])
       # print(Com.lex_table[i])
        #print(Com.operands[i])
        Gramm.segm_table(Com.lex_table[i], i)
    #Syn.print_operands()
    print(Com.error_flags)
  # print(Com.operands)
main()