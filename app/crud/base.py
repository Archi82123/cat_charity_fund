import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def __complete_mark__(
            self,
            db_obj
    ):
        db_obj.fully_invested = True
        db_obj.close_date = datetime.datetime.utcnow()

    async def remaining_amount(
            self,
            model,
            amount,
            session: AsyncSession,
    ):
        that_open = await session.execute(
            select(model).where(
                model.fully_invested.is_(False)
            ).order_by(model.create_date)
        )
        all_open = that_open.scalars().all()
        if all_open:
            for open in all_open:
                if amount > 0:
                    remaining_amount = open.full_amount - open.invested_amount
                    if amount <= remaining_amount:
                        open.invested_amount += amount
                        if open.invested_amount == open.full_amount:
                            await self.__complete_mark__(open)
                        amount = 0

                    else:
                        open.invested_amount = open.full_amount
                        await self.__complete_mark__(open)
                        amount -= remaining_amount
        return amount

    async def update_invested_amount(
            self,
            obj_id: int,
            invested_amount: int,
            session: AsyncSession,
    ):
        db_obj = await self.get(obj_id, session)
        if db_obj:
            db_obj.invested_amount = invested_amount
            if db_obj.invested_amount == db_obj.full_amount:
                await self.__complete_mark__(db_obj)
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
        return db_obj
