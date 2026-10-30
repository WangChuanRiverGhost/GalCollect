from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
# 引入需要注册路由的实例
from api.table_text import router
from api.start_spider import spider
from api.get_reportsTEXT import get_text
from api.get_log import get_log
from api.sql import sql
import os
import sys


if getattr(sys, 'frozen', False):  # 如果是打包后的 exe 运行，强制把工作目录切换到 exe 所在的文件夹
    os.chdir(os.path.dirname(sys.executable))

app = FastAPI()

app.include_router(router)
app.include_router(spider)
app.include_router(get_text)
app.include_router(get_log)
app.include_router(sql)

app.mount("/js",StaticFiles(directory='frontend/js'),name='js')
app.mount("/img",StaticFiles(directory='frontend/img'),name='img')
app.mount("/plugin",StaticFiles(directory='frontend/plugin'),name='plugin')
@app.get("/frontend/select_history.html")
def select_history():
    return FileResponse("frontend/select_history.html")
@app.get("/")
def index():
    return FileResponse("frontend/index.html")

@app.get("/style.css")
def style():
    return FileResponse("frontend/style.css")

@app.get("/favicon.ico")
def favicon():
    return FileResponse("frontend/favicon.ico")

