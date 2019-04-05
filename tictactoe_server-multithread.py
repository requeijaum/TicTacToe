import time
import os
import textwrap
import socket
import threading
import random

# verificar codificação de caracteres de acordo com a plataforma
# ver simulador do IFBA


# Dicas
# print() -> ver apenas no servidor
# imprimir() -> enviar para o cliente e mostrar no servidor

# Como não utilizamos classes para criar instâncias de jogos:
# só é possível sustentar uma sessão a cada par de jogadores.
# a não ser que sejam executadas várias instâncias de servidor usando portas diferentes!

# função de limpar tela universal - entre WinNT e POSIX (Linux, macOS)
from platform import system as system_name 

print("Sistema Operacional: " + os.name)
time.sleep(1)

import locale
if os.name == "nt":
    
    def getpreferredencoding(do_setlocale = True):
        return "cp1252"

    locale.getpreferredencoding = getpreferredencoding
    

print("Locale: " + locale.getpreferredencoding())
time.sleep(2)


def limparTela():
    if os.name == 'nt':         # existe um bug
        print("\r\n" * 24)

    else:
        os.system("clear")


# funções que não podem ser métodos da classe Partida

def enviarCliente(obj) :                           # Função para enviar mensagens ao cliente!
    # tunar isso aqui direito pra receber msg também ?
    # não pq preciso usar ter acesso à msg enviada...

    #global msg                                  # usar variavel global ou argumento?
    #global c
    #global game_condition
    #global askPlayer2

    try:
        time.sleep(0.5)                         # delay utilizado para controlar o uso de CPU ao enviar mensagens... não pode ser muito rápido!
                                                # se for muito rápido: o cliente pode errar a quebra de linhas e mostrar texto mal-formatado
                                                # ajustar pra esse valor ajuda a resolver problemas no cliente
        

        if type(obj.c) != type(None) :              # Verificar se o socket do cliente está "nulo". 
            try:
                obj.c.send(obj.msg.encode())                # O servidor pode tentar enviar algo ao cliente sem um socket conectado!
        
            #except Exception as e:
            #    print(e)                    # subir Exception e ver na tela

            except BrokenPipeError:
                obj.c.close()                   # forçar parada do socket do cliente - está quebrado!
                quit
            
            except OSError :
                obj.game_condition = False
                obj.askPlayer2 = False
                quit
        pass

    except Exception as e:
        print("\r\nDEBUG: Algum erro ocorreu ao processar o envio...\r\n") 
        print(e)
        pass


def imprimir(obj, texto):                            # Função que imprime texto para o cliente e para o servidor!
    #global msg                                  # Precisamos referenciar a mensagem que será enviada para o cliente.
    obj.msg = texto

    enviarCliente(obj)
    #print(texto)                                # não imprimir pra não lotar o texto!!!




match_list = {
    
}


