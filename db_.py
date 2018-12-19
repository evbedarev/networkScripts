import sqlite3
import os

def read_settings(par):
    list = []
    dir = os.path.abspath(os.curdir)
    base_name = dir + r'\portsec_settings.sqlite'
    con = sqlite3.connect(base_name)
    cur = con.cursor()
    cur.execute(
                "select {} from {}".format(par, 'settings')
            )
    res = cur.fetchall()
    for i in res:
        for j in i:
            list.append(j)
    cur.close()
    con.close()
    return(list)


def ins_to_db(par, val):
    dir = os.path.abspath(os.curdir)
    base_name = dir + r'\portsec_settings.sqlite'
    con = sqlite3.connect(base_name)
    cur = con.cursor()

    cur.execute(
         "delete from settings"
    )
    con.commit()
    cur.execute(
            "INSERT INTO 'main'.'settings' ('ip_com','user') VALUES ('{}','{}')".format(par, val)
        )
    con.commit()
    cur.close()
    con.close()