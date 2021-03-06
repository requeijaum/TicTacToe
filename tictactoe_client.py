import os, time
import socket

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



podeConectar = False

HOST = input("Digite o nome do host: ") #'127.0.0.1'
if HOST == "" :
    HOST = socket.gethostname() #"ihack-de-rafael.local"
    print("\r\nUsando " + HOST + "!\r\n")

PORT = 50790  # ADV0 em T9

tcp = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
dest = (HOST, PORT)
print("HOST: " + HOST + ", PORT: " + str(PORT))
try:
    tcp.connect(dest)
    podeConectar = True
    pass
    
except ConnectionRefusedError:
    print("\r\nConexão recusada! O servidor está online?\r\n\r\n")
    exit

def capturarEntrada() :
    global msg
    
    while podeConectar :
        msg = input(">> ")


def interagirSocket():
    global msg
    global tcp
    global podeConectar

    print("Para sair use CTRL+X\r\n")

    msg_inicial = "Olá!"
    msg = msg_inicial

    print("Você disse '" + msg + "' para o servidor...")

    while True:         # respeitar ordem correta de operações para não dar problema
        time.sleep(0.5) # escrever linhas de forma organizada e sem cagar tudo
                        # envia qualquer coisa
        
        try:
            tcp.send(msg.encode())      # send() ou sendall()
            pass


        except BrokenPipeError:
            print("Conexão quebrada! Reinicie o cliente!")
            podeConectar = False
            exit()
    
        msg = "invalido"                # um controle de fluxo simples ;-)

        try:
            data_received = tcp.recv(1024)
        
        except ConnectionResetError:    # caso a conexão caia durante o recebimento do socket...
            print("Conexão reiniciada! Reinicie o cliente!")
            podeConectar = False
            exit()

        
        recv = data_received.decode()
        if len(recv) > 0 and "/cmd" not in recv :
            print(recv)
            #print("")

        if "/cmd " in recv :
            verb = recv.split("/cmd ")[1]
            
            try:

                # condicionais específicas
                if verb == "input" :
                    print("\r\nEntre com a posição desejada: ")
                    recv = "."
                    time.sleep(3)

                if verb == "cls" or verb == "clear" :
                    limparTela()

                if verb == "quit" :
                    tcp.close()
                    podeConectar = False
                    exit()

                #else:
                #    os.system(verb)


            except OSError as e:
                print("Comando não encontrado!")
                print(e)



# criar threads    
import threading
thread_list = {}

# nosso querido entrypoint - especificar para o Python3 executar mais rapidamente
if __name__ == '__main__': 

    # declarar threads
    thread_list["capturarEntrada"]            = threading.Thread(target=capturarEntrada , name="capturarEntrada", args=() )
    thread_list["interagirSocket"]            = threading.Thread(target=interagirSocket , name="interagirSocket", args=() )

    # iniciar threads
    if podeConectar == True :
        thread_list["capturarEntrada"].start()
        thread_list["interagirSocket"].start()

        # DEBUG
        #while True:
        #    thread_list["capturarEntrada"].join(timeout=3)

    # fim da condicional de conexao valida com servidor!

    # não existe como matar threads no Python. 
    # É necessário usar threading.join() e esperar que a thread conclua suas atividades.

    '''
    if not thread_list["interagirSocket"].is_alive() :
        tcp.close()
        quit

    else :
        thread_list["interagirSocket"].join()
    '''

    # exit()