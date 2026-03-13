import socket

HOST = "127.0.0.1"
PORT = 1234

products = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Server started...")

while True:

    client, addr = server.accept()
    print("Client connected:", addr)

    data = client.recv(1024).decode().strip()
    parts = data.split()

    if len(parts) == 0:
        client.send("ERROR empty command".encode())
        client.close()
        continue

    command = parts[0].upper()

    if command == "ADD":
        if len(parts) < 3:
            client.send("ERROR invalid parameters".encode())
        else:
            key = parts[1]
            value = parts[2]
            products[key] = value
            client.send("OK - record add".encode())

    elif command == "GET":
        key = parts[1]
        if key in products:
            client.send(f"DATA {products[key]}".encode())
        else:
            client.send("ERROR invalid key".encode())

    elif command == "REMOVE":
        key = parts[1]
        if key in products:
            del products[key]
            client.send("OK value deleted".encode())
        else:
            client.send("ERROR invalid key".encode())

    elif command == "LIST":

        result = []
        for k, v in products.items():
            result.append(f"{k}={v}")

        response = "DATA|" + ",".join(result)
        client.send(response.encode())

    elif command == "COUNT":

        client.send(f"DATA {len(products)}".encode())

    elif command == "CLEAR":

        products.clear()
        client.send("all data deleted".encode())

    elif command == "UPDATE":

        key = parts[1]
        value = parts[2]

        if key in products:
            products[key] = value
            client.send("Data updated".encode())
        else:
            client.send("ERROR invalid key".encode())

    elif command == "POP":

        key = parts[1]

        if key in products:
            value = products.pop(key)
            client.send(f"DATA {value}".encode())
        else:
            client.send("ERROR invalid key".encode())

    elif command == "QUIT":

        client.send("Server closing".encode())
        client.close()
        break

    else:
        client.send("ERROR unknown command".encode())

    client.close()