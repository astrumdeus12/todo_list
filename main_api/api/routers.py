from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers 
from all_models.schemas.models import Checker, Changer, Deleter, Adder
from main_api.auth.manager import get_user_manager
from main_api.dao.functions import change_status,check_tasks,add_task,delete_task
from fastapi.security import HTTPBearer
from all_models.orm_models.classess import user
from main_api.auth.backauth import auth_backend


http_bearer = HTTPBearer(auto_error=False)

router1 = APIRouter()

fastapi_users_class = FastAPIUsers[user, int](get_user_manager, [auth_backend])

cur_active_verified = fastapi_users_class.current_user( active=True)


@router1.post('/tasks/all')
async def check_get( item : Checker, user: user = Depends(cur_active_verified)):
    
    

    res = await check_tasks(id = item.day_id, user_id = user.id)
    return(res)



@router1.post('/task/add')
async def add_post(task : Adder, user: user = Depends(cur_active_verified)):
    
    
    await add_task( id = task.day_id, txt = task.txt, user_id = user.id)
    return('Task added')



@router1.post('/tasks/change')
async def change_post(item : Changer, user: user = Depends(cur_active_verified)):
    
    
    await change_status(item.day_id, item.task_id, user_id = user.id)
    return('Task status changed')



@router1.post('/tasks/delete')
async def del_post(item : Deleter, user: user = Depends(cur_active_verified)):
    

    await delete_task(item.day_id, item.task_id, user_id = user.id)
    return('task deleted')








