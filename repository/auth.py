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
import os
import asyncio
os.environ["CUDA_VISIBLE_DEVICES"] = '-1'
os.environ["TF_ENABLE_ONEDNN_OPTS"] = '0'
import cv2
from deepface import DeepFace

backends = [
  'opencv', 
  'ssd', 
  'dlib', 
  'mtcnn', 
  'fastmtcnn',
  'retinaface', 
  'mediapipe',
  'yolov8',
  'yunet',
  'centerface',
]

alignment_modes = [True, False]
def resize_image(image_path, size=(224, 224)):
    img = cv2.imread(image_path)
    resized_img = cv2.resize(img, size)
    return resized_img

async def face(
    upload_file:UploadFile,
    user: User,
    db: Session,
):
    file_extension = os.path.splitext(upload_file.filename)[1]
    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    path = await upload_file_to_local(
            upload_file=upload_file, folder=LOCAL_PATH, path=f"/tmp/face-{user.name}{now.replace(' ','_')}{file_extension}"
        )

    loop = asyncio.get_running_loop()
    resized_img1 = await loop.run_in_executor(None, resize_image, f"{LOCAL_PATH}{path}")
    
    # Fetch the user's face image from MinIO
    
    user_face_bytes = download_file_to_bytes(user.face_id)
    user_face_path = f"{LOCAL_PATH}/tmp/{user.face_id.split('/')[-1]}"
    with open(user_face_path, "wb") as f:
        f.write(user_face_bytes)
    
    resized_img2 = await loop.run_in_executor(None, resize_image, user_face_path)
                                            
    # Face verification
    # Try multiple models and detection backends for more robust verification
    verification_results = []
    
    # Try different face recognition models
    models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "ArcFace"]
    for model in models[:2]:  # Using top 2 models for efficiency
        try:
            result = DeepFace.verify(
                img1_path=resized_img1,
                img2_path=resized_img2,
                model_name=model,
                detector_backend='retinaface',  # More accurate face detection
                align=True,  # Enable facial alignment
                enforce_detection=False,
                normalization='base',  # Apply normalization
                distance_metric='cosine'  # More reliable for face matching
            )
            verification_results.append(result['verified'])
        except Exception as e:
            print(f"Error with model {model}: {str(e)}")
    
    # Use majority voting for final decision
    obj = {'verified': sum(verification_results) > len(verification_results) // 2}
    
    # If no results were obtained, fall back to original method
    if not verification_results:
        obj = DeepFace.verify(
            img1_path=resized_img1, 
            img2_path=resized_img2, 
            detector_backend='retinaface',
            align=True,
            enforce_detection=False
        )
    delete_file_in_local(folder=LOCAL_PATH, path=path)
    os.remove(user_face_path)  # Clean up the temporary file
    return obj['verified']

async def face_dua(
    upload_file:UploadFile,
    upload_file_2:UploadFile,
    user: User,
    db: Session,
):
    file_extension = os.path.splitext(upload_file.filename)[1]
    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    path = await upload_file_to_local(
            upload_file=upload_file, folder=LOCAL_PATH, path=f"/tmp/face-{user.name}{now.replace(' ','_')}{file_extension}"
        )
    path2 = await upload_file_to_local(
            upload_file=upload_file_2, folder=LOCAL_PATH, path=f"/tmp/face-{user.name}{now.replace(' ','_')}{file_extension}"
        )

    loop = asyncio.get_running_loop()
    resized_img1 = await loop.run_in_executor(None, resize_image, f"{LOCAL_PATH}{path}")
    resized_img2 = await loop.run_in_executor(None, resize_image, f"{LOCAL_PATH}{path2}")
    
    # Fetch the user's face image from MinIO
    
    # user_face_bytes = download_file_to_bytes(user.face_id)
    # user_face_path = f"{LOCAL_PATH}/tmp/{user.face_id.split('/')[-1]}"
    # with open(user_face_path, "wb") as f:
    #     f.write(user_face_bytes)
    
    # resized_img2 = await loop.run_in_executor(None, resize_image, user_face_path)
                                            
    # Face verification
    # Try multiple models and detection backends for more robust verification
    verification_results = []
    
    # Try different face recognition models
    models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "ArcFace"]
    for model in models[:2]:  # Using top 2 models for efficiency
        try:
            result = DeepFace.verify(
                img1_path=resized_img1,
                img2_path=resized_img2,
                model_name=model,
                detector_backend='retinaface',  # More accurate face detection
                align=True,  # Enable facial alignment
                enforce_detection=False,
                normalization='base',  # Apply normalization
                distance_metric='cosine'  # More reliable for face matching
            )
            verification_results.append(result['verified'])
        except Exception as e:
            print(f"Error with model {model}: {str(e)}")
    
    # Use majority voting for final decision
    obj = {'verified': sum(verification_results) > len(verification_results) // 2}
    
    # If no results were obtained, fall back to original method
    if not verification_results:
        obj = DeepFace.verify(
            img1_path=resized_img1, 
            img2_path=resized_img2, 
            detector_backend='retinaface',
            align=True,
            enforce_detection=False
        )
    delete_file_in_local(folder=LOCAL_PATH, path=path)
    # os.remove(user_face_path)  # Clean up the temporary file
    os.remove(path)  # Clean up the temporary file
    os.remove(path2)  # Clean up the temporary file
    return obj['verified']


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
async def get_user_by_username(
    db: AsyncSession, username: str, exclude_soft_delete: bool = False
) -> Optional[User]:
    try:
        if exclude_soft_delete == True:
            pass
            # query = select(User).filter(func.lower(User.username) == username.lower(), User.deleted_at == None)
        else:
            # why there is delete_at and is_active
            query = select(User).filter(func.lower(User.username) == username.lower(), User.is_active == True)
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
    user = await get_user_by_email(db, email=email)
    if user == None:
        return False
    if validated_user_password(user.password, password):
        return user
    return False

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
