from pb_mailer_service import schemas

TOPICS_MAP = {
    'billing.subscription.success': schemas.general.EmailData(
        subject='Your Payment Has Been Processed',
        short_subject='Payment processed',
        template_path='billing/subscription_success.html',
        schema_model=schemas.billing.SubscriptionSuccess
    ),
    'billing.subscription.cancelled': schemas.general.EmailData(
        subject='Plus Membership Auto-Renewal Canceled',
        short_subject='Auto-renewal canceled',
        template_path='billing/subscription_cancelled.html',
        schema_model=schemas.billing.SubscriptionCancelled
    ),
    'billing.subscription.ended': schemas.general.EmailData(
        subject='You’re Now on the Free Plan',
        short_subject='Plus is canceled',
        template_path='billing/subscription_ended.html',
        schema_model=schemas.billing.SubscriptionEnded
    ),
    'billing.subscription.failure': schemas.general.EmailData(
        subject="We Couldn't Process Your Payment",
        short_subject='Payment failed',
        template_path='billing/subscription_failure.html',
        schema_model=schemas.billing.SubscriptionFailure
    ),
    'billing.subscription.reminder': schemas.general.EmailData(
        subject='Pixelbuddha Plus Renewal Reminder',
        short_subject='Payment reminder',
        template_path='billing/subscription_reminder.html',
        schema_model=schemas.billing.SubscriptionReminder
    ),
    'billing.subscription.upgrade': schemas.general.EmailData(
        subject='Your Plus Plan Upgrade Is Complete',
        short_subject='Upgrade successful',
        template_path='billing/subscription_upgrade.html',
        schema_model=schemas.billing.SubscriptionUpgrade
    ),
    'billing.subscription.renew': schemas.general.EmailData(
        subject='Auto-Renewal Is Now Active for Your Plus Membership',
        short_subject='Plan is renewed',
        template_path='billing/subscription_renew.html',
        schema_model=schemas.billing.SubscriptionRenew
    ),
    'billing.purchase.lifetime.success': schemas.general.EmailData(
        subject='Your Payment Has Been Processed',
        short_subject='Payment processed',
        template_path='billing/purchase_lifetime_success.html',
        schema_model=schemas.billing.PurchaseLifetimeSuccess
    ),
    'billing.purchase.lifetime.upgrade': schemas.general.EmailData(
        subject='Your Plus Plan Upgrade Is Complete',
        short_subject='Upgrade successful',
        template_path='billing/purchase_lifetime_upgrade.html',
        schema_model=schemas.billing.PurchaseLifetimeUpgrade
    ),
    'billing.order.update': schemas.general.EmailData(
        subject='We saved your order',
        short_subject='We saved your order',
        template_path='billing/order_created.html',
        schema_model=schemas.billing.OrderUpdated,
    ),
    'revshare.product.approved': schemas.general.EmailData(
        subject='🟢 Your Submission Has Been Approved',
        short_subject='Product approved',
        template_path='revshare/product_approved.html',
        schema_model=schemas.revshare.ProductStatusApproved,
        is_category_block=False
    ),
    'revshare.product.need_work': schemas.general.EmailData(
        subject='🟡 Your Submission Needs Adjustments',
        short_subject='Product needs work',
        template_path='revshare/product_need_work.html',
        schema_model=schemas.revshare.ProductStatusNeedWork,
        is_category_block=False,
    ),
    'revshare.product.rejected': schemas.general.EmailData(
        subject='🔴 Your Submission Not Approved',
        short_subject='Product rejected',
        template_path='revshare/product_rejected.html',
        schema_model=schemas.revshare.ProductStatusRejected,
        is_category_block=False
    ),
}