#coding: utf8
import re
import time

from Exscript import Account
from Exscript.protocols import ssh2


class huawei():
    ip = ''
    user = ''
    password = ''
    mac = ''
    msg = []
    find_err_string = 'display interface  | inc port-sec'
    find_err_regexp = r'(?im)^GigabitEthernet(\d/0/\d{1,2})'
    portsec_int_string='display mac-address sticky | inc '
    portsec_int_regexp=r'(?im)[a-z0-9]{4}-([a-z0-9]{4}-[a-z0-9]{4})'

    def __init__(self, ip, user, password, mac):
        self.ip = ip
        self.user = user
        self.password = password
        self.mac = mac

    def connect(self):
        self.errors = []
        try:
            acc = Account(self.user, self.password)
            conn = ssh2.SSH2()
            conn.connect(self.ip)
            conn.login(acc)
            conn.set_timeout(60)
            return conn

        except Exception as e:
            self.errors.append('Error')
            for i in e:
                self.errors.append(i)

            return self.errors



    #Поиск мак адреса
    def exec_cmd(self):
        conn = self.connect()
        conn.execute('sys')
        conn.execute('display mac-address | inc ' + self.mac)
        data = conn.response
        fnd_mac = re.findall(r'(?im)^[a-z0-9]{4}-[a-z0-9]{4}-' + self.mac + '.+GE(\d/0/\d{1,2})', data)
        conn.execute('quit')
        try:
            conn.close(True)
        except Exception:
            print('error while close ssh connection')

        if len(fnd_mac) > 0:
            return(fnd_mac)
        else:
            return('On switch ' + self.ip + ' nothing find')

    ###ОЧиска порта
    def clear_port(self, interface, conn):
        conn.execute('sys')
        print('Clearing interface: ' + interface)
        conn.execute('interface G' + interface)
        conn.execute('undo port-security mac-address sticky')
        time.sleep(1)
        conn.execute('port-security mac-address sticky')
        time.sleep(1)
        conn.execute('restart')
        conn.execute('quit')
        time.sleep(1)
        conn.execute('quit')


    def find_err_d(self, conn):
        '''Возвращает список мак адресов заблокированных интерфейсов
        В формате ['xxxx.xxxx']'''


        conn.execute(self.find_err_string)
        data = conn.response
        i_f = re.findall(self.find_err_regexp, data)

        if i_f:
            # print('Найдены заблокированные интерфейсы: ')
            # self.msg.append('Найдены заблокированные интерфейсы: ')
            for i in i_f:
                i_f[i_f.index(i)] = i.encode('utf-8')
                # self.msg.append(i.encode('utf-8'))

            return i_f

    def portsec_int(self, interface, conn):
        '''Возвращает кортеж макадресов на данных интерфейсах
        Принимает интерфейс в формает "x/x/x"
        Возвращает список ['xxxx.xxxx']'''
        conn.execute(self.portsec_int_string + interface)
        data = conn.response
        mac = re.findall(self.portsec_int_regexp, data)

        for i in mac:
            mac[mac.index(i)] = re.subn('-', '.', i.encode('utf-8'))[0]  # перекодируем в utf-8 и меняю в мак адресе '-' на '.'
        return mac

    def find_mac_sticky(self, mac_sticky, conn):
        '''Возвращает список интерфейсов на которых в стики таблице найдет искомый mac-address'''
        conn.execute(self.portsec_int_string + mac_sticky)
        data = conn.response
        interface = re.findall(r'.+GE(\d/0/\d{1,2})', data)
        return interface


    def portsec_addr(self, conn):

        '''Ищет заблокированные порты на которых светится данный мак адрес.
        Возвращает кортеж интерфейсов на которых светится данный мак'''
        '''Возварщает список мак и интерфейс в формате ['xxxx.xxxx'], ['x/x/x']'''

        conn.execute('screen-length 0 temporary')
        conn.execute('display logfile flash:/logfile/log.log | inc L2IFPPI/4/PORTSEC_ACTION_HAVEMAC_ALARM')

        data = conn.response
        i_f = re.findall(r'(?im)((?:[a-fA-f0-9]{2}\.){5}[a-fA-f0-9]{2}).+GigabitEthernet(\d/\d/\d{1,2})', data)
        i_f = [list(m) for m in i_f]
        for m in i_f:
            m[0] = re.findall(r'.{11}$', m[0].encode('utf-8'))[0] # Из мак адреса выделяю последние 11 символов.
            m[0] = re.subn('([a-fA-f0-9]{2}).([a-fA-f0-9]{2}).([a-fA-f0-9]{2}).([a-fA-f0-9]{2})', r'\1\2.\3\4', m[0])[0] # Форматирую мак адрес в формат xxxx.xxxx
            m[1] = m[1].encode('utf-8')
        return i_f

    def unblock_port(self, conn):
        alrady_find = False
        iface = ''
        err_int_clr = []
        self.msg = []

        try:
            err_int = self.find_err_d(conn) # Ищем заблокированные интерфейсы

            if err_int:
                for i in err_int:
                    print('Find blocked interface:', i)
                    iface = i
                    mac = self.portsec_int(i, conn) # Список мак адресов на данном интерфейсе
                    # print(mac)
                    for j in mac:
                        print('find mac address on blocked port: ' + j)
                        if j == self.mac:
                            self.clear_port(i, conn)
                            self.msg.append('find mac {0} address on interface: {1} && was cleaned'.format(j, i))
                            alrady_find = True
            else:
                self.msg.append('Can\'t find mac address on interface.')

            err_int = self.portsec_addr(conn) # Смотрим в логах какие интерфейсы недавно блокировались и какие на них мак адреса

            print('find in log file blocked interfaces: ')
            print(err_int)
            print('first interface is ' + iface)
            print(iface)

            if err_int:

                for ifc in err_int:
                    if ifc not in err_int_clr:
                        err_int_clr.append(ifc)             #  Убираем повторяющиеся элементы списка.

                print('cleared list is:')
                print(err_int_clr)

                for i in err_int_clr:
                    if (i[0] == self.mac) and (i[0] != iface):
                        self.clear_port(i[1], conn)
                        self.msg.append('find mac {0} address on interface: {1}  && was cleaned'.format(i[0], i[1]))
                        alrady_find = True

            if not alrady_find:             #Если мак нигде не найден, то ищется мак в стики таблице и разблокируется интерфейс.
                mac_sticky = self.find_mac_sticky(self.mac, conn)
                if mac_sticky:
                    [self.clear_port(i, conn) for i in mac_sticky]
                    self.msg.append('find sticky mac {0} address on interface: {1}  && was cleaned'.format(self.mac, mac_sticky))


        except Exception as e:
            self.msg.append('Error in unblock_port')
            for er in e:
                self.msg.append(er)

        finally:

            self.close_conn(conn)
            return self.msg

    def close_conn(self, conn):
        '''Функция закрытия соединения'''
        try:
            conn.close(True)
        except Exception:
            print('error while closing ssh connection')



