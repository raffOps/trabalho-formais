import re

class Leitor:
    def __init__(self, arquivo):
        self.__terminais = self.__monta_terminais(arquivo)
        self.__variaveis = self.__monta_variaveis(arquivo)
        self.__inicial = self.__le_linha(arquivo).strip()[2:-2]
        self.__producoes = self.__monta_producoes(arquivo)

    def __le_linha(self, arquivo):
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

    def __splita_linha(self, linha):
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

    def __monta_terminais(self, arquivo):
        """
        Pega os simbolos terminais da gramatica
        Exemplo: gramatica_exemplo2.txt -> ['runs', 'barks', 'eats', ... , 'with', 'at']
        :param arquivo: file
        :return: lista de strings
        """
        self.__le_linha(arquivo)  # esse readline eh pra pular a primeira linha do o arquivo, onde ta escrito "#Terminais"
        terminais = set()
        while True:
            linha = self.__le_linha(arquivo)
            if linha == '#Variaveis':
                break
            else:
                terminais.add(re.split('[ | ]', linha)[1])
        return terminais

    def __monta_producao(self, linha):
        """
        Formata a lista retornada da funcao splita_linha()
        Exemplo: ['', ' S ', ' ', ' ', ' NP ', ' ', ' VP ', '\n'] -> ['S', ['NP', 'VP']]
        :param linha: lista de strings
        :return: lista de strings
        """
        cabeca = linha[1][1:-1]  # A cabeca da producao sempre vai estar no indice 1 da lista. Esse slice [1:-1] eh
                                 #    para tirar os espacos em branco que cercam ela
        corpo = []
        for x in linha[4::2]:# Os membros do corpo da producao comecam a partir do indice 4 da lista e vao ateh o final
                                 #    dela pulando de 2 em 2 para nao pegar os caracteres inuteis ', ' ', '
            corpo.append(x[1:-1])  # Esse slice [1:-1] eh para tirar os espacos em branco

        return (cabeca, tuple(corpo))

    def __monta_producoes(self, arquivo):
        """
        Pega as regras de producao da gramatica
        Exemplo: gramatica_exemplo2.txt -> [['S', ['NP', 'VP']], ... , ['N', ['dog']], ['N', ['cat']]
        :param arquivo: file
        :return: lista de lista de strings
        """
        self.__le_linha(arquivo)
        producoes = set()
        while True:
            linha = self.__le_linha(arquivo)
            if linha == '':
                break
            else:
                linha = self.__splita_linha(linha)
                producao = self.__monta_producao(linha)
                producoes.add(producao)
        return producoes

    def __monta_variaveis(self, arquivo):
        """
        Pega os simbolos variaveis da gramatica
        Exemplo:  gramatica_exemplo2.txt -> ['VB', 'NP', 'DT', 'VP', 'S', 'PP', 'P']
        :param arquivo: file
        :return: lista de strings
        """
        variaveis = set()
        while True:
            linha = self.__le_linha(arquivo)
            if linha == '#Inicial':
                break
            else:
                variaveis.add(re.split('[ | ]', linha)[1])
        return variaveis

    @property
    def terminais(self):
        return self.__terminais

    @property
    def variaveis(self):
        return self.__variaveis

    @property
    def inicial(self):
        return self.__inicial

    @property
    def producoes(self):
        return self.__producoes
