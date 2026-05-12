import argparse
import socket
import time


def createTCPSocket(hostname, port):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
    tcp_socket.bind((hostname, port))
    tcp_socket.listen(2)
    
    print(f"Waiting for connection")

    while True:
      conn, address = tcp_socket.accept()
      with conn:
        print(f"Connected: {address}")
        total = 0
        while True:
          data = conn.recv(1024)
          if not data:
            break
          total += len(data)
          print(f"Bytes received: {len(data)}")
        print(f"Client {address} sent {total} total; closed")
        # while True:
        #   if not data:
        #     break


def closeSocket(socket: socket):
  print("Closing socket")
  socket.close()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--port", type=int, default=5001)
  parser.add_argument("--hostname", type=str, default="localhost")
  args = parser.parse_args()

  createTCPSocket(args.hostname, args.port)