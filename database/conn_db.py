# 连接数据库，并通过conn_cngal()传出连接使其他文件进行调用
 
import sqlite3

def conn_cngal():

    conn = sqlite3.connect("database/cngal_database.db")
    conn.row_factory = sqlite3.Row

    return conn