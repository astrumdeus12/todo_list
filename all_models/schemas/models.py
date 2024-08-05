from pydantic import BaseModel


class Checker(BaseModel):
    day_id : int
    

class Changer(BaseModel):
    day_id : int
    task_id : int


class Deleter(BaseModel):
    day_id : int
    task_id : int


class Adder(BaseModel):
    day_id : int
    txt : str 


class User(BaseModel):
    username : str
    email : str = None
    password : str


