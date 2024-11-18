from networking import Networking
import time

networking = Networking()

recipient_mac = b'\xff\xff\xff\xff\xff\xff' #This mac sends to all
message =  b'Boop'

macs_whitelist = (b'T2\x04!p\xcc',) # a tuple of the mac addresses that we will listen to


def monitor_NOW(verbose = False, verify_mac = True): # keep structured so that it can be turned into an async function
    i = 0
    while True:
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
                print('add a ___ to the order')
            elif message == 1:
                print('add a ___ to the order')
            elif message == 2:
                print('add a ___ to the order')
        time.sleep(1)

def send_NOW(message):
    raise NotImplementedError

if __name__ == '__main__':
    monitor_NOW(verbose = True)