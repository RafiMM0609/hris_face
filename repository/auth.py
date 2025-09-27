import traceback
from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from core.security import validated_user_password, generate_hash_password
from core.utils import generate_token
from core.file import upload_file_to_local, delete_file_in_local, download_file_to_bytes
from core.mail import send_reset_password_email
from models.User import User
from models.ForgotPassword import ForgotPassword
from models.UserToken import UserToken
from datetime import datetime, timedelta
from pytz import timezone
from settings import TZ, LOCAL_PATH
from fastapi import UploadFile
import numpy
import os
import asyncio
import httpx

async def send_uploadfile_to_endpoint(upload_file, user_id):
    try:
        url = f"http://85.31.233.176:8003/face/{user_id}"
        ext = os.path.splitext(upload_file.filename)[1].lower()
        if ext == ".png":
            content_type = "image/png"
        else:
            content_type = "image/jpeg"
        file_bytes = await upload_file.read()
        files = {"file": (upload_file.filename, file_bytes, content_type)}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                files=files,
                timeout=15  # Set timeout to 20 seconds
            )
            print(f"Response status code: {response.status_code}")
            print(f"Response text: {response.text}")
            response.raise_for_status()
            return response.json()
    # except httpx.ConnectTimeout:
    #     print("Connection timed out. Please check the server status.")
    #     return {'status': True}
    except httpx.HTTPError as e:
        print(f"Error Call Face Service: {e}")
        traceback.print_exc()
        # return {"error": str(e)}
        return {'status': True}


async def check_user_status_by_email(
    db: AsyncSession,
    email: str
) -> Optional[User]:

    query = select(User).filter(
                func.lower(User.email) == email.lower(),
                User.is_active == True
            )

    user = db.execute(query).scalar()
    return user


async def get_user_by_email(
    db: AsyncSession, email: str, exclude_soft_delete: bool = False
) -> Optional[User]:
    try:
        if exclude_soft_delete == True:
            pass
            # query = select(User).filter(func.lower(User.email) == email.lower(), User.deleted_at == None)
        else:
            # why there is delete_at and is_active
            query = select(User).filter(func.lower(User.email) == email.lower(), User.isact == True)
        user = db.execute(query).scalar()
        return user
    except Exception as e:
        print(e)
        return None
    
async def delete_user_session(db: AsyncSession, user_id: str, token=str) -> str:
    try:    
        user_token = db.execute(
            select(UserToken).filter(
                UserToken.user_id == user_id,
                UserToken.token == token
            )
        ).scalar()
        user_token.is_active = False
        db.add(user_token)
        db.commit()
        return 'succes'
    except Exception as e:
        print(f"Error delete user session: {e}")
        raise ValueError(e)
    
async def create_user_session(db: AsyncSession, user_id: str, token:str) -> str:
    try:
        exist_data = db.execute(
            select(UserToken).filter(
                UserToken.user_id == user_id,
                UserToken.token == token
            )
        ).scalar()
        if exist_data is not None:
            exist_data.is_active = True
            db.add(exist_data)
            db.commit()
        else:
            user_token = UserToken(user_id=user_id, token=token)
            db.add(user_token)
            db.commit()
        return 'succes'
    except Exception as e:
        print(f"Error creating user session: {e}")
async def create_user_session_me(db: AsyncSession, user_id: str, token:str, old_token:str) -> str:
    try:
        # old_token = db.execute(
        #     select(UserToken).filter(
        #         UserToken.token == old_token,
        #         UserToken.user_id == user_id
        #     )
        # ).scalar()
        # old_token.is_active = False
        exist_data = db.execute(
            select(UserToken).filter(
                UserToken.user_id == user_id,
                UserToken.token == token
            )
        ).scalar()
        if exist_data is not None:
            exist_data.is_active = True
            db.add(exist_data)
            db.commit()
        else:
            user_token = UserToken(user_id=user_id, token=token)
            db.add(user_token)
            db.commit()
        return 'succes'
    except Exception as e:
        print(f"Error creating user session: {e}")

async def check_user_password(db: AsyncSession, email: str, password: str) -> Optional[User]:
    status = False
    user = await get_user_by_email(db, email=email)
    if user == None:
        return False
    if user.first_login:
        print(f"first_login: {user.first_login}")
        print(f"password: {password}")
        status = user.first_login == password
    else:
        if validated_user_password(user.password, password):
            return user
    print(f"status: {status}")
    if status:
        return user
    else:
        return None
    # return False

async def change_user_password(db: AsyncSession, user: User, new_password: str) -> None:
    user.password = generate_hash_password(password=new_password)
    db.add(user)
    db.commit()


async def generate_token_forgot_password(db: AsyncSession, user: User) -> str:
    """
    generate token -> save user and token to database -> return generated token
    """
    token = generate_token()
    forgot_password = ForgotPassword(user=user, token=token, created_date = datetime.now(tz=timezone(TZ)))
    db.add(forgot_password)
    db.commit()
    return token
