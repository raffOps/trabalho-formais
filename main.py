from gramatica import *


#arquivo = input("Digite o nome do arquivo: ")
g = Gramatica(arquivo_gramatica="data/g6.txt")
g.simplifica_gramatica()
g.chonskfy()
palavra = "abba"
print(g.reconhece_palavra(palavra))
g.arvores_de_derivacao(palavra)
#g.limpa_tabela(5)

#print(g.tabela_CYK)


#pprint.pprint(g.tabela_CYK)
