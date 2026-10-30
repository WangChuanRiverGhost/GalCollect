# 添加数据到数据库：
"""
打开json文件，把里面的内容存储起来；
遍历内容，将每一条生成sql添加语句，生成列表；
连接数据库
"""
from datetime import datetime
import json,re,sqlite3

def conn_cngal():

    conn = sqlite3.connect("database/cngal_database.db")
    conn.row_factory = sqlite3.Row

    return conn

log_path = "services/logging.txt"
def write_log(message):
    time_only = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"【{time_only}】{message}\n")

def add_sql():

    data_path = "services/json/read_text/work_artices.json"
    with open(data_path,'r',encoding='utf-8') as f:
        data = json.load(f)

    with conn_cngal() as conn:

        for i in data:
            title = i["title"]
            write_log(f"正在将{title}信息存入数据库...")
            report_type = i["type"]

            text = i["create_time"]
            m = re.search(r'(\d{4})-(\d{2})-(\d{2})', text)

            if m:
                year = m.group(1)  
                month = m.group(2) 
                day = m.group(3)

            url = i["url"]

            n = re.search(r'(\d+)$', url)
            num = n.group(1) if n else ""

            path = i["maintext_path"]

            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO work_artices(report_id,title,report_type,report_url,report_mainTextPath,report_createYear,report_createMonth,report_createDay) VALUES(?,?,?,?,?,?,?,?)",[num,title,report_type,url,path,year,month,day])
            write_log(f"{title}信息存入数据库成功！")

    return True
