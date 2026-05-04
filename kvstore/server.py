import argparse
import socket
import time


def createTCPSocket(hostname, port):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
    tcp_socket.bind((hostname, port))
    tcp_socket.listen(2)
    
    print(f"Waiting for connection")
    time.sleep(30)

    # conn, address = tcp_socket.accept()
    # with conn:
    #   print(f"Connected: {address}")
    #   conn.close()


def closeSocket(socket: socket):
  print("Closing socket")
  socket.close()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--port", type=int, default=5000)
  parser.add_argument("--hostname", type=str, default="localhost")
  args = parser.parse_args()

  createTCPSocket(args.hostname, args.port)