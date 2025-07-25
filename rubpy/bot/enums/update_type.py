from enum import Enum


class UpdateTypeEnum(str, Enum):
    NEW_MESSAGE = "NewMessage"
    UPDATED_MESSAGE = "UpdatedMessage"
    REMOVED_MESSAGE = "RemovedMessage"
    STARTED_BOT = "StartedBot"
    STOPPED_BOT = "StoppedBot"
    UPDATED_PAYMENT = "UpdatedPayment"