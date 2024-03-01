from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import MAX_NAME_LENGTH, MIN_NAME_LENGTH, HTTPDetail
from app.crud import charity_project_crud
from app.crud.base import CRUDBase
from app.models import CharityProject


async def check_project_exist(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        obj_id=charity_project_id, session=session
    )
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=HTTPDetail.PROJECT_NOT_FOUND
        )
    return charity_project


async def check_invested_amount_before_delete(
        charity_project_id: int,
        session: AsyncSession,
):
    charity_project = await charity_project_crud.get(
        obj_id=charity_project_id, session=session
    )
    if charity_project.fully_invested is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=HTTPDetail.CLOSED_PROJECT_DELETE
        )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=HTTPDetail.NON_EMPTY_PROJECT_DELETE
        )


async def check_charity_project_before_edit(
        charity_project_id: int,
        amount: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        obj_id=charity_project_id, session=session
    )
    if charity_project.fully_invested is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=HTTPDetail.CLOSED_PROJECT_EDIT
        )
    if amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=HTTPDetail.LESS_THAN_INVESTED_AMOUNT
        )


async def check_charity_project_name(
        project_name: str,
        session: AsyncSession,
) -> None:
    room_id = await charity_project_crud.get_room_id_by_name(
        project_name, session
    )
    if room_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=HTTPDetail.DUPLICATE_PROJECT_NAME
        )
    if not MIN_NAME_LENGTH <= len(project_name) <= MAX_NAME_LENGTH:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=HTTPDetail.INVALID_PROJECT_NAME_LENGTH
        )


async def check_full_amount(
        db_obj: str,
) -> None:
    if db_obj.full_amount <= 0:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=HTTPDetail.INVALID_PROJECT_AMOUNT
        )


async def check_invested_amount(
        invested_amount: int,
        db_obj,
        model,
        session: AsyncSession,
) -> None:
    obj_crud = CRUDBase(model)
    if invested_amount > 0:
        db_obj_id = db_obj.id
        await obj_crud.update_invested_amount(
            db_obj_id, invested_amount, session
        )
