
class ArvoreDerivacao:
    def __init__(self, conteudo, esquerda=None, direita=None):
        self._conteudo = conteudo
        self._esquerda = esquerda
        self._direita = direita

    @property
    def conteudo(self):
        return self._conteudo

    def print_arvore(self, nivel=1):
        print("{:>{espacos}}".format(self._conteudo, espacos=nivel))
        if self._direita:
            self._direita.print_arvore(nivel + 1)
        if self._esquerda:
            self._esquerda.print_arvore(nivel + 1)

    def palavra_gerada(self):

        if not self._esquerda and not self._direita:
            return self._conteudo

        if self._esquerda:
            prefixo = self._esquerda.palavra_gerada()
        else:
            prefixo = ""

        if self._direita:
            sufixo = self._direita.palavra_gerada()
        else:
            sufixo = ""

        return prefixo + sufixo

if __name__ == '__main__':
    a = ArvoreDerivacao('a')
    b = ArvoreDerivacao('b')
    A = ArvoreDerivacao('A', a)
    B = ArvoreDerivacao('B', b)
    S = ArvoreDerivacao('S', A, B)
    S.print_arvore()
