from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_full_amount
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import DonationCreate, DonationDB, DonationResponse


router = APIRouter()


@router.post(
    '/',
    response_model=DonationResponse,
    response_model_exclude_none=True,
)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    await check_full_amount(donation)
    full_amount = donation.full_amount
    remaining_amount = await donation_crud.remaining_amount(
        CharityProject, full_amount, session
    )
    invested_amount = full_amount - remaining_amount
    new_donation = await donation_crud.create(donation, session, user)
    if invested_amount > 0:
        new_donation_id = new_donation.id
        await donation_crud.update_invested_amount(
            new_donation_id, invested_amount, session
        )
    return new_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my', response_model=list[DonationResponse],
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Получает список всех бронирований для текущего пользователя."""
    donations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return donations
