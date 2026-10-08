from fastapi import APIRouter
import json

from services.get_database import get_article
from services.add_json import get_JsonData

spider = APIRouter()

@spider.get("/start_spider")
def start_spider(year:int,page_start:int,page_end:int,category:str):

    artices_type = {
        "周报":"weekly_reports",
        "游戏":"Game",
        "文章":"Artice"
    }
    print("开始爬取")
    pages = range(page_start,page_end+1)

    data = get_article(year,pages,artices_type[category])

    get_JsonData(data)

    return True
