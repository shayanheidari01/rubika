from enum import Enum


class UpdateTypeEnum(str, Enum):
    NEW_MESSAGE = "NewMessage"
    UPDATED_MESSAGE = "UpdatedMessage"
    REMOVED_MESSAGE = "RemovedMessage"
    STARTED_BOT = "StartedBot"
    STOPPED_BOT = "StoppedBot"
    UPDATED_PAYMENT = "UpdatedPayment"

    # Backwards-compatible camelCase aliases
    NewMessage = NEW_MESSAGE
    UpdatedMessage = UPDATED_MESSAGE
    RemovedMessage = REMOVED_MESSAGE
    StartedBot = STARTED_BOT
    StoppedBot = STOPPED_BOT
    UpdatedPayment = UPDATED_PAYMENT