import re

def splita_linha(linha):
    """
    Separa numa lista cada conjunto de caracteres na linha.
    Exemplo: [ S ] > [ NP ] [ VP ] -> ['', ' S ', ' ', ' ', ' NP ', ' ', ' VP ', '\n']
    :param linha: string
    :return: lista de string
    """
    # Nas 3 proximas linhas eu troco os caracteres inuteis para "|" com o objetivo de facilitar o split
    # Tentei usar o metodo re.split() mas ela retorna o resultado errado
    linha = linha.replace("[", "|")
    linha = linha.replace("]", "|")
    linha = linha.replace(">", "|")
    linha = linha.split("|")
    return linha

def monta_producao(linha):
    """
    Formata a lista retornada da funcao splita_linha()
    Exemplo: ['', ' S ', ' ', ' ', ' NP ', ' ', ' VP ', '\n'] -> ['S', ['NP', 'VP']]
    :param linha: lista de strings
    :return: lista de strings
    """
    cabeca = linha[1][1:-1] # A cabeca da producao sempre vai estar no indice 1 da lista. Esse slice [1:-1] eh
                            #    para tirar os espacos em branco que cercam ela
    corpo = []
    for x in linha[4::2]: # Os membros do corpo da producao comecam a partir do indice 4 da lista e vao ateh o final
                          #    dela pulando de 2 em 2 para nao pegar os caracteres inuteis ', ' ', '
        corpo.append(x[1:-1])# Esse slice [1:-1] eh para tirar os espacos em branco

    return [cabeca, corpo]


def monta_terminais(arquivo):
    """
    Pega os simbolos terminais da gramatica
    Exemplo: gramatica_exemplo2.txt -> ['runs', 'barks', 'eats', ... , 'with', 'at']
    :param arquivo: file
    :return: lista de strings
    """
    arquivo.readline() # esse readline eh pra pular a primeira linha do o arquivo, onde ta escrito "#Terminais"
    terminais = []
    linha = arquivo.readline() #Eu preciso ler um terminal antes de entrar no while. Seria melhor se tivesse do
                               #  while em python
    if linha != '#Variaveis\n':
        terminais.append(re.split('[ | ]', linha)[1]) # Esse re.split() eh como str.split() com multiplos tokens
    while (linha != '#Variaveis\n'): #vai pegando os terminais ateh chegar na linha em qua tah escrito "#Variaveis"
        linha = arquivo.readline()
        if linha != '#Variaveis\n':
            terminais.append(re.split('[ | ]', linha)[1])
    return terminais


def monta_variaveis(arquivo):
    """
    Pega os simbolos variaveis da gramatica
    Exemplo:  gramatica_exemplo2.txt -> ['VB', 'NP', 'DT', 'VP', 'S', 'PP', 'P']
    :param arquivo: file
    :return: lista de strings
    """
    linha = arquivo.readline()
    variaveis = []
    while (linha != '#Inicial\n'): #vai pegando os variaveis ateh chegar na linha em qua tah escrito "#Iniciais"
        linha = arquivo.readline()
        if linha != '#Inicial\n':
            variaveis.append(re.split('[ | ]', linha)[1])
    return variaveis

def monta_producoes(arquivo):
    """
    Pega as regras de producao da gramatica
    Exemplo: gramatica_exemplo2.txt -> [['S', ['NP', 'VP']], ... , ['N', ['dog']], ['N', ['cat']]
    :param arquivo: file
    :return: lista de lista de strings
    """
    arquivo.readline()
    producoes = []
    linha = arquivo.readline()
    linha = splita_linha(linha)
    producao = monta_producao(linha)
    producoes.append(producao)
    while (linha != ''): # vai pegando as regras ateh chegar no fim do arquivo
        linha = arquivo.readline()
        if linha != '':
            linha = splita_linha(linha)
            producao = monta_producao(linha)
            producoes.append(producao)
    return producoes


def le_arquivo(arquivo):

    terminais = monta_terminais(arquivo)
    variaveis = monta_variaveis(arquivo)
    inicial = arquivo.readline()[2:-2]
    producoes = monta_producoes(arquivo)

    print(terminais)
    print(variaveis)
    print(inicial)
    print(producoes)


try:
    arquivo = open("gramatica_exemplo2.txt")
    le_arquivo(arquivo)
except FileNotFoundError:
    print("Arquivo nao encontrado")
