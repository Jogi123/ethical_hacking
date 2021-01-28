import os
import random
import string


class MacChanger:
    def __init__(self, vendor, interface):
        self.vendor = vendor
        self.interface = interface
        self.possible_chars = 'abcdef'
        self.possible_digits = self.possible_chars + string.digits
        self.set_prefix_for_vendor()

    def set_prefix_for_vendor(self):
        """
        set a prefix of a known vendor so it's harder to find out that the mac is fake
        """
        if self.vendor == 'cisco':
            mac = 'e4:c7:22'
        elif self.vendor == 'realtek':
            mac = '00:e0:4c'
        elif self.vendor == 'd-link':
            mac = 'fc:75:16'
        else:
            mac = 'fc:f8:ae'
        self.generate_random_mac(mac)

    def generate_random_mac(self, mac):
        """
        generate random mac address in hex in the form of ff:ff:ff:ff:ff:ff
        """
        for i in range(3):
            first_char = random.choice(self.possible_digits)
            second_char = random.choice(self.possible_digits)
            block = first_char + second_char
            mac += f':{block}'
        print(mac)
        self.change_mac(mac)

    def change_mac(self, mac):
        """
        actually change mac using ip link
        """
        print(os.system(f'ip link show {self.interface}'))
        os.system(f'sudo -S ip link set dev {self.interface} down')
        os.system(f'sudo -S ip link set dev {self.interface} address {mac}')
        os.system(f'sudo -S ip link set dev {self.interface} up')
        print(os.system(f'ip link show {self.interface}'))


if __name__ == '__main__':
    # note: works only with ethernet, not with wifi adapter
    changer = MacChanger('cisco', 'eth0')
