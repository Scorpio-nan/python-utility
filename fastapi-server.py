
"""  fast-api 示例  """

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os


origins = [
    "http://localhost",
    "http://localhost:5173",
]

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)