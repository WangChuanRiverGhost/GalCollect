import uvicorn
import webbrowser
import threading
import time
import os
import sys

# 1. 在这里导入你的 FastAPI 实例
from main import app  

def open_browser():
    time.sleep(3)
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.dirname(sys.executable))
    
    print("正在启动服务，请勿关闭此窗口...")
    threading.Thread(target=open_browser).start()
    
    # 2. 将 "main:app" 改成直接传入 app 对象
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8000, 
        reload=False,
        use_colors=False
    )