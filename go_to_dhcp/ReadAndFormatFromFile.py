import re;
import IP;
import FindMacOnHuawei;

class ReadAndFormat():
    filename = ""

    def __init__(self, filename):
        self.filename = filename

    def formatFile(self):
        listMac = []
        f = open(self.filename, 'r')

        for line in f.readlines():
            ip = re.findall(r'(?im)(172\.29\.\d{2,3}\.\d{1,3})', line)

            mac_find = re.findall(r'(?im)([0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2})', line.lower())

            if mac_find is not None:
                mac = re.split(r':', mac_find[0])

            if mac is not None:
                formated_mac = mac[0] + mac[1] + "." +\
                               mac[2] + mac[3] + "." +\
                               mac[4] + mac[5]
            else:
                formated_mac = []
                formated_mac[0] = "none"

            dhcp_enabled = re.findall(r'(?im)(\d)$', line)

            if dhcp_enabled is None:
                dhcp_enabled = 'n'

            user_name = re.findall(r'(?im)((?:[0-9a-z]|\.|-)*).*172', line)

            print("Ip: " + ip[0] + "  mac: " + formated_mac + " dhcp_enabled: " + dhcp_enabled[0] + " user name: " + user_name[0])

            listMac.append(IP.IpMac(ip[0],
                                    formated_mac,
                                    user_name[0],
                                    "none",
                                    "none",
                                    dhcp_enabled[0]))
        return listMac;

rf = ReadAndFormat('C:\\TEMP\\mac_from_report.txt');
listIP = rf.formatFile();

# hw = FindMacOnCisco.FindMacOnCisco(listIP, '172.29.110.9');
# hw.connect();
# listIP = hw.findMacOnSwitch();
# hw.disconnect();

# hw = FindMacOnHuawei.FindMacOnHuawei(listIP, '172.29.110.5');
# hw.connect();
# listIP = hw.findMacOnSwitch();
# hw.disconnect();
#
# hw = FindMacOnHuawei.FindMacOnHuawei(listIP, '172.29.110.6');
# hw.connect();
# listIP = hw.findMacOnSwitch();
# hw.disconnect();


hw = FindMacOnHuawei.FindMacOnHuawei(listIP, '172.29.110.22');
hw.connect();
listIP = hw.findMacOnSwitch();
hw.disconnect();


hw = FindMacOnHuawei.FindMacOnHuawei(listIP, '172.29.110.21');
hw.connect();
listIP = hw.findMacOnSwitch();
hw.disconnect();

#
# hw = FindMacOnHuawei.FindMacOnHuawei(listIP, '172.29.110.15');
# hw.connect();
# listIP = hw.findMacOnSwitch();
# hw.disconnect();

f = open('C:\\TEMP\\mac_and_port_svod_py.txt', 'w+');

for ls in listIP:
    f.write(ls.ip + ';' + ls.username + ';' + ls.mac + ';' + ls.switch + ';' + ls.port + ';' + ls.dhcp_enabled + '\n');
f.close();
