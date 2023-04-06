
class ArvoreDerivacao:
    def __init__(self, conteudo, esquerda=None, direita=None):
        self._conteudo = conteudo
        self._esquerda = esquerda
        self._direita = direita
        self.children = [self._esquerda, self._direita]

    @property
    def conteudo(self):
        return self._conteudo

    def print_arvore(self, nivel=1):
        """
        Objetivo: imprimir toda a árvore, cuja raíz tem o nivel fornecido.
        :param nivel:
        :type nivel: int
        :rtype: None
        """
        print("Nível {espacos}: {:>{espacos}}".format(self._conteudo, espacos=nivel))
        if self._direita:
            self._direita.print_arvore(nivel + 1)
        if self._esquerda:
            self._esquerda.print_arvore(nivel + 1)

    def palavra_gerada(self):
        """
        Objetivo: Obter a palavra gerada pela árvore de derivação.
        :return: Palavra derivada.
        :rtype: str
        """
        if not self._esquerda and not self._direita:
            return self._conteudo

        prefixo = self._esquerda.palavra_gerada() if self._esquerda else ""
        sufixo = self._direita.palavra_gerada() if self._direita else ""
        return prefixo + sufixo

if __name__ == '__main__':
    a = ArvoreDerivacao('a')
    b = ArvoreDerivacao('b')
    A = ArvoreDerivacao('A', a)
    B = ArvoreDerivacao('B', b)
    S = ArvoreDerivacao('S', A, B)
    S.print_arvore()
