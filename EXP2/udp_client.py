import socket

def start_client(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:  # Use SOCK_DGRAM for UDP
        print(f"UDP client ready to send messages to {host}:{port}")
        
        while True:
            message = input("Enter message to send to server (type 'exit' to quit): ")
            if message.lower() == 'exit':
                print("Exiting client.")
                # Send disconnect signal to server
                s.sendto("DISCONNECT".encode(), (host, port))
                break
            s.sendto(message.encode(), (host, port))  # Send message to server
            
            data, server = s.recvfrom(1024)  # Receive response and server address
            print(f"Server says: {data.decode()}")

if __name__ == "__main__":
    start_client()

