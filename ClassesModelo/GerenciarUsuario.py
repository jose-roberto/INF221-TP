from Usina import Usina


class GerenciarUsuario:
    def __init__(self):
        self.users: Usina = []
        self.user: Usina = None

    def realizar_cadastro(self, nome: str, email: str, senha: str):
        pass

    def autenticar_usuario(self, cnpj: str, senha: str):
        pass

    def alterar_dados(self, usina: Usina):
        pass

    def realizar_logout(self, usina: Usina):
        pass

    def excluir_conta(self, usina: Usina):
        pass
