from Dados import Dados


class DadosIntegridade(Dados):
    def __init__(self, id: int, data: str):
        super().__init__(id, data)
        self.integridade: float
