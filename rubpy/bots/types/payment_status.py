from typing import Literal
from pydantic import BaseModel


class PaymentStatus(BaseModel):
    payment_id: str
    status: Literal['Paid', 'NotPaid']