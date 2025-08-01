import socket

HOST = '0.0.0.0'  # listen on all interfaces
PORT = 6000       # arbitrary port

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"[*] UDP server listening on {HOST}:{PORT}")

    seen_sequences = set()  # simple duplicate detector (sequence numbers)

    while True:
        data, addr = sock.recvfrom(4096)  # max size
        if not data:
            continue

        try:
            # Expecting "<seq>:<message>"
            decoded = data.decode('utf-8', errors='replace')
            seq_str, payload = decoded.split(':', 1)
            seq = int(seq_str)
        except ValueError:
            # malformed, ignore or optionally respond with error
            print(f"[!] Malformed packet from {addr}: {data!r}")
            continue

        if seq in seen_sequences:
            print(f"[.] Duplicate (or replay) seq={seq} from {addr}, ignoring.")
            # optional: still ack
        else:
            seen_sequences.add(seq)
            print(f"[{addr}] Received seq={seq}, msg={payload}")

        # Echo back acknowledgment with same sequence
        reply = f"{seq}:ACK:{payload}"
        sock.sendto(reply.encode('utf-8'), addr)

if __name__ == '__main__':
    start_server()
