from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


#instance of fast API 
app = FastAPI()


@app.get('/blog')
def index(limit:int=10,published:bool=True,sort:Optional[str]=None):
    if published:
        return {'data':f'{limit} published blogs from the db.'}
    else:
        return {'data': f"{limit} blogs from the db."}

@app.get('/blog/unpublished')
def unpublished(id:int):
    return {f'data':"All unpublished records."}

@app.get('/blog/{id}')
def show(id:int):
    #fetch blog with id = id
    return {'data':id}

@app.get('/blog/{id}/comments')
def comments(id):
    #fetch comments of blog with id = id 
    return {'data':{'1','2'}}


class Blog(BaseModel):
    title:str
    body:str
    published: Optional[bool]

@app.post('/blog')
def create_blog(request:Blog):

    return {'data': f"blog is created with title as {request.title}"}