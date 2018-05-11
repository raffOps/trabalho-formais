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
        """
        Objetivo: simplificar um gramatica livre de contexto
        :return:
        """
        self.__remove_producoes_vazias()

    def __remove_producoes_vazias(self):
        """
        Objetivo: Dado um conjunto de producoes de uma glc, remove as producoes vazias diretas e indiretas
        Exemplo: Considere "V" o simbolo de vazio e "T" o simbolo de terminal,
         {(A, ("V",)), (B, ("V",)), (C, ("V",)), (D, ("A","B","C","T"))} ->
            {(D, ("A","B","C","T")), (D, ("A","B","T")), (D, ("A","C","T")), (D, ("B","C","T")),
            (D, ("A", "T")), (D, ("B","T")), (D, ("C","T")), (D, ("T",))}

        :return:
        """
        self.__remove_producoes_vazias_indiretas(self.__pop_producoes_vazias_diretas())

    def __pop_producoes_vazias_diretas(self):
        """
        Objetivo: Remove producoes diretas de producoes vazias e retorna as cabecas destas
        Exemplo: {(A, ("V",)), (B, ("V",)), (C, ("V",)), (D, ("A","B","C","T"))} ->
                    {(D, ("A","B","C","T"))}
        :return: lista de cabecas das producoes excluidas
        :rtype: list
        """
        prod_vazias_dir = set()
        for producao in self._producoes:
            if "V" in producao[1]:
                prod_vazias_dir.add(producao)
        self._producoes = self._producoes - prod_vazias_dir
        return [producao[0] for producao in list(prod_vazias_dir)]

    def __remove_producoes_vazias_indiretas(self, vars_com_prod_vazias_dir):
        """
        Objetivo: Remove producoes indiretas de producoes vazias
        Exemplo: {(D, ("A","B","C","T"))} , ["A","B","C"] ->
                    {(D, ("A","B","C","T")), (D, ("A","B","T")), (D, ("A","C","T")), (D, ("B","C","T")),
                    (D, ("A", "T")), (D, ("B","T")), (D, ("C","T")), (D, ("T",))}
        :param vars_com_prod_vazias_dir: lista de cabecas das producoes com producoes vazias diretas
        :return:
        """
        novas_producoes = []
        for producao in self._producoes:
            combinacoes = self.__get_combinacoes_de_variaveis_com_producao_vazia(producao[1], vars_com_prod_vazias_dir)
            for combinacao in combinacoes:
                if len(combinacao) != len(producao[1]):
                    novas_producoes.append((producao[0], tuple(var for var in producao[1] if var not in combinacao)))
        self._producoes.update(novas_producoes)

    def __get_combinacoes_de_variaveis_com_producao_vazia(self, corpo_da_producao, vars_com_producoes_vazias_dir):
        """
        Objetivo: Dado o corpo de uma producao e lista da variaveis que produzem vazio diretamente, retorna
                    a combinacao da intersecao destes
        Exemplo: ("A","B","C,"D"), ["A", "B", "C"] -> (("A",), ("B",), ("B",), ("A", "B"), ("A", "C"),\
                                                        ("C", "B"), ("A", "B", "C"))
        :param corpo_da_producao: tuple
        :param vars_com_producoes_vazias_dir: list
        :return: combinacao da intersecao entre corpo_da_producao e vars_com_producoes_vazias_dir
        :rtype: tuple
        """
        vars_com_prod_vazias_dir_nesse_corpo = set(corpo_da_producao).intersection(vars_com_producoes_vazias_dir)
        combinacoes = []
        for tamanho in range(len(vars_com_prod_vazias_dir_nesse_corpo)+1):
            combinacoes.extend(tuple(combinations(vars_com_prod_vazias_dir_nesse_corpo, tamanho)))
        return tuple(combinacoes[1:])

    def __str__(self):
        return '''\nG = (V, T, P, {}), onde:
        \nConjunto de variáveis: \n\tV = {}
        \nConjunto de símbolos terminais: \n\tT = {}
        \nRegras de produção: \nP = {}
        \nSímbolo inicial: {}'''.format(self._simbolo_inicial, self._variaveis, self._terminais,
                    pprint.pformat(self._producoes), self._simbolo_inicial)


if __name__ == '__main__':
    arquivo = input("Digite o caminho do arquivo: ")
    print(Gramatica(arquivo))

