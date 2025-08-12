import socket

def start_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:  # Use SOCK_DGRAM for UDP
        s.bind((host, port))
        print(f"UDP server listening on {host}:{port}...")
        
        while True:
            data, addr = s.recvfrom(1024)  # Receive data and client address
            message = data.decode()
            
            # Check if client is disconnecting
            if message == "DISCONNECT":
                print(f"Client {addr} disconnected. Shutting down server.")
                break
                
            print(f"Received message from {addr}: {message}")
            
            reply = input("Enter message to send to client (type 'exit' to quit): ")
            if reply.lower() == 'exit':
                print("Closing server.")
                break
            s.sendto(reply.encode(), addr)  # Send reply to client address

if __name__ == "__main__":
    start_server()

