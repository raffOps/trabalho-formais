import pprint
from leitor import Leitor


class Gramatica():
    def __init__(self, arquivo_gramatica):
        with open(arquivo_gramatica, mode='r', encoding="utf-8") as arquivo:
            dados = Leitor(arquivo)
            self._variaveis = dados.get_variaveis()
            self._terminais = dados.get_terminais()
            self._producoes = dados.get_producoes()
            self._simbolo_inicial = dados.get_inicial()

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
        return '''\nG = (V, T, P, {}), onde:
        \nConjunto de variáveis: \n\tV = {}
        \nConjunto de símbolos terminais: \n\tT = {}
        \nRegras de produção: \nP = {}
        \nSímbolo inicial: {}'''.format(self._simbolo_inicial, self._variaveis, self._terminais,
                    pprint.pformat(self._producoes), self._simbolo_inicial)