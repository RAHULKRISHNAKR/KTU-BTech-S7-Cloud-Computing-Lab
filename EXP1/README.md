## EXP1: TCP Client-Server Communication

This experiment demonstrates how to establish client-server communication using TCP as the transport layer protocol in Python.

---

### Server-side Algorithm

1. **Initialize listening socket**
   - Create a TCP socket.
   - Set `SO_REUSEADDR` so restart doesn’t block.
   - Bind to host/IP and port.
   - Start listening with a backlog.
2. **Install shutdown handlers (optional)**
   - Capture signals (e.g., SIGINT) to gracefully close the listening socket.
3. **Main accept loop**
   - Accept new incoming connections and spawn a worker (thread or async task) to handle each client.
4. **Per-client handler**
   - Read 4 bytes for the length prefix, then the message payload.
   - Process the message and send a response with a 4-byte length prefix.
   - On disconnect or error, close the client socket.
5. **Cleanup on shutdown**
   - Close listening socket and clean up resources.

---

### Client-side Algorithm

1. **Establish connection**
   - Create a TCP socket and connect to the server.
2. **Interactive message loop**
   - Get user input, send with length prefix, and display server response.
3. **Teardown**
   - Close socket on quit or error.

---

### Framing Helper Routines

- `recv_exact(sock, n)`: Receive exactly `n` bytes or treat as disconnect.
- `send_message(sock, payload_bytes)`: Prefix with 4-byte length and send all.
- `receive_message(sock)`: Use `recv_exact` for length and payload.

---

### Pseudocode Summary

#### Server
```python
create listening_socket
bind(listening_socket, HOST, PORT)
listen(listening_socket)

while True:
    conn, addr = accept(listening_socket)
    spawn_thread(handle_client, conn, addr)

def handle_client(conn, addr):
    while True:
        header = recv_exact(conn, 4)
        if header is empty: break
        length = unpack_big_endian(header)
        payload = recv_exact(conn, length)
        process payload
        response = create_response(payload)
        send_message(conn, response)
    close conn
```

#### Client
```python
conn = connect(SERVER_HOST, SERVER_PORT)
while user not quitting:
    input = read_user_input()
    send_message(conn, input)
    reply = receive_message(conn)
    display(reply)
close conn
```

---
