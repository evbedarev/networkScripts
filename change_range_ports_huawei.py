#coding: utf8
from Exscript import Account
from Exscript.protocols import ssh2
import time, os;
import ReadAccountData;

readAccData = ReadAccountData.ReadAccountDataFromFile(os.getcwd() + "\\profile.txt");

user = readAccData.read_username();
password = readAccData.read_password();
readAccData.close();


ip = ['']
exception = [] #['0/0/23', '0/0/24', '1/0/12']
acc = Account(user, password)
try:
    for i in ip:
        conn = ssh2.SSH2()
        conn.connect(i)
        conn.login(acc)
        conn.set_timeout(60)
        conn.execute('sys')

        for k in range(2, 3):
            for j in range(43, 49):  #Перебор модулей и портов
                if '{0}/0/{1}'.format(k, j) not in exception: #Проверяем нет ли порта в исключениях
                    conn.execute('interface g{0}/0/{1}'.format(k, j))
                    # conn.execute('di th')
                    # port - security enable
                    # port - security protect - action shutdown
                    # port - security mac - address sticky
                    print('change configuration on port {0}/0/{1} ...'.format(k, j))
                    time.sleep(0.5)
                    conn.execute('port-security enable')
                    time.sleep(0.5)
                    conn.execute('port-security max-mac-num 1')
                    time.sleep(0.5)
                    conn.execute('port-security mac-address sticky')
                    time.sleep(0.5)
                    conn.execute('port-security protect-action shutdown')
                    time.sleep(0.5)
                    #data = conn.response
                    conn.execute('quit')
                    print('... has changed ...')
                    # print (data)


except Exception as e:
    print(e)

finally:
    conn.close(True)
