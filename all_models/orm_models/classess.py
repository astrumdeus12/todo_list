from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, Relationship
from typing import TYPE_CHECKING
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable
from fastapi_users_db_sqlalchemy.access_token import  SQLAlchemyBaseAccessTokenTable
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


DATABASE_URL = 'postgresql+asyncpg://postgres:rootroot@localhost/todoapp'
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)



class Base(DeclarativeBase):
    metadata = MetaData()


class days(Base):

    __tablename__ = 'days'

    id : Mapped[int] = mapped_column(
        primary_key=True,
        unique=True,
        autoincrement=True
        )
    day : Mapped[str] 

    tasks : Mapped[
        list['todo_day']] = Relationship(
        back_populates='day_task',
        uselist=True,
        lazy='selectin'
        )


class todo_day(Base):

    __tablename__ = 'todo_day'

    id : Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
        )
    
    task : Mapped[str] = mapped_column(
        primary_key=False
        )
    
    day_task : Mapped['days'] = Relationship(
        back_populates='tasks',
        uselist=False,
        lazy='selectin'
        
        )
    
    day_fk : Mapped[int] = mapped_column(
        ForeignKey('days.id')
        )
    
    task_user : Mapped['user'] = Relationship(
        back_populates='user_tasks',
        uselist=False,  
    )

    user_fk : Mapped[int] = mapped_column(
        ForeignKey('users.id')
    )

    status : Mapped[bool] = mapped_column(default=False)








if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class user(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'
    id : Mapped[int] = mapped_column(primary_key=True,
                                     unique=True,
                                     autoincrement=True)
    username : Mapped[str] = mapped_column()
    
    user_tasks : Mapped[list['todo_day']] = Relationship(
        back_populates='task_user',
        uselist=True,
        lazy='selectin'
    )
    @classmethod
    def get_db(cls, session: 'AsyncSession'):
        return SQLAlchemyUserDatabase(session, cls)
        
class AccessToken(SQLAlchemyBaseAccessTokenTable[int], Base):
    __tablename__ = 'accesstokens'
    user_id : Mapped[int] = mapped_column(ForeignKey('users.id'), nullable = False)
    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)










# task1 = todo_day(task = 'brush ann')
# task2 = todo_day(task = 'skdkksks')
# Day.tasks.append(task1)
# Day.tasks.append(task2)

# Base.metadata.create_all(engine)
# print(Day)
# print()
#session.commit()
