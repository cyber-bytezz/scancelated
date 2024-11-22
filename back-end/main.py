from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth_controller
import uvicorn


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)


app.include_router(auth_controller.router, prefix="/api/v1")

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
