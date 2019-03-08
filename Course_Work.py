import LexicalAnalyser as Lex

def main():
<<<<<<< HEAD
    Com.table = Lex.list_to_table(Lex.AsmFileToList("test_programm.asm"))
=======
    table = Lex.list_to_table(Lex.AsmFileToList("test_programm.asm"))
>>>>>>> 8c67715e442b97323116fa135e2681de56b73199
    Lex.output(table)
main()