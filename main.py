from gramatica import Gramatica

if __name__ == '__main__':
    arquivo = input("Digite o nome do arquivo: ")
    g = Gramatica(arquivo_gramatica="data/" + arquivo)
    print(g)
