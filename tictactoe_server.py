import time
import os
import textwrap
import socket
import threading

# globais
score       = []                        # Create a global score object
s           = socket.socket()           # Create a global socket object
c           = None                      # Create a global clientsocket instance
addr        = None


data_recv = ""
data_send = ""
game_condition = False

msg = ""                        # enviar ao cliente
recv = ""                       # recebido do cliente

thread_list = {
    "socketCriado"              : None,
    "buscadorClientes"          : None,
    "novoCliente"               : None,
    "enviarCliente"             : None

}

def createServerSocket(s):
    global game_condition

    # s = socket.socket()       # Create a socket object
    host = '127.0.0.1'          # socket.gethostname() # Get local machine name
    port = 50777                # Reserve a port for your service.

    print('Server started!')
    print("HOST: ", host, ":", str(port))
    print('Waiting for clients...')

    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.

    # print('Got connection from', (host,str(port)))
    # print("Para sair use CTRL+X\n")
    print("\nPlayer X --> Servidor\nPlayer O --> Cliente\n")
    #time.sleep(5)
    #input("\nAperte qualquer tecla para continuar...")


def fiddleSocket(s):
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

    while True:
        time.sleep(1)   # tentar encher buffer?
        data_received = c.recv(1024)
        recv = data_received.decode()
        #if len(recv) > 0 :
        #    print(addr, ' >> ', recv)
        print(addr, ' >> ', recv)

        #debug
        enviarCliente()

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
    
    c.send(msg.encode())
    
    print(">> " + msg)
    #exit  #forçar saída


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

    thread_list["fiddleSocket"] = threading.Thread(target=fiddleSocket , name="fiddleSocket", args=(s,) )

    # comentei o Main para debuggar o socket

    #thread_list["Main"]         = threading.Thread(target=Main , name="Main", args=() )

    thread_list["fiddleSocket"].start()
    

    while game_condition == False:
        print("\n Não encontramos clientes disponiveis...")
        time.sleep(5)

    # \/\/\/\/ comentei isso aqui tudo pra poder debuggar o socket... \/\/\/\/

    #if game_condition == True : #and thread_list["Main"].is_alive() : #and type(thread_list["Main"]) == "Thread" :
    #    thread_list["Main"].start()
    
    
    


def full():
    if ' ' not in score:
        print('\nThe game has resulted into a catgame. ( ͡° ͜ʖ ͡°)')
        return True


def board_display(score):
    print(' '+score[6], '|', score[7], '|', score[8])
    print('---+---+---')
    print(' '+score[3], '|', score[4], '|', score[5])
    print('---+---+---')
    print(' '+score[0], '|', score[1], '|', score[2])


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


def Main():

    global thread_list
    global game_condition
    global score

    # print('Tic Tac Toe\n'.center(70))
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

        imprimir('\nChoose your cells accordingly.The game will begin in 10 seconds.')
        time.sleep(10)

        score = [' ']*9
        while True:
            os.system('clear')
            board_display(score)
            if full():                
                break
            if not thread_list["novoCliente"].is_alive():       # controle de sessão!
                #player2 = ""
                break
            while True:
                try:
                    player1 = int(input('\nPlayer X, choose your position: '))
                    if score[player1-1] != 'X' and score[player1-1] != 'O':
                        score[player1-1] = 'X'
                        break
                    else:
                        imprimir('\nThis position is already taken, please try again.')
                        continue
                except:
                    imprimir('\nKindly enter a valid value')
                    continue
            os.system('clear')
            board_display(score)
            if checkall('X'):
                imprimir('\nPlayer X is the winner')
                time.sleep(0.1)
                break
            if full():
                break
            while True:
                try:
                    player2 = int(input('\nPlayer O, choose your position: '))
                    if score[player2-1] != 'X' and score[player2-1] != 'O':
                        score[player2-1] = 'O'
                        break
                    else:
                        imprimir('\nThis position is already taken, please try again.')
                        continue
                except:
                    imprimir('\nKindly enter a valid value')
                    continue
            os.system('clear')
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
    thread_list["checkGameCondition"]      = threading.Thread(target=checkGameCondition , name="checkGameCondition" , args=() )
    thread_list["checkGameCondition"].start()

    thread_list["socketCriado"].start()
    time.sleep(5) # aguardar uma thread iniciar...
    thread_list["buscadorClientes"].start()
    
    quit