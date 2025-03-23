from fastapi import APIRouter,Depends,HTTPException,status
from .. import database,schemas,models
from sqlalchemy.orm import Session
from ..hashing import Hash


router = APIRouter(prefix='/user',
                   tags=['Users'])

get_db = database.get_db





@router.post('/',response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session=Depends(get_db)):
    new_user = models.User(name = request.name,email=request.email,password = Hash.bcrypt(request.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.get('/{id}',response_model=schemas.ShowUser)
def show_user(id:int, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available.")
    return user


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db:Session=Depends(get_db)):

    user = db.query(models.User).filter(models.User.id==id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found")
    user.delete(synchronize_session=False)
    db.commit()
    return {'Destroyed'}