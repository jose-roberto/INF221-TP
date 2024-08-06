from Dados import Dados

class DadosProducao(Dados):
    def __init__(self, data, id):
        super().__init__(data, id)
        self.producao:float
        self.consumo:float