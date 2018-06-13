
class ArvoreDerivacao:
    def __init__(self, conteudo, esquerda=None, direita=None):
        self._conteudo = conteudo
        self._esquerda = esquerda
        self._direita = direita

    def print_arvore(self, nivel=1):
        print("{:=>{espacos}}".format(self._conteudo, espacos=nivel))
        if self._direita:
            self._direita.print_arvore(nivel + 1)
        if self._esquerda:
            self._esquerda.print_arvore(nivel + 1)


if __name__ == '__main__':
    a = ArvoreDerivacao('a')
    b = ArvoreDerivacao('b')
    A = ArvoreDerivacao('A', a)
    B = ArvoreDerivacao('B', b)
    S = ArvoreDerivacao('S', A, B)
    S.print_arvore()
