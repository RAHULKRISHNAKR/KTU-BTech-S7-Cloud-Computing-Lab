## EXP3: Multiuser Chat Service with TCP and GUI

This experiment implements a multiuser chat service using TCP as the transport protocol and a GUI for the client. Each chat opens in a new window, and users can chat individually with others.

---

### Server-side Algorithm

1. **Initialize**
   - Create a TCP socket, bind to host:port, and start listening.
   - Maintain a thread-safe map: `username -> (conn, addr)`.
2. **Accept loop**
   - On new connection, spawn a thread to handle it.
3. **Register**
   - Receive length-prefixed JSON: `{ "type": "register", "username": <name> }`.
   - If name taken, reply with error and close; else add to map.
4. **Broadcast user list**
   - After registration/disconnection, send all clients `{ "type": "user_list", "users": [...] }`.
5. **Message forwarding**
   - In client handler, receive framed JSON. If `type=="chat"`, forward to recipient if online; else send error.
6. **Cleanup**
   - On disconnect or error, remove user, broadcast updated list, close socket.

---

### Client-side Algorithm (GUI)

1. **Connect & register**
   - Open TCP connection, send `{ "type": "register", "username": <your name> }` as length-prefixed JSON.
   - Receive user list or error.
2. **GUI setup**
   - Show list of online users. Double-click a user to open a private chat window.
3. **Send chat**
   - In chat window, type message. Send as `{ "type": "chat", "to": <peer>, "from": <you>, "msg": <text> }`.
   - Display locally as “Me: …”.
4. **Receive loop (background thread)**
   - Continuously read length-prefixed messages. Update user list, display incoming messages, or show errors.
5. **Teardown**
   - On exit or connection loss, close socket and GUI.

---

### Framing Convention

- Prepend every JSON message with 4-byte big-endian length.
- Encode JSON as UTF-8.

---

### Essential Safeguards

- Thread-safe access to shared state (server’s client map).
- Detect and handle disconnects gracefully.
- Validate message types and required fields; reply with errors for malformed requests.

---