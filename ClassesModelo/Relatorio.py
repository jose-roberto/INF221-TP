from abc import ABC


class Relatorio(ABC):
    def __init__(self, banco):
        self.banco = banco

    def gerar_relatorio(self):
        # pegar os dados, organizar eles, definir estrutura, chamar exportar
        pass

    def exportar(self):
        pass
