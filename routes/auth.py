from email import utils
from fastapi import APIRouter, Depends, Request, BackgroundTasks, Request, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from models import get_db
from core.file import generate_link_download
from models.User import User
from core.security import (
    get_user_from_jwt_token,
)
from core.responses import (
    common_response,
    Ok,
    CudResponse,
    BadRequest,
    Unauthorized,
)
from core.security import (
    generate_jwt_token_from_user,
    oauth2_scheme,
)
from schemas.common import (
    BadRequestResponse,
    UnauthorizedResponse,
    InternalServerErrorResponse,
    CudResponschema,
)
from schemas.auth import (
    LoginSuccessResponse,
    PermissionsResponse,
    LoginRequest,
    CreateUserRequest,
    MeSuccessResponse,
    RegisRequest
)
# from core.file import generate_link_download
from repository import auth as authRepo

router = APIRouter(tags=["Auth"])
    

@router.post(
    "/face-temp",
        responses={
        "201": {"model": MeSuccessResponse},
        "400": {"model": BadRequestResponse},
        "401": {"model": UnauthorizedResponse},
        "500": {"model": InternalServerErrorResponse},
    },
)
async def face_temp(
    file: UploadFile = File(),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    try:
        user = get_user_from_jwt_token(db, token)
        if not user:
            return common_response(Unauthorized(message="Invalid/Expired token"))
        # file_extension = os.path.splitext(file.filename)[1]
        # file_name = os.path.splitext(file.filename)[0]
        # now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        # path = await upload_file(
        #     upload_file=file, path=f"/tmp/{str(file_name).replace(' ','_')}-{user.name}{now.replace(' ','_')}{file_extension}"
        # )
        data = await authRepo.send_file_to_endpoint(
            file_path=file,
            user_name=user.name,
            user_face_id=user.face_id,        )
        if not data:
            raise ValueError('Face not verified')
        return common_response(CudResponse(message="Verified"))
    except Exception as e:
        import traceback
        print("ERROR :",e)
        traceback.print_exc()
        return common_response(BadRequest(message=str(e)))

@router.post(
    "/face",
        responses={
        "201": {"model": MeSuccessResponse},
        "400": {"model": BadRequestResponse},
        "401": {"model": UnauthorizedResponse},
        "500": {"model": InternalServerErrorResponse},
    },
)
async def face(
    file: UploadFile = File(),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    try:
        user = get_user_from_jwt_token(db, token)
        if not user:
            return common_response(Unauthorized(message="Invalid/Expired token"))
        # file_extension = os.path.splitext(file.filename)[1]
        # file_name = os.path.splitext(file.filename)[0]
        # now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        # path = await upload_file(
        #     upload_file=file, path=f"/tmp/{str(file_name).replace(' ','_')}-{user.name}{now.replace(' ','_')}{file_extension}"
        # )
        data = await authRepo.face(
            db=db,
            user=user,
            upload_file=file,
        )
        if not data:
            raise ValueError('Face not verified')
        return common_response(CudResponse(message="Verified"))
    except Exception as e:
        import traceback
        print("ERROR :",e)
        traceback.print_exc()
        return common_response(BadRequest(message=str(e)))
    
@router.post(
    "/face_dua",
        responses={
        "201": {"model": MeSuccessResponse},
        "400": {"model": BadRequestResponse},
        "401": {"model": UnauthorizedResponse},
        "500": {"model": InternalServerErrorResponse},
    },
)
async def face(
    file: UploadFile = File(),
    file_2: UploadFile = File(),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    try:
        user = get_user_from_jwt_token(db, token)
        if not user:
            return common_response(Unauthorized(message="Invalid/Expired token"))
        # file_extension = os.path.splitext(file.filename)[1]
        # file_name = os.path.splitext(file.filename)[0]
        # now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        # path = await upload_file(
        #     upload_file=file, path=f"/tmp/{str(file_name).replace(' ','_')}-{user.name}{now.replace(' ','_')}{file_extension}"
        # )
        data = await authRepo.face_dua(
            db=db,
            user=user,
            upload_file=file,
            upload_file_2=file_2,
        )
        if not data:
            raise ValueError('Face not verified')
        return common_response(CudResponse(message="Verified"))
    except Exception as e:
        import traceback
        print("ERROR :",e)
        traceback.print_exc()
        return common_response(BadRequest(message=str(e)))

@router.post("/token")
async def generate_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    try:
        is_valid = await authRepo.check_user_password(
            db, form_data.username, form_data.password
        )
        if not is_valid:
            return common_response(BadRequest(error="Invalid Credentials"))
        user = is_valid
        token = await generate_jwt_token_from_user(user=user)
        await authRepo.create_user_session(db=db, user_id=user.id, token=token)
        return {"access_token": token, "token_type": "Bearer"}
    except Exception as e:
        return common_response(BadRequest(message=str(e)))