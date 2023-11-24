import socket
import json

class UDP:
    def __init__(
        self,
        rx_addr=("0.0.0.0", 8000),
        tx_addr=("0.0.0.0", 8001),
    ):
        self.rx_addr = rx_addr
        self.tx_addr = tx_addr
        
        # self.sending_freq = 2000.0
        self.tx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("UDP Sender is initialized:", self.tx_addr)

        self.rx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rx_sock.bind(self.rx_addr)
        print("UDP Receiver is initialized:", self.rx_addr)

    def stop(self):
        self.rx_sock.close()

    """
    Receive data

    timeout == None: blocking forever
    timeout == 0: non-blocking (the actual delay is around 0.1s)
    timeout > 0: blocking for timeout seconds

    @param timeout: timeout in seconds
    """
    def recv(self, buffer_size=1024, timeout=None):
        self.rx_sock.settimeout(timeout)
        try:
            buffer, addr = self.rx_sock.recvfrom(buffer_size)
        except (socket.timeout, BlockingIOError):
            return None
        return buffer

    def sendDict(self, data):
        buffer = json.dumps(data)
        buffer = buffer.encode()
        self.send(buffer)

    def send(self, buffer):
        self.tx_sock.sendto(buffer, self.tx_addr)
