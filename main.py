from gramatica import Gramatica

#arquivo = input("Digite o nome do arquivo: ")
g = Gramatica(arquivo_gramatica="data/g1.txt")
g.simplifica_gramatica()
g.chonskfy()
print("FORMA DE CHONSKY")
print(g)

