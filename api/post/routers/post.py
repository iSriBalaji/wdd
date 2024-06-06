from typing import List
from fastapi import APIRouter, FastAPI, Request, Response, Depends, status, HTTPException
from ..schema import ShowPost, ShowUser, User, Post, PostBase
from sqlalchemy.orm import Session
from ..database import get_db
from ..hashing import Hash
from .. import model
from ..repository import post
from ..oauth2 import get_current_user

router = APIRouter(
    tags=['Post'],
    prefix='/post'
)

# @app.post("/create", status_code=201)
# we can import status and put the status code directly here like this(below)
@router.post("/create", status_code=status.HTTP_201_CREATED)
def create(request: Post, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # new_post = model.Post(title = request.title, post = request.post, user_id = 1)
    # db.add(new_post)
    # db.commit()
    # db.refresh(new_post)
    # return new_post
    return post.create_post(request, db)

@router.get("/see", status_code=status.HTTP_200_OK, response_model= List[ShowPost])
def select(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # posts = db.query(model.Post).all()
    # return posts
    return post.see_all_post(db)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model= ShowPost)
def specific_post(id: int, response = Response, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # post = db.query(model.Post).filter(model.Post.id == id).first()
    # if not post:
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog Post of {id} is not present in the db")
    # return post
    return post.see_post(id, db)

@router.delete('/{id}', status_code=status.HTTP_202_ACCEPTED)
def remove_post(id:int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # post = db.query(model.Post).filter(model.Post.id == id)
    # if not post.first():
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"No Post with {id} found")
    #     return {"status": "No post with the ID found"}
    # post.delete(synchronize_session=False)
    # db.commit()
    # return {"status": f"Post({id}) has been deleted"}
    return post.remove_post(id, db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, request: Post, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return post.update_post(id, request, db)