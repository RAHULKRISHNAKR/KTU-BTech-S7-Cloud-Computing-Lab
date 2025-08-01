import socket
import threading
import struct
import json
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox

SERVER_HOST = '127.0.0.1'  # adjust if remote
SERVER_PORT = 7000

# framing helpers
def send_message(sock: socket.socket, obj: dict):
    data = json.dumps(obj).encode('utf-8')
    length = struct.pack('>I', len(data))
    sock.sendall(length + data)

def recv_exact(sock: socket.socket, n: int) -> bytes:
    buf = b''
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("Server disconnected")
        buf += chunk
    return buf

def receive_message(sock: socket.socket) -> dict:
    header = recv_exact(sock, 4)
    (length,) = struct.unpack('>I', header)
    payload = recv_exact(sock, length)
    return json.loads(payload.decode('utf-8'))

class ChatWindow:
    def __init__(self, master, to_user, send_func):
        self.to_user = to_user
        self.send_func = send_func
        self.window = tk.Toplevel(master)
        self.window.title(f"Chat with {to_user}")
        self.text_area = scrolledtext.ScrolledText(self.window, state='disabled', width=50, height=20)
        self.text_area.pack(padx=5, pady=5)
        self.entry = tk.Entry(self.window, width=40)
        self.entry.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        self.entry.bind('<Return>', self.send)
        self.send_btn = tk.Button(self.window, text="Send", command=self.send)
        self.send_btn.pack(side='right', padx=5, pady=5)

    def append(self, sender, msg):
        self.text_area.configure(state='normal')
        self.text_area.insert('end', f"{sender}: {msg}\n")
        self.text_area.see('end')
        self.text_area.configure(state='disabled')

    def send(self, event=None):
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, 'end')
        self.append("Me", text)
        self.send_func(self.to_user, text)

class ClientGUI:
    def __init__(self, root, sock, username):
        self.sock = sock
        self.username = username
        self.root = root
        root.title(f"Chat Client - {username}")
        self.users_listbox = tk.Listbox(root)
        self.users_listbox.pack(side='left', fill='y', padx=5, pady=5)
        self.users_listbox.bind('<Double-Button-1>', self.open_chat)
        self.chat_windows = {}  # target -> ChatWindow

        self.info_label = tk.Label(root, text="Double-click a user to chat")
        self.info_label.pack(side='top', fill='x')

        # Start listener thread
        threading.Thread(target=self.listener_loop, daemon=True).start()

    def open_chat(self, event=None):
        selection = self.users_listbox.curselection()
        if not selection:
            return
        to_user = self.users_listbox.get(selection[0])
        if to_user == self.username:
            return
        if to_user not in self.chat_windows:
            cw = ChatWindow(self.root, to_user, self.send_chat)
            self.chat_windows[to_user] = cw

    def send_chat(self, to_user, msg):
        payload = {
            "type": "chat",
            "to": to_user,
            "from": self.username,
            "msg": msg
        }
        try:
            send_message(self.sock, payload)
        except Exception as e:
            messagebox.showerror("Send error", str(e))

    def listener_loop(self):
        try:
            while True:
                msg = receive_message(self.sock)
                mtype = msg.get("type")
                if mtype == "user_list":
                    self.update_user_list(msg.get("users", []))
                elif mtype == "chat":
                    frm = msg.get("from")
                    text = msg.get("msg")
                    if frm not in self.chat_windows:
                        self.chat_windows[frm] = ChatWindow(self.root, frm, self.send_chat)
                    self.chat_windows[frm].append(frm, text)
                elif mtype == "error":
                    messagebox.showwarning("Server message", msg.get("msg", ""))
                else:
                    # ignore unknown
                    pass
        except ConnectionError:
            messagebox.showerror("Disconnected", "Lost connection to server")
            self.root.quit()
        except Exception as e:
            messagebox.showerror("Listener error", str(e))
            self.root.quit()

    def update_user_list(self, users):
        self.users_listbox.delete(0, 'end')
        for u in sorted(users):
            self.users_listbox.insert('end', u)

def main():
    root = tk.Tk()
    # prompt username
    username = simpledialog.askstring("Username", "Enter your username:", parent=root)
    if not username:
        return
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER_HOST, SERVER_PORT))
    except Exception as e:
        messagebox.showerror("Connection failed", str(e))
        return
    # register
    send_message(sock, {"type":"register","username":username})
    # wait for possible error or user list
    first = receive_message(sock)
    if first.get("type") == "error":
        messagebox.showerror("Registration failed", first.get("msg",""))
        return
    # if it's user_list, proceed; else ignore
    gui = ClientGUI(root, sock, username)
    if first.get("type") == "user_list":
        gui.update_user_list(first.get("users", []))
    root.mainloop()

if __name__ == '__main__':
    main()
