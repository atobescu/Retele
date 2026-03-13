import socket
import threading

HOST = "127.0.0.1"
PORT = 3333
BUFFER_SIZE = 1024


data_store = {}
lock = threading.Lock()


def build_response(message):
    return f"{len(message)} {message}".encode()


def execute_command(cmd):

    tokens = cmd.split()

    if not tokens:
        return "ERROR empty command"

    command = tokens[0].upper()

    if command == "ADD":

        if len(tokens) < 3:
            return "ERROR invalid parameters"

        key = tokens[1]
        value = " ".join(tokens[2:])

        with lock:
            data_store[key] = value

        return "OK record added"


    elif command == "GET":

        if len(tokens) != 2:
            return "ERROR invalid parameters"

        key = tokens[1]

        with lock:
            if key in data_store:
                return f"DATA {data_store[key]}"
            else:
                return "ERROR invalid key"


    elif command == "REMOVE":

        if len(tokens) != 2:
            return "ERROR invalid parameters"

        key = tokens[1]

        with lock:
            if key in data_store:
                del data_store[key]
                return "OK value deleted"
            else:
                return "ERROR invalid key"


    elif command == "LIST":

        with lock:
            pairs = [f"{k}={v}" for k, v in data_store.items()]

        return "DATA|" + ",".join(pairs)


    elif command == "COUNT":

        with lock:
            return f"DATA {len(data_store)}"


    elif command == "CLEAR":

        with lock:
            data_store.clear()

        return "OK all data deleted"


    elif command == "UPDATE":

        if len(tokens) < 3:
            return "ERROR invalid parameters"

        key = tokens[1]
        value = " ".join(tokens[2:])

        with lock:
            if key in data_store:
                data_store[key] = value
                return "OK data updated"
            else:
                return "ERROR invalid key"


    elif command == "POP":

        if len(tokens) != 2:
            return "ERROR invalid parameters"

        key = tokens[1]

        with lock:
            if key in data_store:
                value = data_store.pop(key)
                return f"DATA {value}"
            else:
                return "ERROR invalid key"


    elif command == "QUIT":
        return "OK connection closed"


    return "ERROR unknown command"



def client_thread(conn):

    while True:

        try:
            data = conn.recv(BUFFER_SIZE)

            if not data:
                break

            command = data.decode().strip()

            result = execute_command(command)

            conn.sendall(build_response(result))

            if command.upper() == "QUIT":
                break

        except:
            conn.sendall(build_response("ERROR server problem"))
            break

    conn.close()



def start():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("Server running on port", PORT)

    while True:

        conn, addr = server.accept()

        print("Client connected:", addr)

        t = threading.Thread(target=client_thread, args=(conn,))
        t.start()



if __name__ == "__main__":
    start()