import re
import pprint


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


def le_linha(arquivo):
    """
    Lê uma linha do arquivo e lida com os comentarios, retornado apenas a parte
    significativa da linha.
    :param arquivo: file
    :return: string
    """
    linha = arquivo.readline()
    posicao = linha.find("#")
    if posicao == -1:
        return linha
    elif posicao == 0:
        for prefixo in ["#Terminais", "#Variaveis", "#Inicial", "#Regras"]:
            if linha.startswith(prefixo):
                return prefixo
    return linha[:posicao]


def monta_terminais(arquivo):
    """
    Pega os simbolos terminais da gramatica
    Exemplo: gramatica_exemplo2.txt -> ['runs', 'barks', 'eats', ... , 'with', 'at']
    :param arquivo: file
    :return: lista de strings
    """
    le_linha(arquivo) # esse readline eh pra pular a primeira linha do o arquivo, onde ta escrito "#Terminais"
    terminais = []
    linha = le_linha(arquivo) #Eu preciso ler um terminal antes de entrar no while. Seria melhor se tivesse do
                                    #  while em python
    if linha != '#Variaveis':
        terminais.append(re.split('[ | ]', linha)[1]) # Esse re.split() eh como str.split() com multiplos tokens
    while (linha != '#Variaveis'): #vai pegando os terminais ateh chegar na linha em qua tah escrito "#Variaveis"
        linha = le_linha(arquivo)
        if linha != '#Variaveis':
            terminais.append(re.split('[ | ]', linha)[1])
    return terminais


def monta_variaveis(arquivo):
    """
    Pega os simbolos variaveis da gramatica
    Exemplo:  gramatica_exemplo2.txt -> ['VB', 'NP', 'DT', 'VP', 'S', 'PP', 'P']
    :param arquivo: file
    :return: lista de strings
    """
    linha = le_linha(arquivo)
    variaveis = []
    while (linha != '#Inicial'): #vai pegando os variaveis ateh chegar na linha em qua tah escrito "#Iniciais"
        linha = le_linha(arquivo)
        if linha != '#Inicial':
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
    inicial = le_linha(arquivo).strip()[2:-2]
    producoes = monta_producoes(arquivo)

    return (variaveis, terminais, producoes, inicial)


class Gramatica:
    def __init__(self, arquivo_gramatica):
        with open(arquivo_gramatica, mode='r', encoding="utf-8") as arquivo:
            dados = le_arquivo(arquivo)
            self._variaveis = dados[0]
            self._terminais = dados[1]
            self._producoes = dados[2]
            self._simbolo_inicial = dados[3]

    @property
    def get_variaveis(self):
        return self._variaveis

    @property
    def get_terminais(self):
        return self._terminais

    @property
    def get_producoes(self):
        return self._producoes

    @property
    def get_simbolo_inicial(self):
        return self._simbolo_inicial

    def __str__(self):
        return '''G = (V, T, P, {}), onde:
V = {}, conjunto de variáveis.
T = {}, conjunto de símbolos terminais.
P = {}, regras de produção.
{}, símbolo inicial.'''.format(self._simbolo_inicial, self._variaveis, self._terminais,
                    pprint.pformat(self._producoes), self._simbolo_inicial)




if __name__ == '__main__':
    arquivo = input("Digite o nome do arquivo: ")
    g = Gramatica(arquivo_gramatica=arquivo)
    print(g)
