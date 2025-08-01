### write a python program to establish client server communication with UDP as transport layer protocol


## Server-side algorithm

1. **Setup**

   1. Create a UDP socket.
   2. Bind it to the desired host/address and port.
   3. Initialize a data structure (`seen_sequences`) to track sequence numbers already processed (for duplicate detection).

2. **Main loop**

   1. Wait to receive a datagram with `recvfrom`.
   2. If no data, continue.
   3. Decode the received bytes as UTF-8 (or appropriate encoding).
   4. Parse the message expecting the format: `<sequence>:<payload>`.

      * If parsing fails (malformed), log/ignore and continue.
   5. Convert `<sequence>` to an integer `seq`.
   6. Check if `seq` is in `seen_sequences`:

      * If yes: treat as duplicate/replay; optionally log and proceed to step 7 anyway (or skip processing).
      * If no: record `seq` in `seen_sequences` and process the payload (e.g., log it).
   7. Construct a reply in the format: `<sequence>:ACK:<payload>`.
   8. Send the reply back to the sender’s address with `sendto`.

3. **(Optional) Maintenance**

   * Periodically purge old entries from `seen_sequences` to bound memory if sequences grow unbounded.

---

## Client-side algorithm

1. **Setup**

   1. Create a UDP socket.
   2. Set a receive timeout (e.g., 2 seconds) for waiting for replies.
   3. Initialize a sequence counter `seq = 1`.

2. **Interactive/send loop**

   1. Read user input message. If user signals quit, exit loop.
   2. Frame the message as: `<seq>:<message>`.
   3. Encode the framed string to bytes.
   4. Attempt to send and receive acknowledgment:

      * For a fixed number of retries (e.g., up to 2 attempts):

        1. Send the framed packet with `sendto` to the server address.
        2. Wait for a reply using `recvfrom` (subject to timeout).
        3. If a reply is received:

           * Decode it, display to user, break out of retry loop.
        4. If timeout occurs:

           * Log the timeout; if retries remain, retry; otherwise give up on this message.
   5. Increment `seq` by 1 and repeat.

3. **Teardown**

   * Close the socket upon exit.

---

## Framing convention

* Outgoing message from client:
  `"<sequence_number>:<payload>"`
  Example: `"5:Hello Server"`

* Server reply (ACK):
  `"<sequence_number>:ACK:<original_payload>"`
  Example: `"5:ACK:Hello Server"`

---

## Assumptions

1. **Unreliable transport:** UDP may drop, duplicate, or reorder packets; sequencing plus simple retry handles duplicates and some loss but not reordering robustly.
2. **Stateless per-packet:** Server does not establish a session; each packet is independent except for seen-sequence tracking.
3. **Payload fits within UDP datagram size limit.** No fragmentation handling.
4. **UTF-8 textual messages.** Binary protocols would need different parsing.

---

## Failure modes & mitigations

* **Packet loss:** Client retries on timeout; still possible to lose both original and retry. For higher reliability, implement cumulative ACKs, sliding window, and exponential backoff.
* **Duplicate packets:** Server detects via `seen_sequences` and avoids double-processing.
* **Reordering:** Current scheme doesn’t reorder; out-of-order delivery shows as independent messages — if ordering matters, add buffering and sequence validation at client or application layer.
* **Sequence number wrap / unbounded growth:** If `seq` grows indefinitely, server’s `seen_sequences` can balloon; implement expiry (e.g., keep only last N or time-based eviction).
* **Malformed input:** Server skips or logs malformed frames.

---

## Extensions / Reliability upgrades

1. **Reliable delivery protocol over UDP:**

   * Use acknowledgments with explicit ACK numbers.
   * Maintain a send window and retransmission timers (sliding window).
   * Use cumulative ACKs to reduce overhead.

2. **Ordering guarantees:**

   * Buffer out-of-order messages and deliver to application in sequence.

3. **Flow control / congestion control:**

   * Adjust send rate based on observed loss/latency.

4. **Integrity/authentication:**

   * Append an HMAC or checksum to detect tampering or corruption.

5. **Session identifiers:**

   * If multiple clients behind NAT reuse ports, include client IDs in payload to disambiguate.

---

## Pseudocode summary

### Server

```
create UDP socket
bind to HOST:PORT
seen_sequences = empty set

loop forever:
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

### Client

```
create UDP socket with timeout
seq = 1

loop:
    msg = get_user_input()
    if msg == quit: break
    framed = f"{seq}:{msg}"
    for attempt in 1..max_retries:
        sendto(framed, server)
        try:
            reply = recvfrom()
            display reply
            break
        except timeout:
            if attempt == max_retries:
                report failure
    seq += 1
```