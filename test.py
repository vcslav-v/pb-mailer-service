from pb_mailer_service.setup import TOPICS_MAP
from pb_mailer_service import schemas, mail
import asyncio
from time import sleep


async def make_test_email(raw_msg_data, topic, is_send=False):
    email_data = TOPICS_MAP.get(topic)
    if not isinstance(email_data, schemas.general.EmailData):
        raise ValueError(f'Invalid email data for topic {topic}')
    msg_data = email_data.schema_model.model_validate(raw_msg_data)
    html = mail._render_email(msg_data, email_data)
    if is_send:
        await mail._send_email(
            msg_data.email,
            email_data.subject,
            html,
            is_test=True  # Set to True for testing purposes
        )
    else:
        with open('test_email.html', 'w') as f:
            f.write(html)

if __name__ == '__main__':
    test_email = ''

    test_subscription_cancelled_topic = 'billing.subscription.cancelled'
    test_subscription_cancelled_value = {
        'email': test_email,
        'billing_cycle': 'quarterly',
        'end': '2022-01-01',
        'amount_cents': 3100
    }

    test_subscription_success_topic = 'billing.subscription.success'
    test_subscription_success_value = {
        'email': test_email,
        'billing_cycle': 'quarterly',
        'start': '2022-01-01',
        'end': '2023-01-01',
        'amount_cents': 3100
    }

    test_subscription_reminder_topic = 'billing.subscription.reminder'
    test_subscription_reminder_value = {
        'email': test_email,
        'billing_cycle': 'quarterly',
        'renewal_date': '2022-01-01',
        'amount_cents': 3100
    }

    test_subscription_upgrade_topic = 'billing.subscription.upgrade'
    test_subscription_upgrade_value = {
        'email': test_email,
        'billing_cycle': 'quarterly',
        'next_payment': '2022-01-01',
        'amount_cents': 3100
    }

    test_subscription_ended_topic = 'billing.subscription.ended'
    test_subscription_ended_value = {
        'email': test_email,
        'billing_cycle': 'quarterly',
    }

    test_subscription_failure_topic = 'billing.subscription.failure'
    test_subscription_failure_value = {
        'email': test_email,
        'due': '2022-01-01',
        'billing_cycle': 'quarterly',
        'amount_cents': 3100
    }

    test_subscription_renew_topic = 'billing.subscription.renew'
    test_subscription_renew_value = {
        'email': test_email,
        'billing_cycle': 'quarterly',
        'next_payment': '2022-01-01',
        'amount_cents': 3100
    }

    test_purchase_lifetime_success_topic = 'billing.purchase.lifetime.success'
    test_purchase_lifetime_success_value = {
        'email': test_email,
        'start': '2022-01-01',
        'amount_cents': 3100
    }

    test_purchase_lifetime_upgrade_topic = 'billing.purchase.lifetime.upgrade'
    test_purchase_lifetime_upgrade_value = {
        'email': test_email,
        'start': '2022-01-01',
        'amount_cents': 3100
    }

    # test_value = test_subscription_reminder_value
    # test_topic = test_subscription_reminder_topic

    # asyncio.run(make_test_email(test_value, test_topic, is_send=True))

    for test_value, test_topic in [
        (test_subscription_success_value, test_subscription_success_topic),
        (test_subscription_cancelled_value, test_subscription_cancelled_topic),
        (test_subscription_reminder_value, test_subscription_reminder_topic),
        (test_subscription_upgrade_value, test_subscription_upgrade_topic),
        (test_subscription_ended_value, test_subscription_ended_topic),
        (test_subscription_failure_value, test_subscription_failure_topic),
        (test_subscription_renew_value, test_subscription_renew_topic),
        (test_purchase_lifetime_success_value, test_purchase_lifetime_success_topic),
        (test_purchase_lifetime_upgrade_value, test_purchase_lifetime_upgrade_topic)
    ]:
        print(f'Processing {test_topic}...')
        asyncio.run(make_test_email(test_value, test_topic, is_send=True))
        sleep(5)
