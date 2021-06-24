#!/usr/bin/python3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from datatypes import PostBodyBase
from storagemanager import StorageManager

app = FastAPI()
manager = StorageManager()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8890",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/set")
async def setItem(body: PostBodyBase):
    if body.type == 'category':
        return manager.addCategory(body.body)
    if body.type == 'item':
        return manager.addItem(body.body)

@app.post("/get")
async def getItem(body: PostBodyBase):
    if body.type == 'category':
        return manager.retrieveCategory()
    if body.type == 'item':
        return manager.retrieveItem(body.body['uuid'])
    if body.type == 'allitem':
        return manager.retrieveAllItems()