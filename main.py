from gramatica import Gramatica

#arquivo = input("Digite o nome do arquivo: ")
g = Gramatica(arquivo_gramatica="data/g5.txt")
g.simplifica_gramatica()
print(g)

