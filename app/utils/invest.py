from datetime import datetime
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def close_donation_for_obj(obj: Union[CharityProject, Donation]) -> Union[CharityProject, Donation]:
    """
    Закрыть объект, установив флаг 'fully_invested' в 'True', заполнить дату закрытия и возвратить его.
    """
    obj.invested_amount = obj.full_amount
    obj.fully_invested = True
    obj.close_date = datetime.now()
    return obj


async def get_not_fully_invested_objects(
    obj: Union[CharityProject, Donation],
    session: AsyncSession
) -> List[Union[CharityProject, Donation]]:
    """
    Получить список объектов типа 'obj', которые не полностью инвестированы.
    """
    query = select(obj).where(obj.fully_invested == 0).order_by(obj.create_date)
    objects = await session.execute(query)
    return objects.scalars().all()


async def invest_money(
    obj: Union[CharityProject, Donation],
    model: Union[CharityProject, Donation]
) -> Union[CharityProject, Donation]:
    """
    Инвестировать деньги в проект 'obj' путем перевода необходимой суммы на объект 'model'.
    """
    free_amount_in = obj.full_amount - obj.invested_amount
    free_amount_model = model.full_amount - model.invested_amount

    if free_amount_in > free_amount_model:
        obj.invested_amount += free_amount_model
        await close_donation_for_obj(model)

    elif free_amount_in == free_amount_model:
        await close_donation_for_obj(obj)
        await close_donation_for_obj(model)

    else:
        model.invested_amount += free_amount_in
        await close_donation_for_obj(obj)

    return obj, model


async def investing_process(
    obj: Union[CharityProject, Donation],
    model_add: Union[CharityProject, Donation],
    session: AsyncSession,
) -> Union[CharityProject, Donation]:
    """
    Инвестировать средства в открытый проект.
    """
    objects_model = await get_not_fully_invested_objects(model_add, session)

    for model in objects_model:
        obj, model = await invest_money(obj, model)
        session.add(obj)
        session.add(model)

    await session.commit()
    await session.refresh(obj)

    return obj
