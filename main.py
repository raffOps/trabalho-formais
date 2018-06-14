from gramatica import *

print("Lembrete: O arquivo de entrada deve ser colocados na pasta data")
arquivo = input("Digite o nome do arquivo: ")
g = Gramatica(arquivo_gramatica="data/" + arquivo)
g.remove_producoes_vazias()
print("\nREMOVE PRODUÇÕES VAZIS: ")
print(g)
print("---------------------------------------")
g.remove_producoes_unitarias()
print("\nREMOVE PRODUÇÕES UNITÁRIAS: ")
print(g)
print("---------------------------------------")
g.remove_simbolos_inuteis()
print("\nREMOVE PRODUÇÕES INÚTEIS: ")
print(g)
print("---------------------------------------")
g.chonskfy()
print("\nCONVERTE PARA A FORMA NORMAL DE CHONSKY: ")
print(g)
print("---------------------------------------")

while True:
    palavra = input("\nDigite a palavra a ser reconhecida pela gramática: ")
    palavra_reconhecida = g.reconhece_palavra(palavra)
    pprint.pprint(g.tabela_CYK)
    if palavra_reconhecida:
        print("\nA palavra {} é reconhecida por essa gramática\n".format(palavra))
        g.arvores_de_derivacao()
    else:
        print("\nA palavra {} não é reconhecida por essa gramática\n".format(palavra))

    if str(input("\nReconhecer mais uma palavra? 1 para sim, qualquer outra tecla para nao: ")) != "1":
        break

