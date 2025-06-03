from fastapi import FastAPI
from db import Base, engine
from routers import CategoryRouter, SetRouter, TagRouter

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(CategoryRouter)
app.include_router(TagRouter)
app.include_router(SetRouter)
