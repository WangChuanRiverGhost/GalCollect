# 输入查询条件
from datetime import datetime

log_path = "services/logging.txt"
def write_log(message):
    time_only = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"【{time_only}】{message}\n")

def get_sql():  # 生成sql语句
    pass