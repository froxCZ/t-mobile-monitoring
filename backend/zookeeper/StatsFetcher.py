import socket


class StatsFetcher():
  def __init__(self):
    super().__init__()

  def fetch(self,host,port):
    return send_cmd(host,port,b'stat\n')


def send_cmd(host, port, cmd):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.settimeout(0.5)
  s.connect((host, port))
  result = []
  try:
    s.sendall(cmd)

    # shutting down the socket write side helps ensure that we don't end up with TIME_WAIT sockets
    s.shutdown(socket.SHUT_WR)

    while True:
      data = s.recv(4096)
      if not data:
        break
      data = data.decode()
      result.append(data)
  finally:
    s.close()

  return "".join(result)


if __name__ == '__main__':
  res = StatsFetcher().fetch("localhost",2888)
  print(res)
