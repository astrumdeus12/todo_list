from Sql_Models.classes import days, Todo_day, Base
from sqlalchemy import select, delete, create_engine
from sqlalchemy.orm import Session

engine = create_engine(
    url='postgresql+asyncpg://postgres:rootroot@localhost/todoapp',
      echo=True)

session = Session(engine, expire_on_commit=True)


def check_tasks(id:int):
    with session as ses:
        ses.begin()

        res = ses.execute(
            select(
                days.day,
                Todo_day.task,
                Todo_day.status
                ).where(Todo_day.day_fk == id)).all()
        
        ses.commit()

        return(f'{res}')

def change_status(day:int, tsk:int):
    with session as ses:
       ses.begin()

       ses.scalar(
           select(
               Todo_day
               ).where(
                   Todo_day.day_fk == day
                   ).where(
                       Todo_day.id == tsk
                       )).status = True
       
       ses.commit()

       

def delete_task(day_id:int, task_id:int):
    with session as ses:
        ses.begin()

        ses.execute(
            delete(Todo_day)
            .where(Todo_day.day_fk == day_id)
            .where(Todo_day.id == task_id))
        
        ses.commit()

        

def add_task(id:int, txt:str):
    with session as ses:
        ses.begin()

        day = ses.scalar(
            select(days)
            .where(days.id == id)
            )
        day.tasks.append(
            Todo_day( task = txt)
            )
        
        ses.commit()




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
