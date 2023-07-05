import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mount import Swagger
from apps.dev import dev
from apps.search import search
from apps.meta import meta


app = FastAPI(title='以图搜图对接 milvus 接口', debug=False,
              docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Swagger.doc(app)


@app.get('/')
async def root():
    return {"message": "Hello World"}


app.include_router(dev)
app.include_router(meta)
app.include_router(search)


if __name__ == "__main__":

    uvicorn.run(
        app='api:app',
        host="0.0.0.0",
        port=6200,
    )