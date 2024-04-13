import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, time


# Carregar o banco de dados do acelerômetro com todos os sujeitos
data_geral = pd.read_csv('Resultado AF.csv', sep=';')


class ProcessaAcelerometro():
    
    def __init__(self, dados):
        self.dados = dados
        self.usuario = input('Por favor, digite o ID do usuário cujos dados serão processados: ')
        print('O usuário selecionado foi o: ' + str(self.usuario))
        self.usuario_num = int(self.usuario)
        self.data = None
        
        self.FiltrarUsuario()
        self.ConverteEmData()
        print('Conversão do formato data realizada com sucesso!')
    
        
    def FiltrarUsuario(self):
        self.data = self.dados.loc[self.dados['IDPerfil'] == self.usuario_num]
        n_linhas = len(self.data.iloc[:, 0])
        print('Os dados carregados possuem ' + str(n_linhas) + ' linhas')
        

    def ConverteEmData(self):
        self.data['Date'] = pd.to_datetime(self.data['Date'], format='%d-%m-%Y')
        
        



dados_acc_processados = ProcessaAcelerometro(data_geral)
