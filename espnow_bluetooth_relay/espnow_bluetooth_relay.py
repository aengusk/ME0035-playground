# This module is used on BOTH the Pico and the ESP
# The Pico imports and uses the send() and receive() functions
# The ESP runs be_relay in main

# Python
import time
from sys import platform
# custom
from BLE_Minimal import Sniff, Yell # type: ignore (suppresses Pylance lint warning)
yeller = Yell()
sniffer = Sniff('k', verbose = False)


if platform == 'esp32':
    from networking import Networking   # type: ignore
    networking = Networking()
    # recipient_mac = b'\xff\xff\xff\xff\xff\xff' #This mac sends to all
    macs_whitelist = (b'T2\x04!p\xcc') # a tuple of the mac addresses that we will listen to

print('Networking should have initted by now')

def check_NOW(verbose = False, verify_mac = True):
    messages = list(networking.aen.return_messages())
    print(messages)
    if not messages == [(None, None, None)]:
        if verbose: print('{} messages were received since the last check'.format(len(messages)))
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
                yeller.advertise('k0')
            elif message == 1:
                print('add a smoothie to the order')
                yeller.advertise('k1')
            elif message == 2:
                print('add a ramen to the order')
                yeller.advertise('k2')
    else:
        if verbose: print('no messages were received')

def send_NOW(message):
    raise NotImplementedError
    # This might not be needed if we end up being one-directional

def send_bluetooth(message):
    yeller.advertise('k' + message)

def check_bluetooth():
    message = sniffer.last
    sniffer.last = ''
    if message:
        return message
    else:
        return None

def be_relay(verbose = False, verify_mac = True, refresh_rate = 1): # keep structured so that it can be turned into an async function
    while True:
        check_NOW(verbose = verbose, verify_mac = verify_mac)
        #check_bluetooth(verbose = verbose) # this might not be necessary without two different tables
        time.sleep(refresh_rate)

'''def testmain():
    from sys import platform
    if platform == 'esp32':
        iter = 0
        while True:
            send_bluetooth('aengus{}'.format(iter := iter + 1))
            time.sleep(0.69079)
    elif platform == 'rp2':
        while True:
            message = check_bluetooth()
            print(message)
            time.sleep(1)
    else:
        raise RuntimeError('platform not understood: {}'.format(platform))'''
    

sniffer.scan(0)

if __name__ == '__main__':
    if platform == 'rp2':
        print('about to start checking bluetoooth once every second')
        iter = 0
        while True:
            print(iter := iter + 1)
            message = check_bluetooth()
            print(message)
            time.sleep(1)
    elif platform == 'esp32':
        print('about to start being an ESP relay')
        be_relay(verbose = True, verify_mac = False)