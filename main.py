from gramatica import Gramatica

#arquivo = input("Digite o nome do arquivo: ")
g = Gramatica(arquivo_gramatica="data/gramatica_exemplo3.txt")
g.coloca_forma_chonsky()
#g.simplifica_gramatica()
print(g)