class Partida :
    'Classe base para uma partida'
    contador = 0

    banner = r'''
                    _____  _  ____     _____  ____  ____     _____  ____  _____
                    /__ __\/ \/   _\   /__ __\/  _ \/   _\   /__ __\/  _ \/  __/
                    / \  | ||  / _____ / \  | / \||  / _____ / \  | / \||  \
                    | |  | ||  \_\____\| |  | |-|||  \_\____\| |  | \_/||  /_
                    \_/  \_/\____/     \_/  \_/ \|\____/     \_/  \____/\____\ '''


    def __init__(self, s, id):

        self.c, self.addr = s.accept()     # Establish connection with client.

        self.score       = []                        # Criar um vetor global de pontuação (score)
        
        # usar con,addr do socket!
        #s           = socket.socket()           # Criar um objeto global de socket
        #c           = None                      # Criar uma instância global de socket do cliente - é um tuple: (c,addr)
        
        #self.c           = con
        #self.addr        = addr

        self.game_condition = False                  # Variável global que armazena o estado de condição de um jogo - válido ou inválido - para sustentar a conexão

        self.msg = "Testando 1234"           # enviar ao cliente - mensagem inicial nunca pode ser nula, pois socket não envia algo com 0 bytes!
        self.recv = ""                       # recebido do cliente

        self.askPlayer2 = True               # variável booleana que verifica se pode perguntar algo ao cliente (Jogador O - remoto)


        self.id   = id
        #self.nome = nome
        #self.con  = con
        
        Partida.contador += 1

        # dict que armazena as threads. Estou definindo elas aqui por boas-práticas.
        self.thread_list = {
            "socketCriado"              : None,
            "buscadorClientes"          : None,
            "novoCliente"               : None,
            "enviarCliente"             : None

        }



    def quantosJogadores(self):
        print ("Partidas totais: %d" % Partida.contador)

    def mostraPartida(self):
        #print ("Nome : ", self.nome,  ", Conexao: ", self.c) #(self.c,self.addr) )
        print ("ID: ", self.id  + " Conexao: ", self.c)


    def procurarClientes(self):                         # Função para ser utilizada na thread que procura por conexões válidas antes de iniciar a lógica do jogo
        #global game_condition
        #global thread_list

        # declarar thread para a função que faz-tudo pelo cliente "fiddleSocket()" - e declarar thread para lógica do jogo em "Main()"
        self.thread_list["fiddleSocket"] = threading.Thread(target=self.fiddleSocket , name="fiddleSocket" + str(self.id) , args=() )
        self.thread_list["jogo"]         = threading.Thread(target=self.jogo , name="jogo" + str(self.id) , args=() )

        self.thread_list["fiddleSocket"].start()         # iniciar interação por socket
        # DEBUG
        #print(">> game_condition da partida" + str(self.id) + " : " + str(self.game_condition))

        if not self.thread_list["fiddleSocket"].is_alive() :
            print(">> fiddleSocket da partida" + self.id + " não subiu. :(")
            
        

        while self.game_condition == False:              # verifica a condição de jogo periodicamente.
            print("\r\n Não encontramos clientes disponiveis na partida" + self.id + " ...")
            time.sleep(3)


        if self.game_condition == True :                 # a condição de jogo é válida! Vamos jogar!
            self.thread_list["jogo"].start()


    def fiddleSocket(self):                         # não passar parâmetro... precisamos referenciar os dados!
        #global s
        #global game_condition
        #global thread_list
        #global msg                              # o Python3 vai criar um ponteiro automaticamente - precisamos usar a variável global "msg"
        #global c
        #global addr

        #c, addr = s.accept()                    # Estabelecer conexão com o cliente!
        self.game_condition = True                   # E mudar a condição de jogo para válida!

        # declarar thread que instancia um novo cliente conectado - e iniciar assim que possível!
        self.thread_list["novoCliente"]      = threading.Thread(target=self.novoCliente   , name="novoCliente" + str(self.id) , args=() )
        self.thread_list["novoCliente"].start()

        # caso a thread esteja viva e funcionando: entre no processo e verifique quando ele vai parar - detectar encerramento da thread com join()
        if self.thread_list["novoCliente"].is_alive():
            self.thread_list["novoCliente"].join()   # essa thread pode mudar o game_condition


        if self.game_condition == False :            # caso algo dê errado no jogo: feche o socket!
            self.c.close()                           # fechar conexão... e não o socket mestre



    def novoCliente(self):
        #global game_condition
        #global askPlayer2
        #global recv
        #global msg
        #global c
        #global addr

        # precisamos de uma string não nula no estado inicial
        self.msg = "Olá!"

        while True :    # loop infinito

            # esse delay aqui é muito importante para não causar 100% de uso da CPU ao processar mensagens!
            time.sleep(0.1)   # tentar encher buffer? serve pra escrever \r\n corretamente - no cliente

            try:                                    # tentar receber algo do socket... se vier vazio: rode "except"
                self.data_received = self.c.recv(1024)
                pass

            except:                                 # caso não consiga receber... suba uma exceção e avise que deu erro antes de sair do jogo!
                self.anunciar("Ocorreu um erro ao processar o comando recebido!")
                self.askPlayer2 = False
                self.game_condition = False
                break

            # tentativa de conectar por Telnet... pode falhar abaixo:
            #try:
            test = None
            test = self.data_received.decode()

            if len(test) > 0:     # decodificar fluxo de bytes para string. Caso a string resultante não seja vazia:
                self.recv = test

                if self.recv != "invalido":                     # string utilizada para controle de fluxo entre servidor e cliente
                    #print(self.addr, ' >> ', self.recv)        # caso o servidor receba "invalido": não imprima na tela. Essa mensagem é inútil para os jogadores.
                    self.anunciar(str(self.recv))               # fail-safe using str() on print()

            #    continue
            #except UnicodeDecodeError:
            #    self.anunciar("Erro ao decodificar string Unicode!")
            #    pass

        # a partir daqui: significa que o socket do cliente foi encerrado e o servidor não irá receber mais dados!
        self.c.close()   
        print("\r\nQue feio, servidor! O cliente saiu do jogo!\r\n")
        self.game_condition = False                      # sem cliente: sem jogo!


    # funções auxiliares para jogo()

    def full(self):                                     # Função que verifica se todas as casas 3x3 estão preenchidas
        if ' ' not in self.score:
            imprimir(self, '\r\nO jogo resultou em um empate... jogo de gato e rato!\r\n( ͡° ͜ʖ ͡°)')
            self.anunciar("Resultado: empate!")
            return True


    def board_display(self, score):                       # Função que imprime o tabuleiro. Recebe o vetor "score" como parâmetro.
        
        imprimir(self, ' '+self.score[6]+ ' | '+ self.score[7]+ ' | '+ self.score[8] )#+ "\r\n")
        imprimir(self, '---+---+---'  )#+ "\r\n")   
        imprimir(self, ' '+self.score[3]+ ' | '+ self.score[4]+ ' | '+ self.score[5] )#+ "\r\n")
        imprimir(self, '---+---+---' )#+ "\r\n")
        imprimir(self, ' '+ self.score[0]+ ' | '+ self.score[1]+ ' | '+ self.score[2] )#+ "\r\n")


    def check(self, char, posi1, posi2, posi3):           # Função que verifica posições e caracteres válidos dentro de uma linha do tabuleiro (3x3)
                                                    # Serve para verificar que uma linha foi completada por um dos jogadores.

        if self.score[posi1] == char and self.score[posi2] == char and self.score[posi3] == char:
            return True


    def checkall(self, char):                             # Algoritmo que verifica todas as linhas possíveis que podem ser feitas no tabuleiro
        if self.check(char, 0, 1, 2):
            return True
        if self.check(char, 3, 4, 5):
            return True
        if self.check(char, 6, 7, 8):
            return True
        if self.check(char, 0, 3, 6):
            return True
        if self.check(char, 1, 4, 7):
            return True
        if self.check(char, 2, 5, 8):
            return True
        if self.check(char, 0, 4, 8):
            return True
        if self.check(char, 2, 4, 6):
            return True
        return False


    def comandoSistema(self, cmd):                        # Função que executa um comando do sistema em ambos cliente e servidor
        #global msg
        self.msg = "/cmd " + cmd
        enviarCliente(self)
        #limparTela()
        
    def anunciar(self, msg) :
        print("\n*** Partida " + str(self.id) + " com " + str(self.addr) + ": >> " + msg + " *** \n")


    # fim das funções auxiliares


    def jogo(self):                                     # Função que contêm a lógica principal do jogo.
                                                    # Deve ser invocada usando uma thread.

        #global thread_list
        #global game_condition
        #global score
        #global msg
        #global recv
        #global askPlayer2
        #global banner



        self.comandoSistema("clear")
        # imprimir('Tic Tac Toe\r\n'.center(70))
        
        imprimir(self, self.banner)
        imprimir(self, '\r\nO tabuleiro é numerado em forma de teclado numérico, conforme impresso abaixo.\r\n')

        time.sleep(0.01)
        self.score = ['1', '2', '3',
                '4', '5', '6',
                '7', '8', '9']

        self.board_display(self.score)
        imprimir(self, "\r\n")
        
        # imprimir instruções de jogo de forma estilizada com quebra de linha automática em 72 caracteres
        value = '\r\n\r\nO objetivo do Jogo da Velha é obter três marcas em linha. Você joga em um tabuleiro de três por três. O primeiro jogador é conhecido como X e o segundo é O. Os jogadores alternam colocando Xs e Os no tabuleiro até que um dos oponentes tenha três em sequência ou todos os nove quadrados estejam preenchidos. X sempre vai primeiro. No caso de ninguém ter três em linha, o empate é chamado de jogo de gato!\r\n'
        wrapper = textwrap.TextWrapper(width=72)
        string = wrapper.fill(text=value)
        
        #imprimir('\r\n' )
        imprimir(self, string)

        while self.game_condition :                      # Enquanto a condição de jogo for verdadeira... executar a lógica de jogo!

            imprimir(self, '\r\nEm suas marcas...\r\nO jogo começará em 10 segundos.')
            time.sleep(10)
            self.anunciar("Iniciando partida.")

            self.score = [' ']*9                         # iniciar tabuleiro e vetor de pontuação

            while True:                             # loop infinito

                self.comandoSistema('clear')
                self.board_display(self.score)
                                                    # parar o jogo...    
                if self.full():                          # caso o tabuleiro não tenha células vazias!
                    break                           # caso a thread de conexão não esteja rodando!
                if not self.thread_list["novoCliente"].is_alive():       
                    break

                while True:                         # loop infinito
                    try:                            # explicar essa coisa louca
                        self.msg = "\r\n>> Esperando Jogador X"
                        enviarCliente(self)
                        #player1 = int(input('\r\nJogador X, escolha sua posição: '))
                        #print("\r\nO computador está escolhendo a posição da marca...")
                        self.anunciar("O computador está escolhendo a posição da marca...")
                        player1 = random.randint(1,9)
                        if self.score[player1-1] != 'X' and self.score[player1-1] != 'O':
                            self.score[player1-1] = 'X'
                            break
                        else:
                            imprimir(self, '\r\n>> A posição ' + str(player1) +' já foi escolhida! Por favor, tente novamente.')    # possível bug: o PC pula a jogada
                            time.sleep(1)
                            continue        #break - arranquei isso pra tentar remover o bug
                    except:
                        print('\r\nPor favor... entre um valor válido...')            # mensagem exclusiva ao Jogador X
                        continue
                self.comandoSistema('clear')
                self.board_display(self.score)
                if self.checkall('X'):
                    imprimir(self, '\r\nJogador X é o vencedor!')
                    self.anunciar("Jogador X é o vencedor!")
                    time.sleep(0.1)
                    break
                if self.full():
                    break
                # mostrar que está esperando o cliente remoto fazer a jogada
                #print("\r\n\r\n>> Esperando Jogador O...")    
                self.anunciar("Esperando Jogador O...")

                contarPergunta = 0
                while self.askPlayer2:                   # enquanto for o momento de interagir com o cliente e esperar uma entrada de dados dele...
                    try:
                        #while len(recv) < 1 :       # explicar essa mágica
                        #    time.sleep(3)
                        
                        if len(self.recv) != 1:          # acho que vai quebrar a mágica
                            #msg = "\r\nJogador O, escolha sua posição: "
                            self.msg = "/cmd input"
                            
                        else: 
                            self.msg = "."
                        

                        if contarPergunta < 1 :
                            enviarCliente(self)
                            contarPergunta = contarPergunta + 1   

                        else:
                            self.msg = "/cmd nothing"                 
                        
                        enviarCliente(self)
                        time.sleep(1)               # outro delay?

                        #print("DEBUG: recv = " + recv)
                        if len(self.recv) == 1 and int(self.recv) != 0 : # and (int(recv) in [0,1,2,3,4,5,6,7,8,9]) :
                            #msg = "."        # tentar limpar msg pra não cometer erro por redundância
                            player2 = int(self.recv)
                            contarPergunta = 0
                            

                            # caso seja um valor numérico válido de jogada...

                            if self.score[player2-1] != 'X' and self.score[player2-1] != 'O':
                                self.score[player2-1] = 'O'
                                break
                            else:
                                if len(self.recv) == 0 or len(self.recv) == 1 :
                                    imprimir(self, '\r\nA posição \"' + str(self.recv) + '\" já foi marcada! Por favor, tente novamente.')
                                    time.sleep(1)
                                continue

                            break
                            
                        
                        if len(self.recv) != 1 and self.recv != "invalido" :  # nunca verificar nada contra a string "invalido" a ser recebida
                            imprimir(self, '\r\n>> Por favor... entre um valor válido... e não \"' + str(self.recv) + '\" ')
                            time.sleep(1)
                            #continue    # forçar ir ao pass do try? Não!

                        pass  # talvez isso quebre tudo! # explicar isso aqui...


                    except Exception as e :
                        print(e)
                        #imprimir('\r\nOLD: Por favor... entre um valor válido... e não \"' + str(recv) + '\" ' )
                        continue


                self.comandoSistema('clear')
                self.board_display(self.score)

                if self.checkall('O'):
                    imprimir(self, '\r\nJogador O é o vencedor!')
                    self.anunciar("Jogador O é o vencedor!")
                    time.sleep(0.1)
                    break
                if self.full():
                    break

            # forçar fechar socket - não usarrrrr
            #if self.thread_list["novoCliente"].is_alive() :
            #    self.c.close()
            #    imprimir(self, "\nDEBUG: fechar socket? novoCliente é uma thread viva!\n")

            again = ""    

            imprimir(self, '\r\nVocê quer jogar de novo? Entre com \"sim\" ou \"nao\": ')
                
            while again.lower() != 'sim':

                    again = self.recv

                    if again.lower() == 'nao' or not self.thread_list["novoCliente"].is_alive() :
                        #try:
                        self.anunciar("Desconectando do jogo...")
                        imprimir(self, " ")
                        imprimir(self, 'Obrigado por jogar!!! Volte sempre!!!'.center(80))
                        imprimir(self, '\r\nSaindo em  3..')
                        time.sleep(1)
                        imprimir(self, '           2..')
                        time.sleep(1)
                        imprimir(self, '           1..')
                        time.sleep(1)
                        self.msg = "/cmd quit"
                        enviarCliente(self)
                        #exit() # verificar como matar fiddleSocket e novoCliente...
                        break

                        #except SystemExit:
                        #    print("DEBUG: " + str(self.id) + " exit()")
                        #    self.askPlayer2 = False
                        #    self.game_condition = False
                        #    break
                    else :
                        
                        #for palavra in ["invalido","sim","nao"] :
                        if self.recv.lower() != "invalido" :
                            imprimir(self, '\r\nEntre uma escolha correta! E não: \"' + str(again) + '\"' )
                        else:
                            imprimir(self, " . ")
                            time.sleep(3)


                
        exit

    # fim do jogo aqui
    


    def run(self):

        self.thread_list["buscadorClientes"]        = threading.Thread(target=self.procurarClientes   , name="procurarClientes" + str(self.id) , args=() )
        
        # DEBUGGING de sessão válida para executar a lógica do jogo
        # thread_list["checkGameCondition"]      = threading.Thread(target=checkGameCondition , name="checkGameCondition" , args=() )
        # thread_list["checkGameCondition"].start()

        #print(self.thread_list)                    # DEBUG
        time.sleep(1)                               # aguardar uma thread iniciar antes de buscar clientes
    
        self.thread_list["buscadorClientes"].start()
        
        if not self.thread_list["buscadorClientes"].is_alive():
            print("\nA partida " + str(self.id) +" não subiu o buscador de clientes...\n")

    # depois definir a instância do jogador


    #def player_instance(self, con,addr) : 
    





def Main():

    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 50790                # Reserve a port for your service.

    print('Servidor iniciado!')
    print("HOST: ", host, ":", str(port))
    print('Esperando conexão do cliente...')

    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.

    
    print("Para sair use CTRL+C\n")
    
    contadorGlobal = 0
    
    while True: #msg != '\x18':
        
        match_list["partida" + str(contadorGlobal)] =  Partida( s, contadorGlobal )
        match_list["partida" + str(contadorGlobal)].run()

        # Debug pra saber do match_list e quais partidas ele contem...
        #ml_ctl = True
        #if ml_ctl :
        #    print(match_list) 
        #    ml_ctl = False

        contadorGlobal = contadorGlobal + 1

        
        
    s.close()


if __name__ == '__main__': 
    Main() 
    quit