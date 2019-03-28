import time
import os
import textwrap
import socket
import threading

# Dicas
# print() -> ver apenas no servidor
# imprimir() -> enviar para o cliente e mostrar no servidor



# globais
score       = []                        # Create a global score object
s           = socket.socket()           # Create a global socket object
c           = None                      # Create a global clientsocket instance
addr        = None


data_recv = ""
data_send = ""
game_condition = False

msg = "Testando 1234"           # enviar ao cliente - mensagem inicial não-nula
recv = ""                       # recebido do cliente

askPlayer2 = True

thread_list = {
    "socketCriado"              : None,
    "buscadorClientes"          : None,
    "novoCliente"               : None,
    "enviarCliente"             : None

}

def createServerSocket(s):
    global game_condition

    # s = socket.socket()       # Create a socket object
    host = 'ihack-de-rafael.local'          # socket.gethostname() # Get local machine name
    port = 50790                # Reserve a port for your service.

    print('Server started!')
    print("HOST: ", host, ":", str(port))
    print('Waiting for clients...')

    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.

    # print('Got connection from', (host,str(port)))
    # print("Para sair use CTRL+X\n")
    imprimir("\nPlayer X --> Servidor\nPlayer O --> Cliente\n")
    #time.sleep(5)
    #input("\nAperte qualquer tecla para continuar...")


def fiddleSocket():
    global s
    global game_condition
    global thread_list
    global msg  # criar ponteiro automaticamente
    global c
    global addr

    #while msg != '\x18':
    #game_condition = True

    #while game_condition = True:
    c, addr = s.accept()     # Establish connection with client.
    game_condition = True

    thread_list["novoCliente"]      = threading.Thread(target=novoCliente   , name="novoCliente" , args=() )
    #thread_list["enviarCliente"]    = threading.Thread(target=enviarCliente , name="enviarCliente" , args=() )    # este msg precisa apontar para o msg global
    
    thread_list["novoCliente"].start()
    #thread_list["enviarCliente"].start()  # não enviar agora!

    if thread_list["novoCliente"].is_alive():
        thread_list["novoCliente"].join()

    if game_condition == False : 
        s.close()


def checkGameCondition() :
    global game_condition

    while True :
        print("game_condition: " + str(game_condition))
        time.sleep(3)


def novoCliente():
    global game_condition
    global recv
    global msg
    global c
    global addr

    #first setup
    msg = "Olá!"

    while True:
        time.sleep(0.1)   # tentar encher buffer? serve pra escrever \n corretamente - no cliente5
        try:
            data_received = c.recv(1024)
            pass

        except:
            print("Ocorreu um erro ao processar o comando recebido!")
            exit

        if len(data_received.decode()) > 0:
            recv = data_received.decode()
            if recv != "invalido":
                print(addr, ' >> ', recv)
        

        #debug
        #enviarCliente()
        #imprimir("")

        #if not data_received: break        
        #do some checks and if msg == someWeirdSignal: break:
        
        

        #msg = input('SERVER >> ')
        
        #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
        
        #c.send(msg.encode())

    c.close()
    print("\nQue feio, servidor! O cliente saiu do jogo!\n")
    game_condition = False


def enviarCliente() :
    global msg         # usar argumento
    global c
    
    try:
        time.sleep(0.5) # na verdade a magica da impressao e envio de dados fica aqui... ajustar pra esse valor sempre funciona
        #print(str(type(c)))
        
        if type(c) != type(None) :
            c.send(msg.encode())
        
        pass

    except:
        print("\nDEBUG: Algum erro ocorreu ao processar o envio...\n")
        pass

    '''
    print(getattr(s, "getpeername"))

    if not type(c) == "NoneType" : 
        if getattr(s, "getpeername") :
            c.send(msg.encode())
        else:
            print("Não foi possível enviar: " + msg)
    else :
        print("\n>> Calma! O socket ainda não foi instanciado!\n")
        #print(msg)
        #exit  #forçar saída
    '''

def imprimir(texto):
    global msg
    msg = texto
    enviarCliente()
    
    #if thread_list["enviarCliente"].is_alive() :
    #    thread_list["enviarCliente"].join()
    #else: 
    #    thread_list["enviarCliente"].start()  # mudou msg pra texto e roda

    #thread_list["enviarCliente"].join() # redundancia pra verificar se a thread acabou

        
    print(texto)



def procurarClientes():
    global game_condition
    global thread_list

    thread_list["fiddleSocket"] = threading.Thread(target=fiddleSocket , name="fiddleSocket", args=() )

    # comentei o Main para debuggar o socket

    thread_list["Main"]         = threading.Thread(target=Main , name="Main", args=() )

    thread_list["fiddleSocket"].start()
    

    while game_condition == False:
        print("\n Não encontramos clientes disponiveis...")
        time.sleep(3)

    # \/\/\/\/ comentei isso aqui tudo pra poder debuggar o socket... \/\/\/\/

    if game_condition == True : #and thread_list["Main"].is_alive() : #and type(thread_list["Main"]) == "Thread" :
        thread_list["Main"].start()
    
    
    


def full():
    if ' ' not in score:
        imprimir('\nThe game has resulted into a catgame. ( ͡° ͜ʖ ͡°)')
        return True


def board_display(score):
    imprimir(' '+score[6]+ ' | '+ score[7]+ ' | '+ score[8] )#+ "\n")
    imprimir('---+---+---'  )#+ "\n")   
    imprimir(' '+score[3]+ ' | '+ score[4]+ ' | '+ score[5] )#+ "\n")
    imprimir('---+---+---' )#+ "\n")
    imprimir(' '+score[0]+ ' | '+ score[1]+ ' | '+ score[2] )#+ "\n")


