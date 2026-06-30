import ssl
import certifi

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from django.conf import settings


def send_reset_password_email(
        to_email,
        reset_link,
        username,
):
    
    subject = "Reset Your Password"

    html_content = f"""
    <h2> Password Reset Request </h2>
    <p> Hi {username}, </p>
    <p> We received a request to reset your password. Click the link below to set a new password: </p>

    <a href="{settings.FRONTEND_URL}/reset-password?token={reset_link}" 
       style="
       background:#2563eb;
       color:white;
       padding:10px 18px;
       text-decoration:none;
       border-radius:5px;
       display:inline-block;
       ">
       Reset Password
       </a>

    <p> If you didn't request a password reset, please ignore this email. </p>

    """

    message = Mail(
        from_email = settings.FROM_EMAIL,
        to_emails= to_email,
        subject = subject,
        html_content=html_content,
    )

    try:
        sg = SendGridAPIClient(
            settings.SENDGRID_API_KEY
        )

        sg.client.session.verify = certifi.where()

        response = sg.send(message)

        return{
            "success" : True,
            "status_code": response.status_code
        }
    except Exception as e:
        print("Error sending email:")
        print(str(e))
        return{
            "success":False,
            "status_code" : str(e)
        }
    
def send_password_reset_confirmation_email(
        to_email,
        username,
):
    subject = "Password Reset Successful"

    html_content = f"""
    <h2>Password Reset Successful</h2>

    <p> Hello {username}, </p>

    <p> Your Password has been reset Successfully.</p>

    <p> 
       if you did not perform this action,
       please secure your account immediatly.
    </p>

    """

    message = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails = to_email,
        subject = subject,
        html_content=html_content,
    )

    try:
        sg = SendGridAPIClient(
            settings.SENDGRID_API_KEY
        )

        sg.client.session.verify = certifi.where()

        response = sg.send(message)

        return {
            "success":True,
            "status_code":response.status_code
        }
        
    except Exception as e:
        return {
            "success":False,
            "status_code": str(e)
        }


def user_registeration_confirmation_email(
    to_email,
    username,
):
    subject = "Welcome to thinkforge blog app"

    html_content = f"""
    <h2>Hello, {username}!</h2>

    <p> Thank you for registering with us. We're excited to have you on board. </p>

    <p> Start exploring and sharing your thoughts with the community! </p>

    """

    message = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_content,
    )

    try:
        sg = SendGridAPIClient(
            settings.SENDGRID_API_KEY
        )

        sg.client.session.verify = certifi.where()
        response = sg.send(message)

        return {
            "success": True,
            "status_code": response.status_code
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }