import LexicalAnalyser as Lex
import Common as Com
import SyntaxAnalyser as Syn
import GrammarAnalysis as Gramm

def main():
    syntax_table = list()
    Com.lex_table = Lex.list_to_table(Lex.AsmFileToList("test_programm.asm"))
    syntax_table = Syn.syntax_check(Com.lex_table)
    Com.active_seg = 0
    
    for i in range(len(Com.lex_table)):
        Syn.instruction_analysis(Com.lex_table[i], i, syntax_table[i])
        Gramm.shift_count(Com.lex_table[i], i)
    for i in range(len(Com.lex_table)):
        Gramm.second_pass(Com.lex_table[i], i)
        Gramm.listing(Com.lex_table[i], i)
    #print(Com.error_flags)
#print(Com.bytes)
   # print(Com.lex_table)
main()