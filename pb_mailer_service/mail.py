from email.message import EmailMessage

from aiosmtplib import send
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel

from pb_mailer_service import avro, config
from pb_mailer_service.buisness import email_postprocess
from pb_mailer_service.schemas.general import EmailData
import asyncio

from random import randint

def format_usd(cents: int) -> str:
    dollars = cents / 100
    return f'{dollars:,.2f}'

def format_date(date_obj) -> str:
    if hasattr(date_obj, 'strftime'):
        return date_obj.strftime('%b %d, %Y')
    return str(date_obj)


env = Environment(loader=FileSystemLoader(config.TEMPLATES_DIR))
env.filters['format_usd'] = format_usd
env.filters['format_date'] = format_date


env.globals['billing_cycle_period_map'] = {
    'monthly': 'month',
    'yearly': 'year',
    'quarterly': 'quarter',
}
env.globals['billing_cycle_names_map'] = {
    'monthly': 'monthly',
    'yearly': 'annual',
    'quarterly': 'quarterly',
}

env.globals['subscription_img_urls'] = {
    'monthly': 'https://pixelbuddha.ams3.cdn.digitaloceanspaces.com/mail-service/1-month.jpeg',
    'yearly': 'https://pixelbuddha.ams3.cdn.digitaloceanspaces.com/mail-service/12-months.jpeg',
    'quarterly': 'https://pixelbuddha.ams3.cdn.digitaloceanspaces.com/mail-service/3-month.jpeg',
    'lifetime': 'https://pixelbuddha.ams3.cdn.digitaloceanspaces.com/mail-service/lifetime.jpeg',
}

env.globals['abandoned_coupon_code'] = {
    'monthly': {'code': '5149-7303', 'discount': 10},
    'yearly': {'code': 'Heat30', 'discount': 30},
    'quarterly': {'code': 'Heat30', 'discount': 30},

}

env.globals['plus_price_cents'] = {
    'monthly': 3000,
    'quarterly': 6000,
    'yearly': 12000,
}


async def process(
        raw_msg_data: bytes,
        mail_data: EmailData,
    ):
    msg_data = await avro.decode_avro_message(raw_msg_data, mail_data.schema_model)
    msg_data, mail_data = email_postprocess(msg_data, mail_data)
    if msg_data is None or mail_data is None:
        await asyncio.sleep(1)
        return
    html_content = _render_email(msg_data, mail_data)
    await _send_email(
        msg_data.email,
        mail_data.subject,
        html_content
    )


def _render_email(template_data: BaseModel, mail_data: EmailData) -> str:
    template = env.get_template(mail_data.template_path)
    return template.render({
        'data': template_data,
        'config': mail_data,
    })



async def _send_email(to: str, subject: str, html: str, is_test: bool = False):
    msg = EmailMessage()
    msg['From'] = f'{config.SMTP_FROM_NAME} <{config.SMTP_SENDER}>'
    msg['To'] = to
    if is_test:
        msg['Subject'] = f'Test Email: {subject} - {randint(1000, 9999)}'
    else:
        msg['Subject'] = subject
    msg.set_content('Please view this email in a HTML compatible viewer.')
    msg.add_alternative(html, subtype='html')

    await send(
        msg,
        hostname=config.SMTP_HOSTNAME,
        port=config.SMTP_PORT,
        username=config.SMTP_USERNAME,
        password=config.SMTP_PASSWORD,
        start_tls=config.SMTP_START_TLS,
        timeout=10,
    )