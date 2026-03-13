import socket

HOST = "127.0.0.1"
PORT = 3333
BUFFER_SIZE = 1024


def read_message(sock):

    data = sock.recv(BUFFER_SIZE).decode()

    if not data:
        return None

    parts = data.split(" ", 1)

    if len(parts) != 2:
        return "Invalid server response"

    length = int(parts[0])
    message = parts[1]

    while len(message) < length:
        message += sock.recv(BUFFER_SIZE).decode()

    return message


def run_client():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    print("Connected to server")

    while True:

        cmd = input("cmd> ")

        s.send(cmd.encode())

        response = read_message(s)

        print("Server:", response)

        if cmd.upper() == "QUIT":
            break

    s.close()


if __name__ == "__main__":
    run_client()