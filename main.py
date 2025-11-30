from fastapi import FastAPI
from . import routers


app = FastAPI() 


app.include_router(routers.router)


if __name__ == "__maine__":
    import uvicorn
    uvicorn.run(app, host = '127.0.0.1', port = '8081')



    