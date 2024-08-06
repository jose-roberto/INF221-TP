class Usina:
    def __init__(self, cnpj: str, nome: str, email: str, senha: str, localizacao: str, telefone: str):
        self.cnpj: str = cnpj
        self.nome: str = nome
        self.email: str = email
        self.senha: str = senha
        self.localizacao: str = localizacao
        self.telefone: str = telefone

    def gerar_relatorios(self, tipo_relatorio: str, dados):
        pass
