import socket

def socketClient(hostname, port):
  tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  tcp_socket.connect((hostname, port))
  print("Connected to socket: ", hostname, ":", port)



def closeSocket(socket: socket):
  print("Closing socket")
  socket.close()