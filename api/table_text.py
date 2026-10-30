# 读取json文件，获取表格内容；通过传入的json数据以及其他数据，创建表格文件
from fastapi import APIRouter
from datetime import datetime
import json,csv,os,subprocess
from pydantic import BaseModel
from typing import List

class Row(BaseModel):
    title: str = ""
    type: str = ""            # ← 加这一行
    create_time: str = ""
    maintext_path: str = ""
    url: str = ""

log_path = "services/logging.txt"
def write_log(message):
    time_only = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"【{time_only}】{message}\n")

router = APIRouter()

@router.get("/get_table")
def get_workArtices(tp:str):

    urls = {
        "artices_history":"services/json/history/artices_history.json",
        "work_artices":"services/json/read_text/work_artices.json"
    }

    with open(urls[tp],"r",encoding="utf-8") as f:
        data = json.load(f)

    return data

@router.post("/get_excel")
def get_excel(data: List[Row]):
    # 表头：5 列
    report_csv = [
        ["文章标题", "文章类型", "文章创建时间", "文章正文", "文章网址"]
    ]
    write_log("正在生成表格...")
    for d in data:
        if not d.maintext_path:
            continue

        title = d.title
        article_type = d.type
        create_time = d.create_time
        maintext_path = d.maintext_path
        url = d.url

        # 用项目根目录 + 相对路径，避免工作目录不对
        file_path = os.path.join(maintext_path)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                maintext = f.read()
        except FileNotFoundError:
            maintext = ""   # 找不到就留空，别中断整个导出

        # 如果你想导出的是“正文内容”，就放 maintext；
        # 如果只想导出“路径”，就把下面这行的 maintext 换成 maintext_path，
        # 并把表头第 4 列改成“正文文件路径”。
        report_data = [title, article_type, create_time, maintext, url]
        report_csv.append(report_data)

    time_only = datetime.now().strftime("%Y-%m-%d %H%M%S")
    name = f"csv{time_only}"

    csv_dir = os.path.join("database", "csv_file")
    os.makedirs(csv_dir, exist_ok=True)

    path = os.path.join(csv_dir, f"{name}.csv")

    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerows(report_csv)
    write_log("表格生成成功")
    return path

@router.get("/open_csv")
def open_csv(path:str):
    
    path = os.path.abspath(path)

    subprocess.Popen(f'explorer /select,"{path}"')
    return True