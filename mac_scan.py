#!/bin/python

import scapy.all as scapy


class ArpScanner:
    def __init__(self, ip):
        self.ip = ip
        self.scan()

    def scan(self):
        request = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst=self.ip)
        answered, unanswered = scapy.srp(request, timeout=2, retry=1)
        for sent, received in answered:
            print(f'IP: {received.psrc} MAC: {received.hwsrc}')


if __name__ == '__main__':
    scan = ArpScanner('192.168.0.0/24')
