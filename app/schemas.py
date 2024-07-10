from pydantic import BaseModel

class UserSchema(BaseModel):
    """The input fields of user information"""
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "pytest",
                "password": "password"
            }
        }

class TaskSchema(BaseModel):
    """The input fields of task information"""
    title: str
    description: str
    completed: int

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Make a ToDo List",
                "description": "Use Python, FastAPI and Sqlite to make a ToDo List Application.",
                "completed": 1
            }
        }