from fastapi import FastAPI
from db import Base, engine
from routers import CategoryRouter, SetRouter, TagRouter
from jwt_token import TokenRouter

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(TokenRouter)
app.include_router(CategoryRouter)
app.include_router(TagRouter)
app.include_router(SetRouter)
