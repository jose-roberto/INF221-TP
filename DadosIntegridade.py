from Dados import Dados

class DadosIntegridade(Dados):
    def __init__(self, data, id):
        super().__init__(data, id)
        self.integridade:float