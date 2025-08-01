### program to implement a multiuser chat  service with tcp as tlp using gui. Each chat should open in a new window and each user should be able to chat individually with the other

### Server-side algorithm (TCP router)

1. **Initialize:**

   * Create TCP socket, bind to host\:port, start listening.
   * Maintain a thread-safe map `username -> (conn, addr)`.

2. **Accept loop:**

   * On new connection, spawn a thread to handle it.

3. **Register:**

   * Receive length-prefixed JSON; expect `{"type":"register","username":<name>}`.
   * If name taken, reply with error and close; else add to map.

4. **Broadcast user list:**

   * After any registration/disconnection, send all connected clients `{"type":"user_list","users":[...current names...]}`.

5. **Message forwarding:**

   * In client handler loop, receive framed JSON.
   * If `type=="chat"`, lookup `to` user; if online, forward the same message to them; else send error back.

6. **Cleanup:**

   * On disconnect or error, remove user, broadcast updated list, close socket.

---

### Client-side algorithm (GUI)

1. **Connect & register:**

   * Open TCP connection to server.
   * Send `{"type":"register","username":<your name>}` as length-prefixed JSON.
   * Receive initial user list or error.

2. **GUI setup:**

   * Show list of online users.
   * Double-click a user to open a private chat window (one window per peer).

3. **Send chat:**

   * In a chat window, user types message.
   * Package as `{"type":"chat","to":<peer>,"from":<you>,"msg":<text>}` and send framed to server.
   * Display locally as “Me: …”.

4. **Receive loop (background thread):**

   * Continuously read length-prefixed messages.
   * If `type=="user_list"`, refresh online list.
   * If `type=="chat"`, ensure a window exists for `from` and display the incoming message.
   * If `type=="error"`, show warning.

5. **Teardown:**

   * On exit or connection loss, close socket and GUI.

---

### Framing convention (shared)

* Prepend every JSON message with 4-byte big-endian length.
* Encode JSON as UTF-8.

---

### Essential safeguards

* Thread-safe access to shared state (server’s client map).
* Detect and handle disconnects gracefully.
* Validate message types and required fields; reply with errors for malformed requests.

---