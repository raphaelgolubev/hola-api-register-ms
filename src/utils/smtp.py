from ssl import create_default_context
from smtplib import SMTP_SSL

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template
from pydantic import BaseModel

from src.config import settings


class Email(BaseModel):
    recipient: str
    subject: str
    jinja_variables: dict


def _send_email(email: Email, template_file: str):
    templates_dir = settings.paths.jinja_templates_dir  # settings.email.email_templates_dir
    
    file_loader = FileSystemLoader(searchpath=Path(templates_dir))
    environment = Environment(loader=file_loader)
    template: Template = environment.get_template(template_file)

    ssl_context = create_default_context()

    with SMTP_SSL(settings.email.host, settings.email.port, context=ssl_context) as server:
        html = template.render(**email.jinja_variables)

        message = MIMEMultipart()
        message["Subject"] = email.subject
        message["From"] = settings.email.user
        message["To"] = email.recipient
        message.attach(MIMEText(html, "html"))

        server.login(settings.email.user, settings.email.password)

        server.send_message(
            from_addr=settings.email.user,
            to_addrs=email.recipient,
            msg=message
        )


def send_verification_code(recipient: str, code: str):
    email = Email(
        recipient=recipient,
        subject="Код подтверждения для нового аккаунта HOLA App",
        jinja_variables={
            "verification_code": code,
            "expire_min": int(settings.security.verification_code_expiration_seconds / 60)
        }
    )

    _send_email(email=email, template_file="new_account.html")