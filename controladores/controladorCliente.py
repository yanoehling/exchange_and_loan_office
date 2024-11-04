from abstratas.absControlador import Controlador
from telas.telaCliente import TelaCliente
from telas.telaEmprestimo import TelaEmprestimo
from telas.telaTroca import TelaTroca
from entidades.organizacao import Organizacao
from entidades.pessoa import Pessoa
from controladores.funcoes import eh_pessoa

class ControladorCliente(Controlador):
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_cliente = TelaCliente()
        self.__tela_emprestimo = TelaEmprestimo()
        self.__tela_troca = TelaTroca()
        self.__pessoas = []
        self.__organizacoes = []

    def abre_tela(self):
        lista_comandos = {1: self.mostra_dados, 2: self.inclui, 3: self.exclui, 4: self.altera, 5: self.mostra_todas, 0: self.voltar_tela}
        while True:
            comando = lista_comandos[self.__tela_cliente.tela_opcoes()]
            comando()

    def mostra_dados(self):
        id = self.__tela_cliente.ver_dados()
        existente = False
        eh_pes = eh_pessoa(id)
        if eh_pes == True: #cpf
            for pessoa in self.__pessoas:
                if pessoa.id == id:
                    self.__tela_cliente.mostrar_dados({'nome': pessoa.nome, 'id': pessoa.id, 
                                                       'credito_usd': pessoa.credito_usd, 'idade':pessoa.idade})
                    existente = True
        elif eh_pes == False: #cnpj
            for org in self.__organizacoes:
                if org.id == id:
                    self.__tela_cliente.mostrar_dados({'nome': org.nome, 'id': org.id, 'credito_usd': org.credito_usd})
                    existente = True
        if not existente and eh_pes != None:
            print("\n## Nenhum cliente registrado com esta identidade ##\n")

    def pega_objeto(self, id):
        for cli in self.__pessoas:
            if cli.id == id:
                return cli 
        for cli in self.__organizacoes:
            if cli.id == id:
                return cli 

    def inclui(self):
        dados_cliente = self.__tela_cliente.cadastrar_dados()
        if dados_cliente is not None:
            if eh_pessoa(dados_cliente['id']) and 'idade' in dados_cliente: 
                self.__pessoas.append(Pessoa(dados_cliente['nome'], dados_cliente['id'], 0, dados_cliente['idade']))
            elif not eh_pessoa(dados_cliente['id']):
                self.__organizacoes.append(Organizacao(dados_cliente['nome'], dados_cliente['id'], 0))
            else:
                print('\n## Dados incorretos para o tipo de cliente ##\n')

    def exclui(self):
        id = self.__tela_cliente.excluir()
        cliente = self.pega_objeto(id)
        if cliente != None:
            if eh_pessoa(id):
                self.__pessoas.remove(cliente)
            else:
                self.__organizacoes.remove(cliente)
            self.__tela_cliente.mostrar_msg(f'Cliente "{cliente.nome}" excluído.')
        else:
            self.__tela_cliente.mostrar_msg('\n## Nenhum cliente cadastrado com esta identidade ##\n')

    def mostra_todas(self):
        if len(self.__organizacoes) > 0:
            for org in self.__organizacoes:
                self.__tela_cliente.mostrar_dados({'nome': org.nome, 'id': org.id, 'credito_usd': org.credito_usd})
        else:
            self.__tela_cliente.mostrar_msg("Nenhuma Organização cadastrada.\n")

        if len(self.__pessoas) > 0:
            for pessoa in self.__pessoas:
                self.__tela_cliente.mostrar_dados({'nome': pessoa.nome, 'id': pessoa.id, 'idade': pessoa.idade, 'credito_usd': pessoa.credito_usd})
        else:
            self.__tela_cliente.mostrar_msg("Nenhuma Pessoa cadastrada.\n")
        

    def altera(self):
        self.mostra_todas()
        id = self.__tela_cliente.alterar_dados()
        id_a_alterar = self.pega_objeto(id)
        if id_a_alterar != None:
            lista = self.__pessoas if len(id) == 11 else self.__organizacoes
            for cliente in lista:
                if cliente.id == id_a_alterar.id:
                    novo_cliente = self.__tela_cliente.cadastrar_dados()
                    cliente.nome = novo_cliente['nome']
                    cliente.id = novo_cliente['id']
                    if len(id) == 11:
                        cliente.idade = novo_cliente['idade']
        else:
            self.__tela_cliente.mostrar_msg('\n## Organização não existe ##\n')
            
    
    def mostra_transacoes(self):
        id = self.__tela_cliente.ver_dados()
        existente = False
        eh_pes = eh_pessoa(id)
        if eh_pes == True: #cpf
            for pessoa in self.__pessoas:
                if pessoa.id == id:
                    cliente = pessoa
                    existente = True
        elif eh_pes == False: #cnpj
            for org in self.__organizacoes:
                if org.id == id:
                    cliente = org
                    existente = True
        if existente:
            if len(cliente.emprestimos_pedidos) > 0:
                print('\n- EMPRESTIMOS PEDIDOS: \n')
                for emps in cliente.emprestimos_pedidos:
                    for t in emps:
                        cliente_id = cliente.cpf if eh_pessoa(cliente) else cliente.cnpj
                        emp_id = t.emprestador.cpf if eh_pessoa(t.emprestador) else t.emprestador.cnpj
                        self.__tela_emprestimo.mostrar_dados({'id':t.id, 'cliente':cliente_id, 'emprestador':emp_id, 'moeda':t.moeda.nome, 'quantia':t.quantia, 
                                                            'data_do_repasse':t.data_do_repasse, 'data_devolvida':t.data_devolvida, 'data_pretendida':t.data_pretendida, 
                                                            'juros_normal':t.juros_normal, 'juros_mensal_atraso':t.juros_mensal_atraso})
            else:
                print('\nEste cliente não pediu nenhum empréstimo. \n')

            if len(cliente.emprestimos_concedidos) > 0:
                print('\n- EMPRESTIMOS CONCEDIDOS: \n')
                for emps in cliente.emprestimos_concedidos:
                    for t in emps:
                        cliente_id = cliente.cpf if eh_pessoa(cliente) else cliente.cnpj
                        emp_id = t.emprestador.cpf if eh_pessoa(t.emprestador) else t.emprestador.cnpj
                        self.__tela_emprestimo.mostrar_dados({'id':t.id, 'cliente':cliente_id, 'emprestador':emp_id, 'moeda':t.moeda.nome, 'quantia':t.quantia, 
                                                            'data_do_repasse':t.data_do_repasse, 'data_devolvida':t.data_devolvida, 'data_pretendida':t.data_pretendida, 
                                                            'juros_normal':t.juros_normal, 'juros_mensal_atraso':t.juros_mensal_atraso})
            else:
                print('\nEste cliente não concedeu empréstimos a ninguém. \n')

            if eh_pes:
                if len(cliente.trocas_feitas) > 0:
                    print('\n- TROCAS CAMBIAIS FEITAS: \n')
                    for trocas in cliente.trocas_feitas:
                        for t in trocas:
                            self.__tela_troca.mostrar_dados({'id': t.id, 'id_pessoa':cliente.cpf, 'data': t.data, 
                                                            'moeda_entrada': t.moeda_entrada.nome, 'moeda_saida': t.moeda_saida.nome, 
                                                            'quantidade_entrada': t.quantidade_entrada, 'quantidade_saida': t.quantidade_saida, 
                                                            'juros': t.porcentagem_juros})   
                else:
                    print('\nEste cliente não fez nenhuma troca cambial. \n')
        elif eh_pes != None:
            print("\n## Nenhum cliente registrado com esta identidade ##\n")


    def voltar_tela(self):
        self.__controlador_sistema.abre_tela()
