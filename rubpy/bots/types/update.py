from typing import Optional, Literal
from pydantic import BaseModel
from .message import Message
from .payment_status import PaymentStatus


class Update(BaseModel):
    type: Literal['UpdatedMessage', 'NewMessage', 'RemovedMessage', 'StartedBot', 'StoppedBot', 'UpdatedPayment']
    chat_id: str
    removed_message_id: Optional[str]
    new_message: Message
    updated_message: Optional[Message]
    updated_payment: Optional[PaymentStatus]