import socket

def start_client(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"Connected to server {host}:{port}")
        while True:
            message = input("Enter message to send to server (type 'exit' to quit): ")
            if message.lower() == 'exit':
                print("Closing connection.")
                break
            s.sendall(message.encode())
            
            data = s.recv(1024)
            if not data:
                print("Connection closed by server.")
                break
            print(f"Server says: {data.decode()}")

if __name__ == "__main__":
    start_client()

