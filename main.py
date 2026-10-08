from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
# 引入需要注册路由的实例
from api.table_text import router
from api.start_spider import spider


app = FastAPI()

app.include_router(router)
app.include_router(spider)

app.mount("/js",StaticFiles(directory='frontend/js'),name='js')
app.mount("/img",StaticFiles(directory='frontend/img'),name='img')
app.mount("/plugin",StaticFiles(directory='frontend/plugin'),name='plugin')
@app.get("/")
def index():
    return FileResponse("frontend/index.html")

@app.get("/style.css")
def style():
    return FileResponse("frontend/style.css")

@app.get("/favicon.ico")
def favicon():
    return FileResponse("frontend/favicon.ico")

