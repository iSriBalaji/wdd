from fastapi import FastAPI, Depends, status, Response, HTTPException
from post.schema import Post, ShowPost, User, ShowUser
from post import model
from post.database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from typing import List
from post.hashing import Hash
from .routers import user, post, auth

app = FastAPI()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# we are creating all the database tables in the sqllite when there is no table in it
model.Base.metadata.create_all(engine)

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)

# # @app.post("/create", status_code=201)
# # we can import status and put the status code directly here like this(below)
# @app.post("/create", status_code=status.HTTP_201_CREATED, tags=['post'])
# def create(request: Post, db: Session = Depends(get_db)):
#     new_post = model.Post(title = request.title, post = request.post, user_id = 1)
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post

# @app.get("/see", status_code=status.HTTP_200_OK, response_model= List[ShowPost], tags=['post'])
# def select(db: Session = Depends(get_db)):
#     posts = db.query(model.Post).all()
#     return posts

# @app.get("/post/{id}", status_code=status.HTTP_200_OK, response_model= ShowPost, tags=['post'])
# def specific_post(id, response = Response, db: Session = Depends(get_db)):
#     post = db.query(model.Post).filter(model.Post.id == id).first()
#     if not post:
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog Post of {id} is not present in the db")
#     return post

# @app.delete('/post/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['post'])
# def remove_post(id, db: Session = Depends(get_db)):
#     post = db.query(model.Post).filter(model.Post.id == id)
#     if not post.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"No Post with {id} found")
#         return {"status": "No post with the ID found"}
#     post.delete(synchronize_session=False)
#     db.commit()
#     return {"status": f"Post({id}) has been deleted"}

# @app.put('/post/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['post'])
# def update_post(id, request: Post, db: Session = Depends(get_db)):
#     post = db.query(model.Post).filter(model.Post.id == id)
#     if not post.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"No Post with {id} found")
#         return {"status": "No post with the ID found"}
#     # update_data = request.dict(exclude_unset=True)
#     # for key, value in update_data.items():
#     #     setattr(post, key, value)
#     post.update({
#     "id": id,
#     "title": request.title,
#     "post": request.post
#     })
#     db.commit()
#     return {"status": f"Post({id}) has been updated {request}"}

# @app.post('/user', status_code=status.HTTP_201_CREATED, response_model=ShowUser, tags=['user'])
# def create_user(request: User, db: Session = Depends(get_db)):
#     encrypt_password = Hash.encrypt(request.password)
#     new_user = model.User(name = request.name, email = request.email, password = encrypt_password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# @app.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=ShowUser, tags=['user'])
# def show_user(id, db: Session = Depends(get_db)):
#     user_data = db.query(model.User).filter(model.User.id == id).first()
#     if not user_data:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} not found//")
#         return {"status": "No post with the ID found"}
#     return user_data