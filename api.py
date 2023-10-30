import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mount import Swagger
from apps.dev import dev
from apps.sample import sample
from apps.meta import meta
import settings

description = """
这个系统的逻辑是，把图片转成向量，512 维度的向量，512 个  float，一个 float 4字节

所以一个图片生成后的向量是 2048字节

存储在向量数据库里面，向量数据库是内存数据库，等于一个图片要占用 2048 字节

----


生成向量的效率：单核每秒生成5个向量
检索向量的效率：取决于母本量
"""

app = FastAPI(
    title='「以图搜图」接口',
    debug=settings.API_CONFIG.debug,
    docs_url=None,
    redoc_url=None,
    version=settings.API_CONFIG.version,
    description=description
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Swagger.doc(app)


@app.get('/')
def root():
    return {"message": "Hello World"}


app.include_router(dev)
app.include_router(meta)
app.include_router(sample)


if __name__ == "__main__":

    uvicorn.run(
        app='api:app',
        host="0.0.0.0",
        port=settings.API_CONFIG.bind_port,
        reload=settings.API_CONFIG.reload,
        workers=settings.API_CONFIG.workers_num
    )
