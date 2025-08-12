## EXP3: GUI Multiuser Chat (Work-in-Progress)

This experiment aims to implement a multiuser chat system with a Tkinter GUI for both client and (optional) server monitoring. The current code base is an *incomplete skeleton* containing placeholders and missing logic blocks that must be filled in for a functional application.

---
### Current Status
- `chat_client.py` and `chat_server.py` include GUI scaffolding (Tkinter windows, widgets, and layout).
- Networking logic (socket creation, message framing, threading) is partially present or commented by implication, but many branches are empty.
- Error handling, broadcast logic, per‑client message routing, and graceful disconnects are not yet implemented.

---
### Files
- `chat_client.py`: Tkinter client with fields for server IP, port, username, message entry, and scrolling chat view. Missing actual send/receive handling in several methods.
- `chat_server.py`: Tkinter server console showing status, connected clients, and server log. Missing core accept loop and broadcast implementation.

---
### Intended Design (Target Behavior)
1. Server accepts multiple TCP clients.
2. First message from each client is a desired username.
3. If username free, server acknowledges; else rejects and closes connection.
4. Server maintains mapping: `username -> socket`.
5. Messages from one client are broadcast (or privately routed, if extended) to others.
6. GUI panes update in real time (log + clients list).
7. Client GUI displays incoming messages and allows sending via Enter key or Send button.

---
### Skeleton Gaps (Need Implementation)
| Component | Missing Pieces |
|-----------|----------------|
| `chat_server.server_loop` | Accept connections loop, spawn handler threads. |
| `chat_server.handle_client` | Username validation branch bodies; message receive loop; disconnect cleanup. |
| `chat_server.broadcast_message` | Conditional skip + actual send + exception handling. |
| `chat_server.stop_server` | Closing client sockets and server socket logic. |
| `chat_client.connect_to_server` | Handling `USERNAME_TAKEN` response + socket close on failure. |
| `chat_client.disconnect` | Sending a disconnect notice + closing socket. |
| `chat_client.receive_messages` | Loop to `recv`, decode, and display or trigger disconnect. |
| `chat_client.send_message` | Send encoded message over socket + local echo. |
| `chat_client.on_closing` | Proper disconnect before window destroy. |

---
### Recommended Next Steps
1. Define a simple protocol (e.g., plain lines or length‑prefixed JSON with keys: type/chat/username/message).
2. Implement server accept loop with a daemon thread per client.
3. Implement broadcast with thread‑safe access to `self.clients` (use a `threading.Lock`).
4. Add a disconnect protocol (e.g., client sends `/quit` or closes socket; server removes entry and notifies others).
5. Wrap all socket send/recv in try/except to handle abrupt disconnects.
6. Update GUI elements only from main thread (use `root.after` if needed from worker threads).

---
### Example Simple Text Protocol (Suggestion)
- Client first send: `HELLO <username>`
- Broadcast messages: `MSG <username> <text>`
- Server broadcast format: `MSG <username> <text>`
- Disconnect notice: `BYE <username>`
- Server rejection: `ERR USERNAME_TAKEN`

---
### Running (Current Prototype)
At present, running either script will open a GUI but functionality is incomplete:
```
python chat_server.py
python chat_client.py
```
Expect errors or no message flow until missing code is implemented.

---
### Future Enhancements
- Private messaging windows.
- User presence / typing indicators.
- Message history persistence.
- Encryption (TLS) or authentication layer.

---
### Contributing
Focus first on completing the missing logic blocks listed under Skeleton Gaps. Test with multiple clients after stabilizing the basic broadcast path.

---