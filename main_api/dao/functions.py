from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from all_models.orm_models.classess import days, todo_day, async_session_maker




session = async_session_maker


async def check_tasks(id:int, user_id : int):
    async with session() as ses:
        

        res = await ses.execute(
            select(    
                days.day,
                todo_day.task,
                todo_day.status
                ).where(days.id == id)
                .where(todo_day.day_fk == id)
                .where(todo_day.user_fk == user_id)
                )
        
        await ses.commit()

        task_list = [f'Day = {row.day} : Task {row.task}, status = {row.status}' for row in res]

        
        return ", ".join(task_list) 

async def change_status(day:int, tsk:int, user_id):
    async with session() as ses:
       

        res = await ses.scalar(
           select(todo_day)
           .where(todo_day.day_fk == day)
           .where(todo_day.id == tsk)
           .where(todo_day.user_fk == user_id))
        res.status = True
        await ses.commit()

    

async def delete_task(day_id:int, task_id:int, user_id):
    async with session() as ses:

        await ses.execute(
            delete(todo_day)
            .where(todo_day.day_fk == day_id)
            .where(todo_day.id == task_id)
            .where(todo_day.user_fk == user_id))
            
        
        await ses.commit()

        

async def add_task(id:int, txt:str, user_id):
    async with session() as ses:

        day = await ses.scalar(
        select(days)
        .options(selectinload(days.tasks))
        .where(days.id == id))
            
        day.tasks.append(
            todo_day( task = txt,
                    user_fk = user_id))
        
        await ses.commit()


