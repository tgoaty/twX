from aiosmtplib import send
from email.message import EmailMessage
from app.config import MAIL_PASSWORD, MAIL_SMTP_HOST, MAIL_SMTP_PORT, MAIL_EMAIL


async def send_activation_mail(to, link):
    message = EmailMessage()
    message["From"] = MAIL_EMAIL
    message["To"] = to
    message["Subject"] = "Activation Link"

    message.add_alternative(
        f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f6f9fc; margin: 0; padding: 0;">
        <table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="background-color: #f6f9fc; padding: 40px 0;">
          <tr>
            <td align="center">
              <table width="600" cellpadding="0" cellspacing="0" role="presentation" style="background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); padding: 40px;">
                <tr>
                  <td style="text-align: center; padding-bottom: 30px;">
                    <h1 style="color: #333;">Welcome!</h1>
                  </td>
                </tr>
                <tr>
                  <td style="font-size: 16px; color: #555; line-height: 1.5;">
                    <p>Thank you for registering with us.</p>
                    <p>Please click the button below to activate your account:</p>
                    <p style="text-align: center; margin: 30px 0;">
                      <a href="{link}" style="background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold;">Activate Account</a>
                    </p>
                    <p>If the button above does not work, please copy and paste the following link into your browser:</p>
                    <p style="word-break: break-all;"><a href="{link}" style="color: #007bff;">{link}</a></p>
                    <p>The twX Team</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </body>
    </html>
    """,
        subtype="html",
    )
    try:
        await send(
            message,
            hostname=MAIL_SMTP_HOST,
            port=MAIL_SMTP_PORT,
            start_tls=True,
            username=MAIL_EMAIL,
            password=MAIL_PASSWORD,
        )
    except Exception as e:
        raise Exception(f"Failed to send activation mail: {e}")
