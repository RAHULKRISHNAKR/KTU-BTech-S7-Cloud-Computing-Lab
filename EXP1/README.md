## EXP1: TCP Client-Server Communication

This experiment provides a minimal interactive TCP echo-style application in Python.

Unlike a length‑prefixed framed protocol, the current implementation sends raw UTF‑8 encoded strings up to 1024 bytes and reads them directly with `recv(1024)`.

---

### Files

- `tcp_server.py`: Waits for a single client, receives messages, and interactively types replies.
- `tcp_client.py`: Connects to the server, lets the user send messages and displays server responses.

---

### How It Works

1. Server binds to `127.0.0.1:65432`, listens, and accepts the first incoming connection.
2. Client connects to the same host/port.
3. Client loop:
   - Prompt user for input.
   - Send message (`socket.sendall(message.encode())`).
   - Wait for reply (`recv(1024)`).
4. Server loop:
   - Receive data (`recv(1024)`); when empty, client disconnected.
   - Display client message.
   - Prompt server operator for a reply and send it back.
5. Either side can terminate:
   - Client types `exit`.
   - Server types `exit`.

---

### Characteristics / Limitations

- Single client only (no concurrency / multi‑client handling).
- No explicit message framing (messages are limited by user entry size and `1024` byte buffer).
- Blocking I/O (no threads / async).
- Plain text only (UTF‑8 strings).

---

### Possible Improvements

- Add length‑prefixed framing for arbitrary message sizes.
- Support multiple clients with threading or `asyncio`.
- Add graceful shutdown signal handling.
- Include simple protocol commands (e.g., `/quit`, `/who`).

---

### Quick Start

Server:

```
python tcp_server.py
```

Client (in another terminal):

```
python tcp_client.py
```

Type `exit` on either side to close the session.

---
