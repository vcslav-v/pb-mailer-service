from pb_mailer_service import schemas
from typing import cast, TypeVar

T = TypeVar('T', bound=schemas.general.EmailEvent)

def email_postprocess(msg_data: T, mail_data: schemas.general.EmailData) -> tuple[T | None, schemas.general.EmailData | None]:
    
    # if OrderUpdated but not abandoned subscription order, ignore
    if isinstance(msg_data, schemas.billing.OrderUpdated):
        order = cast(schemas.billing.OrderUpdated, msg_data)
        is_subscription = order.subscription_id is not None
        is_abandoned = order.status == schemas.billing.PaymentStatus.EXPIRED or order.status == schemas.billing.PaymentStatus.CANCELLED
        if not is_subscription or not is_abandoned:
            return None, None
        is_coupon_used = order.coupon is not None
        if not is_coupon_used:
            mail_data.template_path = 'billing/order_update_sub_without_coupon.html'
        else:
            mail_data.template_path = 'billing/order_update_sub_with_coupon.html'

    return msg_data, mail_data
