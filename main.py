from gramatica import Gramatica

#arquivo = input("Digite o nome do arquivo: ")
g = Gramatica(arquivo_gramatica="data/g6.txt")
#g.simplifica_gramatica()
#g.chonskfy()
#print("FORMA DE CHONSKY")
palavra = "abaab"
print("\nA palavra {} eh reconhecida pela gramatica?".format(palavra), g.reconhece_palavra(palavra))
print(g.tabela_CYK)