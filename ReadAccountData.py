import os,re;

class ReadAccountDataFromFile():
    path = "";
    t = "";
    rows_file = "";

    def __init__(self, path):
        self.path = path;
        self.t = open(self.path);
        self.rows_file = self.t.readlines();

    def read_username(self):
        for line in self.rows_file:
            if len(re.findall(r'(?im)^username:(.+)', line)) > 0:
                username = re.findall(r'(?im)^username:(.+)', line);
                return username[0];

    def read_password(self):
        for line in self.rows_file:
            if len(re.findall(r'(?im)^password:(.+)', line)) > 0:
                password = re.findall(r'(?im)^password:(.+)', line);
                return password[0];
        self.t.close();

    def close(self):
        self.t.close()