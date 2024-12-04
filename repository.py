from database import UserOrm, new_session
from sqlalchemy import select
from database import UserOrm, new_session
from schemas import User, UserEntity
from sqlalchemy import select

async def add_user(data: dict) -> int:
    async with new_session() as session:
        new_user = UserOrm(**data)
        session.add(new_user)
        await session.flush()
        await session.commit()
        return new_user.id
    

async def get_users():
   async with new_session() as session:
      query = select(UserOrm)
      result = await session.execute(query)
      user_models = result.scalars().all()
      return user_models
  

class UserRepository:
    @classmethod
    async def add_user(cls, user: User) -> int:
        async with new_session() as session:
            data = user.model_dump()
            new_user = UserOrm(**data)
            session.add(new_user)
            await session.flush()
            await session.commit()
            return new_user.id

    @classmethod
    async def get_users(cls) -> list[UserEntity]:
        async with new_session() as session:
            query = select(UserOrm)
            result = await session.execute(query)
            user_model = result.scalars().all()
            users = [UserEntity.model_validate(user_model) for user_model in user_model]
            return users