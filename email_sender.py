import os
import base64
import json

import sendgrid
import sendgrid.helpers.mail as mail

from logconfig import logger


DIRECTORY = os.path.dirname(__file__) + "/"

with open("email_data.json", "r") as file:
    EMAIL_DATA = json.load(file)
SENDGRID_API = EMAIL_DATA["SENDGRID_API"]

FROM_EMAIL = mail.Email("mlgreenhouse1@outlook.com")
TEST_EMAILS = ["maxwublouin@gmail.com"]
TO_EMAILS = EMAIL_DATA["MAILING_LIST"]

sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API)


def _create_attachment(file_path: str):
    """
    Takes file path and returns a corresponding Attachment object.
    Returns None if file couldn't be opened.

    Args:
        file_path:  The path to the file attachment (relative to the
                    MLGreenhouse directory)

    Returns:
        Attachment: The attached file as an Attachment object.
    """
    try:
        with open(file_path, "rb") as file:
            data = file.read()
            file.close()
    except:
        return
    
    encoded_file = base64.b64encode(data).decode()
    
    attached_file = mail.Attachment(
        file_content=mail.FileContent(encoded_file),
        file_name=mail.FileName(file_path.split("/")[-1])
    )

    return attached_file


def send_email(subject: str = "MLGreenhouse update",
               content: str = "This is an automatically generated message from your favorite hydroponics garden.",
               attachments: list = []):
    """
    Sends an email given a subject, content, and attachments list.
    The recipient emails can be found in TO_EMAILS.

    Args:
        subject (str):  The subject of the email.
        content (str):  Body text of the email.
        attachments (list): List of file paths corresponding to attachments.
                            File paths are relative to the MLGreenhouse
                            directory.

    Returns:
        status_code (int):  202 if email sent successfully.
    """
    email = mail.Mail(from_email=FROM_EMAIL,
                      to_emails=TO_EMAILS,
                      subject=subject,
                      plain_text_content=content)

    for attachment in attachments:
        attached_file = _create_attachment(attachment)
        if attached_file is not None:
            email.add_attachment(attached_file)

    mail_json = email.get()
    
    try:
        response = sg.client.mail.send.post(request_body=mail_json)
        status_code = response.status_code
    except:
        status_code = 404

    logger.info(f"Sent email with status code {status_code}.")

    return status_code


if __name__ == "__main__":

    print(SENDGRID_API)
    print(TO_EMAILS)