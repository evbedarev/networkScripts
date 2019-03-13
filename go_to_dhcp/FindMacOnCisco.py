
import re
from Exscript import Account
from Exscript.protocols import ssh2
import time
import ReadAccountData, os;

class FindMacOnCisco():
    readAccData = ReadAccountData.ReadAccountDataFromFile(os.getcwd() + "\\profile.txt");
    user = readAccData.read_username();
    password = readAccData.read_password();
    readAccData.close();

    print(user + " " + password)
    acc = Account(user, password)
    conn = ssh2.SSH2()
    list_ip = []
    ip_switch = ""

    def __init__(self, list_ip, ip_switch):
        self.list_ip = list_ip
        self.ip_switch = ip_switch

    def connect(self):
        self.conn.connect(self.ip_switch)
        self.conn.login(self.acc)
        self.conn.set_timeout(60)
        print('_______________connect to ' + self.ip_switch + '____________')


    def exec_command(self, command):
        try:
            self.conn.execute(command)
            return self.conn.response
        except Exception:
            print("error cisco in command: " + command )

    def exec_command_without_return(self, command):
            self.conn.execute(command);
            time.sleep(1)

    def findMacOnSwitch(self):
        for ip in self.list_ip:
            if ip.port != "none":
                print("skiping ip_port=" + ip.port);
                continue;

            if ip.dhcp_enabled == '1':
                print("skiping dhcp enabled " + ip.ip);
                continue;

            data = self.exec_command('show mac address-table | inc {0}'.format(ip.mac))

            if (len(data) > 0):
                fnd_mac = re.findall(r'(?im).*(GigabitEthernet\d/\d{1,2}).*', data)

            if len(fnd_mac) > 0:
                print(fnd_mac[0]);
                ip.port = fnd_mac[0];
                ip.switch = self.ip_switch;

        # self.exec_command_without_return("exit")
        try:
            self.exec_command_without_return("exit")
        except Exception:
            print("error cisco in command: " + 'show mac address-table | inc {0}'.format(ip.mac) )
        # finally:
        #     self.disconnect()
        return self.list_ip;

    def disconnect(self):
        try:
            self.conn.close(True)
        except Exception:
            print('error while close ssh connection')

