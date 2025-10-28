import socket

host = '172.18.110.126'
port  = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host,port))
    s.listen()
    print(f"Listening on {host}:{port}")
    conn,add = s.accept()

    with conn:
        print('Connected by', add)

        while True:
            data = conn.recv(1024).decode()

            if not data:
                break
            if data.lower == 'exit':
                print('Connection closed by client.')
                break
            print(f'Client: {data}')
            reply = input('Server: ')
            conn.sendall(reply.encode())

            if reply.lower() == 'exit':
                print('Connection closed by server.')
                break

