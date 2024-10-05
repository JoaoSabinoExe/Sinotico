from selenium.webdriver.common.by import By
import keyboard
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import customtkinter as ctk
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time

mensagem = ""

#Funcao para limpar os campos
def limpar_campos():
    input_login_entry.delete(0, ctk.END)
    input_senha_entry.delete(0, ctk.END)

def mostrar_ocultar_senha():
    if input_senha_entry.cget('show') == '':
        input_senha_entry.configure(show='*')
    else:
        input_senha_entry.configure(show='')

def iniciar_programa():

    global mensagem

    interface.focus()

    #Variaveis que vieram do input da interface grafica
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

        #O WebDriverWait serve para esperar o tempo de carregamento do elemento concluir
        elemento_espera_login = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="ucLogarUsuario_txtLogin"]'))
        )

        #Logando com o usuario no site da citatti
        elemento_espera_login.send_keys(login)
        navegador.find_element(By.XPATH, '//*[@id="ucLogarUsuario_txtSenha"]').send_keys(senha)
        navegador.find_element(By.XPATH, '//*[@id="ucLogarUsuario_btnLogar"]').click()

        #Aguardando o elemento carregar e acessando a area de monitoramento
        elemento_espera_monitoramento = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="item_menu_2"]'))
        )
        
        elemento_espera_monitoramento.click()

        #Esperando o elemento Sinotico carregar
        elemento_espera_sinotico = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="40109"]'))
        )

        elemento_espera_sinotico.click()

        janela_atual = navegador.current_window_handle

        janelas_antes = navegador.window_handles

        # Aguardar até que uma nova janela seja aberta
        WebDriverWait(navegador, 10).until(EC.new_window_is_opened(janelas_antes))

        # Obter as janelas depois que a nova foi aberta
        todas_janelas = navegador.window_handles

        # Encontrar a nova janela que foi aberta
        for janela in todas_janelas:
            if janela != janela_atual:
                navegador.switch_to.window(janela)

        # Agora esperar pelo iframe, e trocar para ele
        WebDriverWait(navegador, 10).until(EC.frame_to_be_available_and_switch_to_it(0))

        #Esperando o elemento pesquisar do sinotico carregar
        elemento_espera_pesquisar = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="btnBuscar"]'))
        )

        elemento_espera_pesquisar.click()

        mensagem = 'Carregamento de páginas concluido.'

    #Caso de erro no programa sera imprimido uma mensagem de erro
    except Exception as erro_sinotico:
        mensagem = "Aconteceu um erro inesperado. Entre em contato com o suporte técnico.\n"
        mensagem += f"{str(erro_sinotico).splitlines()[:4]}"

    adicionar_mensagem()

    limpar_campos()

    def tratar_elementos_sinotico(tratar_elementos_sinotico_var):
        navegador.find_element(By.XPATH, '//*[@id="uscTratarEventos_chkMarcarTodos"]').click()
        navegador.find_element(By.XPATH, '//*[@id="uscTratarEventos_btnTratarSelecionados"]').click()

        #Aguardando o elemento Mensagem Evento carregar
        selecionar_elemento = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="uscComponenteMensagemEvento_ddlMotivo"]'))
        )
        selecionar = Select(selecionar_elemento)
        selecionar.select_by_visible_text(tratar_elementos_sinotico_var)

        navegador.find_element(By.XPATH, '//*[@id="uscComponenteMensagemEvento_btnTratarEvento"]').click()

    #Definido uma funcao atrelada ao comando shift+w
    def tratar_sinotico():

        global mensagem

        #O script vai tentar encontrar o nome do envento, caso seja excesso de velocidade vai ser tratado como OP - INDISCIPLINA DO OPERADOR, caso seja comprimento de partida ou de
        #viagem vai ser fechado e não sera tratado, qualquer outro tipo de evento sera selecionado e tratado em branco, caso de erro ira retornar uma mensagem
        try:
            pegar_texto_elemento = navegador.find_element(By.XPATH, '//*[@id="uscTratarEventos_lblNomeEvento"]')
            nome_elemento = pegar_texto_elemento.text
            if nome_elemento == 'Excesso de Velocidade':
               
                tratar_elementos_sinotico('OP - INDISCIPLINA DO OPERADOR')

            elif nome_elemento == 'Cumprimento de Partidas' or nome_elemento == 'Cumprimento de Viagem':
                navegador.find_element(By.XPATH, '//*[@id="uscTratarEventos_btnFechar"]').click()

            else:
                navegador.find_element(By.XPATH, '//*[@id="uscTratarEventos_chkMarcarTodos"]').click()
                navegador.find_element(By.XPATH, '//*[@id="uscTratarEventos_btnTratar"]').click()
        except Exception as erro_tratativa:
            mensagem = "Não foi possivel realizar esta ação\n"
            mensagem += f"{str(erro_tratativa).splitlines()[:4]}"
            adicionar_mensagem()

    #Adicionando o comando para a funcao tratar_sinotico
    keyboard.add_hotkey('shift+w', tratar_sinotico)

    def tratar_falha_gps():

        global mensagem

        try:
            pegar_texto_elemento = navegador.find_element(By.XPATH, '//*[@id="uscTratarEventos_lblNomeEvento"]')

            nome_elemento = pegar_texto_elemento.text

            if nome_elemento == 'Cumprimento de Partidas':

                tratar_elementos_sinotico('SS - FALHA DE GPS')

            elif nome_elemento == 'Cumprimento de Viagem':

                tratar_elementos_sinotico('SS - FALHA DE GPS')

            else:
                tratar_sinotico()

        except Exception as tratar_falha_gps_erro:
            mensagem = "Não foi possivel realizar esta ação\n"
            mensagem += f"{str(tratar_falha_gps_erro).splitlines()[:4]}"
            adicionar_mensagem()

    keyboard.add_hotkey('shift+e', tratar_falha_gps)

    def elemento_fechar():
        espera_componente_fechar_verdinho_amarelo = WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="uscVisualizadorEventos_btnFechar"]'))
        )

        espera_componente_fechar_verdinho_amarelo.click()
    
    def elemento_pesquisar():
        espera_componente_buscar_verdinho_amarelo = WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="btnBuscar"]'))
        )

        espera_componente_buscar_verdinho_amarelo.click()

    def tratar_verdinho_amarelo(duplo_click_verdinho_amarelo_xpath):

        global mensagem

        try:
            for tratador_verdinho_for in range(1000):

                if keyboard.is_pressed("esc"):
                    mensagem = "O looping foi encerrado pelo usuário!"
                    adicionar_mensagem()
                    return

                try:
                    espera_carregar_componente_verdinho_amarelinho = WebDriverWait(navegador, 10).until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="btnBuscar"]'))
                    )

                    duplo_click_elemento = navegador.find_element(By.XPATH, duplo_click_verdinho_amarelo_xpath)

                    instancia_actionchains = ActionChains(navegador)

                    instancia_actionchains.double_click(duplo_click_elemento).perform()

                except Exception as erro_carregar_elemento_verdinho_amarelo:
                    mensagem = "Não foi possivel encontrar o elemento\n"
                    mensagem += f"{str(erro_carregar_elemento_verdinho_amarelo).splitlines()[:4]}"
                    adicionar_mensagem()
                    return

                try:
                    espera_primeiro_item_tratavel = WebDriverWait(navegador, 10).until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="uscVisualizadorEventos_dtlListagemEventos_uscItemResumoEvento_0_lnkTratarEvento_0"]'))
                    )
                except Exception as erro_selecionar_primeiro_item_tratavel:
                    elemento_fechar()
                    elemento_pesquisar()
                    mensagem = "Não foi possivel encontrar o primeiro item tratavel"
                    adicionar_mensagem()
                    return

                espera_primeiro_item_tratavel.click()

                espera_carregar_componente_tratar = WebDriverWait(navegador, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="uscTratarEventos_btnTratar"]'))
                )

                tratar_sinotico()

                elemento_fechar()
                elemento_pesquisar()

        except Exception as erro_verdinho_amarelo:
            mensagem = "Não foi possivel realizar esta ação\n"
            mensagem += f"{str(erro_verdinho_amarelo).splitlines()[:4]}"
            adicionar_mensagem()
            return

    def tratar_verdinho():
        tratar_verdinho_amarelo(duplo_click_verdinho_amarelo_xpath = '//ul[@class="normal"]//li[@idempresa="vb1@transportes.com.br"]')
    
    #Adicionando o comando para a funcao tratar_verdinho
    keyboard.add_hotkey('f2', tratar_verdinho)

    def tratar_amarelo():
        tratar_verdinho_amarelo(duplo_click_verdinho_amarelo_xpath = '//ul[@class="medio"]//li[@idempresa="vb1@transportes.com.br"]')
    
    #Adicionando o comando para a funcao tratar_amarelo
    keyboard.add_hotkey('f8', tratar_amarelo)

    def tratar_verdinho_automatico():

        global mensagem

        for tratar_verdinho_automatico_loop in range(100):
            try:
                tratar_verdinho()

                mensagem = f"Execução Finalizada."
                adicionar_mensagem()
                adicionar_mensagem()

                for espera_nova_execucao in range(30, 0, -1):
                    if keyboard.is_pressed('esc'):
                        mensagem = "O tratador automático foi encerrado pelo usuário!"
                        atualizar_mensagem_deletar_ultima()
                        return
                    
                    minutos_restantes = espera_nova_execucao // 60
                    segundos_restantes = espera_nova_execucao % 60

                    mensagem = f"Próxima execução em {minutos_restantes:02d}:{segundos_restantes:02d}"
                    atualizar_mensagem_deletar_ultima()
                    
                    time.sleep(1)

                mensagem = f"Executanto..."
                atualizar_mensagem_deletar_ultima()

                elemento_pesquisar()

            except Exception as tratar_verdinho_automatico_loop_erro:
                mensagem = "Não foi possivel realizar esta ação\n"
                mensagem += f"{str(tratar_verdinho_automatico_loop_erro).splitlines()[:4]}"
                adicionar_mensagem()
                return

    keyboard.add_hotkey('f9', tratar_verdinho_automatico)

