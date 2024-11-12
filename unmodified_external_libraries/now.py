import network
import espnow
import time

class Now():
    def __init__(self, callback = None):
        self.connected= False
        self.everyone = b'\xff\xff\xff\xff\xff\xff'    # talk to all mac addresses
        self.callback = callback if callback else self.default
        self.peers = []
    
    def default(self, msg, mac):
        mac_str = ':'.join(f'{b:02x}' for b in mac)
        print(msg.decode(),mac_str)

    def irq_receive(self, remote_network):
        try:
            mac, msg = remote_network.irecv()
            if mac != None and mac not in self.peers: #check if the peer has already been added
                self.peers.append(mac)
                self.now_network.add_peer(mac)
            self.callback(msg, mac)
        except Exception as e:
            print(f"Receive Error: {e}")

    def connect(self):
        # Set up the network and ESPNow
        self.wifi = network.WLAN(network.STA_IF) # ESP network type
        self.wifi.active(True)
        self.now_network = espnow.ESPNow()
        self.now_network.active(True)
        self.now_network.add_peer(self.everyone)
        self.now_network.irq(self.irq_receive)
        self.connected = True

    def publish(self, msg, mac = None):
        if not mac:
            mac = self.everyone
        if self.connected:
            self.now_network.send(mac, msg)

    def close(self):
        self.now_network.irq(None)
        self.now_network.active(False)
        self.wifi.active(False)
        self.connected = False
        print("Cleanup complete.")