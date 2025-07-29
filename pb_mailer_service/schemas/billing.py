from pydantic import BaseModel
from enum import Enum
from datetime import date
from pb_mailer_service.schemas.general import EmailEvent

class BillingCycle(str, Enum):
    MONTHLY = 'monthly'
    QUARTERLY = 'quarterly'
    YEARLY = 'yearly'


class SubscriptionSuccess(EmailEvent):
    billing_cycle: BillingCycle
    start: date
    end: date
    amount_cents: int

class SubscriptionEnded(EmailEvent):
    billing_cycle: BillingCycle

class SubscriptionFailure(EmailEvent):
    billing_cycle: BillingCycle
    due: date
    amount_cents: int

class SubscriptionReminder(EmailEvent):
    billing_cycle: BillingCycle
    renewal_date: date
    amount_cents: int

class SubscriptionUpgrade(EmailEvent):
    billing_cycle: BillingCycle
    next_payment: date
    amount_cents: int

class SubscriptionCancelled(EmailEvent):
    billing_cycle: BillingCycle
    end: date
    amount_cents: int

class SubscriptionRenew(EmailEvent):
    billing_cycle: BillingCycle
    next_payment: date
    amount_cents: int

class PurchaseLifetimeSuccess(EmailEvent):
    start: date
    amount_cents: int

class PurchaseLifetimeUpgrade(PurchaseLifetimeSuccess):
    pass