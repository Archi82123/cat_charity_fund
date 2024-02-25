from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_before_edit,
                                check_charity_project_name, check_full_amount,
                                check_invested_amount_before_delete,
                                check_project_exist)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_charity_project_name(charity_project.name, session)
    await check_full_amount(charity_project)
    full_amount = charity_project.full_amount
    remaining_amount = await charity_project_crud.remaining_amount(
        Donation, full_amount, session
    )
    invested_amount = full_amount - remaining_amount
    new_charity_project = await charity_project_crud.create(
        charity_project, session
    )
    if invested_amount > 0:
        new_charity_project_id = new_charity_project.id
        await charity_project_crud.update_invested_amount(
            new_charity_project_id, invested_amount, session
        )
    return new_charity_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)
):
    charity_projects = await charity_project_crud.get_multi(session)
    return charity_projects


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_project_exist(
        project_id, session
    )
    await check_invested_amount_before_delete(project_id, session)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_project_exist(
        project_id, session
    )
    if obj_in.full_amount:
        await check_charity_project_before_edit(
            project_id, obj_in.full_amount, session
        )
    if obj_in.name:
        await check_charity_project_name(obj_in.name, session)
    charity_project = await charity_project_crud.update(
        db_obj=charity_project,
        obj_in=obj_in,
        session=session,
    )
    return charity_project
