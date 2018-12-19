#coding: utf8
'''
Находит интерфейсы которые не в 10 или 12 вланах
'''
from Exscript import Account;
from Exscript.protocols import ssh2;
import re;
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

for j in range(1, 11):
    for i in range(1, 49):
        # print(i,j)
        if j < 5 or j > 6:
            conn.execute('show running-config interface g{0}/{1}'.format(j, i))
            data = conn.response
            if re.findall(r'(?im)(.*vlan 10.*)', data) == [] and re.findall(r'(?im)(.*vlan 12.*)', data) == []:
                print(re.findall(r'(?im)(interface GigabitEthernet\d{1,2}/\d{1,2})', data))
                print(re.findall(r'(?im)(.*desc.*)', data))
                print(re.findall(r'(.*vlan.*)|(.*trunk.*)', data))
                # print(re.findall(r'(^interface GigabitEthernet\d/\d/\d{1,2}$).*((^.*vlan.*$)|(^.*mode trunk.*$))', data))

conn.close(True)