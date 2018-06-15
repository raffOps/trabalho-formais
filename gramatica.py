import pprint
from itertools import combinations
from arvore_derivacao import ArvoreDerivacao
from leitor import Leitor


class Gramatica():
    def __init__(self, arquivo_gramatica):
        with open(arquivo_gramatica, mode='r', encoding="utf-8") as arquivo:
            dados = Leitor(arquivo)
            self._variaveis = dados.variaveis
            self._terminais = dados.terminais
            self._producoes = dados.producoes
            self._simbolo_inicial = dados.inicial
            self._tabela_CYK = None

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

    @property
    def tabela_CYK(self):
        return self._tabela_CYK

    def simplifica_gramatica(self):
        """
        Objetivo: simplificar um gramatica livre de contexto
        :return:
        """
        self.remove_producoes_vazias()
        self.remove_producoes_unitarias()
        self.remove_simbolos_inuteis()

    def remove_producoes_vazias(self):
        """
        Objetivo: Dado um conjunto de producoes de uma glc, remove as producoes vazias diretas e indiretas
        Exemplo: Considere "V" o simbolo de vazio e "T" o simbolo de terminal,
         {(A, ("V",)), (B, ("V",)), (C, ("V",)), (D, ("A","B","C","T"))} :
            {(D, ("A","B","C","T")), (D, ("A","B","T")), (D, ("A","C","T")), (D, ("B","C","T")),
            (D, ("A", "T")), (D, ("B","T")), (D, ("C","T")), (D, ("T",))}

        :return:
        """
        self.__remove_producoes_vazias_indiretas(self.__pop_producoes_vazias_diretas())
        self._producoes.add((self._simbolo_inicial, ("V",)))  # inclusao da palavra vazia

    def __pop_producoes_vazias_diretas(self):
        """
        Objetivo: Remove producoes diretas de producoes vazias e retorna as cabecas destas
        Exemplo: {(A, ("V",)), (B, ("V",)), (C, ("V",)), (D, ("A","B","C","T"))} :
                    {(D, ("A","B","C","T"))}, ["A", "B", "C"]
        :return: lista de cabecas das producoes excluidas
        :rtype: list
        """
        prod_vazias_dir = set()
        vars_com_producoes_vazias = set()
        for producao in self._producoes:
            if "V" in producao[1]:
                prod_vazias_dir.add(producao)
                vars_com_producoes_vazias.add(producao[0])
        self._producoes.difference_update(prod_vazias_dir)
        return vars_com_producoes_vazias

    def __remove_producoes_vazias_indiretas(self, vars_com_prod_vazias_dir):
        """
        Objetivo: Remove producoes indiretas de producoes vazias
        Exemplo: {(D, ("A","B","C","T"))} , ["A","B","C"] :
                    {(D, ("A","B","C","T")), (D, ("A","B","T")), (D, ("A","C","T")), (D, ("B","C","T")),
                    (D, ("A", "T")), (D, ("B","T")), (D, ("C","T")), (D, ("T",))}
        :param vars_com_prod_vazias_dir: lista de cabecas das producoes com producoes vazias diretas
        :return:
        """
        novas_producoes = []
        for producao in self._producoes:
            combinacoes = self.__get_combinacoes_de_variaveis_com_producao_vazia(producao[1], vars_com_prod_vazias_dir)
            for combinacao in combinacoes:
                if len(combinacao) != len(producao[1]):  # evita insercao de producao vazia
                    novas_producoes.append((producao[0], tuple(var for var in producao[1] if var not in combinacao)))
        self._producoes.update(novas_producoes)

    def __get_combinacoes_de_variaveis_com_producao_vazia(self, corpo_da_producao, vars_com_producoes_vazias_dir):
        """
        Objetivo: Dado o corpo de uma producao e lista da variaveis que produzem vazio diretamente, retorna
                    a combinacao da intersecao destes
        Exemplo: ("A","B","C,"D"), ["A", "B", "C"] : (("A",), ("B",), ("B",), ("A", "B"), ("A", "C"),
                                                        ("C", "B"), ("A", "B", "C"))
        :param corpo_da_producao: o corpo de uma producao qualquer da gramatica
        :type corpo_da_producao: tuple
        :param vars_com_producoes_vazias_dir: lista das variaveis que produzem vazio diretamente
        :type vars_com_producoes_vazias_dir: tuple
        :return: combinacao da intersecao entre corpo_da_producao e vars_com_producoes_vazias_dir
        :rtype: tuple
        """
        vars_com_prod_vazias_dir_nesse_corpo = set(corpo_da_producao).intersection(vars_com_producoes_vazias_dir)
        combinacoes = []
        for tamanho in range(len(vars_com_prod_vazias_dir_nesse_corpo) + 1):
            combinacoes.extend(tuple(combinations(vars_com_prod_vazias_dir_nesse_corpo, tamanho)))
        return tuple(combinacoes[1:])

    def __encontra_producoes_terminais(self, variavel):
        """
        Objetivo: encontrar todas as produções terminais de uma variável.
        :param variavel:
        :type variavel: str
        :return: produções encabeçadas por variavel que possuem terminais
        :rtype: set
        """

        possiveis_producoes = {producao for producao in self._producoes if producao[0] == variavel}
        producoes_terminais = set()

        for producao in possiveis_producoes:
            palavra = ''
            for simbolo in producao[1]:
                palavra = palavra + simbolo
            if palavra not in self._variaveis:
                producoes_terminais.add(producao)
        return producoes_terminais

    def remove_producoes_unitarias(self):
        """
        Objetivo: remover as produções unitárias da gramática
        :rtype: None
        """
        fechos = {variavel: set() for variavel in self._variaveis}

        for variavel in self._variaveis:
            vars_unitarias = set()
            for producao in self._producoes:
                if producao[0] == variavel and len(producao[1]) == 1 and producao[1][0] in self._variaveis:
                    vars_unitarias.add(producao[1][0])
            fechos[variavel] = vars_unitarias

        tamanhos = [len(fechos[variavel]) for variavel in fechos]
        tamanhos_novo = []
        while tamanhos != tamanhos_novo:
            for variavel in self._variaveis:
                for cabeca in fechos:
                    if variavel in fechos[cabeca]:
                        fechos[cabeca] = fechos[cabeca].union(fechos[variavel])
            tamanhos = tamanhos_novo
            tamanhos_novo = [len(fechos[variavel]) for variavel in fechos]

        for cabeca in fechos:
            if cabeca in fechos[cabeca]:
                fechos[cabeca].remove(cabeca)

        p1 = set()
        for variavel in self._variaveis:
            p1 = p1.union(self.__encontra_producoes_terminais(variavel))

        for variavel in fechos:
            for B in fechos[variavel]:
                producoes_terminais = self.__encontra_producoes_terminais(B)
                producoes_terminais = {(variavel, prod[1]) for prod in producoes_terminais}
                p1 = p1.union(producoes_terminais)

        self._producoes = p1

    def remove_simbolos_inuteis(self):
        """
        Objetivo: Dada uma glc, remove as variáveis inuteis, suas produções
        e as produções que as contém
        Exemplo:
        Dados os conjuntos de produções e variáveis
        Variáveis: {S,A,B,C,D}
        Produções: {S->AC|AA|b, A->aC|a, B->BC, C->c}
        Remove as variáveis B e C e suas produções e as produções que as contém, resultando em:
        Variáveis: {S,A,C}
        Produções: {S->AC|AA|b, A->aC|a, C->c}
        """
        self.__remove_variaveis_nao_terminais_e_producoes_com_elas_no_corpo()
        self.__remove_simbolos_nao_atingiveis()

    def __remove_producoes_que_tenham_variaveis_nao_terminais_no_corpo(self):
        """
        Objetivo: Dado um conjunto de produções, remove todas aquelas que tenham
        variaveis nao terminais
        Exemplo:
        Produções: {S->AC|AA|b, A->aC|a, B->D, C->c}
        Gera
        Produções: {S->AC|AA|b, A->aC|a, C->c}
        """
        variaveis_e_terminais = self.terminais | self.variaveis
        novo_set_producoes = set()
        for producao in self.producoes:
            if all(item in variaveis_e_terminais for item in producao[1]):
                novo_set_producoes.add(producao)

        self.producoes.intersection_update(novo_set_producoes)

    def __remove_producoes_com_variaveis_ou_terminais_nao_pertencentes_a_gramatica(self):
        """Objetivo: Dado um conjunto de produções, variaveis e terminais, remove todas as produções
        que que contenham variaveis ou terminais nao pertencentes a gramatica
        Exemplo:
        Variaveis: {A,S,C}
        Terminais: {a,b,c}
        Produções: {S->AC|AA|b, A->aC|a, B->D, C->c|d}
        Gera
        Produções: {S->AC|AA|b, A->aC|a, C->c}
        """
        variaveis_e_terminais = self.terminais | self.variaveis
        novo_set_producoes = set()
        for producao in self.producoes:
            if(producao[0] in self.variaveis):
                if all(item in variaveis_e_terminais for item in producao[0]):
                    novo_set_producoes.add(producao)
        self.producoes.intersection_update(novo_set_producoes)

    def __remove_variaveis_nao_terminais_e_producoes_com_elas_no_corpo(self):
        """
        Remove as variais que nao geram terminais direta ou indiretamente
        Exemplo:
        Dada uma gramatico que tenha
        Variáveis: {S,A,B,C,D}
        Produções: {S->AC|AA|b, A->aC|a, B->BC, C->c}
        A gramatica é modificada e fica:
        Variáveis: {S,A,C}
        Produções: {S->AC|AA|b, A->aC|a, C->c}
        """
        variaveis_terminais = set()
        terminais_absolutos = set() | self.terminais
        tamanho_antigo = 0

        while True:
            for producao in self.producoes:
                if all(item in terminais_absolutos for item in producao[1]):
                    terminais_absolutos.add(producao[0])
                    variaveis_terminais.add(producao[0])
            tamanho_novo = len(variaveis_terminais)

            if tamanho_antigo == tamanho_novo:
                break
            else:
                tamanho_antigo = tamanho_novo

        self.variaveis.intersection_update(variaveis_terminais)
        self.__remove_producoes_que_tenham_variaveis_nao_terminais_no_corpo()
        terminais_absolutos.clear()

    def __remove_simbolos_nao_atingiveis(self):
        """
        Objetivo: Remover variaveis e terminais nao atingiveis e producoes que os contenham
        Exemplo:
        Dada uma gramatico que tenha
        Variáveis: {S,A,C,D}
        Terminais: {a,b,c,d}
        Produções: {S->AC|AA|b, A->aC|a, C->c, D->a|d}
        A gramatica é modificada e fica:
        Variáveis: {S,A,C}
        Terminais: {a,b,c}
        Produções: {S->AC|AA|b, A->aC|a, C->c}
        """
        terminais = set()
        variaveis = set()
        variaveis.add(self.simbolo_inicial)
        len_terminais_antigo = 0
        len_terminais_novo = 0
        len_variaveis_antigo = 0
        len_variaveis_novo = 0
        while True:
            for producao in self.producoes:
                if producao[0] in variaveis:
                    for item in producao[1]:
                        if item in self.variaveis:
                            variaveis.add(item)
                        elif item in self.terminais:
                            terminais.add(item)
            len_terminais_novo = len(terminais)
            len_variaveis_novo = len(variaveis)
            if len_terminais_antigo == len_terminais_novo and len_variaveis_antigo == len_variaveis_novo:
                break
            else:
                len_terminais_antigo = len_terminais_novo
                len_variaveis_antigo = len_variaveis_novo
        self.variaveis.intersection_update(variaveis)
        self.terminais.intersection_update(terminais)

        self.__remove_producoes_que_tenham_variaveis_nao_terminais_no_corpo()

    def chonskfy(self):
        """
        Objetivo: converte uma gramatica qualquer para o forma normal de chonsky
        :return:
        """
        # Criacao da lista de variaveis disponiveis
        lista_vars = "A B C D E F G H I J L M N O P Q R S T U V X W Y Z".split()
        # adiciona a combinacao 2 a 2 dos termos da lista na lista
        lista_vars.extend([b + c for c in lista_vars for b in lista_vars])

        # Retira as variaveis jah utilizadas
        vars_disponiveis = [vars for vars in lista_vars if vars not in self._variaveis]

        vars_disponiveis = self.__somente_vars_em_producoes_maioresq2(vars_disponiveis)
        self.__remove_producoes_maioresq2(vars_disponiveis)

    def __somente_vars_em_producoes_maioresq2(self, variaveis_disponiveis):
        """
        Objetivo: Garantir que há somente variáveis do lado direito das produções de comprimento ≥ 2
        Exemplo:  ("A", ("a", "B")) : ("A",(<variavel_livre_disponivel>, "B")), (<variavel_livre_disponivel>, ("a",))
        """

        producoes = list(self._producoes)
        dict_vars_novas = dict()

        for producao in range(len(producoes)):

            # tamanho da corpo de cada producao
            tamanho_corpo = len(producoes[producao][1])

            # Se houver terminais em producoes maiores que 2, troca por uma nova variavel
            if tamanho_corpo > 1:
                for item_corpo in range(tamanho_corpo):
                    if producoes[producao][1][item_corpo] in self._terminais:
                        # copia da producao
                        producao_substituta = list(producoes[producao][1])
                        # Verifica se ja existe uma variavel que produza o terminal. Se sim retorna a variavel, se nao
                        #    pega uma variavel nova e insere no dicionario
                        nova_variavel = dict_vars_novas.setdefault(producao_substituta[item_corpo],
                                                                   variaveis_disponiveis[0])
                        # troca terminal por uma variavel
                        producao_substituta[item_corpo] = nova_variavel

                        # adiciona a variavel novas as variaveis da gramatica
                        self._variaveis.update(nova_variavel)

                        # Atualiza as producoes
                        producoes.append((nova_variavel, producoes[producao][1][item_corpo]))
                        producoes[producao] = (producoes[producao][0], tuple(producao_substituta))

                        # Retira variaveis jah utilizadas das lista de vars disponiveis
                        if nova_variavel == variaveis_disponiveis[0]:
                            variaveis_disponiveis.pop(0)

        self._producoes = set(producoes)
        return variaveis_disponiveis

    def __remove_producoes_maioresq2(self, vars_disponiveis):
        """
        Objetivo: Garantir que há exatamente duas variáveis no lado direito das produções de uma gramatica
        :param vars_disponiveis: lista das variaveis que podem ser usadas para criar producoes novas
        :type vars_disponiveis: list
        :return:
        """
        producoes = list(self._producoes)
        for producao in producoes:
            # Atualiza as producoes para que elas sejam de tamanho 2 no maximo
            if len(producao[1]) > 2:
                novas_producoes = self.__separa_producao(producao, vars_disponiveis)
                self._producoes.remove(producao)
                self._producoes.update(novas_producoes)

    def __separa_producao(self, producao, vars_disponiveis):
        """
        Objetivo: Garantir que há exatamente duas variáveis no lado direito de uma producao
        Exemplo ("A", ("B","C", "D")), ["E"] :  ("A", ("E", "D")), ("E",("B","C"))
        :param vars_disponiveis: lista das variaveis que podem ser usadas para criar producoes novas
        :type vars_disponiveis: list
        :param producao: um producao da gramatica
        :type producao: tuple
        :return:
        """
        producao = [producao[0], list(producao[1])]
        tamanho_producao = len(producao[1])
        novas_producoes = []
        vars_novas = []

        # Vai reduzindo o tamanho da producao enquanto ela for maior que 2
        while tamanho_producao > 2:
            vars_novas.clear()
            # Agrupa de 2 em 2 os simbolos que estao na producao junto com as suas novas cabecas
            #   e adiciona nas novas producoes da gramatica
            for index in range(0, tamanho_producao - 1, 2):
                novas_producoes.append((vars_disponiveis[0], tuple(producao[1][index:index + 2])))
                vars_novas.append(vars_disponiveis[0])
                vars_disponiveis.pop(0)
            if tamanho_producao % 2 == 1:
                vars_novas.append(producao[1][-1])
            # adiciona nas variaveis da gramatica as gramatica as novas vars utilizadas como cabecas no agrupamento
            self._variaveis.update(vars_novas)
            # atualiza a producao com as novas variaveis no corpo
            producao = [producao[0], vars_novas.copy()]

            tamanho_producao = len(producao[1])
        novas_producoes.append((producao[0], tuple(vars_novas)))
        return novas_producoes

    def reconhece_palavra(self, palavra):
        """
        Objetivo: identificar se uma palavra pertence a gramatica
        :param palavra:
        :type palavra: str
        :return: Se a palavra pertence ou nao a gramatica
        :rtype: bool
        """
        self.__cria_tabela(palavra)
        self._tabela_CYK = self._tabela_CYK[::-1]
        return self._simbolo_inicial in self._tabela_CYK[0][0]

    def __cria_tabela(self, palavra):
        self.__cyk_primeira_etapa(palavra)
        self.__cyk_segunda_etapa(len(palavra))

    def __cyk_primeira_etapa(self, palavra):
        """
        Objetivo: prencher a tabela com as letras da palavra, assim como com as variaveis que produzem cada letra
        :param palavra: a palavra a ser reconhecida pela gramatica
        :type palavra: str
        :return:
        """
        self._tabela_CYK = []
        self._tabela_CYK.append(list(palavra))
        self._tabela_CYK.append([])
        for terminal in self._tabela_CYK[0]:
            self._tabela_CYK[1].append(set([cabeca for cabeca, corpo in self._producoes if ''.join(corpo) == terminal]))

    def __cyk_segunda_etapa(self, tamanho_palavra):
        """
        Objetivo: prencher a tabela com as variaveis que produzem 2 variaveis
        :param tamanho_palavra: o tamanho da palavra a ser reconhecida pela gramatica
        :type tamanho_palavra: int
        :return:
        """
        # Percorre as linhas da tabela
        for s in range(2, tamanho_palavra + 1):
            linha = []
            # Percorre as colunas da tabela
            for r in range(0, tamanho_palavra - s + 1):
                celula_mestre = set()
                for k in range(1, s):
                    # Percorre em ordens opostas as celulas abaixo e na diagonal da celula mestre
                    elemento_b = self._tabela_CYK[k][r]  # Elemento abaixo
                    elemento_c = self._tabela_CYK[s - k][r + k]  # Elemento na diagonal
                    bc_combinacoes = [[b, c] for c in elemento_c for b in elemento_b]  # combinacao 2 a 2 dos elementos
                    for cabeca, corpo in self._producoes:
                        for producao in bc_combinacoes:
                            # Se a combinacao for valida, adiciona o pai de tal producao na celula mestre
                            if list(corpo) == producao:
                                celula_mestre.add(cabeca)
                # adiciona a celula mestre na linha atual
                linha.append(celula_mestre)
            self._tabela_CYK.append(linha)

    def __gera_arvores(self, linha_raiz, coluna_raiz):
        """
        Objetivo: retornar todas as árvores de derivação cuja raíz está na
        em self._tabela_CYK[linha_raiz][coluna_raiz]
        :param linha_raiz:
        :type linha_raiz: int
        :param coluna_raiz:
        :type coluna_raiz: int
        :return: todas as arvores de derivação com raíz de índices linha_raiz,
        coluna_raiz
        :rtype: list
        """

        tabela = self._tabela_CYK
        arvores = []
        if linha_raiz == len(tabela) - 2:
            for raiz in tabela[linha_raiz][coluna_raiz]:
                teste = ArvoreDerivacao(tabela[linha_raiz + 1][coluna_raiz])
                arvores.append(ArvoreDerivacao(raiz, teste, None))
        else:
            for raiz in tabela[linha_raiz][coluna_raiz]:
                for r, s in zip(range(len(tabela) - 2, linha_raiz, -1), range(linha_raiz + 1, len(tabela) - 1)):
                    sub_r = self.__gera_arvores(r, coluna_raiz)
                    sub_s = self.__gera_arvores(s, coluna_raiz + (s - linha_raiz))
                    for arv_r in sub_r:
                        for arv_s in sub_s:
                            if (raiz, (arv_r.conteudo, arv_s.conteudo)) in self._producoes:
                                arvores.append(ArvoreDerivacao(raiz, arv_r, arv_s))
        return arvores

    def arvores_de_derivacao(self):
        """
        Objetivo: imprimir todas as árvores de derivação que geram a palavra
        parseada
        :rtype: None
        """

        arvores = self.__gera_arvores(0, 0)

        arvore_valida = (lambda arvore: arvore.palavra_gerada() == "".join(self.tabela_CYK[-1])
                                        and arvore.conteudo == self._simbolo_inicial)

        arvores = list(filter(arvore_valida, arvores))
        print("{} ÁRVORES DE DERIVAÇÃO ENCONTRADAS\n".format(len(arvores)))

        for arvore in arvores:
            arvore.print_arvore()
            print("----------------------------------------\n")

    def __str__(self):
        return '''\nG = (V, T, P, {}), ondse:
        \nConjunto de variáveis: \n\tV = {}
        \nConjunto de símbolos terminais: \n\tT = {}
        \nRegras de produção: \nP = {}
        \nSímbolo inicial: {}'''.format(self._simbolo_inicial, self._variaveis, self._terminais,
                                        pprint.pformat(self._producoes), self._simbolo_inicial)


if __name__ == '__main__':
    arquivo = input("Digite o caminho do arquivo: ")
    g = Gramatica(arquivo)
    # print(g)
    # g.remove_producoes_unitarias()
    # print(g)
