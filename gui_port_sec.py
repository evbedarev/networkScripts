# coding=utf-8
from tkinter import *
import Portsec
from db_ import read_settings, ins_to_db
import Exscript



class Application(Frame, object):
    """docstring for Application"""

    def __init__(self, master):
        super(Application, self).__init__(master)
        self.readFile()
        self.grid(row=5, column=5)
        self.create_widgets()

    def create_widgets(self):
        self.lbl_path_utc = Label(self, text='mac address ')
        self.lbl_path_utc.grid(row=2, column=0, columnspan=4, sticky=W)
        self.mac = Entry(self, width=30)
        self.mac.grid(row=3, column=0, columnspan=2, sticky=W)

        self.ip_com = Label(self, text='ip commutator:')
        self.ip_com.grid(row=4, column=0, columnspan=4, sticky=W)
        self.ip_com = Entry(self, width=30)
        self.ip_com.grid(row=5, column=0, columnspan=2, sticky=W)
        self.ip_com.insert(0, self.ip[0])

        self.login = Label(self, text='login')
        self.login.grid(row=6, column=0, columnspan=4, sticky=W)
        self.login = Entry(self, width=30)
        self.login.grid(row=7, column=0, columnspan=2, sticky=W)
        self.login.insert(0, self.user[0])

        self.pwd = Label(self, text='password')
        self.pwd.grid(row=8, column=0, columnspan=4, sticky=W)
        self.pwd = Entry(self, width=30, show="*")
        self.pwd.grid(row=9, column=0, columnspan=2, sticky=W)

        self.text = Label(self, text='message:')
        self.text.grid(row=10, column=0, columnspan=4, sticky=W)
        self.text = Text(self, width=50, height=7, wrap=WORD)
        self.text.grid(row=11, column=0, columnspan=2, sticky=W)
        self.text.delete("0.0", END)

        self.ok_bttn = Button(self, text="Start", width=10, command= self.clear_port)
        self.ok_bttn.grid(row=12, column=0, sticky=W)

        self.ok_bttn = Button(self, text="Save", width=10, command= self.SaveToFile)
        self.ok_bttn.grid(row=12, column=1, sticky=W)


    def clear_port(self):
        self.msg = []
        self.inc = 1

        Stack = ['', '']

        self.text.delete("0.0", END)
        if self.ip_com.get() == 'ZD':
            for st in Stack:
                self.msg = []
                self.msg = self.connection(st)
                [self.render_message(ms) for ms in self.msg]
        else:
            self.msg = self.connection(self.ip_com.get())
            [self.render_message(ms) for ms in self.msg]


    def readFile(self):
        self.ip = read_settings('ip_com')
        self.user = read_settings('user')

    def render_message(self, msg):
        self.text.insert(str(self.inc) + ".0", msg + "\n")
        self.inc = self.inc + 1

    def connection(self, ip):
        '''Устанавливает соединение и проверяет является ли возвращенное значение
        инстансом Exscript. 
        - Если является то запускается функция поиска мак адреса.
        - Если возвращается список, то выдается ошибка'''

        fnd = Portsec.huawei(ip,
                             self.login.get(),
                             self.pwd.get(),
                             self.mac.get())
        self.render_message('connecting to stack: ' + ip)
        conn = fnd.connect()
        if isinstance(conn, Exscript.protocols.ssh2.SSH2):
            return fnd.unblock_port(conn)
        else:
            self.render_message('Error in module ssh2.SSH2. Problem with auth...')
            raise Exception('Type conn not SSH2.  Problem with auth...')


    def SaveToFile(self):
        ins_to_db(self.ip_com.get().strip(), self.login.get().strip())

root = Tk()
root.title("Clear interface")
root.geometry("450x350")
app = Application(master=root)
root.mainloop()