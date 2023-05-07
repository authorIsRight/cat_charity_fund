from datetime import datetime
from typing import Optional
from dateutil import parser

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)
    full_amount: Optional[PositiveInt] = Field(None)

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: str = Field(...)
    full_amount: PositiveInt = Field(...)

    class Config:
        min_anystr_length = 1


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int = Field(0)
    fully_invested: bool = Field(False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }

    @classmethod
    def from_orm(cls, obj):
        model = super().from_orm(obj)
        if obj.create_date:
            model.create_date = parser.parse(obj.create_date)
        if obj.close_date:
            model.close_date = parser.parse(obj.close_date)
        return model


class CharityProjectUpdate(CharityProjectBase):
    pass