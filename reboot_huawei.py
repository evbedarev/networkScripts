#coding: utf8
'''
Находит интерфейсы которые не в 10 или 12 вланах
'''

from Exscript import Account
from Exscript.protocols import ssh2
import time
import ReadAccountData,os;

readAccData = ReadAccountData.ReadAccountDataFromFile(os.getcwd() + "\\profile.txt");

user = readAccData.read_username();
password = readAccData.read_password();
readAccData.close();

ip_addr = ['', '']

for i in ip_addr:
    acc = Account(user, password)
    conn = ssh2.SSH2()
    conn.connect(i)
    conn.login(acc)
    conn.execute('reboot')
    time.sleep(10)
    conn.execute('y')
    time.sleep(10)
    conn.close(True)