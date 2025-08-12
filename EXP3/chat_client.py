import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog

class ChatClient:
    def __init__(self):
        self.client_socket = None
        self.username = None
        self.connected = False
        self.online_users = []
        
        # Setup main window
        self.root = tk.Tk()
        self.root.title("Chat Client")
        self.root.geometry("600x400")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Connection frame
        self.conn_frame = tk.Frame(self.root)
        self.conn_frame.pack(pady=10, fill="x", padx=10)
        
        tk.Label(self.conn_frame, text="Server IP:").grid(row=0, column=0, padx=5)
        self.server_ip = tk.Entry(self.conn_frame, width=15)
        self.server_ip.insert(0, "127.0.0.1")
        self.server_ip.grid(row=0, column=1, padx=5)
        
        tk.Label(self.conn_frame, text="Port:").grid(row=0, column=2, padx=5)
        self.server_port = tk.Entry(self.conn_frame, width=5)
        self.server_port.insert(0, "9999")
        self.server_port.grid(row=0, column=3, padx=5)
        
        tk.Label(self.conn_frame, text="Username:").grid(row=0, column=4, padx=5)
        self.username_entry = tk.Entry(self.conn_frame, width=10)
        self.username_entry.grid(row=0, column=5, padx=5)
        
        self.connect_button = tk.Button(self.conn_frame, text="Connect", command=self.connect_to_server)
        self.connect_button.grid(row=0, column=6, padx=5)
        
        self.disconnect_button = tk.Button(self.conn_frame, text="Disconnect", command=self.disconnect, state="disabled")
        self.disconnect_button.grid(row=0, column=7, padx=5)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Not connected", fg="red")
        self.status_label.pack(pady=5)
        
        # Chat display
        self.chat_frame = tk.Frame(self.root)
        self.chat_frame.pack(fill="both", expand=True, padx=10)
        
        self.chat_display = scrolledtext.ScrolledText(self.chat_frame, state="disabled")
        self.chat_display.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Message input
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(fill="x", pady=5, padx=10)
        
        self.message_input = tk.Entry(self.input_frame)
        self.message_input.pack(side="left", fill="x", expand=True, padx=5)
        self.message_input.bind("<Return>", self.send_message)
        
        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side="right", padx=5)
        
        # Initially disable controls
        self.message_input.config(state="disabled")
        self.send_button.config(state="disabled")
        
    def connect_to_server(self):
        if self.connected:
            return
            
        host = self.server_ip.get()
        try:
            port = int(self.server_port.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid port number")
            return
            
        username = self.username_entry.get()
        if not username:
            messagebox.showerror("Error", "Username cannot be empty")
            return
            
        try:
            # Create socket and connect to server
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))
            
            # Send username
            self.client_socket.send(username.encode('utf-8'))
            
            # Check if username is accepted
            response = self.client_socket.recv(1024).decode('utf-8')
            if response == "USERNAME_TAKEN":
                messagebox.showerror("Error", "Username already taken")
                self.client_socket.close()
                return
            
            # Setup successful connection
            self.username = username
            self.connected = True
            self.status_label.config(text=f"Connected as {username}", fg="green")
            
            # Update the window title to the username
            self.root.title(f"{username}")
            
            # Update UI
            self.connect_button.config(state="disabled")
            self.disconnect_button.config(state="normal")
            self.message_input.config(state="normal")
            self.send_button.config(state="normal")
            self.server_ip.config(state="disabled")
            self.server_port.config(state="disabled")
            self.username_entry.config(state="disabled")
            
            # Start receiving messages
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            # Display welcome message
            self.display_message("Connected to the server. Welcome to the chat!")
            # Display client's own name in the chatbox upon connection
            self.display_message(f"You are connected as {username}.")
            
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
            if self.client_socket:
                self.client_socket.close()
    
    def disconnect(self):
        if self.connected:
            try:
                self.client_socket.close()
            except:
                pass
            
            self.connected = False
            self.status_label.config(text="Not connected", fg="red")
            
            # Reset UI
            self.connect_button.config(state="normal")
            self.disconnect_button.config(state="disabled")
            self.message_input.config(state="disabled")
            self.send_button.config(state="disabled")
            self.server_ip.config(state="normal")
            self.server_port.config(state="normal")
            self.username_entry.config(state="normal")
            
            self.display_message("Disconnected from server.")
    
    def receive_messages(self):
        while self.connected:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                
                if not message:
                    # Connection closed by server
                    self.root.after(0, self.handle_disconnect, "Server connection closed")
                    break
                
                # Display the received message
                self.root.after(0, self.display_message, message)
            except Exception as e:
                if self.connected:  # Only show error if we weren't explicitly disconnecting
                    self.root.after(0, self.handle_disconnect, f"Connection error: {str(e)}")
                break
    
    def handle_disconnect(self, message):
        self.disconnect()
        messagebox.showinfo("Disconnected", message)
    
    def send_message(self, event=None):
        if not self.connected:
            return

        message = self.message_input.get().strip()
        if not message:
            return

        try:
            # Prefix the message with 'You:' for the client's own messages
            self.display_message(f"You: {message}")
            self.client_socket.send(message.encode('utf-8'))
            self.message_input.delete(0, tk.END)
        except:
            messagebox.showerror("Error", "Failed to send message")
            self.disconnect()
    
    def display_message(self, message):
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state="disabled")
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.disconnect()
            self.root.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    client = ChatClient()
    client.run()