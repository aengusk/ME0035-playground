from networking import Networking
import time

#Initialise
networking = Networking()

###Example code###

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


            print(mac, message, receive_time)
        print()
        if message is not None:
            if int(message) == 2:
                print('we received an order of 2')
                print()
        time.sleep(1)


if __name__ == '__main__':
    monitor_NOW()