import time
import os
import textwrap
import socket
import threading

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
def limparTela():
    os.system('cls' if os.name == 'nt' else 'clear')



# variáveis globais

host = socket.gethostname()             #'localhost' ou socket.gethostname() --> Saber o nome de host da máquina
port = 50790                            # Reservar/alocar uma porta para o serviço


banner = r'''
                 _____  _  ____     _____  ____  ____     _____  ____  _____
                /__ __\/ \/   _\   /__ __\/  _ \/   _\   /__ __\/  _ \/  __/
                  / \  | ||  / _____ / \  | / \||  / _____ / \  | / \||  \
                  | |  | ||  \_\____\| |  | |-|||  \_\____\| |  | \_/||  /_
                  \_/  \_/\____/     \_/  \_/ \|\____/     \_/  \____/\____\ '''


score       = []                        # Criar um vetor global de pontuação (score)
s           = socket.socket()           # Criar um objeto global de socket
c           = None                      # Criar uma instância global de socket do cliente - é um tuple: (c,addr)
addr        = None

game_condition = False                  # Variável global que armazena o estado de condição de um jogo - válido ou inválido - para sustentar a conexão

msg = "Testando 1234"           # enviar ao cliente - mensagem inicial nunca pode ser nula, pois socket não envia algo com 0 bytes!
recv = ""                       # recebido do cliente

askPlayer2 = True               # variável booleana que verifica se pode perguntar algo ao cliente (Jogador O - remoto)

# dict que armazena as threads. Estou definindo elas aqui por boas-práticas.
thread_list = {
    "socketCriado"              : None,
    "buscadorClientes"          : None,
    "novoCliente"               : None,
    "enviarCliente"             : None

}

def createServerSocket(s):                  # Criar socket no servidor - chamar via thread
    global game_condition
    global host
    global port

    print('Server started!')
    print("HOST: ", host, ":", str(port))
    print('Waiting for clients...')

    # colocar esse try dentro de um while para permitir tentativas sucessivas de subir o servidor

    try:
        s.bind((host, port))                # Fazer bind da porta
        s.listen(5)                         # Esperar conexão do cliente!

        imprimir("\nJogador X --> Servidor\nJogador O --> Cliente\n")

        # esperar um pouco antes de chamar a thread que conecta o cliente com o servidor
        #time.sleep(5)
        #input("\nAperte qualquer tecla para continuar...")

    except OSError :                        # caso o endereço ou porta não possa ser ofertado
        print("Erro!!! Verificar se o endereço ou porta estão corretos!")
        host = input("Entre com o nome de HOST para tentar novamente: ")
        exit


def fiddleSocket():                         # não passar parâmetro... precisamos referenciar os dados!
    global s
    global game_condition
    global thread_list
    global msg                              # o Python3 vai criar um ponteiro automaticamente - precisamos usar a variável global "msg"
    global c
    global addr

    c, addr = s.accept()                    # Estabelecer conexão com o cliente!
    game_condition = True                   # E mudar a condição de jogo para válida!

    # declarar thread que instancia um novo cliente conectado - e iniciar assim que possível!
    thread_list["novoCliente"]      = threading.Thread(target=novoCliente   , name="novoCliente" , args=() )
    thread_list["novoCliente"].start()

    # caso a thread esteja viva e funcionando: entre no processo e verifique quando ele vai parar - detectar encerramento da thread com join()
    if thread_list["novoCliente"].is_alive():
        thread_list["novoCliente"].join()   # essa thread pode mudar o game_condition


    if game_condition == False :            # caso algo dê errado no jogo: feche o socket!
        s.close()


def checkGameCondition() :                  # Função para DEBUGGING da thread que verifica se o jogo ainda é válido e a conexão deve persistir
    global game_condition

    while True :
        print("game_condition: " + str(game_condition))
        time.sleep(3)


