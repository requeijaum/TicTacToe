import time
import os
import socket

HOST = input("Digite o nome do host: ") #'127.0.0.1'
if HOST == "" :
    HOST = "localhost"
    print("\nUsando localhost!\n")

PORT = 50790  # ADV0 em T9

tcp = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
dest = (HOST, PORT)
print("HOST: " + HOST + ", PORT: " + str(PORT))
tcp.connect(dest)
print("Para sair use CTRL+X\n")

msg = "Olá!"
print("Você disse '" + msg + "' para o servidor...")


def capturarEntrada() :
    global msg
    msg = input(">> ")


def interagirSocket():
    global msg
    global tcp

    while True: #(msg != '\x18') or (msg != "/kick " + nomeJogador) :            # respeitar ordem correta de operações para não dar merda

        # envia qualquer coisa
        if len(msg) > 0 :
            tcp.sendall(msg.encode())
            msg = ""    # limpar msg

        data_received = tcp.recv(1024)
        texto = data_received.decode()
        if len(texto) > 0:
            print(texto)

        #tcp.send (msg.encode())
        #msg = input(">> ")

        if texto == "/quit 0" :
            print("AVISO: O servidor fechou o jogo!")
            tcp.close()
    
import threading
thread_list = {}


if __name__ == '__main__': 

    # declarar threads
    thread_list["capturarEntrada"]            = threading.Thread(target=capturarEntrada , name="capturarEntrada", args=() )
    thread_list["interagirSocket"]            = threading.Thread(target=interagirSocket , name="interagirSocket", args=() )

    # iniciar threads
    thread_list["capturarEntrada"].start()
    thread_list["interagirSocket"].start()



    #tcp.close()
    quit
