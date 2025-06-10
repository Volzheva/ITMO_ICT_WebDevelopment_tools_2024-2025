from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from task2.parser import save_sync, scrape_html

app = FastAPI()



class HTMLRequest(BaseModel):
    html: str


@app.post('/parse')
def parse_and_save(request: HTMLRequest):
    try:
        data = scrape_html(request.html)
        save_sync(request.html)
        return {"message": "Parsed successfully","data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
