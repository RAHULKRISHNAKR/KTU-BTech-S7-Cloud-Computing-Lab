import socket
import threading
import struct
import signal
import sys

HOST = '0.0.0.0'  # listen on all interfaces
PORT = 5000       # arbitrary non-privileged port

# Helper to send a length-prefixed message
def send_message(conn: socket.socket, data: bytes):
    length = struct.pack('>I', len(data))  # 4-byte big-endian length
    conn.sendall(length + data)

# Helper to receive exactly n bytes or raise
def recv_exact(conn: socket.socket, n: int) -> bytes:
    buf = b''
    while len(buf) < n:
        chunk = conn.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("Socket closed during recv")
        buf += chunk
    return buf

# Receive one framed message
def receive_message(conn: socket.socket) -> bytes:
    header = recv_exact(conn, 4)
    (length,) = struct.unpack('>I', header)
    if length == 0:
        return b''
    return recv_exact(conn, length)

def client_handler(conn: socket.socket, addr):
    print(f"[+] Connection from {addr}")
    try:
        while True:
            try:
                msg = receive_message(conn)
            except ConnectionError:
                print(f"[-] Client {addr} disconnected abruptly.")
                break
            if not msg:
                print(f"[.] Client {addr} closed connection.")
                break
            text = msg.decode('utf-8', errors='replace')
            print(f"[{addr}] Received: {text}")
            # Echo back with acknowledgement
            response = f"Server echo: {text}".encode('utf-8')
            send_message(conn, response)
    except Exception as e:
        print(f"[!] Error with client {addr}: {e}")
    finally:
        conn.close()
        print(f"[.] Closed connection with {addr}")

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print(f"[*] TCP server listening on {HOST}:{PORT}")

    def shutdown_handler(signum, frame):
        print("\n[!] Shutting down server.")
        sock.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    while True:
        try:
            conn, addr = sock.accept()
            thread = threading.Thread(target=client_handler, args=(conn, addr), daemon=True)
            thread.start()
        except OSError:
            break  # socket closed, exiting

if __name__ == '__main__':
    start_server()
