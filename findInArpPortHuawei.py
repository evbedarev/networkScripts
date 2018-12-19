from Exscript import Account
from Exscript.protocols import ssh2
import re
import ReadAccountData, os;

readAccData = ReadAccountData.ReadAccountDataFromFile(os.getcwd() + "\\profile.txt");

user = readAccData.read_username();
password = readAccData.read_password();
readAccData.close();

acc = Account(user, password)
conn = ssh2.SSH2()
ip = ''

conn.connect(ip)
conn.login(acc)
conn.set_timeout(60)
path_to_read_file = 'C:\\TEMP\\mac.txt'
file_to_write = open('C:\\TEMP\\mac_and_port_' + ip + '.txt', 'w+')


def findInArp(conn, mac):
    global ethTrunk
    conn.execute('display mac-address | inc  {0}'.format(mac))
    data = conn.response
    list = re.search(r'GE\d/\d/\d{2}', data)
    if list is not None:
        file_to_write.write(mac + ";" + list.group() + ";Switch IP: " + ip + '\n')
    else:
        file_to_write.write(mac + " - Cant'find" + '\n')

file_read = open(path_to_read_file, 'r')
list_macs = file_read.readlines()

for lm in list_macs:
    findInArp(conn, lm.lower().strip())
# string = "28D2.444D.9D17"
# findInArp(conn, string.lower())

file_to_write.close()
file_read.close()
conn.close(True)
