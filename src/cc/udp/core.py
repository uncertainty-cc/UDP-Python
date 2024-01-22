import socket
import json

import numpy as np

class UDPRx:
    """
    Args:
        addr: address to listen on
    """
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

    Args:
        buffer_size: size of data to receive
        timeout: timeout in seconds
    """
    def recv(self, buffer_size=1024, timeout=None):
        self._sock.settimeout(timeout)
        try:
            buffer, addr = self._sock.recvfrom(buffer_size)
        except (socket.timeout, BlockingIOError):
            return None
        return buffer


class UDPTx:
    """
    Args:
        addr: address of target host
    """
    def __init__(self, addr=("0.0.0.0", 8000)):
        self.addr = addr
        
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        print("UDP Tx is initialized:", self.addr)

    def stop(self):
        self._sock.close()

    def sendDict(self, data):
        buffer = json.dumps(data)
        buffer = buffer.encode()
        self.send(buffer)

    def send(self, buffer):
        self._sock.sendto(buffer, self.addr)


class UDP:
    def __init__(self, recv_addr, send_addr):
        self.tx = UDPTx(send_addr)
        self.rx = UDPRx(recv_addr)

        self.tx._sock.settimeout(0.1)
        self.rx._sock.settimeout(0.1)
    
    def recvDict(self, timeout=None):
        buffer = self.rx.recv(timeout=timeout)
        if not buffer:
            return None
        serialized_data = buffer.decode("utf-8")
        data = json.loads(serialized_data)
        return data
    
    def sendDict(self, data: dict):
        serialized_data = json.dumps(data)
        buffer = serialized_data.encode("utf-8")
        self.tx.send(buffer)

    def recvNp(self, dtype=np.float32, timeout=None):
        buffer = self.rx.recv(timeout=timeout)
        if not buffer:
            return None
        data = np.frombuffer(buffer, dtype=dtype)
        return data
    
    def sendNp(self, data: np.ndarray):
        buffer = data.tobytes()
        self.tx.send(buffer)


