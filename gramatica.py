import pprint
from leitor import Leitor
from itertools import combinations

#todo: documentacao da


class Gramatica():
    def __init__(self, arquivo_gramatica):
        with open(arquivo_gramatica, mode='r', encoding="utf-8") as arquivo:
            dados = Leitor(arquivo)
            self._variaveis = dados.variaveis
            self._terminais = dados.terminais
            self._producoes = dados.producoes
            self._simbolo_inicial = dados.inicial

    @property
    def variaveis(self):
        return self._variaveis

    @property
    def terminais(self):
        return self._terminais

    @property
    def producoes(self):
        return self._producoes

    @property
    def simbolo_inicial(self):
        return self._simbolo_inicial

    def simplifica_gramatica(self):
        self.__remove_producoes_vazias()

    def __remove_producoes_vazias(self):
        variaveis_com_prod_vazias = self.__pop_producoes_vazias()
        adicao = []
        for producao in self._producoes:
            combinacoes = self.__get_comb_var_prod_vazias(producao, variaveis_com_prod_vazias)
            for combinacao in combinacoes:
                if len(combinacao) != len(producao[1]):
                    adicao.append([producao[0], self.__diferenca(producao[1], combinacao)])
        self._producoes.extend(adicao)

    def __pop_producoes_vazias(self):
        variaveis_com_prod_vazias = []
        for producao in self._producoes:
            if "V" in producao[1]:
                variaveis_com_prod_vazias.append(producao[0])
                del (self._producoes[self._producoes.index(producao)])
        return variaveis_com_prod_vazias


    def __diferenca(self, lista1, lista2):
        diferenca = []
        for elemento in lista1:
            if elemento not in lista2:
                diferenca.append(elemento)
        return diferenca


    def __get_comb_var_prod_vazias(self, producao, variaveis_com_prod_vazias):
        """
        Objetivo: Dado um producao e a lista das variaveis com producoes vazias, retorna
                    a combinacao dos termos que estao na intersecao desta com o corpo da producao
        :Exemplo [['S', ['X', 'Y', 'Z', 'A']], ["X","Y", "A"] ->
                        [["X"],["Y"],["A"],["X","A"],["X","Y"],["A","Y"],["X","Y","A"]]
        :param producao: list
        :param variaveis_com_prod_vazias: list
        :return: combinacao_variaveis_com_prod_vazias
        :rtype: list
        """
        variaveis_com_prod_vazias_no_corpo_prod = list(set(producao[1]).intersection(variaveis_com_prod_vazias))
        combinacao_variaveis_com_prod_vazias = []
        for tamanho in range(len(variaveis_com_prod_vazias_no_corpo_prod) + 1):
            for combinacao in (combinations(variaveis_com_prod_vazias_no_corpo_prod, tamanho)):
                combinacao_variaveis_com_prod_vazias.append(list(combinacao))
        return combinacao_variaveis_com_prod_vazias[1:]

    def __str__(self):
        return '''\nG = (V, T, P, {}), onde:
        \nConjunto de variáveis: \n\tV = {}
        \nConjunto de símbolos terminais: \n\tT = {}
        \nRegras de produção: \nP = {}
        \nSímbolo inicial: {}'''.format(self._simbolo_inicial, self._variaveis, self._terminais,
                    pprint.pformat(self._producoes), self._simbolo_inicial)