from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(self,
                                     project_name: str,
                                     session: AsyncSession,
                                     ) -> Optional[int]:
        result = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return self._get_first_result(result)

    async def get_charity_project_by_id(self,
                                        session: AsyncSession,
                                        project_id: int,
                                        ) -> Optional[CharityProject]:
        result = await session.execute(
            select(CharityProject).where(
                CharityProject.id == project_id
            )
        )
        return self._get_first_result(result)

    @staticmethod
    def _get_first_result(result):
        return result.scalars().first()


charity_project_crud = CRUDCharityProject(CharityProject)
