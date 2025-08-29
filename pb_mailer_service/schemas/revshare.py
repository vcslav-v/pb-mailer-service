from pb_mailer_service.schemas.general import EmailEvent


class ProductStatusNeedWork(EmailEvent):
    product_title: str
    product_edit_url: str
    submission_slots: int
    used_slots: int
    moderation_message: str

class ProductStatusRejected(EmailEvent):
    product_title: str
    submission_slots: int
    used_slots: int
    moderation_message: str

class ProductStatusApproved(EmailEvent):
    product_title: str
    submission_slots: int
    used_slots: int