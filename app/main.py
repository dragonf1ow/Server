from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
import os
import uvicorn
app = FastAPI()
templates = Jinja2Templates(directory="templates")


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    files = os.listdir(UPLOAD_FOLDER)
    return templates.TemplateResponse("index1.html", {"request": request, "files": files})


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        return RedirectResponse("/", status_code=303)
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    return RedirectResponse("/", status_code=303)

@app.get("/download/{filename}", response_class=FileResponse)
async def download(filename: str):
    return FileResponse(path=f"C:/Users/dragonflow/Work/server/uploads/{filename}")


@app.get("/delete/{filename}")
async def delete_file(filename: str):
    file_path = UPLOAD_FOLDER + f"/{filename}"
    try:
        os.remove(path=file_path)
    except:
        return RedirectResponse("/", status_code=404) 
        
    return RedirectResponse("/", status_code=303)   


if __name__ == "__main__":
    uvicorn.run(host="localhost", port=8000)
    