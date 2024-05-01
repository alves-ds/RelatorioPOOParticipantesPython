import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, time
import tkinter as Tkinter, tkinter.filedialog as tkFileDialog
import customtkinter



class ProcessaAcelerometro():
    
    def __init__(self):
        self.dados = None
        self.usuario = None
        self.usuario_num = None
        self.data = None
        self.data_inicio = None
        self.data_final = None
        self.sem1 = list()
        self.sem2 = list()
        self.sem3 = list()
        self.sem4 = list()
        self.sem5 = list()
        self.intensidades = ['Leve', 'Moderada', 'Vigorosa']
        self.dias_da_semana = ['Segunda-feira', 'Terça-feira','Quarta-feira', 'Quinta-feira','Sexta-feira', 'Sábado','Domingo']
        self.leve_sem1 = None
        self.leve_sem2 = None
        self.leve_sem2 = None
        self.leve_sem2 = None
        self.leve_sem2 = None
        self.moderada_sem1 = None
        self.moderada_sem2 = None
        self.moderada_sem3 = None
        self.moderada_sem4 = None
        self.moderada_sem5 = None
        self.vigorosa_sem1 = None
        self.vigorosa_sem2 = None
        self.vigorosa_sem3 = None
        self.vigorosa_sem4 = None
        self.vigorosa_sem5 = None
        self.diretorio = None
        
        self.TelaInicial()
        
         

    def TelaInicial(self):
        
        janela_input = customtkinter.CTk()
        janela_input.geometry("500x500")

        
        def clique():
        
            self.usuario = ID.get()
            self.data_inicio = data_inicio_monitoramento.get()
            self.data_final = data_fim_monitoramento.get()
            self.usuario_num = int(self.usuario)
            janela_input.destroy()
            self.getfile()
            self.FiltrarUsuario()
            self.ConverteEmData()
            print('Conversão do formato data realizada com sucesso!')
            self.FiltrarDadosData()
            print('Agora vamos ordenar o banco de dados!')
            self.OrdenarBanco()
            self.SalvarBancoDados() # Crie uma função para perguntar se a pessoa deseja salvar o banco de dados
            self.DividirBancoEmSemanas()
            print('...')
            print('Aguarde os teus dados estão sendo processados...')
            print('...')
            self.ProcessarDadosSemanas()
            print('Dados processados com sucesso!')
            self.CriarGraficos()
            
            janela_input.quit()

        
        texto_id = customtkinter.CTkLabel(janela_input, text='Insira o ID do usuário abaixo')
        texto_id.pack(padx=10, pady=10)
        ID = customtkinter.CTkEntry(janela_input, placeholder_text='ex: 738')
        ID.pack(padx=10, pady=10)
        texto_data_inicio = customtkinter.CTkLabel(janela_input, text='Insira a data de início do monitoramento. exemplo: 2023-08-07')
        texto_data_inicio.pack(padx=10, pady=10)
        data_inicio_monitoramento = customtkinter.CTkEntry(janela_input, placeholder_text='Insira a data de início do monitoramento')
        
        data_inicio_monitoramento.pack(padx=10, pady=10)
        
        texto_data_fim = customtkinter.CTkLabel(janela_input, text='Insira a data de fim do monitoramento. exemplo: 2023-09-10')
        texto_data_fim.pack(padx=10, pady=10)
        data_fim_monitoramento = customtkinter.CTkEntry(janela_input, placeholder_text='Insira a data de fim do monitoramento')
        data_fim_monitoramento.pack(padx=10, pady=10)

        botao = customtkinter.CTkButton(janela_input, text='Continuar', command=clique)
        botao.pack(padx=10, pady=10)
        

        janela_input.mainloop()

        


    def getfile(self):
        root = Tkinter.Tk()
        root.after(100, root.focus_force)
        root.after(200,root.withdraw)    
        data_geral = tkFileDialog.askopenfilename(parent=root,title='Selecione o arquivo')   
        self.diretorio = data_geral[0:len(data_geral)-16]
        self.dados = pd.read_csv(data_geral, sep=';')      


    def FiltrarUsuario(self):
        self.data = self.dados.loc[self.dados['IDPerfil'] == self.usuario_num]
        n_linhas = len(self.data.iloc[:, 0])
        print('Os dados carregados possuem ' + str(n_linhas) + ' linhas')
        

    def ConverteEmData(self):
        self.data['Date'] = pd.to_datetime(self.data['Date'], format='%d-%m-%Y')
        
    def ConverterEmString(self):
        self.data['Date'] = self.data['Date'].dt.strftime('%d-%m-%Y')
        


    def FiltrarDadosData(self):
        # Filtrar o DataFrame para incluir apenas as datas dentro do intervalo especificado
        self.data = self.data[(self.data['Date'] >= self.data_inicio) & (self.data['Date'] <= self.data_final)]
        print('Dados filtrados com sucesso, correspondentes ao período de ' + str(self.data_inicio) + ' e ' + str(self.data_final))


    def OrdenarBanco(self):
        # Criar a coluna "ordem" com base na ordem das datas dentro do intervalo
        self.data['ordem'] = self.data['Date'].rank(method='dense').astype(int)
        
        # Ordenar o banco de dados
        self.data = self.data.sort_values(by='ordem')
        
        print('Dados ordenados com sucesso!')


    def SalvarBancoDados(self):
        #Salvar os dados do sujeito na pasta
        self.data.to_excel(self.diretorio+'data.xlsx', index=False) 


    def DividirBancoEmSemanas(self):
        #Dividir o banco de dados do sujeito em cada uma das 5 semanas
        self.sem1 = self.data.iloc[0:7]
        self.sem2 = self.data.iloc[7:14]
        self.sem3 = self.data.iloc[14:21]
        self.sem4 = self.data.iloc[21:28]
        self.sem5 = self.data.iloc[28:35]


    def ProcessarDadosSemanas(self):
        #dados da semana 1 FLEEM
        #AF leve
        leve_sem1 = self.sem1['Ligth'].values.tolist() #CRIAR VARIÁVEL GLOBAL
        #leve_sem1 = list(map(lambda x: str(x), leve_sem1))


        # Definir os valores de horas por dia para o gráfico do comportamento diário
        leve_sem1 = [int(h.split(":")[0]) + int(h.split(":")[1]) / 100 for h in leve_sem1]
        self.leve_sem1 = leve_sem1

        # Converter os valores para o formato datetime para poder converter as horas em minutos
        self.sem1['Ligth'] = self.sem1['Ligth'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())

        # Convertendo as horas para minutos
        self.sem1['leve_minutos'] = self.sem1['Ligth'].apply(lambda x: x.hour * 60 + x.minute + x.second / 60)

        #Salvandos os valores de minutos em uma lista para poder somar a quantia semanal
        leve_sem1min = self.sem1['leve_minutos'].values.tolist()


        #AF moderada
        moderada_sem1 = self.sem1['Moderate'].values.tolist()
        moderada_sem1 = [int(h.split(":")[0]) + int(h.split(":")[1]) / 100 for h in moderada_sem1]
        self.moderada_sem1 = moderada_sem1

        # Converter os valores para o formato datetime para poder converter as horas em minutos
        self.sem1['Moderate'] = self.sem1['Moderate'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())

        # Convertendo as horas para minutos
        self.sem1['moderada_minutos'] = self.sem1['Moderate'].apply(lambda x: x.hour * 60 + x.minute + x.second / 60)

        #Salvandos os valores de minutos em uma lista para poder somar a quantia semanal
        moderada_sem1min = self.sem1['moderada_minutos'].values.tolist()


        #AF vigorosa
        vigorosa_sem1 = self.sem1['Vigorous'].values.tolist()
        strong_sem1 = self.sem1['Strong'].values.tolist()
        strong_sem1 = [int(h.split(":")[0]) + int(h.split(":")[1]) / 100 for h in strong_sem1]
        vigorosa_sem1 = [int(h.split(":")[0]) + int(h.split(":")[1]) / 100 for h in vigorosa_sem1]
        vigorosa_sem1 = [vigorosa_sem1 + strong_sem1 for vigorosa_sem1, strong_sem1 in zip(vigorosa_sem1, strong_sem1)]
        self.vigorosa_sem1 = vigorosa_sem1


        # Converter os valores para o formato datetime para poder converter as horas em minutos
        self.sem1['Vigorous'] = self.sem1['Vigorous'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())
        self.sem1['Strong'] = self.sem1['Strong'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())


        # Convertendo as horas para minutos
        self.sem1['vigorosa_minutos'] = self.sem1['Vigorous'].apply(lambda x: x.hour * 60 + x.minute + x.second / 60)
        self.sem1['strong_minutos'] = self.sem1['Strong'].apply(lambda x: x.hour * 60 + x.minute + x.second / 60)
        self.sem1['vig+strong_minutos'] = self.sem1['vigorosa_minutos'] + self.sem1['strong_minutos']

        vigorosa_sem1min = self.sem1['vig+strong_minutos'].values.tolist()



        #dados da semana 2 FLEEM
        #AF leve
        leve_sem2 = self.sem2['Ligth'].values.tolist()
        leve_sem2 = [int(h.split(":")[0]) + int(h.split(":")[1]) / 100 for h in leve_sem2]
        self.leve_sem2 = leve_sem2

        # Converter os valores para o formato datetime para poder converter as horas em minutos
        self.sem2['Ligth'] = self.sem2['Ligth'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())

        # Convertendo as horas para minutos
        self.sem2['leve_minutos'] = self.sem2['Ligth'].apply(lambda x: x.hour * 60 + x.minute + x.second / 60)

        #Salvandos os valores de minutos em uma lista para poder somar a quantia semanal
        leve_sem2min = self.sem2['leve_minutos'].values.tolist()


        #AF moderada
        moderada_sem2 = self.sem2['Moderate'].values.tolist()
        moderada_sem2 = [int(h.split(":")[0]) + int(h.split(":")[1]) / 100 for h in moderada_sem2]
        self.moderada_sem2 = moderada_sem2

        # Converter os valores para o formato datetime para poder converter as horas em minutos
        self.sem2['Moderate'] = self.sem2['Moderate'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())

        # Convertendo as horas para minutos
        self.sem2['moderada_minutos'] = self.sem2['Moderate'].apply(lambda x: x.hour * 60 + x.minute + x.second / 60)

        #Salvandos os valores de minutos em uma lista para poder somar a quantia semanal
        moderada_sem2min = self.sem2['moderada_minutos'].values.tolist()


        #AF vigorosa
        vigorosa_sem2 = self.sem2['Vigorous'].values.tolist()
        strong_sem2 = self.sem2['Strong'].values.tolist()
        strong_sem2 = [int(h.split(":")[0]) + int(h.split(":")[1]) / 100 for h in strong_sem2]
        vigorosa_sem2 = [int(h.split(":")[0]) + int(h.split(":")[1]) / 100 for h in vigorosa_sem2]
        vigorosa_sem2 = [vigorosa_sem2 + strong_sem2 for vigorosa_sem2, strong_sem2 in zip(vigorosa_sem2, strong_sem2)]
        self.vigorosa_sem2 = vigorosa_sem2


        # Converter os valores para o formato datetime para poder converter as horas em minutos
        self.sem2['Vigorous'] = self.sem2['Vigorous'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())
        self.sem2['Strong'] = self.sem2['Strong'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())


        # Convertendo as horas para minutos
        self.sem2['vigorosa_minutos'] = self.sem2['Vigorous'].apply(lambda x: x.hour * 60 + x.minute + x.second / 60)
        self.sem2['strong_minutos'] = self.sem2['Strong'].apply(lambda x: x.hour * 60 + x.minute + x.second / 60)
        self.sem2['vig+strong_minutos'] = self.sem2['vigorosa_minutos'] + self.sem2['strong_minutos']

        vigorosa_sem2min = self.sem2['vig+strong_minutos'].values.tolist()



        #dados da semana3 FLEEM
        #AF leve
        leve_sem3 = self.sem3['Ligth'].values.tolist()
        leve_sem3 = [int(h.split(":")[0]) + int(h.split(":")[1]) / 100 for h in leve_sem3]
        self.leve_sem3 = leve_sem3

        # Converter os valores para o formato datetime para poder converter as horas em minutos
        self.sem3['Ligth'] = self.sem3['Ligth'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())

        # Convertendo as horas para minutos
        self.sem3['leve_minutos'] = self.sem3['Ligth'].apply(lambda x: x.hour * 60 + x.minute + x.second / 60)

        #Salvandos os valores de minutos em uma lista para poder somar a quantia semanal
        leve_sem3min = self.sem3['leve_minutos'].values.tolist()


        #AF moderada
        moderada_sem3 = self.sem3['Moderate'].values.tolist()
        moderada_sem3 = [int(h.split(":")[0]) + int(h.split(":")[1]) / 100 for h in moderada_sem3]
        self.moderada_sem3 = moderada_sem3

        # Converter os valores para o formato datetime para poder converter as horas em minutos
        self.sem3['Moderate'] = self.sem3['Moderate'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())

        # Convertendo as horas para minutos
        self.sem3['moderada_minutos'] = self.sem3['Moderate'].apply(lambda x: x.hour * 60 + x.minute + x.second / 60)

        #Salvandos os valores de minutos em uma lista para poder somar a quantia semanal
        moderada_sem3min = self.sem3['moderada_minutos'].values.tolist()


        #AF vigorosa
        vigorosa_sem3 = self.sem3['Vigorous'].values.tolist()
        strong_sem3 = self.sem3['Strong'].values.tolist()
        strong_sem3 = [int(h.split(":")[0]) + int(h.split(":")[1]) / 100 for h in strong_sem3]
        vigorosa_sem3 = [int(h.split(":")[0]) + int(h.split(":")[1]) / 100 for h in vigorosa_sem3]
        vigorosa_sem3 = [vigorosa_sem3 + strong_sem3 for vigorosa_sem3, strong_sem3 in zip(vigorosa_sem3, strong_sem3)]
        self.vigorosa_sem3 = vigorosa_sem3


        # Converter os valores para o formato datetime para poder converter as horas em minutos
        self.sem3['Vigorous'] = self.sem3['Vigorous'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())
        self.sem3['Strong'] = self.sem3['Strong'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())


        # Convertendo as horas para minutos
        self.sem3['vigorosa_minutos'] = self.sem3['Vigorous'].apply(lambda x: x.hour * 60 + x.minute + x.second / 60)
        self.sem3['strong_minutos'] = self.sem3['Strong'].apply(lambda x: x.hour * 60 + x.minute + x.second / 60)
        self.sem3['vig+strong_minutos'] = self.sem3['vigorosa_minutos'] + self.sem3['strong_minutos']

        vigorosa_sem3min = self.sem3['vig+strong_minutos'].values.tolist()


        #dados da semana 4 FLEEM
        #AF leve
        leve_sem4 = self.sem4['Ligth'].values.tolist()
        leve_sem4 = [int(h.split(":")[0]) + int(h.split(":")[1]) / 100 for h in leve_sem4]
        self.leve_sem4 = leve_sem4


        # Converter os valores para o formato datetime para poder converter as horas em minutos
        self.sem4['Ligth'] = self.sem4['Ligth'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())

        # Convertendo as horas para minutos
        self.sem4['leve_minutos'] = self.sem4['Ligth'].apply(lambda x: x.hour * 60 + x.minute + x.second / 60)

        #Salvandos os valores de minutos em uma lista para poder somar a quantia semanal
        leve_sem4min = self.sem4['leve_minutos'].values.tolist()


        #AF moderada
        moderada_sem4 = self.sem4['Moderate'].values.tolist()
        moderada_sem4 = [int(h.split(":")[0]) + int(h.split(":")[1]) / 100 for h in moderada_sem4]
        self.moderada_sem4 = moderada_sem4

        # Converter os valores para o formato datetime para poder converter as horas em minutos
        self.sem4['Moderate'] = self.sem4['Moderate'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())

        # Convertendo as horas para minutos
        self.sem4['moderada_minutos'] = self.sem4['Moderate'].apply(lambda x: x.hour * 60 + x.minute + x.second / 60)

        #Salvandos os valores de minutos em uma lista para poder somar a quantia semanal
        moderada_sem4min = self.sem4['moderada_minutos'].values.tolist()

        #AF vigorosa
        vigorosa_sem4 = self.sem4['Vigorous'].values.tolist()
        strong_sem4 = self.sem4['Strong'].values.tolist()
        strong_sem4 = [int(h.split(":")[0]) + int(h.split(":")[1]) / 100 for h in strong_sem4]
        vigorosa_sem4 = [int(h.split(":")[0]) + int(h.split(":")[1]) / 100 for h in vigorosa_sem4]
        vigorosa_sem4 = [vigorosa_sem4 + strong_sem4 for vigorosa_sem4, strong_sem4 in zip(vigorosa_sem4, strong_sem4)]
        self.vigorosa_sem4 = vigorosa_sem4


        # Converter os valores para o formato datetime para poder converter as horas em minutos
        self.sem4['Vigorous'] = self.sem4['Vigorous'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())
        self.sem4['Strong'] = self.sem4['Strong'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())


        # Convertendo as horas para minutos
        self.sem4['vigorosa_minutos'] = self.sem4['Vigorous'].apply(lambda x: x.hour * 60 + x.minute + x.second / 60)
        self.sem4['strong_minutos'] = self.sem4['Strong'].apply(lambda x: x.hour * 60 + x.minute + x.second / 60)
        self.sem4['vig+strong_minutos'] = self.sem4['vigorosa_minutos'] + self.sem4['strong_minutos']

        vigorosa_sem4min = self.sem4['vig+strong_minutos'].values.tolist()


        #dados da semana 5 FLEEM
        #AF leve
        leve_sem5 = self.sem5['Ligth'].values.tolist()
        leve_sem5 = [int(h.split(":")[0]) + int(h.split(":")[1]) / 100 for h in leve_sem5]
        self.leve_sem5 = leve_sem5

        # Converter os valores para o formato datetime para poder converter as horas em minutos
        self.sem5['Ligth'] = self.sem5['Ligth'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())

        # Convertendo as horas para minutos
        self.sem5['leve_minutos'] = self.sem5['Ligth'].apply(lambda x: x.hour * 60 + x.minute + x.second / 60)

        #Salvandos os valores de minutos em uma lista para poder somar a quantia semanal
        leve_sem5min = self.sem5['leve_minutos'].values.tolist()

        #AF moderada
        moderada_sem5 = self.sem5['Moderate'].values.tolist()
        moderada_sem5 = [int(h.split(":")[0]) + int(h.split(":")[1]) / 100 for h in moderada_sem5]
        self.moderada_sem5 = moderada_sem5

        # Converter os valores para o formato datetime para poder converter as horas em minutos
        self.sem5['Moderate'] = self.sem5['Moderate'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())

        # Convertendo as horas para minutos
        self.sem5['moderada_minutos'] = self.sem5['Moderate'].apply(lambda x: x.hour * 60 + x.minute + x.second / 60)

        #Salvandos os valores de minutos em uma lista para poder somar a quantia semanal
        moderada_sem5min = self.sem5['moderada_minutos'].values.tolist()

        #AF vigorosa
        vigorosa_sem5 = self.sem5['Vigorous'].values.tolist()
        strong_sem5 = self.sem5['Strong'].values.tolist()
        strong_sem5 = [int(h.split(":")[0]) + int(h.split(":")[1]) / 100 for h in strong_sem5]
        vigorosa_sem5 = [int(h.split(":")[0]) + int(h.split(":")[1]) / 100 for h in vigorosa_sem5]
        vigorosa_sem5 = [vigorosa_sem5 + strong_sem5 for vigorosa_sem5, strong_sem5 in zip(vigorosa_sem5, strong_sem5)]
        self.vigorosa_sem5 = vigorosa_sem5

        # Converter os valores para o formato datetime para poder converter as horas em minutos
        self.sem5['Vigorous'] = self.sem5['Vigorous'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())
        self.sem5['Strong'] = self.sem5['Strong'].apply(lambda x: datetime.strptime(x, "%H:%M:%S").time())


        # Convertendo as horas para minutos
        self.sem5['vigorosa_minutos'] = self.sem5['Vigorous'].apply(lambda x: x.hour * 60 + x.minute + x.second / 60)
        self.sem5['strong_minutos'] = self.sem5['Strong'].apply(lambda x: x.hour * 60 + x.minute + x.second / 60)
        self.sem5['vig+strong_minutos'] = self.sem5['vigorosa_minutos'] + self.sem5['strong_minutos']

        vigorosa_sem5min = self.sem5['vig+strong_minutos'].values.tolist()
    

    def CriarGraficos(self):
        #Construindo gráfico do perfil dos dias ao longo das semanas FLEEM
        fig, ax = plt.subplots(nrows = 5, ncols = 1, figsize=(6,18), sharey=True)

        ax[0].plot(self.dias_da_semana, self.leve_sem1, color = '#228B22', linestyle='--', marker = 'o', markersize = 4, label = 'Leve')
        ax[0].plot(self.dias_da_semana, self.moderada_sem1, color = '#FF8C00', linestyle='--', marker = 'o', markersize = 4, label = 'Moderada')
        ax[0].plot(self.dias_da_semana, self.vigorosa_sem1, color = '#FF0000',linestyle='--', marker = 'o', markersize = 4, label = 'Vigorosa')
        ax[0].set_title('Semana 1 ' + str(self.sem1['Date'].iloc[0]) + ' à' + str(self.sem1['Date'].iloc[-1]), fontsize=12)
        ax[0].set_ylabel('Tempo (horas)')


        ax[1].plot(self.dias_da_semana, self.leve_sem2, color = '#228B22',linestyle='--', marker = 'o', markersize = 4)
        ax[1].plot(self.dias_da_semana, self.moderada_sem2, color = '#FF8C00', linestyle='--', marker = 'o', markersize = 4)
        ax[1].plot(self.dias_da_semana, self.vigorosa_sem2, color = '#FF0000', linestyle='--', marker = 'o', markersize = 4)
        ax[1].set_title('Semana 2 ' + str(self.sem2['Date'].iloc[0]) + ' à' + str(self.sem2['Date'].iloc[-1]), fontsize=12)
        ax[1].set_ylabel('Tempo (horas)')


        ax[2].plot(self.dias_da_semana, self.leve_sem3, color = '#228B22', linestyle='--', marker = 'o', markersize = 4)
        ax[2].plot(self.dias_da_semana, self.moderada_sem3, color = '#FF8C00', linestyle='--', marker = 'o', markersize = 4)
        ax[2].plot(self.dias_da_semana, self.vigorosa_sem3, color = '#FF0000', linestyle='--', marker = 'o', markersize = 4)
        ax[2].set_title('Semana 3 ' + str(self.sem3['Date'].iloc[0]) + ' à' + str(self.sem3['Date'].iloc[-1]), fontsize=12)
        ax[2].set_ylabel('Tempo (horas)')


        ax[3].plot(self.dias_da_semana, self.leve_sem4, color = '#228B22', linestyle='--', marker = 'o', markersize = 4)
        ax[3].plot(self.dias_da_semana, self.moderada_sem4, color = '#FF8C00', linestyle='--', marker = 'o', markersize = 4)
        ax[3].plot(self.dias_da_semana, self.vigorosa_sem4, color = '#FF0000', linestyle='--', marker = 'o', markersize = 4)
        ax[3].set_title('Semana 4 ' + str(self.sem4['Date'].iloc[0]) + ' à' + str(self.sem4['Date'].iloc[-1]), fontsize=12)
        ax[3].set_ylabel('Tempo (horas)')


        ax[4].plot(self.dias_da_semana, self.leve_sem5, color = '#228B22', linestyle='--', marker = 'o', markersize = 4)
        ax[4].plot(self.dias_da_semana, self.moderada_sem5, color = '#FF8C00', linestyle='--', marker = 'o', markersize = 4)
        ax[4].plot(self.dias_da_semana, self.vigorosa_sem5, color = '#FF0000', linestyle='--', marker = 'o', markersize = 4)
        ax[4].set_title('Semana 5 ' + str(self.sem5['Date'].iloc[0]) + ' à' + str(self.sem5['Date'].iloc[-1]), fontsize=12)
        ax[4].set_ylabel('Tempo (horas)')


        plt.rcParams['axes.labelsize']=12
        plt.rcParams['axes.titlesize']=12


        plt.tight_layout()
        fig.autofmt_xdate(rotation=45)
        fig.legend(loc='upper right', bbox_to_anchor=(1.18, 0.975))
        fig.savefig(self.diretorio+'af_ao_longo_dos_dias_durante_as_semanas_fleem.jpg', bbox_inches='tight', dpi=300)
        plt.close(fig)
        


dados_acc_processados = ProcessaAcelerometro()


a = dados_acc_processados.data
b = dados_acc_processados.sem1
