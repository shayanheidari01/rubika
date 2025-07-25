import enum

class PaymentStatusEnum(str, enum.Enum):
    Paid = 'Paid'
    NotPaid = 'NotPaid'