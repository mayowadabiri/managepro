from enum import Enum


class Cycle(Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class Status(Enum):
    ACTIVE = 'active'
    TOEXPIRE = 'to_expire'
    EXPIRED = 'expired'


class Currency(Enum):
    NAIRA = 'naira'
    DOLLARS = 'dollars'
    POUNDS = 'pounds'
    EUROS = 'euros'
