from fastapi import APIRouter
import json

router = APIRouter()

@router.get("/get_table")
def get_workArtices(tp:str):

    urls = {
        "artices_history":"services/json/history/artices_history.json",
        "work_artices":"services/json/read_text/work_artices.json"
    }

    with open(urls[tp],"r",encoding="utf-8") as f:
        data = json.load(f)

    print(data)

    return data
