from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models,hashing
from sqlalchemy.orm import Session
from . database import engine, SessionLocal
from typing import List
from .hashing import Hash


app =FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/blog',status_code= status.HTTP_200_OK, response_model=List[schemas.ShowBlog],tags=['Blogs'])
def all(db: Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog,tags=['Blogs'])
def show_blog(id:int, reponse:Response, db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"Blog with id {id} is not available")
    else:
        return blog

@app.post('/blog',status_code=status.HTTP_201_CREATED,tags=['Blogs'])
def create(request:schemas.Blog, db: Session=Depends(get_db)):

    new_blog = models.Blog(title=request.title, body= request.body,user_id=1)

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT,tags=['Blogs'])
def destroy(id, db: Session=Depends(get_db)):

    blog =db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    
    blog.delete(synchronize_session=False)
    db.commit()
    return {'Destroyed'}

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=['Blogs'])
def update(id:int, request:schemas.Blog, db: Session= Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    blog.update(request.model_dump())
    db.commit()
    return "Blog details updated"


@app.post('/user',response_model=schemas.ShowUser,tags=['Users'])
def create_user(request: schemas.User, db: Session=Depends(get_db)):
    new_user = models.User(name = request.name,email=request.email,password = Hash.bcrypt(request.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@app.get('/user/{id}',response_model=schemas.ShowUser,tags=['Users'])
def show_user(id:int, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available.")
    return user


@app.delete('/user/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['Users'])
def destroy(id:int, db:Session=Depends(get_db)):

    user = db.query(models.User).filter(models.User.id==id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found")
    user.delete(synchronize_session=False)
    db.commit()
    return {'Destroyed'}