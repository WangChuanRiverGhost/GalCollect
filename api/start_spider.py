# 传入爬取数据的条件并调用爬虫脚本，并将数据保存至json文件和正文文件
from fastapi import APIRouter
import json

from services.get_database import get_article
from services.add_json import get_JsonData
from services.add_database import add_sql

spider = APIRouter()

@spider.get("/start_spider")
def start_spider(year:int,page_start:int,page_end:int,category:str):

    artices_type = {
        "周报":"weekly_reports",
        "游戏":"Game",
        "文章":"Artice",
        "词条":"Entry",
        "角色":"Role",
        "组织":"ProductionGroup",
        "Staff":"Staff",
        "感想":"Tought",
        "攻略":"Strategy",
        "访谈":"Interview",
        "动态":"News",
        "评测":"Evaluation",
        "周边文章":"PeripheralArticle",
        "公告":"Notice",
        "杂谈":"OtherArticle",
        "二创":"Fan",
        "标签":"Tag",
        "视频":"Video",
        "周边":"Periphery",
        "设定集":"SetorAlbumEtc",
        "原声集":"Ost",
        "套装":"Set",
        "其他周边":"OtherPeriphery"
    }
    print("开始爬取")
    pages = range(page_start,page_end+1)

    data = get_article(year,pages,artices_type[category])

    get_JsonData(data)

    return True

@spider.get("/add_sql")
def add_db():
    add_sql()
    return True


