from enum import Enum


class VerificationType(Enum):
    REGISTER = "register"
    FORGOT_PASSWORD = "forgot_password"
    CHANGE_PASSWORD = "change_password"
