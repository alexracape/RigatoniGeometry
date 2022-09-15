import socket
import re
import threading

import rigatoni

from rigatoni.noodle_objects import BufferID


class ByteServer(object):


    def __init__(self, host: str='0.0.0.0', port: int=8000):
        self.host = host
        self.port = port
        self.socket = None
        self.buffers = {}
        self.next_tag = 0
        self.url = f"http://{host}:{port}"
        self.thread = threading.Thread(target=self.run, args=())

        self.thread.start()


    def get_tag(self):
        tag = self.next_tag
        self.next_tag += 1
        return str(tag)


    def get_buffer(self, uri: str):
        """Helper to get bytes for a uri"""

        m = re.search(f'(?<={self.port}\/).+\Z', uri)
        if m:
            tag = m.group(0)
            bytes = self.buffers[tag]
            return bytes
        else:
            raise Exception("Invalid HTTP Request")
        


    def run(self):

        # Create socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))

        self.socket = server_socket

        server_socket.listen(1)
        print(f'Listening on port {self.port} ...')

        while True:
            # Wait for client connections
            print("Waiting for connection...")
            client_connection, client_address = server_socket.accept()

            # Get the client request
            request = client_connection.recv(1024).decode()
            print(request)

            # Try to get tag from request with regex
            m = re.search('(?<=GET \/)(.+?)(?= HTTP)', request)
            if m:
                tag = m.group(0)
            else:
                raise Exception("Invalid HTTP Request")

            # Send HTTP response
            response = self.buffers[tag]
            print(f"Response:\n{response}")
            client_connection.sendall(response)
            client_connection.close()

    
    def add_buffer(self, buffer) -> str:
        """Add buffer to server and return url to reach it"""

        tag = self.get_tag()
        self.buffers[tag] = buffer
        url = f"{self.url}/{tag}"
        print(f"Buffer URL: {url}")

        return url


    def shutdown(self):
        if self.socket:
            self.socket.close()


def main():

    server = ByteServer(port=50000)
    server.add_buffer(b'TEST')



if __name__ == "__main__":
    main()
