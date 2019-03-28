import socket

HOST = input("Digite o nome do host: ") #'127.0.0.1'
if HOST == "" :
    HOST = "localhost"
    print("\nUsando localhost!\n")

PORT = 50777  # ADV0 em T9

tcp = socket.socket(
    socket.AF_INET , socket.SOCK_STREAM
)

dest = (HOST, PORT)

print("HOST: " + HOST + ", PORT: " + str(PORT))


tcp.connect(dest)
print("Para sair use CTRL+X\n")

#msg = input() # estado inicial
msg = "Olá!"

print("Você disse '" + msg + "' para o servidor...")

nomeJogador     = ""
armaJogador     = ""


while True: #(msg != '\x18') or (msg != "/kick " + nomeJogador) :            # respeitar ordem correta de operações para não dar merda
    # envia qualquer coisa
    tcp.sendall(msg.encode())

    data_received = tcp.recv(1024)
    texto = data_received.decode()
    if len(texto) > 0:
        print(texto)

    #tcp.send (msg.encode())
    msg = input(">> ")
    

tcp.close()
quit
