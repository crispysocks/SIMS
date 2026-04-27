from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=50, description='登录账号')
    password: str = Field(..., min_length=1, max_length=50, description='登录密码')
    roles: str = Field(default='teacher', max_length=100, description='角色列表，逗号分隔')


class UserLogin(BaseModel):
    username: str = Field(..., min_length=1, max_length=50, description='登录账号')
    password: str = Field(..., min_length=1, max_length=50, description='登录密码')


class UserRead(BaseModel):
    id: int
    username: str
    roles: str
    is_active: int

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    username: str
    roles: list[str]
