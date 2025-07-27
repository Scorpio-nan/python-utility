
"""  fast-api 示例  """

from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os


origins = [
    "http://localhost",
    "http://localhost:5173",
]

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()
# 设置模板目录
templates = Jinja2Templates(directory="templates")
# 设置静态文件目录
app.mount(f'/{UPLOAD_DIR}', StaticFiles(directory=UPLOAD_DIR), name=UPLOAD_DIR)
# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # 保存文件
        with open(file_path, "wb") as buffer:
            # 分块读取文件，适合大文件上传
            while chunk := await file.read(1024 * 1024):  # 每次读取1MB
                buffer.write(chunk)
        return {
            'code': 200,
            'msg': '请求成功',
            'data': {
                "name": file.filename,
                "status": "success",
                "size": file.size,
                "url": f"http://localhost:8000/{file_path}",
                "thumbUrl": f"http://localhost:8000/{file_path}",
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,  # 必须包含
            "title": "登录页面",
            "content": "欢迎来到我的网站!"
        }
    )



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapi-server:app", host="0.0.0.0", port=8000, reload=True)