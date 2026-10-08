# 返回并储存文章数据（txt与json）
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pickle,asyncio,sqlite3,json,os,time


import sqlite3

def conn_cngal():

    conn = sqlite3.connect("database/cngal_database.db")
    conn.row_factory = sqlite3.Row

    return conn


cookie_file = 'services/cookies.pkl'
def cookies_is_expired():  # 检测cookie是否过期

    now_ts = time.time()                 # 当前时间戳（秒）
    now_minutes = now_ts / 60

    #遍历cookie文件对比最近的过期时间
    with open(cookie_file, 'rb') as f:
        datas = pickle.load(f)

    for data in datas:

        if len(str(data['expires'])) <= 10:
            continue

        ts = data['expires']
        ts_minutes = ts / 60

        if ts_minutes-now_minutes <= 2:  # 时间小于2min表示将要过期，重新获取

            return True

    return False

def save_cookies():  # 手动获取cookie

    url = 'https://www.cngal.org/search?Sort=PubulishTime%20desc'
    print("建立浏览器连接中...")
    #自动获取cookies,创建playwright实例,启动浏览器
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="msedge",
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        #创建窗口,对网址发起访问
        context = browser.new_context()
        page = context.new_page()
        page.goto(url,wait_until="domcontentloaded")
        print("建立连接成功，请手动完成人机验证...")

        # 等验证通过
        page.wait_for_selector(".search-page__search-bar", timeout=120000)
        print("验证成功，保存cookie中...")

        #获取该窗口的cookies值并序列化存储到硬盘
        cookies = context.cookies()
        with open(cookie_file,'wb') as f:
            pickle.dump(cookies,f)
        print(f"已保存 {len(cookies)} 个 cookie") 

        browser.close()

    return True  

def get_weekly_reports_urls(user_pages,year):  # 获取爬取的周报路径列表

    print("开始获取请求地址列表...")
    json_path = "services/json/plugin/website_page.json"
    urls = []

    with open(json_path,"r",encoding="utf-8") as f:  # 打开json文件
        url_data = json.load(f)  # 获取json数据

    print("正在建立数据库连接...")
    with conn_cngal() as conn:  # 建立数据库连接

        print("正在查询重复数据...")
        imes_start = url_data[str(year)]["imes_start"]  # 通过json数据获取url起始id
        imes_end = url_data[str(year)]["imes_end"]  # 通过json数据获取url结束id

        page_nums = []  # 储存已查询过的页面id
        cursor = conn.cursor()  # 创建游标
        cursor.execute("SELECT page_id FROM artices_history WHERE year = ? AND type = ?",[str(year),"weekly_reports"])  # 塞入查询语句
        results = cursor.fetchall()  # 获取查询结果（返回字典数据）

        for row in results:  # 遍历查询到的page_history表的page_id，获取已查询过的页面id
            page_num = int(row[0].replace(str(year),"0"))  # 去掉page_id中的年份和0的部分，得到已查询过的页码
            page_nums.append(page_num)  # 把page_id储存起来

        for user_page in user_pages:  # 遍历用户选择的页码范围
            if user_page in page_nums:  #用户选择的id在已储存的page_id内 
                continue  # 跳过
            url = f"https://www.cngal.org/search?Text=cngal%E6%AF%8F%E5%91%A8%E9%80%9F%E6%8A%A5&Sort=PubulishTime%20desc&Times={imes_start}-{imes_end}&Page={user_page}"  # 生成用户选择过且没有查询过的路径
            urls.append(url)  # 储存url到列表
    print("请求地址列表获取完成")
    return urls

def get_reports_urls(reports_type,year,user_pages):  # 获取爬取的文章路径列表

    print("开始获取请求地址列表...")
    urls = []
    print("正在建立数据库连接...")
    with conn_cngal() as conn:  # 建立数据库连接

        print("正在查询重复数据...")

        page_nums = []  # 储存已查询过的页面id
        cursor = conn.cursor()  # 创建游标
        cursor.execute("SELECT page_id FROM artices_history WHERE year = ? AND type = ?",[str(year),str(reports_type)])  # 塞入查询语句
        results = cursor.fetchall()  # 获取查询结果（返回字典数据）

        for row in results:  # 遍历查询到的表的page_id，获取已查询过的页面id
            page_num = int(row[0].replace(str(year),"0"))  # 去掉page_id中的年份和0的部分，得到已查询过的页码
            page_nums.append(page_num)  # 把page_id储存起来

        for user_page in user_pages:  # 遍历用户选择的页码范围
            
            if user_page in page_nums:  #用户选择的id在已储存的page_id内 
                continue  # 跳过
            
            url = f"https://www.cngal.org/search?Sort=PubulishTime%20desc&Types={reports_type}&Page={user_page}"
            urls.append(url)

    print("请求地址列表获取完成")
    return urls

