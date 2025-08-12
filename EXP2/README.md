## EXP2: UDP Client-Server Communication

This experiment demonstrates a minimal interactive UDP request/response exchange between a single client and server using Python's `socket` library.

The current implementation is simpler than a reliable UDP pattern: it does not implement sequence numbers, retries, or duplicate detection. It relies on the user to terminate the session.

---

### Files

- `udp_server.py`: Receives datagrams, displays them, and lets the operator type a reply.
- `udp_client.py`: Sends user-entered messages as individual UDP datagrams and prints server responses.

---

### Protocol Overview

- Each datagram payload is a raw UTF‑8 string (no framing / headers).
- Client sends normal text; to quit it sends the literal `DISCONNECT` (and then exits locally).
- Server, upon receiving `DISCONNECT`, prints a notice and shuts down.
- Either side can also type `exit` locally (server on prompt, client before sending) to terminate its process (server's `exit` stops the loop, client's `exit` stops sending).

---

### Flow

1. Server binds to `127.0.0.1:65432` (default) and waits for `recvfrom()`.
2. Client sends a message with `sendto()` to the server address.
3. Server prints the message and prompts operator for a reply; reply is sent via `sendto()` back to the *source address* of the last message.
4. Client receives the reply with `recvfrom()` and displays it.
5. Repeat until termination condition.

---

### Characteristics / Limitations

- Stateless: server does not track multiple clients separately (would always reply to the most recent sender in this loop).
- No sequencing / ordering guarantees (native UDP behavior).
- No retry / timeout handling on client (client blocks waiting for a reply).
- Manual termination using `DISCONNECT` or `exit`.

---

### Potential Enhancements

- Add timeouts and retransmission logic for basic reliability.
- Support multiple concurrent clients (store last address per conversation or maintain a list).
- Add simple command keywords (e.g., `/quit`).
- Introduce sequence numbers + ACK for duplicate/loss handling (restore earlier extended design if needed).

---

### Quick Start

**Server:**
```
python udp_server.py
```

**Client (another terminal):**
```
python udp_client.py
```

Enter messages; server will reply interactively.

**To close:**
- Client: type `exit` (local) or send `DISCONNECT`.
- Server: type `exit` or wait for `DISCONNECT` message.

---