from Dados import Dados


class DadosProducao(Dados):
    def __init__(self, id: int, data: str):
        super().__init__(id, data)
        self.producao: float
        self.consumo: float
