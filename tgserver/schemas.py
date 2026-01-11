from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Literal
from datetime import datetime


class ReminderCreater(BaseModel):  # тест (удалить!)
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


class TestDjango(BaseModel):
    """Схема для тестового пост запроса от Django"""

    msg: str = Field()


class NewNoticeSchema(BaseModel):
    """ Схема для создания напоминания внутри бота """

    username: str = Field(max_length=33, min_length=6)
    title: str = Field(max_length=100)
    date: str = datetime
    chat_id: int


class NoticeShiftSchema(BaseModel):
    """ Схема для смещения напоминания на час/день """

    user_id: int = Field(gt=0)
    reminder_id: int = Field(gt=0)
    mode: Literal["hour", "day"]
    chat_id: int


class UserInfoSchema(BaseModel):
    """ Схема для сохранения игформации о пользователе """

    tg_user_id: int
    chat_id: int


class _OneNoticeSchema(BaseModel):
    """ Схема каждого напоминания в списке на сохранение от сервера """

    chat_id: int
    text: str
    user_id: int = Field(gt=0)
    reminder_id: int = Field(gt=0)


class NoticeListSchema(BaseModel):
    """ Схема для сохранения списка ближайших напоминаний """

    notice_list: list[_OneNoticeSchema]
    next_date: datetime
