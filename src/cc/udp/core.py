import socket
import json


class UDPRx:
    def __init__(self, addr=("0.0.0.0", 8000)):
        self.addr = addr
        
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self._sock.bind(self.addr)
        print("UDP Rx is initialized:", self.addr)

    def stop(self):
        self._sock.close()

    """
    Receive data

    timeout == None: blocking forever
    timeout == 0: non-blocking (the actual delay is around 0.1s)
    timeout > 0: blocking for timeout seconds

    @param timeout: timeout in seconds
    """
    def recv(self, buffer_size=1024, timeout=None):
        self._sock.settimeout(timeout)
        try:
            buffer, addr = self._sock.recvfrom(buffer_size)
        except (socket.timeout, BlockingIOError):
            return None
        return buffer


class UDPTx:
    def __init__(self, target_addr=("0.0.0.0", 8000)):
        self.target_addr = target_addr
        
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        print("UDP Tx is initialized:", self.target_addr)

    def stop(self):
        self._sock.close()

    def sendDict(self, data):
        buffer = json.dumps(data)
        buffer = buffer.encode()
        self.send(buffer)

    def send(self, buffer):
        self._sock.sendto(buffer, self.target_addr)


