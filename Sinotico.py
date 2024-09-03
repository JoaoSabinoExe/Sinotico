import time
from selenium.webdriver.common.by import By
import keyboard
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import customtkinter as ctk

mensagem = ""

#Funcao para limpar os campos
def limpar_campos():
    input_login_entry.delete(0, ctk.END)
    input_senha_entry.delete(0, ctk.END)
    input_time_set_entry.delete(0, ctk.END)
    input_time_page_entry.delete(0, ctk.END)

def iniciar_programa():

    global mensagem

    #Variaveis que vieram do input da interface grafica
    time_set = float(input_time_set_entry.get())
    time_page = float(input_time_set_entry.get())
    login = str(input_login_entry.get())
    senha = str(input_senha_entry.get())

    mensagem = 'Iniciando programa.'

    adicionar_mensagem()

    try:
        #Este Service serve para atualizar automaticamente o drivemanager
        servico = Service(ChromeDriverManager().install())

        navegador = webdriver.Chrome(service=servico) 

        #Abrindo o site da Citatti
        navegador.get("https://gool.cittati.com.br/Login.aspx?ReturnUrl=%2f")

        navegador.find_element('xpath', '//*[@id="ucTrocarModulo_btnIconeUrbano"]').click()

        #O time.sleep serve dar tempo da pagina carregar
        time.sleep(time_set)

        #Logando com o usuario no site da citatti
        navegador.find_element(By.XPATH, '//*[@id="ucLogarUsuario_txtLogin"]').send_keys(login)
        navegador.find_element(By.XPATH, '//*[@id="ucLogarUsuario_txtSenha"]').send_keys(senha)
        navegador.find_element(By.XPATH, '//*[@id="ucLogarUsuario_btnLogar"]').click()

        time.sleep(time_set)

        #Acessando a area de monitoramento
        navegador.find_element(By.XPATH, '//*[@id="item_menu_2"]').click()

        time.sleep(time_set)

        #Acessando o sinotico
        navegador.find_element(By.XPATH, '//*[@id="40109"]').click()

        time.sleep(time_set)

        #Trocando de janela para a janela do sinotico que é um iframe
        todas_janelas = navegador.window_handles

        for janela in todas_janelas:
            navegador.switch_to.window(janela)

        navegador.switch_to.frame(0)

        time.sleep(time_set)

        #Botao para realizar a busca no sinotico
        navegador.find_element(By.XPATH, '//*[@id="btnBuscar"]').click()

        mensagem = 'Carregamento de páginas concluido.'

    #Caso de erro no programa sera imprimido uma mensagem de erro
    except Exception as erro_sinotico:
        mensagem = "Aconteceu um erro inesperado. Entre em contato com o suporte técnico."
        mensagem += f"{str(erro_sinotico)}"

    adicionar_mensagem()

    limpar_campos()

    #Definido uma funcao atrelada ao comando shift+w
    def acao():

        global mensagem

        #O script vai tentar encontrar o nome do envento, caso seja excesso de velocidade vai ser tratado como OP - INDISCIPLINA DO OPERADOR, caso seja comprimento de partida ou de
        #viagem vai ser fechado e não sera tratado, qualquer outro tipo de evento sera selecionado e tratado em branco, caso de erro ira retornar uma mensagem
        try:
            pegar_texto_elemento = navegador.find_element(By.XPATH, '//*[@id="uscTratarEventos_lblNomeEvento"]')
            nome_elemento = pegar_texto_elemento.text
            if nome_elemento == 'Excesso de Velocidade':
                navegador.find_element(By.XPATH, '//*[@id="uscTratarEventos_chkMarcarTodos"]').click()
                navegador.find_element(By.XPATH, '//*[@id="uscTratarEventos_btnTratarSelecionados"]').click()

                time.sleep(time_page)

                selecionar_elemento = navegador.find_element(By.XPATH, '//*[@id="uscComponenteMensagemEvento_ddlMotivo"]')
                selecionar = Select(selecionar_elemento)
                selecionar.select_by_visible_text("OP - INDISCIPLINA DO OPERADOR")

                navegador.find_element(By.XPATH, '//*[@id="uscComponenteMensagemEvento_btnTratarEvento"]').click()

            elif nome_elemento == 'Cumprimento de Partidas' or nome_elemento == 'Cumprimento de Viagem':
                navegador.find_element(By.XPATH, '//*[@id="uscTratarEventos_btnFechar"]').click()

            else:
                navegador.find_element(By.XPATH, '//*[@id="uscTratarEventos_chkMarcarTodos"]').click()
                navegador.find_element(By.XPATH, '//*[@id="uscTratarEventos_btnTratar"]').click()
        except Exception as erro_tratativa:
            mensagem = "Não foi possivel realizar esta ação"
            mensagem += f"{str(erro_tratativa)}"
            adicionar_mensagem()


    #Adicionando o comando para a funcao acao
    keyboard.add_hotkey('shift+w', acao)


def adicionar_mensagem():
    caixa_log.insert("end", mensagem + "\n")
    caixa_log.yview("end")

#Interface grafica com CustomTkInter
interface = ctk.CTk()
interface.geometry("500x450")

ctk.set_appearance_mode("dark")

interface.title('Sinótico 1.0.0.1')

primeiro_texto = ctk.CTkLabel(interface, text='Sinótico', font=("Arial", 25))
primeiro_texto.place(relx=0.5, rely=0.1, anchor="center")

segundo_texto = ctk.CTkLabel(interface, text='1.0.0.1')
segundo_texto.place(relx=0.5, rely=0.2, anchor="center")

terceiro_texto = ctk.CTkLabel(interface, text='Atalho: SHIFT + W')
terceiro_texto.place(relx=0.5, rely=0.3, anchor="center")

input_login_entry = ctk.CTkEntry(interface, placeholder_text="Seu login")
input_login_entry.place(relx=0.5, rely=0.4, anchor="center")

input_senha_entry = ctk.CTkEntry(interface, placeholder_text="Sua senha")
input_senha_entry.place(relx=0.5, rely=0.5, anchor="center")

input_time_set_entry = ctk.CTkEntry(interface, placeholder_text="Time_Set", width=80)
input_time_set_entry.place(relx=0.4, rely=0.6, anchor="center")

input_time_page_entry = ctk.CTkEntry(interface, placeholder_text="Time_Page", width=80)
input_time_page_entry.place(relx=0.6, rely=0.6, anchor="center")

botao_iniciar = ctk.CTkButton(interface, text='Iniciar', command=iniciar_programa)
botao_iniciar.place(relx=0.5, rely=0.7, anchor="center")

caixa_log = ctk.CTkTextbox(interface, width=400, height=100, wrap="word")
caixa_log.place(relx=0.5, rely=0.87, anchor="center")

interface.mainloop()
