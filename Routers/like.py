from fastapi import APIRouter, status, Depends, HTTPException # type: ignore
from sqlalchemy.orm import Session # type: ignore

from ..oauth2 import get_current_user
from ..schema import likemodel
from ..database import get_db
from ..models import Post, Like

router = APIRouter(prefix="/likes", tags=["Like"])

@router.put("/", status_code=status.HTTP_200_OK)
def likeApost(like: likemodel, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == like.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    isLiked_query = db.query(Like).filter(Like.post_id == like.post_id, Like.user_id == current_user.id)
    isLiked = isLiked_query.first()

    if like.order > 0:
        if isLiked:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already liked this post")
        
        postLike = Like(post_id=like.post_id, user_id=current_user.id)
        db.add(postLike)
        db.commit()
        db.refresh(postLike)
        return {"message": "successfully liked the post"}
    else:
        if not isLiked:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have not liked this post")
        
        isLiked_query.delete(synchronize_session=False)
        db.commit()
