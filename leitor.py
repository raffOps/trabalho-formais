import re

def splita_linha(linha):
    linha = linha.replace("[", "|")
    linha = linha.replace("]", "|")
    linha = linha.replace(">", "|")
    linha = linha.split("|")
    return linha

def monta_producao(linha):
    #print(linha[1][1:-1])
    cabeca = linha[1][1:-1]
    corpo = []
    for x in linha[4::2]:
        corpo.append(x[1:-1])

    return [cabeca, corpo]


def monta_terminais(arquivo):
    arquivo.readline()
    terminais = []
    linha = arquivo.readline()
    if linha != '#Variaveis\n':
        terminais.append(re.split('[ | ]', linha)[1])
    while (linha != '#Variaveis\n'):
        linha = arquivo.readline()
        if linha != '#Variaveis\n':
            terminais.append(re.split('[ | ]', linha)[1])
    return terminais


def monta_variaveis(arquivo):
    linha = arquivo.readline()
    variaveis = []
    while (linha != '#Inicial\n'):
        linha = arquivo.readline()
        if linha != '#Inicial\n':
            variaveis.append(re.split('[ | ]', linha)[1])
    return variaveis

def monta_producoes(arquivo):
    arquivo.readline()
    producoes = []
    linha = arquivo.readline()
    linha = splita_linha(linha)
    producao = monta_producao(linha)
    producoes.append(producao)
    while (linha != ''):
        linha = arquivo.readline()
        if linha != '':
            linha = splita_linha(linha)
            producao = monta_producao(linha)
            producoes.append(producao)
    return producoes


def le_arquivo(arquivo):

    terminais = monta_terminais(arquivo)
    variaveis = monta_variaveis(arquivo)
    inicial = arquivo.readline()
    producoes = monta_producoes(arquivo)

    print(terminais)
    print(producoes)
    print(inicial)
    print(producoes)


try:
    arquivo = open("gramatica_exemplo2.txt")
    le_arquivo(arquivo)
except FileNotFoundError:
    print("Arquivo nao encontrado")
