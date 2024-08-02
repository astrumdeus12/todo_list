from fastapi import Depends
import fastapi_users

from sqlalchemy import select, delete, create_engine
from sqlalchemy.orm import Session
from Dao.orm_models.classess import user, days, todo_day, engine



print(fastapi_users)
session = Session(engine, expire_on_commit=True)
current_active_verified_user = fastapi_users.current_user(active=True, verified=True)

def check_tasks(id:int):
    with session as ses:
        ses.begin()

        res = ses.execute(
            select(
                days.day,
                todo_day.task,
                todo_day.status
                ).where(todo_day.day_fk == id)).all()
        
        ses.commit()

        return(f'{res}')

def change_status(day:int, tsk:int):
    with session as ses:
       ses.begin()

       ses.scalar(
           select(
               todo_day
               ).where(
                   todo_day.day_fk == day
                   ).where(
                       todo_day.id == tsk
                       )).status = True
       
       ses.commit()

    

def delete_task(day_id:int, task_id:int):
    with session as ses:
        ses.begin()

        ses.execute(
            delete(todo_day)
            .where(todo_day.day_fk == day_id)
            .where(todo_day.id == task_id))
        
        ses.commit()

        

def add_task(id:int, txt:str):
    with session as ses:
        ses.begin()

        day = ses.scalar(
            select(days)
            .where(days.id == id)
            )
        day.tasks.append(
            todo_day( task = txt)
            )
        
        ses.commit()

def protected_route(user: user = Depends(current_active_verified_user)):
    return f"Hello, {user.email}"


# def add_user(username : str, email : str, password : str):
#     with session as ses:
#         ses.begin()
#         ses.add(User(username = username, email = email, password = password))
#         ses.commit()
    

# def get_user(username : str):
#     with session as ses:
#         ses.begin()
#         res = ses.execute(
#             select(User)
#             .where(User.username == username))
#         ses.commit()
#         return(f'{res}')
    


# def change_user(username : str, changable : User, change : str):
#     with session as ses:
#         ses.begin()
#         ses.execute(select(
#             User
#         )
#         .where(User.username == username)).changable = change
#         ses.commit
    

# def delete_user(username : str, password : str):
#     with session as ses:
#         ses.begin()
#         ses.delete(select(User)
#                    .where(User.username == username)
#                    .where(User.password == password)
#                    )
#         ses.commit() 
    
        



# change_status(1, 1)
#delete_task(1, 2)
# day1 = days( day = 'monday')
# task1 = todo_day(task = 'wake up')
# task2 = todo_day(task = 'dskkskdskajdkskjdkaksjksaksdkakdakjdksdakjskdasjkdas')
# day1.tasks.append(task1)
# day1.tasks.append(task2)
# session.add(day1)
# # print(day1.tasks)

# session.commit()
#check_tasks(id=1)
# add_task(1, txt='waseee upeesss')
