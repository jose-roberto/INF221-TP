class Usina:
    def __init__(self, nome, email, senha, cnpj, telefone, localizacao):
        self.nome: str = nome
        self.email:str = email
        self.senha:str = senha
        self.CNPJ:str = cnpj
        self.telefone:str = telefone
        self.localizacao:str = localizacao

    def gerar_relatorios(self, dados, tipo_relatorio):
        print('oi')