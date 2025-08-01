## EXP2: UDP Client-Server Communication

This experiment demonstrates how to establish client-server communication using UDP as the transport layer protocol in Python.

---

### Server-side Algorithm

1. **Setup**
   - Create a UDP socket and bind to the desired address and port.
   - Track processed sequence numbers to detect duplicates.
2. **Main loop**
   - Receive datagrams, parse as `<sequence>:<payload>`.
   - If new sequence, process payload; always reply as `<sequence>:ACK:<payload>`.
3. **Maintenance (optional)**
   - Periodically purge old sequence numbers to bound memory.

---

### Client-side Algorithm

1. **Setup**
   - Create a UDP socket with a receive timeout.
   - Initialize a sequence counter.
2. **Send loop**
   - Read user input, frame as `<seq>:<message>`, and send.
   - Wait for acknowledgment, retry on timeout up to a limit.
   - Increment sequence number for each message.
3. **Teardown**
   - Close the socket on exit.

---

### Framing Convention

- Outgoing: `<sequence_number>:<payload>` (e.g., `5:Hello Server`)
- Reply: `<sequence_number>:ACK:<original_payload>` (e.g., `5:ACK:Hello Server`)

---

### Assumptions

1. UDP is unreliable (may drop, duplicate, or reorder packets).
2. Server is stateless per packet except for duplicate detection.
3. Payload fits within UDP datagram size.
4. Messages are UTF-8 encoded.

---

### Failure Modes & Mitigations

- Packet loss: client retries on timeout.
- Duplicate packets: server detects and avoids double-processing.
- Reordering: not handled; out-of-order messages are independent.
- Sequence number growth: implement expiry for old entries.
- Malformed input: server skips or logs.

---

### Extensions / Reliability Upgrades

1. Reliable delivery: explicit ACKs, send window, retransmission timers.
2. Ordering: buffer and deliver in sequence.
3. Flow/congestion control: adjust send rate.
4. Integrity/authentication: use HMAC/checksum.
5. Session IDs: disambiguate clients behind NAT.

---

### Pseudocode Summary

#### Server
```python
create UDP socket
bind to HOST:PORT
seen_sequences = empty set

while True:
    data, addr = recvfrom()
    if data is empty: continue
    parsed_seq, payload = parse(data)  # "<seq>:<payload>"
    if parse fails: continue
    if parsed_seq not in seen_sequences:
        add parsed_seq to seen_sequences
        process payload
    reply = f"{parsed_seq}:ACK:{payload}"
    sendto(reply, addr)
```

#### Client
```python
create UDP socket with timeout
seq = 1

while True:
    msg = get_user_input()
    if msg == quit: break
    framed = f"{seq}:{msg}"
    for attempt in range(max_retries):
        sendto(framed, server)
        try:
            reply = recvfrom()
            display(reply)
            break
        except timeout:
            if attempt == max_retries - 1:
                report failure
    seq += 1
```

---