import socket
import json

import numpy as np

class UDPRx:
    def __init__(self, addr=("0.0.0.0", 8000)):
        """
        Args:
            addr: address to listen on
        """
        self.addr = addr
        
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self._sock.bind(self.addr)
        print("UDP Rx is initialized:", self.addr)

    def stop(self):
        self._sock.close()

    def recv(self, buffer_size=1024, timeout=None) -> bytes:
        """
        Receive data

        timeout == None: blocking forever
        timeout == 0: non-blocking (the actual delay is around 0.1s)
        timeout > 0: blocking for timeout seconds

        Args:
            buffer_size: size of data to receive
            timeout: timeout in seconds
        """
        self._sock.settimeout(timeout)
        try:
            buffer, addr = self._sock.recvfrom(buffer_size)
        except (socket.timeout, BlockingIOError):
            return None
        return buffer

    def recvDict(self, timeout=None) -> dict:
        buffer = self.recv(timeout=timeout)
        if not buffer:
            return None
        serialized_data = buffer.decode("utf-8")
        data = json.loads(serialized_data)
        return data
    
    def recvNumpy(self, dtype=np.float32, timeout=None) -> np.ndarray:
        buffer = self.rx.recv(timeout=timeout)
        if not buffer:
            return None
        data = np.frombuffer(buffer, dtype=dtype)
        return data


class UDPTx:
    def __init__(self, addr=("0.0.0.0", 8000)):
        """
        Args:
            addr: address of target host
        """
        self.addr = addr
        
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        print("UDP Tx is initialized:", self.addr)

    def stop(self):
        self._sock.close()

    def send(self, buffer):
        self._sock.sendto(buffer, self.addr)

    def sendDict(self, data: dict):
        buffer = json.dumps(data)
        buffer = buffer.encode()
        self.send(buffer)

    def sendNumpy(self, data: np.ndarray):
        buffer = data.tobytes()
        self.tx.send(buffer)


class UDP:
    def __init__(self, recv_addr, send_addr):
        self.tx = UDPTx(send_addr)
        self.rx = UDPRx(recv_addr)

        self.tx._sock.settimeout(0.1)
        self.rx._sock.settimeout(0.1)
    
    def recvDict(self, timeout=None) -> dict:
        return self.rx.recvDict(timeout)
    
    def sendDict(self, data: dict):
        self.tx.sendDict(data)

    def recvNumpy(self, dtype=np.float32, timeout=None) -> np.ndarray:
        self.rx.recvNumpy(dtype, timeout)

    def sendNumpy(self, data: np.ndarray):
        self.tx.sendNumpy(data)
    


