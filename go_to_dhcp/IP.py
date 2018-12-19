
class IpMac():
    ip = "";
    mac = "";
    username = "";
    switch = "";
    port = "";
    dhcp_enabled = 0;

    def __init__(self, ip, mac, username, switch, port, dhcp_enabled):
        self.ip = ip;
        self.mac = mac;
        self.username = username;
        self.switch = switch;
        self.port = port;
        self.dhcp_enabled = dhcp_enabled;