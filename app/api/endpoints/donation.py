from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_full_amount, check_invested_amount
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation, User
from app.schemas.donation import DonationCreate, DonationDB, DonationResponse


router = APIRouter()


@router.post(
    '/',
    response_model=DonationResponse,
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
    await check_invested_amount(
        invested_amount,
        new_donation,
        Donation,
        session
    )
    return new_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationResponse],
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Получает список всех бронирований для текущего пользователя."""
    return await donation_crud.get_by_user(
        session=session, user=user
    )
