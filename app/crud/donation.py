from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_by_user(self, user: User, session: AsyncSession) -> List[Donation]:
        async with session() as db:
            donations = await db.execute(
                select(Donation)
                .where(Donation.user_id == user.id)
                .order_by(Donation.create_date.desc())
            )
            return donations.scalars()


donation_crud = CRUDDonation(Donation)