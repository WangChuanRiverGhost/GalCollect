# 读取文章正文文件的api
from fastapi import APIRouter
import json


get_text = APIRouter()

@get_text.get("/get_maintext")
def get_reportstext(path:str):
    
    with open(path,"r",encoding="utf-8") as f:
        data = f.read()

    return data