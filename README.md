# KTU BTech S7 Cloud Computing Lab

This repository contains Python implementations (and some in‑progress code) for several networking and distributed systems related lab experiments.

## Experiments Overview

| Experiment | Folder | Status | Description |
|-----------|--------|--------|-------------|
| EXP1 | `EXP1/` | Complete (basic) | Single-client interactive TCP echo style without framing. |
| EXP2 | `EXP2/` | Complete (basic) | Simple UDP request/response with manual replies and `DISCONNECT` message. |
| EXP3 | `EXP3/` | In Progress | Tkinter multiuser chat (GUI) skeleton; networking logic incomplete. |
| EXP4 | `EXP4/` | Complete (core) | Distance Vector Routing simulation (synchronous rounds, no split horizon). |

---
## Quick Start Commands

TCP Server / Client:
```
python EXP1/tcp_server.py
python EXP1/tcp_client.py
```

UDP Server / Client:
```
python EXP2/udp_server.py
python EXP2/udp_client.py
```

Chat (work-in-progress):
```
python EXP3/chat_server.py
python EXP3/chat_client.py
```

Distance Vector Routing:
```
python EXP4/dvr.py
```

---
## Roadmap Ideas
- Enhance TCP example with multi-client support.
- Add reliability features to UDP example (sequence numbers, retries).
- Finish chat application: protocol, broadcast, disconnect handling.
- Add split horizon + poison reverse and link failure simulation to DVR.

---
## License
Educational use for KTU BTech S7 lab exercises.

---

