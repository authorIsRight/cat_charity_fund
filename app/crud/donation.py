from typing import List

from app.crud.base import CRUDBase
from app.models import Donation, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDDonation(CRUDBase):

    async def get_by_user(self, user: User, session: AsyncSession) -> List[Donation]:

        donations = await session.execute(
            select(Donation)
            .where(Donation.user_id == user.id)
            .order_by(Donation.create_date.desc())
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)