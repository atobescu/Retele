import socket

HOST = "127.0.0.1"
PORT = 1234

while True:

    command = input("Enter command: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    client.send(command.encode())

    response = client.recv(1024).decode()

    print("Server:", response)

    client.close()

    if command.upper() == "QUIT":
        break