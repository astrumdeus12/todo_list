from fastapi import APIRouter, Depends
from schemas.models import Checker, Changer, Deleter, Adder
from Dao.functions import change_status,check_tasks,add_task,delete_task 
from fastapi.security import HTTPBearer
http_bearer = HTTPBearer(auto_error=False)

router1 = APIRouter()



@router1.post('/tasks/all')
def check_get(item : Checker):

    res = check_tasks(item.day_id)
    return(res)



@router1.post('/task/add')
def add_post(task : Adder):
    
    add_task( id = task.day_id, txt = task.txt)
    return('Task added')



@router1.post('/tasks/change')
def change_post(item : Changer):
    
    change_status(item.day_id, item.task_id)
    return('Task status changed')



@router1.post('/tasks/delete')
def del_post(item : Deleter):

    delete_task(item.day_id, item.task_id)
    return('task deleted')




#add_user(username='skjsjs', email='ssjsjsjj@djdjdj.com', password='kdkkdkddkkddkkd')


