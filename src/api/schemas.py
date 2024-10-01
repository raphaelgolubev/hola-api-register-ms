from enum import Enum
from uuid import UUID
from typing import Dict, List, Optional
from pydantic import BaseModel, EmailStr


class UserType(str, Enum):
    """
    Тип пользователя:
    - Business - Предприниматель
    - Customer - Покупатель
    - Moderator - Модератор
    """
    business = "Business"
    customer = "Customer"
    moderator = "Moderator"


class CompanyType(str, Enum):
    """
    Тип компании:
    - IP - ИП, Индивидуальный предприниматель
    - CP - Компания
    - SZ - Самозанятый
    """
    IP = "IP"
    CP = "CP"
    SZ = "SZ"


class Gender(str, Enum):
    """
    Половая принадлежность:
    - Male - Мужской
    - Female - Женский
    - Unselected - Не выбрано
    """
    male = "Male"
    female = "Female"
    unselected = "Unselected"

class RegisterIn(BaseModel):
    """
    Данные для регистрации от клиентского приложения
    """
    email: EmailStr
    password: str
    user_type: UserType
    phone: str

class RegisterOut(BaseModel):
    id: UUID
    user_type: UserType