def novoCliente():
    global game_condition
    global askPlayer2
    global recv
    global msg
    global c
    global addr

    # precisamos de uma string não nula no estado inicial
    msg = "Olá!"

    while True :    # loop infinito

        # esse delay aqui é muito importante para não causar 100% de uso da CPU ao processar mensagens!
        time.sleep(0.1)   # tentar encher buffer? serve pra escrever \n corretamente - no cliente

        try:                                    # tentar receber algo do socket... se vier vazio: rode "except"
            data_received = c.recv(1024)
            pass

        except:                                 # caso não consiga receber... suba uma exceção e avise que deu erro antes de sair do jogo!
            print("Ocorreu um erro ao processar o comando recebido!")
            askPlayer2 = False
            game_condition = False
            break


        if len(data_received.decode()) > 0:     # decodificar fluxo de bytes para string. Caso a string resultante não seja vazia:
            recv = data_received.decode()

            if recv != "invalido":              # string utilizada para controle de fluxo entre servidor e cliente
                print(addr, ' >> ', recv)       # caso o servidor receba "invalido": não imprima na tela. Essa mensagem é inútil para os jogadores.
    

    # a partir daqui: significa que o socket do cliente foi encerrado e o servidor não irá receber mais dados!
    c.close()   
    print("\nQue feio, servidor! O cliente saiu do jogo!\n")
    game_condition = False                      # sem cliente: sem jogo!


def enviarCliente() :                           # Função para enviar mensagens ao cliente!

    global msg                                  # usar variavel global ou argumento?
    global c
    global game_condition
    global askPlayer2

    try:
        time.sleep(0.5)                         # delay utilizado para controlar o uso de CPU ao enviar mensagens... não pode ser muito rápido!
                                                # se for muito rápido: o cliente pode errar a quebra de linhas e mostrar texto mal-formatado
                                                # ajustar pra esse valor ajuda a resolver problemas no cliente
        

        if type(c) != type(None) :              # Verificar se o socket do cliente está "nulo". 
            try:
                c.send(msg.encode())                # O servidor pode tentar enviar algo ao cliente sem um socket conectado!
        
            #except Exception as e:
            #    print(e)                    # subir Exception e ver na tela

            except BrokenPipeError:
                c.close()                   # forçar parada do socket do cliente - está quebrado!
                quit
            
            except OSError :
                game_condition = False
                askPlayer2 = False
                quit
        pass

    except:
        print("\nDEBUG: Algum erro ocorreu ao processar o envio...\n") 
        pass


def imprimir(texto):                            # Função que imprime texto para o cliente e para o servidor!
    global msg                                  # Precisamos referenciar a mensagem que será enviada para o cliente.
    msg = texto

    enviarCliente()
    print(texto)



def procurarClientes():                         # Função para ser utilizada na thread que procura por conexões válidas antes de iniciar a lógica do jogo
    global game_condition
    global thread_list

    # declarar thread para a função que faz-tudo pelo cliente "fiddleSocket()" - e declarar thread para lógica do jogo em "Main()"
    thread_list["fiddleSocket"] = threading.Thread(target=fiddleSocket , name="fiddleSocket", args=() )
    thread_list["Main"]         = threading.Thread(target=Main , name="Main", args=() )

    thread_list["fiddleSocket"].start()         # iniciar interação por socket
    

    while game_condition == False:              # verifica a condição de jogo periodicamente.
        print("\n Não encontramos clientes disponiveis...")
        time.sleep(3)


    if game_condition == True :                 # a condição de jogo é válida! Vamos jogar!
        thread_list["Main"].start()
    
    

def full():                                     # Função que verifica se todas as casas 3x3 estão preenchidas
    if ' ' not in score:
        imprimir('\nO jogo resultou em um empate... jogo de gato e rato!\n( ͡° ͜ʖ ͡°)')
        return True


def board_display(score):                       # Função que imprime o tabuleiro. Recebe o vetor "score" como parâmetro.
    
    imprimir(' '+score[6]+ ' | '+ score[7]+ ' | '+ score[8] )#+ "\n")
    imprimir('---+---+---'  )#+ "\n")   
    imprimir(' '+score[3]+ ' | '+ score[4]+ ' | '+ score[5] )#+ "\n")
    imprimir('---+---+---' )#+ "\n")
    imprimir(' '+score[0]+ ' | '+ score[1]+ ' | '+ score[2] )#+ "\n")


