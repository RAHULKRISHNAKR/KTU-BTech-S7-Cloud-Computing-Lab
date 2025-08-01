import socket
import threading
import struct
import json

HOST = '0.0.0.0'
PORT = 7000

clients_lock = threading.Lock()
# username -> (conn, addr)
clients = {}

def send_message(conn: socket.socket, obj: dict):
    data = json.dumps(obj).encode('utf-8')
    length = struct.pack('>I', len(data))
    conn.sendall(length + data)

def recv_exact(conn: socket.socket, n: int) -> bytes:
    buf = b''
    while len(buf) < n:
        chunk = conn.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("Disconnected")
        buf += chunk
    return buf

def receive_message(conn: socket.socket) -> dict:
    header = recv_exact(conn, 4)
    (length,) = struct.unpack('>I', header)
    payload = recv_exact(conn, length)
    return json.loads(payload.decode('utf-8'))

def broadcast_user_list():
    with clients_lock:
        user_list = list(clients.keys())
        for uname, (c, _) in clients.items():
            try:
                send_message(c, {"type": "user_list", "users": user_list})
            except Exception:
                pass  # ignore send errors here

def handle_client(conn: socket.socket, addr):
    username = None
    try:
        # Expect registration first
        msg = receive_message(conn)
        if msg.get("type") != "register" or not msg.get("username"):
            send_message(conn, {"type":"error","msg":"Must register with a username"})
            conn.close()
            return
        desired = msg["username"]
        with clients_lock:
            if desired in clients:
                send_message(conn, {"type":"error","msg":"Username already taken"})
                conn.close()
                return
            username = desired
            clients[username] = (conn, addr)
        print(f"[+] {username} registered from {addr}")
        broadcast_user_list()

        # Main loop
        while True:
            msg = receive_message(conn)
            if msg.get("type") == "chat":
                to = msg.get("to")
                with clients_lock:
                    target = clients.get(to)
                if target:
                    target_conn, _ = target
                    # forward message as-is (server could add stamping)
                    send_message(target_conn, msg)
                else:
                    send_message(conn, {"type":"error","msg":f"User {to} not online"})
            else:
                send_message(conn, {"type":"error","msg":"Unknown message type"})
    except ConnectionError:
        pass
    except Exception as e:
        print(f"[!] Exception for {username or addr}: {e}")
    finally:
        with clients_lock:
            if username and username in clients:
                del clients[username]
        print(f"[-] {username or addr} disconnected")
        broadcast_user_list()
        conn.close()

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(10)
    print(f"[*] Chat server listening on {HOST}:{PORT}")
    try:
        while True:
            conn, addr = sock.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\n[!] Shutting down.")
    finally:
        sock.close()

if __name__ == '__main__':
    start_server()
