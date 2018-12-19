from Exscript import Account
from Exscript.protocols import ssh2
import re
import ReadAccountData, os;


class FindMacOnHuawei():
    readAccData = ReadAccountData.ReadAccountDataFromFile(os.getcwd() + "\\profile.txt");
    user = readAccData.read_username();
    password = readAccData.read_password();
    readAccData.close();

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
        self.conn.execute(command)
        return self.conn.response

    def exec_command_without_return(self, command):
        self.conn.execute(command);


    def findMacOnSwitch(self):
        for ip in self.list_ip:
            if ip.port != "none":
                print("skiping ip_port=" + ip.port);
                continue;

            if ip.dhcp_enabled == '1':
                print("skiping dhcp enabled");
                continue;

            print (ip.mac)
            data = self.exec_command('display mac-address | inc  {0}'.format(ip.mac))
            fnd_mac = re.findall(r'(?im).*(GE\d/0/\d{1,2}).*', data)
            if len(fnd_mac) > 0:
                print(fnd_mac[0]);
                ip.port = fnd_mac[0];
                ip.switch = self.ip_switch;

        return self.list_ip;


    def disconnect(self):
        try:
            self.conn.close(True)
        except Exception:
            print('error while close ssh connection')