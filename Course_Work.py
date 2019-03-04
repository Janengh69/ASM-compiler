import LexicalAnalyser as Lex

def main():
    table = Lex.list_to_table(Lex.AsmFileToList("test_programm.asm"))
    Lex.output(table)
main()