def check(char, posi1, posi2, posi3):           # Função que verifica posições e caracteres válidos dentro de uma linha do tabuleiro (3x3)
                                                # Serve para verificar que uma linha foi completada por um dos jogadores.

    if score[posi1] == char and score[posi2] == char and score[posi3] == char:
        return True


def checkall(char):                             # Algoritmo que verifica todas as linhas possíveis que podem ser feitas no tabuleiro
    if check(char, 0, 1, 2):
        return True
    if check(char, 3, 4, 5):
        return True
    if check(char, 6, 7, 8):
        return True
    if check(char, 0, 3, 6):
        return True
    if check(char, 1, 4, 7):
        return True
    if check(char, 2, 5, 8):
        return True
    if check(char, 0, 4, 8):
        return True
    if check(char, 2, 4, 6):
        return True
    return False


def comandoSistema(cmd):                        # Função que executa um comando do sistema em ambos cliente e servidor
    global msg
    msg = "/cmd " + cmd
    enviarCliente()

    if cmd != "clear" or cmd != "cls" :         # verificar condição de limpar tela... de acordo com o sistema operacional
        os.system(cmd)

    else:
        limparTela()


def Main():                                     # Função que contêm a lógica principal do jogo.
                                                # Deve ser invocada usando uma thread.

    global thread_list
    global game_condition
    global score
    global msg
    global recv
    global askPlayer2
    global banner

    comandoSistema("clear")
    # imprimir('Tic Tac Toe\n'.center(70))
    
    imprimir(banner)
    imprimir('\nO tabuleiro é numerado em forma de teclado numérico, conforme impresso abaixo.\n')

    time.sleep(0.01)
    score = ['1', '2', '3',
            '4', '5', '6',
            '7', '8', '9']

    board_display(score)
    imprimir("\n")
    
    # imprimir instruções de jogo de forma estilizada com quebra de linha automática em 72 caracteres
    value = '\n\nO objetivo do Jogo da Velha é obter três marcas em linha. Você joga em um tabuleiro de três por três. O primeiro jogador é conhecido como X e o segundo é O. Os jogadores alternam colocando Xs e Os no tabuleiro até que um dos oponentes tenha três em sequência ou todos os nove quadrados estejam preenchidos. X sempre vai primeiro. No caso de ninguém ter três em linha, o empate é chamado de jogo de gato!\n'
    wrapper = textwrap.TextWrapper(width=72)
    string = wrapper.fill(text=value)
    
    #imprimir('\n' )
    imprimir(string)

    while game_condition :                      # Enquanto a condição de jogo for verdadeira... executar a lógica de jogo!

        imprimir('\nEm suas marcas...\nO jogo começará em 10 segundos.')
        time.sleep(10)

        score = [' ']*9                         # iniciar tabuleiro e vetor de pontuação

        while True:                             # loop infinito

            comandoSistema('clear')
            board_display(score)
                                                # parar o jogo...    
            if full():                          # caso o tabuleiro não tenha células vazias!
                break                           # caso a thread de conexão não esteja rodando!
            if not thread_list["novoCliente"].is_alive():       
                break

            while True:                         # loop infinito
                try:                            # explicar essa porra
                    msg = "\n>> Esperando Jogador X"
                    enviarCliente()
                    player1 = int(input('\nJogador X, escolha sua posição: '))
                    if score[player1-1] != 'X' and score[player1-1] != 'O':
                        score[player1-1] = 'X'
                        break
                    else:
                        imprimir('\nEssa posição já foi escolhida! Por favor, tente novamente.')
                        break
                except:
                    print('\nPor favor... entre um valor válido...')            # mensagem exclusiva ao Jogador X
                    continue
            comandoSistema('clear')
            board_display(score)
            if checkall('X'):
                imprimir('\nJogador X é o vencedor!')
                time.sleep(0.1)
                break
            if full():
                break
            # mostrar que está esperando o cliente remoto fazer a jogada
            print("\n\n>> Esperando Jogador O...")    
            
            contarPergunta = 0
            while askPlayer2:                   # enquanto for o momento de interagir com o cliente e esperar uma entrada de dados dele...
                try:
                    #while len(recv) < 1 :       # explicar essa mágica
                    #    time.sleep(3)
                      
                    if len(recv) != 1:          # acho que vai quebrar a mágica
                        #msg = "\nJogador O, escolha sua posição: "
                        msg = "/cmd input"
                        
                    else: 
                        msg = "."
                    

                    if contarPergunta < 1 :
                        enviarCliente()
                        contarPergunta = contarPergunta + 1   

                    else:
                        msg = " . "                 
                    
                    enviarCliente()
                    time.sleep(1)               # outro delay?

                    #print("DEBUG: recv = " + recv)
                    if len(recv) == 1 : # and (int(recv) in [0,1,2,3,4,5,6,7,8,9]) :
                        #msg = "."        # tentar limpar msg pra não cometer erro por redundância
                        player2 = int(recv)
                        contarPergunta = 0
                        

                        # caso seja um valor numérico válido de jogada...

                        if score[player2-1] != 'X' and score[player2-1] != 'O':
                            score[player2-1] = 'O'
                            break
                        else:
                            if len(recv) == 0 or len(recv) == 1 :
                                imprimir('\nA posição \"' + str(recv) + '\" já foi marcada! Por favor, tente novamente.')
                                
                            continue

                        break
                        
                    
                    if len(recv) != 1 and recv != "invalido" :  # nunca verificar nada contra a string "invalido" a ser recebida
                        imprimir('\nNEW: Por favor... entre um valor válido... e não \"' + str(recv) + '\" ')
                        continue    # forçar ir ao pass do try? Não!

                    pass  # talvez isso quebre tudo! # explicar essa porra


                except Exception as e :
                    print(e)
                    #imprimir('\nOLD: Por favor... entre um valor válido... e não \"' + str(recv) + '\" ' )
                    continue


            comandoSistema('clear')
            board_display(score)

            if checkall('O'):
                imprimir('\nJogador O é o vencedor!')
                time.sleep(0.1)
                break
            if full():
                break

        # forçar fechar socket
        if thread_list["novoCliente"].is_alive() :
            s.close()
        
        msg = "O servidor está decidindo se ele quer jogar de novo..."
        enviarCliente()
        
        again = input('\nVocê quer jogar de novo? Entre com \"sim\" ou \"nao\": ')
        if again.lower() == 'sim':
            continue
        elif again.lower() == 'nao' or not thread_list["novoCliente"].is_alive() :
            imprimir(" ")
            imprimir('Obrigado por jogar!!! Volte sempre!!!'.center(80))
            imprimir('\nSaindo em  3..')
            time.sleep(1)
            imprimir('           2..')
            time.sleep(1)
            imprimir('           1..')
            time.sleep(1)
            msg = "/cmd quit"
            enviarCliente()
            break
        else:                       # verificar se esse ELIF tá correto!
            imprimir('\nEntre uma escolha correta')

    exit

# fim do jogo aqui

if __name__ == '__main__': 

    # declarar threads - segundo: https://nitratine.net/blog/post/python-threading-basics/
    thread_list["socketCriado"]            = threading.Thread(target=createServerSocket , name="createServerSocket", args=(s,) )
    thread_list["buscadorClientes"]        = threading.Thread(target=procurarClientes   , name="procurarClientes", args=() )

    # DEBUGGING de sessão válida para executar a lógica do jogo
    # thread_list["checkGameCondition"]      = threading.Thread(target=checkGameCondition , name="checkGameCondition" , args=() )
    # thread_list["checkGameCondition"].start()

    thread_list["socketCriado"].start()         # iniciar createServerSocket(s)
    thread_list["socketCriado"].join()          # verificar se deu tudo certo ao criar o socket do servidor

    time.sleep(5)                               # aguardar uma thread iniciar antes de buscar clientes
    thread_list["buscadorClientes"].start()
    

        