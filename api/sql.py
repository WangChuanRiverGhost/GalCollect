from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import datetime
import sqlite3


log_path = "services/logging.txt"
def write_log(message):
    time_only = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"【{time_only}】{message}\n")
def get_db():

    conn = sqlite3.connect("database/cngal_database.db")
    conn.row_factory = sqlite3.Row

    return conn
sql = APIRouter()

# 类别映射：前端中文 → 数据库 report_type 值
artices_type = {
    "周报": "weekly_reports",
    "游戏": "Game",
    "文章": "Artice",
}


class Row(BaseModel):
    dbtype: str = ""
    year: str = ""
    month_start: str = ""
    month_end: str = ""


@sql.post("/select_history")
def select_db(data: List[Row]):
    write_log("正在准备查询数据库...")
    if not data:
        return []

    or_parts = []      # 每个元素形如 "(a = ? AND b = ?)"
    params = []        # 对应占位符的值

    for cond in data:
        sub = []

        # 1. 类别
        dbtype_cn = (cond.dbtype or "").strip()
        if dbtype_cn:
            report_type = artices_type.get(dbtype_cn)
            if report_type:
                sub.append("report_type = ?")
                params.append(report_type)

        # 2. 年份
        year = (cond.year or "").strip()
        if year:
            sub.append("report_createYear = ?")
            params.append(year)

        # 3. 起始月份
        ms = (cond.month_start or "").strip()
        if ms:
            sub.append("CAST(report_createMonth AS INTEGER) >= ?")
            params.append(int(ms))

        # 4. 结束月份
        me = (cond.month_end or "").strip()
        if me:
            sub.append("CAST(report_createMonth AS INTEGER) <= ?")
            params.append(int(me))

        # 这一条至少有一个字段才加进 OR
        if sub:
            or_parts.append("(" + " AND ".join(sub) + ")")
    write_log("正在生成sql语句")
    # 所有条件都空 → 返回空
    if not or_parts:
        return []

    where_sql = "WHERE " + " OR ".join(or_parts)

    query = f"""
        SELECT DISTINCT title, report_type, report_url,
               report_mainTextPath, report_createYear, report_createMonth,report_createDay
        FROM work_artices
        {where_sql}
        ORDER BY report_createYear DESC,
                 CAST(report_createMonth AS INTEGER) DESC
    """
    write_log("正在连接数据库...")
    conn = get_db()
    cursor = conn.cursor()
    write_log("连接数据库成功，开始查询")
    cursor.execute(query, params)
    rows = cursor.fetchall()

    results = []
    for row in rows:
        # 如果是 sqlite3.Row，可以用 row["字段名"]；
        # 如果是普通 tuple，用 row[0]、row[1]...
        results.append({
            "title": row["title"],
            "type": row["report_type"],
            "url": row["report_url"],
            "maintext_path": row["report_mainTextPath"],
            "create_time": f"{row['report_createYear']}-{row['report_createMonth']}-{row['report_createDay']}"
        })
    write_log("查询结束，关闭数据库")
    cursor.close()
    conn.close()

    return results