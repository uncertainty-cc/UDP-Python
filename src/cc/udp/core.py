import socket
import json

import numpy as np


class UDPRx:
    """
    UDP Rx class for receiving data from a UDP socket.
    """
    def __init__(self, addr=("0.0.0.0", 8000)):
        """
        Initialize UDP Rx

        Args:
            addr: address to listen on
        """
        self.addr = addr
        
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self._sock.bind(self.addr)
        print("UDP Rx is initialized:", self.addr)

    def stop(self):
        """
        Close the socket.
        """
        self._sock.close()

    def recv(self, bufsize=1024, timeout=None) -> bytes:
        """
        Receive data

        timeout == None: blocking forever
        timeout == 0: non-blocking (the actual delay is around 0.1s)
        timeout > 0: blocking for timeout seconds

        Args:
            bufsize: size of data buffer to receive
            timeout: timeout in seconds
        """
        self._sock.settimeout(timeout)
        try:
            buffer, addr = self._sock.recvfrom(bufsize)
        except (socket.timeout, BlockingIOError):
            return None
        return buffer

    def recvDict(self, bufsize=1024, timeout=None) -> dict:
        """
        Receive data and deserialize it into a python dictionary.

        See `recv()` for more information on timeout.

        Args:
            bufsize: size of data buffer to receive
            timeout: timeout in seconds
        """
        buffer = self.recv(bufsize=bufsize, timeout=timeout)
        if not buffer:
            return None
        serialized_data = buffer.decode("utf-8")
        data = json.loads(serialized_data)
        return data
    
    def recvNumpy(self, bufsize=1024, dtype=np.float32, timeout=None) -> np.ndarray:
        """
        Receive data and deserialize it into a numpy array.
        
        See `recv()` for more information on timeout.
        
        Args:
            bufsize: size of data buffer to receive
            dtype: numpy data type
            timeout: timeout in seconds
        """
        buffer = self.recv(bufsize=bufsize, timeout=timeout)
        if not buffer:
            return None
        data = np.frombuffer(buffer, dtype=dtype)
        return data


class UDPTx:
    """
    UDP Tx class for sending data to a UDP socket.
    """
    def __init__(self, addr=("0.0.0.0", 8000)):
        """
        Initialize UDP Tx

        Args:
            addr: address of target host
        """
        self.addr = addr
        
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        print("UDP Tx is initialized:", self.addr)

    def stop(self):
        """
        Close the socket.
        """
        self._sock.close()

    def send(self, buffer):
        """
        Send data
        
        Args:
            buffer: data to send
        """
        self._sock.sendto(buffer, self.addr)

    def sendDict(self, data: dict):
        """
        Serialize a python dictionary and send it.
        
        Args:
            data: data to send
        """
        buffer = json.dumps(data)
        buffer = buffer.encode()
        self.send(buffer)

    def sendNumpy(self, data: np.ndarray):
        """
        Serialize a numpy array and send it.
        
        Args:
            data: data to send
        """
        buffer = data.tobytes()
        self.send(buffer)


class UDP(UDPTx, UDPRx):
    """
    UDP class for sending and receiving data from a UDP socket.
    """
    def __init__(self, recv_addr, send_addr):
        """
        Initialize UDP Tx and Rx
        
        Args:
            recv_addr: address to listen on
            send_addr: address of target host
        """
        UDPRx.__init__(self, addr=recv_addr)
        UDPTx.__init__(self, addr=send_addr)
