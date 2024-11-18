# This module is used on BOTH the Pico and the ESP
# The Pico imports and uses the send() and receive() functions
# The ESP runs be_relay in main

# Python
import time
# custom
from BLE_Minimal import Sniff, Yell # type: ignore (suppresses Pylance lint warning)
from networking import Networking   # type: ignore (suppresses Pylance lint warning)

networking = Networking()
yeller = Yell()
#sniffer = Sniff()

# recipient_mac = b'\xff\xff\xff\xff\xff\xff' #This mac sends to all

macs_whitelist = (b'T2\x04!p\xcc',) # a tuple of the mac addresses that we will listen to

def send_NOW(message):
    raise NotImplementedError
    # This might not be needed if we end up being one-directional


def check_NOW(verbose = False, verify_mac = True):
    messages = list(networking.aen.return_messages())
    if verbose: print('{} messages were received since the last check'.formate(len(messages)))

    if verify_mac:
        messages = [message for message in messages if message[0] in macs_whitelist]
        if verbose: print('{} messages were from our MAC addresses'.format(len(messages)))
    for mac, message, receive_time in messages: # <class 'bytes'>, <class 'str'>, <class 'int'>
        try: 
            message = int(message)
        except (TypeError, ValueError) as e: 
            if verbose: print('the message "{}" of type {} raised {}'.format(message, type(message), e))
            continue
        if message == 0:
            print('add a burger to the order')
            yeller.advertize('k0')
        elif message == 1:
            print('add a smoothie to the order')
            yeller.advertize('k1')
        elif message == 2:
            print('add a ramen to the order')
            yeller.advertize('k2')

def check_bluetooth():
    raise NotImplementedError

refresh_rate = 0.5 #seconds

def be_relay(verbose = False, verify_mac = True): # keep structured so that it can be turned into an async function
    while True:
        check_NOW(verbose = verbose, verify_mac = verify_mac)
        #check_bluetooth(verbose = verbose) # this might not be necessary without two different tables
        time.sleep(refresh_rate)

if __name__ == '__main__':
    be_relay()