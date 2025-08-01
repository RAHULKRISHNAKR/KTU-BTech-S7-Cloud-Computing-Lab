import socket
import time

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 6000
TIMEOUT_SECONDS = 2.0  # wait for reply

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT_SECONDS)
    server_addr = (SERVER_HOST, SERVER_PORT)
    seq = 1

    try:
        while True:
            msg = input("Enter message (or 'quit'): ")
            if msg.lower() == 'quit':
                break

            framed = f"{seq}:{msg}".encode('utf-8')
            # send and wait for ACK (simple retry once)
            for attempt in range(1, 3):
                sock.sendto(framed, server_addr)
                try:
                    data, _ = sock.recvfrom(4096)
                    decoded = data.decode('utf-8', errors='replace')
                    print("Received reply:", decoded)
                    break  # got response
                except socket.timeout:
                    print(f"[!] Timeout waiting for reply (attempt {attempt})")
                    if attempt == 2:
                        print("[!] Giving up on this message.")
            seq += 1
    except KeyboardInterrupt:
        print("\n[.] Interrupted by user.")
    finally:
        sock.close()

if __name__ == '__main__':
    main()
