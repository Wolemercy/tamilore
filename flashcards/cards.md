# Flashcards

Running record of every flashcard generated for this curriculum. Organized by topic. Each fenced block is a single Anki import — paste into a `.txt` and import, or paste directly into Anki's text-import dialog.

## Quality rules

1. **One fact per card.** If the answer has "and also..." or "swap X for Y" — split.
2. **Specific atomic answer.** Should fit on one line. No "explain..." or "discuss...".
3. **No tangents.** Don't pad answers with motivations, comparisons, or "frameworks do this." Each tangent is its own card.
4. **No long enumerations.** Break lists into individual cards. Exception: enumerations that genuinely form a single concept (TCP handshake order, 5-tuple).
5. **Distinct neighbors.** If two cards have near-identical questions, they'll interfere — reword or merge.
6. **Avoid yes/no questions** when a content-recall reframe is clean. Y/N gives a 50% guess rate.
7. **Flashcards retain, mastery checks teach.** Don't try to learn a concept cold from a flashcard.

---

## A1 — Socket creation and binding

```
#separator:tab
#html:false
What is a file descriptor?	A small integer the OS gives you as a handle to an I/O resource (file, socket, pipe).
What does AF_INET stand for?	Address Family for IPv4.
What socket type does TCP use?	SOCK_STREAM
What socket type does UDP use?	SOCK_DGRAM
What does SOCK_STREAM provide?	A reliable, ordered byte stream.
What does SOCK_DGRAM provide?	Connectionless, message-oriented delivery.
How many bytes is an IPv4 address?	4 bytes (32 bits).
How many bytes is an IPv6 address?	16 bytes (128 bits).
What byte order does the network use?	Big-endian (most significant byte first).
What does bind(('localhost', 0)) do?	Asks the OS to assign an unused ephemeral port.
What is the macOS ephemeral port range?	49152–65535
What is the Linux ephemeral port range?	32768–60999 (default; configurable via /proc/sys/net/ipv4/ip_local_port_range)
What error does macOS raise when binding to a port already in use?	OSError: [Errno 48] Address already in use
What error does Linux raise when binding to a port already in use?	OSError: [Errno 98] Address already in use
What tuple does the kernel use to route an incoming packet to the right socket?	(protocol, address, port)
```

---

## A2 — Listening and accepting

```
#separator:tab
#html:false
What does accept() return?	A new file descriptor for one specific client connection, plus the client's address.
What is the backlog queue?	The kernel's queue of fully-established connections waiting for accept() to dequeue them.
After accept() returns, what is the role of the listening fd?	It stays open and continues accepting new connections.
After accept() returns, what is the role of the new fd?	It is dedicated to one specific client connection.
Which side completes the TCP handshake — the application or the kernel?	The kernel. The handshake finishes before accept() is called.
What are the three packets of the TCP handshake, in order?	SYN (client → server), SYN-ACK (server → client), ACK (client → server).
What 5-tuple uniquely identifies a TCP connection?	(protocol, local_addr, local_port, remote_addr, remote_port)
What does the server kernel send when a client connects to a port with no listening socket?	A TCP RST packet.
What exception does the client raise when connecting to a port with no listening socket?	ConnectionRefusedError
What is a TCP RST packet?	A control packet that immediately tears down or refuses a TCP connection (RESET).
```

---

## A3 — TCP byte stream

```
#separator:tab
#html:false
Is TCP a byte stream or a message stream?	Byte stream.
Does TCP preserve the boundaries between send() calls?	No.
What is the maximum number of bytes recv(N) can return?	N
What does recv() returning 0 indicate?	The peer cleanly closed the connection.
What four guarantees does TCP make about delivered bytes?	In-order, no loss, no duplicates, no inserted bytes.
What is the difference between send() and sendall()?	send() may write fewer bytes than requested; sendall() loops until every byte is written or raises.
On loopback, why does recv(1024) usually return exactly 1024 even with chunked sends?	The kernel buffer fills before recv runs — no real network delay spreads the data.
Name one place bytes can sit between sender and receiver after a partial recv.	Receiver's kernel receive buffer (others: in flight on the wire, sender's kernel send buffer, sender's app yet to call send).
```

---

## OS / shell commands

```
#separator:tab
#html:false
Which shell command lists processes using a TCP/UDP port?	lsof -i :PORT
Which shell command restricts lsof to TCP port 5000 only?	lsof -i tcp:5000
What signal does `kill -9 PID` send?	SIGKILL (signal 9)
What signal does plain `kill PID` send by default?	SIGTERM (signal 15)
Which signal cannot be caught or ignored by a process?	SIGKILL
What does the `d` suffix on Unix programs mean (e.g. sshd, httpd, ftpd)?	Daemon — a long-running background process.
```
