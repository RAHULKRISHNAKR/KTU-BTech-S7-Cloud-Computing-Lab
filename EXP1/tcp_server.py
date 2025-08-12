import socket

def start_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}...")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    print("Connection closed by client.")
                    break
                print(f"Client says: {data.decode()}")
                
                reply = input("Enter message to send to client (type 'exit' to quit): ")
                if reply.lower() == 'exit':
                    print("Closing connection.")
                    break
                conn.sendall(reply.encode())

if __name__ == "__main__":
    start_server()

