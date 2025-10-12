from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Literal
from datetime import datetime


class ReminderCreater(BaseModel):
    """ Schema for creating new reminder using the TG Bot """

    nickname: str = Field(max_length=33, min_length=6)
    title: str = Field(max_length=1000)
    mode: Literal['hour', 'day']
    date: datetime

    model_config = ConfigDict(extra='forbid')  # запрет екстра полей

    @field_validator('nickname')
    def check_at(cls, value):
        if value[0] != '@':
            print(value[0])
            raise ValueError('Никнейм должен начинаться на @')
        return value
