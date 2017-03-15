def socketAddressToHostAndPort(socketAddress):
  host,port = socketAddress.split(":")
  return (host,int(port))