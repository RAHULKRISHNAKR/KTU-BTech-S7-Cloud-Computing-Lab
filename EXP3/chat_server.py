import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

class ChatServer:
    def __init__(self, host='127.0.0.1', port=9999):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {}  # {username: (connection, address)}
        
        # Set up GUI
        self.root = tk.Tk()
        self.root.title("Chat Server")
        self.root.geometry("500x400")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Server status
        self.status_frame = tk.Frame(self.root)
        self.status_frame.pack(pady=5)
        tk.Label(self.status_frame, text="Server Status:").grid(row=0, column=0)
        self.status_label = tk.Label(self.status_frame, text="Offline", fg="red")
        self.status_label.grid(row=0, column=1)
        
        # Server controls
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=5)
        self.start_button = tk.Button(self.control_frame, text="Start Server", command=self.start_server)
        self.start_button.grid(row=0, column=0, padx=5)
        self.stop_button = tk.Button(self.control_frame, text="Stop Server", command=self.stop_server, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=5)
        
        # Server log
        self.log_frame = tk.Frame(self.root)
        self.log_frame.pack(pady=5, fill="both", expand=True)
        tk.Label(self.log_frame, text="Server Log:").pack(anchor="w")
        self.log_area = scrolledtext.ScrolledText(self.log_frame, state="disabled", height=15)
        self.log_area.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Connected clients
        self.clients_frame = tk.Frame(self.root)
        self.clients_frame.pack(pady=5, fill="both")
        tk.Label(self.clients_frame, text="Connected Clients:").pack(anchor="w")
        self.clients_area = scrolledtext.ScrolledText(self.clients_frame, state="disabled", height=5)
        self.clients_area.pack(fill="both", expand=True, padx=5, pady=5)

    def start_server(self):
        self.server_thread = threading.Thread(target=self.server_loop)
        self.server_thread.daemon = True
        self.server_thread.start()
        self.status_label.config(text="Online", fg="green")
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.log_message("Server started on {}:{}".format(self.host, self.port))
    
    def server_loop(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            while True:
                client_socket, client_address = self.server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.daemon = True
                client_thread.start()
        except Exception as e:
            self.log_message(f"Server error: {str(e)}")
        finally:
            if self.server_socket:
                self.server_socket.close()
    
    def handle_client(self, client_socket, client_address):
        username = None
        try:
            # Receive username
            username = client_socket.recv(1024).decode('utf-8')
            if username in self.clients:
                client_socket.send("USERNAME_TAKEN".encode('utf-8'))
                client_socket.close()
                return
            else:
                client_socket.send("USERNAME_OK".encode('utf-8'))
                
            # Add client to the list
            self.clients[username] = (client_socket, client_address)
            self.log_message(f"New connection from {client_address} - Username: {username}")
            self.update_clients_list()
            
            # Broadcast new user joined
            self.broadcast_message(f"SERVER: {username} has joined the chat!", exclude_username=username)
            
            # Handle client messages
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                
                # Broadcast the message to all clients except the sender
                self.broadcast_message(f"{username}: {message}", exclude_username=username)
                
        except Exception as e:
            self.log_message(f"Error handling client {client_address}: {str(e)}")
        finally:
            if username in self.clients:
                client_socket.close()
                del self.clients[username]
                self.broadcast_message(f"SERVER: {username} has left the chat!", exclude_username=username)
                self.log_message(f"Connection closed: {client_address} - Username: {username}")
                self.update_clients_list()
    
    def broadcast_message(self, message, exclude_username=None):
        self.log_message(f"Broadcasting: {message}")
        for username, (client_socket, _) in list(self.clients.items()):
            if username == exclude_username:
                continue
            try:
                client_socket.send(message.encode('utf-8'))
            except:
                # Client connection may be broken
                pass
    
    def stop_server(self):
        if self.server_socket:
            # Notify clients that server is shutting down
            self.broadcast_message("SERVER: Server is shutting down!")
            
            # Close all client connections
            for username, (client_socket, _) in list(self.clients.items()):
                try:
                    client_socket.close()
                except:
                    pass
            
            # Close server socket
            try:
                self.server_socket.close()
            except:
                pass
            
            self.server_socket = None
            self.clients = {}
            self.status_label.config(text="Offline", fg="red")
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.log_message("Server stopped")
            self.update_clients_list()
    
    def log_message(self, message):
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state="disabled")
    
    def update_clients_list(self):
        self.clients_area.config(state="normal")
        self.clients_area.delete(1.0, tk.END)
        
        for i, username in enumerate(self.clients.keys()):
            self.clients_area.insert(tk.END, f"{i+1}. {username} - {self.clients[username][1]}\n")
            
        self.clients_area.config(state="disabled")
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to close the server?"):
            self.stop_server()
            self.root.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    server = ChatServer()
    server.run()
    self.start_button.config(state="normal")
    self.stop_button.config(state="disabled")
    self.log_message("Server stopped")
    self.update_clients_list()

    def log_message(self, message):
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state="disabled")
    
    def update_clients_list(self):
        self.clients_area.config(state="normal")
        self.clients_area.delete(1.0, tk.END)
        
        for i, username in enumerate(self.clients.keys()):
            self.clients_area.insert(tk.END, f"{i+1}. {username} - {self.clients[username][1]}\n")
            
        self.clients_area.config(state="disabled")
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to close the server?"):
            self.stop_server()
            self.root.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    server = ChatServer()
    server.run()
