from fastapi import APIRouter, status, Depends, HTTPException, Response # type: ignore
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import func, desc # type: ignore
from typing import List, Optional

from ..schema import getPost, createPost, updatePost, getPostWithLikes
from ..oauth2 import get_current_user
from ..database import get_db
from ..models import Post, User, Like

router = APIRouter(prefix="/posts", tags=["Post"])

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[getPostWithLikes])
def getAllPost(db: Session = Depends(get_db), Title: Optional[str] = "", limit: int = 10, skip: int = 0):
    posts = db.query(Post, func.count(Like.post_id).label("likes"), User.name).join(Like, Like.post_id == Post.id, isouter=True).join(User, User.id == Post.user_id).group_by(Post.id, User.name).filter(Post.title.contains(Title)).order_by(desc(Post.created_at)).limit(limit).offset(skip).all()
    return [getPostWithLikes(**post.__dict__, likes=like, user=name) for post, like, name in posts]

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=getPostWithLikes)
def getApost(id: int, db: Session = Depends(get_db)):
    post = db.query(Post, func.count(Like.post_id).label("likes"), User.name).join(Like, Like.post_id == Post.id, isouter=True).join(User, User.id == Post.user_id).filter(Post.id == id).group_by(Post.id, User.name).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    postData, like, user = post
    return getPostWithLikes(id=postData.id, title=postData.title, content=postData.content, published=postData.published, created_at=postData.created_at, likes=like, user=user)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=getPost)
def createPost(post: createPost, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    new_post = Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=getPost)
def updatePost(post: updatePost, id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    existing_post_query = db.query(Post).filter(Post.id == id)
    existing_post = existing_post_query.first()

    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if existing_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    existing_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return existing_post_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
