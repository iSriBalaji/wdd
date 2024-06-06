from .. import model
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends



def create_post(request, db: Session):
    new_post = model.Post(title = request.title, post = request.post, user_id = 1)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def see_all_post(db: Session):
    posts = db.query(model.Post).all()
    return posts

def see_post(id: int, db: Session):
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog Post of {id} is not present in the db")
    return post

def remove_post(id:int, db: Session):
    post = db.query(model.Post).filter(model.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"No Post with {id} found")
        return {"status": "No post with the ID found"}
    post.delete(synchronize_session=False)
    db.commit()
    return {"status": f"Post({id}) has been deleted"}

def update_post(id:int, request, db: Session):
    post = db.query(model.Post).filter(model.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"No Post with {id} found")
        return {"status": "No post with the ID found"}
    # update_data = request.dict(exclude_unset=True)
    # for key, value in update_data.items():
    #     setattr(post, key, value)
    post.update({
    "id": id,
    "title": request.title,
    "post": request.post
    })
    db.commit()
    return {"status": f"Post({id}) has been updated {request}"}