def check(char, posi1, posi2, posi3):
    if score[posi1] == char and score[posi2] == char and score[posi3] == char:
        return True


def checkall(char):
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


def comandoSistema(cmd):
    global msg
    msg = "/cmd " + cmd
    enviarCliente()
    os.system(cmd)

def Main():

    global thread_list
    global game_condition
    global score
    global msg
    global recv
    global askPlayer2

    comandoSistema("clear")
    # imprimir('Tic Tac Toe\n'.center(70))
    banner = r'''
                 _____  _  ____     _____  ____  ____     _____  ____  _____
                /__ __\/ \/   _\   /__ __\/  _ \/   _\   /__ __\/  _ \/  __/
                  / \  | ||  / _____ / \  | / \||  / _____ / \  | / \||  \
                  | |  | ||  \_\____\| |  | |-|||  \_\____\| |  | \_/||  /_
                  \_/  \_/\____/     \_/  \_/ \|\____/     \_/  \____/\____\ '''

    imprimir(banner)
    imprimir('\nThe board is numbered in the form of the numpad keyboard as printed below.\n')
    time.sleep(0.01)
    score = ['1', '2', '3',
            '4', '5', '6',
            '7', '8', '9']

    board_display(score)

    value = '\nThe object of Tic Tac Toe is to get three in a row. You play on a three by three game board. The first player is known as X and the second is O. Players alternate placing Xs and Os on the game board until either opponent has three in a row or all nine squares are filled. X always goes first, and in the event that no one has three in a row, the stalemate is called a cat game.'
    wrapper = textwrap.TextWrapper(width=72)
    string = wrapper.fill(text=value)
    imprimir('\n' )
    imprimir(string)

    while game_condition :

        imprimir('\nChoose your cells accordingly.\nThe game will begin in 10 seconds.')
        time.sleep(10)

        score = [' ']*9
        while True:
            comandoSistema('clear')
            board_display(score)
            if full():                
                break
            if not thread_list["novoCliente"].is_alive():       # controle de sessão!
                #player2 = ""
                break
            while True:
                try:
                    msg = "Waiting Player X"
                    enviarCliente()
                    player1 = int(input('\nPlayer X, choose your position: '))
                    if score[player1-1] != 'X' and score[player1-1] != 'O':
                        score[player1-1] = 'X'
                        break
                    else:
                        imprimir('\nThis position is already taken, please try again.')
                        #continue
                        break
                except:
                    imprimir('\nKindly enter a valid value')
                    continue
            comandoSistema('clear')
            board_display(score)
            if checkall('X'):
                imprimir('\nPlayer X is the winner')
                time.sleep(0.1)
                break
            if full():
                break
            #special stuff
            print("\n\n > Waiting player O")    
            
            while askPlayer2:
                try:
                    while len(recv) < 1 : #or recv == "invalido" :   # a mágica está aqui e em recv = "invalido"
                        #print("\n\n > Waiting player O")
                        time.sleep(3)
                        #time.sleep()
                        #continue

                    #player2 = int(input('\nPlayer O, choose your position: '))
                    msg = "\nPlayer O, choose your position: "
                    enviarCliente()
                    time.sleep(5)
                    #print("DEBUG: recv = " + recv)
                    #if len(recv) > 0 and int(recv) in [0,1,2,3,4,5,6,7,8,9] :
                    if len(recv) == 1:
                        player2 = int(recv)



                        if score[player2-1] != 'X' and score[player2-1] != 'O':
                            score[player2-1] = 'O'
                            break
                        else:
                            if len(recv) == 0 or len(recv) == 1 :
                                imprimir('\nThis position ' + str(recv) + ' is already taken, please try again.')
                                #time.sleep(5)
                            continue

                        break
                    #recv = "100"    # setar pra um valor fora do escopo [0-9]... tem que ser um número. Nunca pode ser uma string vazia!
                    #break
                    pass  # talvez isso quebre tudo!
                except:
                    #if len(recv) == 0 : 
                    imprimir('\nKindly enter a valid value - not ' + str(recv))
                    #time.sleep(5)
                    continue
            comandoSistema('clear')
            board_display(score)
            if checkall('O'):
                imprimir('\nPlayer O is the winner')
                time.sleep(0.1)
                break
            if full():
                break

        # forçar fechar socket
        if thread_list["novoCliente"].is_alive() :
            s.close()
        msg = "O servidor está decidindo se ele quer jogar de novo..."
        enviarCliente()
        again = input('\nDo you want to play again? Enter Yes or No: ')
        if again.lower() == 'yes':
            continue
        elif again.lower() == 'no':
            imprimir(" ")
            imprimir('Thanks for playing TIC TAC TOE, do come again!!'.center(80))
            imprimir('\nExiting in 3..')
            time.sleep(1)
            imprimir('           2..')
            time.sleep(1)
            imprimir('           1..')
            time.sleep(1)
            msg = "/cmd quit"
            enviarCliente()
            break
        else:
            imprimir('\nEnter a correct choice')

    exit

# fim do jogo aqui

if __name__ == '__main__': 

    # declarar threads - nitratine.net...
    thread_list["socketCriado"]            = threading.Thread(target=createServerSocket , name="createServerSocket", args=(s,) )
    thread_list["buscadorClientes"]        = threading.Thread(target=procurarClientes   , name="procurarClientes", args=() )

    # verificar sessão válida para executar a lógica do jogo
    #thread_list["checkGameCondition"]      = threading.Thread(target=checkGameCondition , name="checkGameCondition" , args=() )
    #thread_list["checkGameCondition"].start()

    thread_list["socketCriado"].start()
    time.sleep(5) # aguardar uma thread iniciar...
    thread_list["buscadorClientes"].start()
    
    quit