class Cisco(huawei):
    find_err_string = 'show interfaces status | inc err-d'
    find_err_regexp = r'(?im)^Gi(\d/0/\d{1,2})'
    portsec_int_string = 'show port-security interface G'
    portsec_int_regexp = r'(?im)[a-z0-9]{4}\.([a-z0-9]{4}\.[a-z0-9]{4})'

    def exec_cmd(self, conn):
        conn.execute('show mac address-table | inc ' + self.mac)
        data = conn.response
        fnd_mac = re.findall(r'(?im).+[a-z0-9]{4}\.[a-z0-9]{4}\.' + self.mac + '.+Gi(\d/0/\d{1,2})', data)

        self.close_conn(conn)

        if len(fnd_mac, conn) > 0:
            return(fnd_mac)
        else:
            return('On switch ' + self.ip + ' nothing find')

    def clear_port(self, interface, conn):
        '''Очистка порта
        1. Чистим нужный порт
        2. Переходим в режим конфигурирования
        3. Перезагружаем порт'''
        for i in interface:
            conn.execute('clear port-security all interface G' + i)
            time.sleep(1)
            conn.execute('conf t')
            time.sleep(0.5)
            conn.execute('interface G' + i)
            time.sleep(0.5)
            conn.execute('shu')
            time.sleep(0.5)
            conn.execute('no shu')
            time.sleep(0.5)
            conn.execute('exit')
            time.sleep(0.5)
            conn.execute('exit')


    def portsec_addr(self, conn):

        '''Ищет заблокированные порты на которых светится данный мак адрес.
        Возвращает кортеж интерфейсов на которых светится данный мак'''

        conn.execute('show port-security address | inc ' + self.mac)
        data = conn.response
        i_f = re.findall(r'(?im).+Gi(\d/0/\d{1,2})', data)

        if len(i_f) > 0 :
            return i_f
        else:
            return False


    def unblock_port(self, conn):
        '''Основная функция
        1. Смотрит мак адрес, если находит разблокирует
        2. Смотрит заблокированные интерфейсы
        3. В каждом интерфейсе ищет мак, если находит то разблокирует'''
        try:
            msg = ''
            addr = self.portsec_addr(conn)

            if addr:

                self.clear_port(addr, conn)
                self.msg.append('find mac address on interface: ')
                [self.msg.append(a) for a in addr]

            else:
                self.msg.append('Can\'t find mac address on interface.')

            err_int = self.find_err_d(conn)

            if err_int:
                for mc in err_int:
                    macaddr = self.portsec_int(mc, conn)
                    if macaddr:
                            if macaddr[0] == self.mac:
                                print('Clear interface g' + mc + '  mac address: ' + macaddr[0])
                                self.msg.append('Clear interface g' + mc + '  mac address: ' + macaddr[0])
                                self.clear_port([mc], conn)

        except Exception as e:
            # print('Error in unblock_port')
            self.msg.append('Error in unblock_port')
            for er in e:
                self.msg.append(er)

        finally:
            self.close_conn(conn)
            return self.msg






