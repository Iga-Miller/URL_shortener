from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.tasks import shorten_url_task
from app.db import get_db, URLMapping

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class URLItem(BaseModel):
    url: str

@app.get("/home")
async def read_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/u/{short_url}")
async def redirect_to_url(short_url: str, db: Session = Depends(get_db)):
    print(f"Szukam skróconego URL-a: {short_url}")  
    db_url_mapping = db.query(URLMapping).filter(URLMapping.short_url == short_url).first()

    if not db_url_mapping:
        print(f"Nie znaleziono URL-a: {short_url}")  
        raise HTTPException(status_code=404, detail="URL not found")

    print(f"Przekierowanie na: {db_url_mapping.original_url}")  
    return RedirectResponse(url=db_url_mapping.original_url, status_code=307)


@app.post("/shorten")
async def shorten_url(url_item: URLItem):
    original_url = url_item.url
    if not is_valid_url(original_url):
        raise HTTPException(status_code=400, detail="Invalid URL")
    task = shorten_url_task.delay(original_url)
    return {"task_id": task.id, "status": "Processing"}


def is_valid_url(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://")


@app.get("/task_status/{task_id}")
async def get_task_status(task_id: str):
    task = shorten_url_task.AsyncResult(task_id)
    if task.state == 'SUCCESS':
        return {"status": task.state, "result": task.result}
    return {"status": task.state}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
