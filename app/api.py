import bcrypt
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import sign_jwt
from app.schemas import UserSchema
from app.schemas import TaskSchema
from app.models import User, Task
from app.database import get_session

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Welcome to the ToDo List application"}

@app.post("/register")
def create_user(request: UserSchema, session: Session = Depends(get_session)):
    """The API function to create users

    Parameters:
    request: new user information
    session: the session to connect the database

    Returns:
    response message to show the creation succeed or not
    """
    exist_user = session.query(User).filter(User.username == request.username).first()
    if exist_user:
        raise HTTPException(status_code=401, detail="Username has already been registered")
    
    password = request.password
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)

    user = User(username=request.username, password=hash)
    session.add(user)
    session.commit()
    return {
        "message": "User has been successfully registered."
    }

@app.post("/login")
def user_login(request: UserSchema, session: Session = Depends(get_session)):
    """The API function to login users

    Parameters:
    request: username and password
    session: the session to connect the database

    Returns:
    response message to show the login succeed or not
    """
    user = session.query(User).filter(User.username == request.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Wrong login details!")
    
    password = request.password
    bytes = password.encode('utf-8')
    if not bcrypt.checkpw(bytes, user.password):
        raise HTTPException(status_code=401, detail="Wrong login details!")
    
    token = sign_jwt(user.id)
    return {
        "message": "Login successful",
        "token": token
    }

@app.get("/tasks")
def get_tasks(session: Session = Depends(get_session), user_id: int = Depends(JWTBearer())):
    """The API function to get all tasks for the user

    Parameters:
    session: the session to connect the database
    user_id: user ID

    Returns:
    The list of tasks for the user
    """
    tasks = session.query(Task).filter(Task.user_id == user_id).all()
    if tasks:
        return tasks
    else:
        return []

@app.get("/tasks/{task_id}")
def get_single_task(task_id: int, session: Session = Depends(get_session), user_id: int = Depends(JWTBearer())):
    """The API function to get specific task

    Parameters:
    task_id: the task ID
    session: the session to connect the database
    user_id: the user ID

    Returns:
    the specific task
    """
    task = session.query(Task).filter(Task.id == task_id).first()
    if task:
        if task.user_id == user_id:
            return task
        else:
            raise HTTPException(status_code=401, detail="Not authorized for other users' task")
    else:
        return {}
    
@app.put("/tasks/{task_id}")
def update_single_task(task_id: int, request: TaskSchema, session: Session = Depends(get_session), user_id: int = Depends(JWTBearer())):
    """The API function to update a task

    Parameters:
    task_id: the task ID
    session: the session to connect the database
    user_id: the user ID

    Returns:
    the task updated when success; otherwise returns error message
    """
    task = session.query(Task).filter(Task.id == task_id).first()
    if task:
        if task.user_id == user_id:
            task.title = request.title
            task.description = request.description
            task.completed = request.completed
            session.add(task)
            session.commit()
            session.refresh(task)
            return task
        else:
            raise HTTPException(status_code=401, detail="Not authorized to update other users' task")
    else:
        return {
            "error": "Task not found"
        }
    
@app.delete("/tasks/{task_id}")
def delete_single_task(task_id: int, session: Session = Depends(get_session), user_id: int = Depends(JWTBearer())):
    """The API function to delete a task

    Parameters:
    task_id: the task ID
    session: the session to connect the database
    user_id: the user ID

    Returns:
    response message to show the deletion succeed or not
    """
    task = session.query(Task).filter(Task.id == task_id).first()
    if task:
        if task.user_id == user_id:
            session.delete(task)
            session.commit()
            return {
                "message": "Task successfully deleted"
            }
        else:
            raise HTTPException(status_code=401, detail="Not authorized to delete other users' task")
    else:
        return {
            "error": "Task not found"
        }
        
@app.post("/tasks")
def add_task(request: TaskSchema, session: Session = Depends(get_session), user_id: int = Depends(JWTBearer())):
    """The API function to add a task

    Parameters:
    request: new task information
    session: the session to connect the database
    user_id: the user ID

    Returns:
    response message to show the creation succeed or not
    """
    task = Task(title=request.title, description=request.description, completed=request.completed, user_id=user_id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
