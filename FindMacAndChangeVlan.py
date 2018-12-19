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
path = 'C:\\TEMP\\mac.txt'


def exec_cmd(conn, mac):
    conn.execute('sys')
    conn.execute('display mac-address | inc ' + mac)
    data = conn.response
    fnd_mac = re.findall(r'(?im)^[a-z0-9]{4}-' + mac + '.+GE(\d/0/\d{1,2})', data)
    try:
        if len(fnd_mac) > 0:
            for mc in fnd_mac:
                conn.execute('interface G' + mc)
                conn.execute('port default vlan 12')
                print ("Changed port " + mc)
            conn.execute('quit')
    except Exception:
        print('error while close ssh connection')
        conn.execute('quit')
    conn.execute('quit')

#exec_cmd(conn, 'd5e9-232c')
list_mac = open(path, 'r').readlines()
list_mac_new = []

for t in list_mac:
    list_mac_new.append(re.findall(r'(?im)^[a-z0-9]{4}-(.*)', t)[0])

for t in list_mac_new:
    exec_cmd(conn, t)

# conn.execute('quit')

try:
    conn.close(True)
except Exception:
    print('error while close ssh connection')




