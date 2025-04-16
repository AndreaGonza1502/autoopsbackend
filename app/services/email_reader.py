import imaplib
import email
from email.header import decode_header
from typing import List

def fetch_emails(email_user: str, email_pass: str, imap_url: str = "imap.gmail.com") -> List[dict]:
    mails = []

    mail = imaplib.IMAP4_SSL(imap_url)
    mail.login(email_user, email_pass)
    mail.select("inbox")

    result, data = mail.search(None, 'UNSEEN')  # Solo no leídos
    mail_ids = data[0].split()

    for i in mail_ids[-10:]:  # últimos 10 nuevos
        res, msg_data = mail.fetch(i, "(RFC822)")
        raw_msg = msg_data[0][1]
        msg = email.message_from_bytes(raw_msg)

        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")

        from_ = msg.get("From")

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        mails.append({
            "from": from_,
            "subject": subject,
            "body": body,
        })

    mail.logout()
    return mails
