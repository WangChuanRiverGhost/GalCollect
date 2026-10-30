import json
from datetime import datetime

log_path = "services/logging.txt"
def write_log(message):
    time_only = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"【{time_only}】{message}\n")

def get_JsonData(data):  # 传入元组并遍历判断这个数据传入哪个json文件并传入

    write_log("正在将数据写入json文件...")
    add_json(data[0],"services/json/history/artices_history.json")

    add_json(data[1],"services/json/read_text/work_artices.json")

    write_log("数据成功写入json文件！")
def add_json(json_data,json_path):  # 传入要写入json文件的数据（列表套字典的python数据）以及要写入的json文件路径
    
    with open(json_path,"w+",encoding="utf-8") as f:

        data = json.dumps(json_data,ensure_ascii=False,indent=2)
        
        f.write(f"{data}")

