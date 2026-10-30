# 读取logging文件，并返回文本和读取位置给前端
from fastapi import APIRouter
import json

get_log = APIRouter()

@get_log.get("/get_log")
def get_logging(offset: int = 0):
    log_path = "services/logging.txt"
    datas = []
    
    import os
    if not os.path.exists(log_path):
        return []
    
    file_size = os.path.getsize(log_path)
    if offset > file_size:
        offset = 0
    
    with open(log_path, 'r', encoding='utf-8') as f:
        f.seek(offset)
        while True:
            line = f.readline()
            if not line:
                break
            clean_line = line.strip()
            if clean_line:  # 跳过空行
                new_offset = f.tell()
                datas.append({"content": clean_line, "new_offset": new_offset})
    
    return datas