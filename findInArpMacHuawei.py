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

conn.connect('')
conn.login(acc)
conn.set_timeout(60)
path_to_read_file = 'C:\\TEMP\\mac.txt'
file_to_write = open('C:\\TEMP\\mac_and_pc.txt', 'w+')


def findInArp(conn, mac):
    global ethTrunk
    conn.execute('display mac-address | inc  {0}'.format(mac))
    data = conn.response
    list = re.search(r'Eth-Trunk\d', data)
    if list is not None:
        if list.group() == "Eth-Trunk1":
            ethTrunk = "to C4510"

        if list.group() == "Eth-Trunk2":
            ethTrunk = "To S5720 172.29.110.6"

        if list.group() == "Eth-Trunk3":
            ethTrunk = "TO S5720 172.29.110.22"

        if list.group() == "Eth-Trunk4":
            ethTrunk = "TO S5720 172.29.110.21"

        if list.group() == "Eth-Trunk6":
            ethTrunk = "to S5720 172.29.110.5"

        if list.group() == "Eth-Trunk7":
            ethTrunk = "To 172.29.110.15"
        file_to_write.write(mac + ";" + list.group() + ";" + ethTrunk + '\n')
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
