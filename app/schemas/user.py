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


class UserUpdate(BaseModel):
    roles: str | None = Field(default=None, max_length=100, description='角色列表，逗号分隔')
    is_active: int | None = Field(default=None, ge=0, le=1, description='账号状态 1=启用 0=禁用')
    password: str | None = Field(default=None, min_length=1, max_length=50, description='新密码')


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    username: str
    roles: list[str]
