from dataclasses import dataclass
from typing import Optional

from .dict_like import DictLike
from rubpy.bot.enums.payment_status import PaymentStatusEnum


@dataclass
class PaymentStatus(DictLike):
    payment_id: Optional[str] = None
    status: Optional[PaymentStatusEnum] = None