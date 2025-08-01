### write a python program to establish client server communication with TCP as transport layer protocol

## Server-side algorithm

1. **Initialize listening socket**

   * Create a TCP socket.
   * Set `SO_REUSEADDR` so restart doesn’t block.
   * Bind to host/IP and port.
   * Start listening with a backlog.

2. **Install shutdown handlers (optional but good)**

   * Capture signals (e.g., SIGINT) to gracefully close the listening socket.

3. **Main accept loop**

   * Loop forever (until shutdown):

     * Accept new incoming connection, yielding a connected socket and client address.
     * Spawn a worker (thread or async task) to handle that client, passing the connection socket.

4. **Per-client handler**

   * Log/record the new client.
   * Loop:

     * Read exactly 4 bytes from the socket to get the length prefix.

       * If read fails or returns zero bytes, treat as client disconnect.
     * Decode the 4-byte big-endian integer to obtain `N` (message length).
     * Read exactly `N` bytes to get the full message payload.

       * If the socket closes mid-read, handle as abrupt disconnect.
     * Decode or interpret the payload as needed (e.g., UTF-8 string).
     * Process the message (business logic; in example, prepare an echo).
     * Prepare response bytes.
     * Prefix response with its 4-byte length and send it all (`sendall`).
   * On any unrecoverable error or clean close, tear down: close client socket, log.

5. **Cleanup on shutdown**

   * Close listening socket, optionally wait/join worker threads if not daemonized.

---

## Client-side algorithm

1. **Establish connection**

   * Create a TCP socket.
   * Connect to server’s IP/hostname and port.

2. **Interactive message loop**

   * Loop until user quits:

     * Get user input (e.g., a string).
     * Encode input into bytes (e.g., UTF-8).
     * Compute length `L` of payload; pack into 4-byte big-endian.
     * Send length prefix + payload using `sendall`.
     * Read exactly 4 bytes from server to get response length.

       * If connection closes, abort.
     * Unpack length, then read exactly that many bytes for the response.
     * Decode and display to user.

3. **Teardown**

   * On user quit or error, close socket.

---

## Framing helper routines (used by both sides)

* `recv_exact(sock, n)`:

  * Repeatedly call `recv` until `n` bytes are accumulated or connection breaks.
  * If `recv` returns empty before full length, raise error / treat as disconnect.

* `send_message(sock, payload_bytes)`:

  * Prefix with 4-byte length and send all.

* `receive_message(sock)`:

  * Use `recv_exact` to get length prefix, unpack it, then `recv_exact` for payload.

---

## Pseudocode summary (server)

```
create listening_socket
bind(listening_socket, HOST, PORT)
listen(listening_socket)

while true:
    conn, addr = accept(listening_socket)
    spawn_thread(handle_client, conn, addr)

function handle_client(conn, addr):
    loop:
        header = recv_exact(conn, 4)
        if header is empty: break
        length = unpack_big_endian(header)
        payload = recv_exact(conn, length)
        process payload
        response = create_response(payload)
        send_message(conn, response)
    close conn
```

## Pseudocode summary (client)

```
conn = connect(SERVER_HOST, SERVER_PORT)
while user not quitting:
    input = read_user_input()
    send_message(conn, input)
    reply = receive_message(conn)
    display(reply)
close conn
```

---
