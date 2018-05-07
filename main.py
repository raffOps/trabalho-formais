from gramatica import Gramatica

if __name__ == '__main__':
    #arquivo = input("Digite o nome do arquivo: ")
    g = Gramatica(arquivo_gramatica="data/gramatica_exemplo1.txt")
    g.simplifica_gramatica()
    print(g)

