from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    position: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    position: str
    email: EmailStr


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]
