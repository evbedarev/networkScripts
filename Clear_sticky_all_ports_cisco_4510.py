#coding: utf8
'''
Находит интерфейсы которые не в 10 или 12 вланах
'''
from Exscript import Account
from Exscript.protocols import ssh2
import re
import ReadAccountData, os;

readAccData = ReadAccountData.ReadAccountDataFromFile(os.getcwd() + "\\profile.txt");

user = readAccData.read_username();
password = readAccData.read_password();
readAccData.close();

path_to_read_file = 'C:\\TEMP\\port4510.txt'

acc = Account(user, password)
conn = ssh2.SSH2()

conn.connect('')
conn.login(acc)
conn.set_timeout(60)

listPorts = open(path_to_read_file, 'r')

def findMacPortSticky(conn, port):
    conn.execute('show run interface ' + port)
    data = conn.response
    listF = re.findall(r'(?im).*(switchport port-security mac-address sticky [0-9a-f]{4}.[0-9a-f]{4}.[0-9a-f]{4}).*', data)
    if len(listF) > 0:
        for elm in listF:
            print('clear port: ' + port + ' ' + elm)
            clearPortSecSticky(conn, port, listF)

def clearPortSecSticky(conn, port, listMacs):
    conn.execute('conf t')
    conn.execute('interface ' + port)
    for mac in listMacs:
        conn.execute('no ' + mac)
    conn.execute('exit')
    conn.execute('exit')

rowsPorts = listPorts.readlines()
for line in rowsPorts:
    findMacPortSticky(conn, line.strip())

listPorts.close()
conn.close(True)