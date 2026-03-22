"""
Email notification service for blog updates
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_notification(recipient, subject, body):
    """Send email notification """
    smtp_server = "localhost"
    smtp_port = 25

    msg = MIMEMultipart()
    msg['From'] = "noreply@blog.local"
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.send_message(msg)
    server.quit()
    return True


def notify_new_post(recipient, post_title, post_url):
    """Notify subscriber about new blog post"""
    subject = f"New post: {post_title}"
    body = f"<p>Check out our new post: <a href='{post_url}'>{post_title}</a></p>"
    return send_notification(recipient, subject, body)


def notify_comment(recipient, comment_author, post_title):
    """Notify about new comment"""
    subject = f"New comment on: {post_title}"
    body = f"<p>{comment_author} commented on your post.</p>"
    return send_notification(recipient, subject, body)