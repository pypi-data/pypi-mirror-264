# -*- coding: utf-8 -*-
from typing import List
from django.template import Context, Template
from django.core.mail import EmailMessage


def render_template(template_file_path: str, context_dict: dict):
    template_file = open(template_file_path)
    template = Template(template_file.read())
    template_file.close()
    return template.render(Context(context_dict))


def send_html_email(
        subject: str,
        html_message: str,
        recipient_list: List[str],
        cc_list: List[str] = None,
        attach_filename_list: List[str] = None
):
    email = EmailMessage(
        subject=subject,
        body=html_message,
        to=recipient_list,
        cc=cc_list,
    )
    email.content_subtype = 'html'
    if attach_filename_list not in [None, []]:
        for filename in attach_filename_list:
            email.attach_file(filename)
    email.send()
