import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('172.18.110.126',12345))
    print("Connected to server.")

    while True:
        message = input("Client: ")
        s.sendall(message.encode())

        if message.lower() == 'exit':
            print("Connection closed by client.")
            break   
        data = s.recv(1024).decode()
        print(f"Server: {data}")

        if data.lower() == 'exit':
            print("Connection closed by server.")
            break