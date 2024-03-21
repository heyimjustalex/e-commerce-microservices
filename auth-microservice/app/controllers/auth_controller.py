from fastapi import APIRouter, Depends, status, Response
from app.schemas.schemas import UserCreateRequest, UserRegisterResponse, UserLoginRequest, UserLoginResponse
from app.services.user_service import UserService
from app.services.token_service import TokenService
from app.models.models import User
from app.dependencies.dependencies import get_user_service, get_token_service

router = APIRouter(
    prefix='/api/auth',
    tags=['auth']
)

@router.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserCreateRequest, service:UserService = Depends(get_user_service)):   
    user:User = service.create_user(data,"user")
    return UserRegisterResponse(email=user.email, role=user.role)

@router.post("/login",response_model=UserLoginResponse, status_code=status.HTTP_200_OK)
def login(data:UserLoginRequest, response: Response, user_service:UserService = Depends(get_user_service), token_service:TokenService = Depends(get_token_service)):
     user:User = user_service.check_user_credentials(data.email,data.password)
     access_token :str = token_service.create_access_token(user)
     refresh_token : str = token_service.create_refresh_token(user)
 
     response_model : UserLoginResponse = UserLoginResponse(email=user.email,access_token=access_token, refresh_token=refresh_token, token_type='Bearer')
     response.headers.append("Token-Type","Bearer")
     
     return response_model