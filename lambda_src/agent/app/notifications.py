import os

import boto3

ses = boto3.client("ses")

SES_FROM_EMAIL = os.getenv("SES_FROM_EMAIL", "")


def send_appointment_confirmation(to_email: str, subject: str, body: str) -> bool:
    """Send appointment confirmation using SES.

    In SES sandbox, both sender and recipient must be verified.
    If SES_FROM_EMAIL is blank, we skip sending but keep the app flow working.
    """
    if not SES_FROM_EMAIL or not to_email:
        print("SES email skipped: SES_FROM_EMAIL or recipient is missing")
        return False

    ses.send_email(
        Source=SES_FROM_EMAIL,
        Destination={"ToAddresses": [to_email]},
        Message={
            "Subject": {"Data": subject},
            "Body": {"Text": {"Data": body}},
        },
    )
    return True
