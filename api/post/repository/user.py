from sqlalchemy.orm import Session
from ..hashing import Hash
from .. import model
from fastapi import HTTPException, status




def create_user(request, db: Session):
    encrypt_password = Hash.encrypt(request.password)
    new_user = model.User(name = request.name, email = request.email, password = encrypt_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show_user(id: int, db: Session):
    user_data = db.query(model.User).filter(model.User.id == id).first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} not found//")
        return {"status": "No post with the ID found"}
    return user_data