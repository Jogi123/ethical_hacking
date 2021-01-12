#!/bin/python

import sys
import socket


class Server_Socket:
    def __init__(self, address_to_listen_for, listen_on_port):
        self.address_to_listen_for = address_to_listen_for
        self.listen_on_port = listen_on_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.initialize_socket()
        (self.client_socket, self.client_address) = self.accept_client()
        self.send_commands()

    def initialize_socket(self):
        self.sock.bind((self.address_to_listen_for, self.listen_on_port))
        self.sock.listen()

    def accept_client(self):
        (client_socket, client_address) = self.sock.accept()
        if client_address:
            print('Client connected!')
        return client_socket, client_address

    def send_commands(self):
        while True:
            cmd = input('')
            if cmd == 'quit':
                self.sock.close()
                sys.exit()
            if len(cmd) > 0:
                self.client_socket.send(cmd.encode())
                client_response = self.client_socket.recv(1024).decode()
                print(client_response)


if __name__ == '__main__':
    test_socket = Server_Socket('0.0.0.0', 1234)