def atualizar_mensagem_deletar_ultima():
    caixa_log.configure(state="normal")
    caixa_log.delete("end-2l", "end-1l") 
    caixa_log.insert("end", mensagem + "\n")
    caixa_log.yview("end")
    caixa_log.configure(state="disabled")

def adicionar_mensagem():
    caixa_log.configure(state="normal")
    caixa_log.insert("end", mensagem + "\n")
    caixa_log.yview("end")
    caixa_log.configure(state="disabled")

#Interface grafica com CustomTkInter
interface = ctk.CTk()
interface.geometry("500x450")

def iniciar_programa_enter(event):
    iniciar_programa()

ctk.set_appearance_mode("dark")

interface.title('Sinótico 2.0.0.3')

primeiro_texto = ctk.CTkLabel(interface, text='Sinótico', font=("Arial", 25))
primeiro_texto.place(relx=0.5, rely=0.1, anchor="center")

segundo_texto = ctk.CTkLabel(interface, text='2.0.0.3')
segundo_texto.place(relx=0.5, rely=0.15, anchor="center")

terceiro_texto = ctk.CTkLabel(interface, text='Atalhos:', font=("Arial", 20))
terceiro_texto.place(relx=0.01, rely=0.0, anchor="nw")

terceiro_texto = ctk.CTkLabel(interface, text='Sinotico: SHIFT + W\nFalha de GPS: SHIFT + E\nVerdinho: F2\nAmarelo: F8\nVerdinho Automático: F9\nEncerrar Automático: ESC', justify = "left")
terceiro_texto.place(relx=0.01, rely=0.05, anchor="nw")

input_login_entry = ctk.CTkEntry(interface, placeholder_text="Seu login")
input_login_entry.place(relx=0.5, rely=0.25, anchor="center")

input_senha_entry = ctk.CTkEntry(interface, placeholder_text="Sua senha", show='*')
input_senha_entry.place(relx=0.5, rely=0.35, anchor="center")

mostrar_ocultar_senha_combobox = ctk.CTkCheckBox(interface, text='Mostrar', command=mostrar_ocultar_senha, checkbox_height=20, checkbox_width=20, border_width=1)
mostrar_ocultar_senha_combobox.place(relx=0.76, rely=0.35, anchor="center")

botao_iniciar = ctk.CTkButton(interface, text='Iniciar', command=iniciar_programa)
botao_iniciar.place(relx=0.5, rely=0.45, anchor="center")

caixa_log = ctk.CTkTextbox(interface, width=400, height=220, wrap="word")
caixa_log.place(relx=0.5, rely=0.742, anchor="center")

caixa_log.configure(state="disabled")

input_login_entry.bind('<Return>', iniciar_programa_enter)
input_senha_entry.bind('<Return>', iniciar_programa_enter)

interface.mainloop()