async def get_html(year,context,url,reports_type):  # 访问并生成该页面html文件，返回文件路径和页码id

    page = await context.new_page()  # 创建page
    try:

        user_page = url.split("Page=")[1]  # 获取此次爬取页码
        page_id = f"{year}{int(user_page):03d}"  # 生成该页码page_id

        print(f"正在访问{year}年第{user_page}页...")
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)  # 访问url
        await page.wait_for_timeout(1000)  # 访问后暂停1s

        html_content = await page.content()  # 储存页码代码

        print(f"访问成功，正在保存{year}年第{user_page}页html文件...")
        page_path = f"services/html_contents/{reports_type}/{page_id}.html"  # 生成该页码生成的html文件路径

        with open(page_path,"w",encoding="utf-8") as f:  # 根据文件路径创建文件
            f.write(html_content)  # 填入该页面html

        print(f"{year}年第{user_page}页html文件保存完毕，保存路径：{page_path}")

    finally:
        await page.close()  # 关闭连接

    return [year,page_id,page_path,reports_type]
              
async def main(year,urls,reprots_type):  # 创建加入了cookies的连接并调用get_html()
    print("建立浏览器连接中...")
    async with async_playwright() as p:  # 创建异步playwright实例
        browser = await p.chromium.launch(  # 创建请求方式
            channel="msedge",
            headless=True,  # 创建请求头
            args=['--disable-blink-features=AutomationControlled']
        )
        context = await browser.new_context()  # 创建请求

        with open(cookie_file,'rb') as f:  # 打开cookies文件
            cookies = pickle.load(f)  # 储存文件中的cookies内容
        await context.add_cookies(cookies)  # 为请求添加cookies
        print("开始获取页面html数据")
        tasks = [get_html(year,context,url,reprots_type) for url in urls]  # 创建任务
        pages = await asyncio.gather(*tasks)  # 让小人去一起做事情

        await browser.close()

    return pages

def analysis_html(path):  #解析html代码

    reports_data = []  # 储存周报信息：名称，正文路径，文章网址
    page_isdone = []  # 储存该页码解析结果

    page_id = path.replace("services/html_contents/","").replace(".html","")
    print(f"正在解析{page_id}...")
    with open(path,"r",encoding="utf-8") as f:  # 打开该文件
        content = f.read()  # 获取文件内文本
        
    soup = BeautifulSoup(content,'html.parser')  # 解析文本为html代码
    print(f"解析成功，正在查找{page_id}内含标题与正文...")
    main = soup.find('main')  # 寻找main标签
    notices = main.find_all('div',class_='search-page__results')  # 找到周报的div
    for notice in notices:

        a_tags = notice.find_all('a')

        for a in a_tags:
                
            title = a.find(class_='search-result-card__title').text  # 周报标题
                
            link_data = a.get('href')  # 网站url分区路径
            link = "https://www.cngal.org" + link_data  # 网站url
            num = link_data.strip('/articles/index/')  # 文章号

            main_text = a.find_all(class_='search-result-card__brief')
            text_content = '\n\n'.join([p.get_text() for p in main_text])  # 正文内容
            path = f"services/text_file/reports{num}.txt"  # 创建正文文件路径
            print(f"查找《{title}》标题与正文成功，正在创建正文文件...")
            with open(path,"w",encoding="utf-8") as f:  # 创建正文文件
                f.write(text_content)
            print(f"创建《{title}》正文文件成功，文件路径：{path}")
            report_data = {"title" : title,"maintext_path" : path,"url" : link}
            reports_data.append(report_data)


    return reports_data

def get_article(year,pages,category):  # 储存文章数据到数据库|储存临时jsonl数据到jsonl文件|保存文章正文txt文件
    
    # 检测cookie是否存在与是否过期

    if not os.path.exists(cookie_file):
        print("首次启动，获取cookie文件中...")
        save_cookies()

    if cookies_is_expired():
        print("cookie即将过期，重新获取中...")
        save_cookies()
    else:
        print("cookie未过期，准备就绪")

    # 获取url列表

    if category == "weekly_reports":

        urls = get_weekly_reports_urls(user_pages=pages,year=year)

    else:

        urls = get_reports_urls(category,year,pages)

    # 获取html文件

    pages = asyncio.run(main(year,urls,category))

    # 解析html文件

    print("正在准备解析html文件")

    artices_history = []  # 储存历史查询页面
    artices = []  # 储存文章信息

    for page in pages:

        reports_data = analysis_html(page[2])
        for report_data in reports_data:  # 创建文章信息表的数据
            
            artice = {"title":report_data["title"],"maintext_path":report_data["maintext_path"],"url":report_data["url"],"type":page[3]}
            artices.append(artice)

        page.append("is_done")

        artice_history = {"year":page[0],"page_id":page[1],"page_html_path":page[2],"is_done":"True","type":page[3]}  # 创建历史查询表的数据
        artices_history.append(artice_history)

 

    print("全部解析完成，准备传输数据")

    return artices_history,artices
