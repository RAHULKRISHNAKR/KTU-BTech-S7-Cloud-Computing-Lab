import socket
import struct

SERVER_HOST = '127.0.0.1'  # adjust if server is remote
SERVER_PORT = 5000

def send_message(sock: socket.socket, data: bytes):
    length = struct.pack('>I', len(data))
    sock.sendall(length + data)

def recv_exact(sock: socket.socket, n: int) -> bytes:
    buf = b''
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("Server closed connection")
        buf += chunk
    return buf

def receive_message(sock: socket.socket) -> bytes:
    header = recv_exact(sock, 4)
    (length,) = struct.unpack('>I', header)
    if length == 0:
        return b''
    return recv_exact(sock, length)

def main():
    with socket.create_connection((SERVER_HOST, SERVER_PORT)) as sock:
        print(f"Connected to server at {SERVER_HOST}:{SERVER_PORT}")
        try:
            while True:
                msg = input("Enter message (or 'quit'): ")
                if msg.lower() == 'quit':
                    break
                encoded = msg.encode('utf-8')
                send_message(sock, encoded)
                response = receive_message(sock)
                print("Server replied:", response.decode('utf-8', errors='replace'))
        except KeyboardInterrupt:
            print("\n[.] Interrupted by user. Exiting.")
        except Exception as e:
            print(f"[!] Error: {e}")

if __name__ == '__main__':
    main()
