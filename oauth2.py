#this file is a scanner, it scans that token is valid or not

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic_settings import BaseSettings
from database import get_db
from sqlalchemy.orm import Session
import models

class Settings(BaseSettings):
    secret_key: str
    ALGORITHM: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #it extracts the token

def get_current_user(token:str = Depends(oauth2_scheme), db:Session=Depends(get_db)):  #we got token from Depends(oauth2_scheme)
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate Credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.ALGORITHM]) #used to decode that token with the
                                                                                          #help of secret_key
        user_id:str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if user is None:
        raise credentials_exception
        
    return user

 

