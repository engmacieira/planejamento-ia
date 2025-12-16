from typing import Generic, TypeVar, Type, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from pydantic import BaseModel

ModelT = TypeVar("ModelT")
CreateSchemaT = TypeVar("CreateSchemaT", bound=BaseModel)
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=BaseModel)

class BaseRepository(Generic[ModelT, CreateSchemaT, UpdateSchemaT]):
    def __init__(self, model: Type[ModelT], db_session: AsyncSession):
        self.model = model
        self.db_session = db_session

    async def create(self, obj_in: CreateSchemaT) -> ModelT:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        self.db_session.add(db_obj)
        await self.db_session.commit()
        await self.db_session.refresh(db_obj)
        return db_obj

    async def get_by_id(self, id: Any) -> Optional[ModelT]:
        query = select(self.model).where(self.model.id == id)
        result = await self.db_session.execute(query)
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelT]:
        query = select(self.model).offset(skip).limit(limit)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def update(self, db_obj: ModelT, obj_in: UpdateSchemaT | dict) -> ModelT:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        self.db_session.add(db_obj)
        await self.db_session.commit()
        await self.db_session.refresh(db_obj)
        return db_obj

    async def delete(self, id: Any) -> bool:
        obj = await self.get_by_id(id)
        if obj:
            await self.db_session.delete(obj)
            await self.db_session.commit()
            return True
        return False
