import resend

from .env_provider import RESEND_API_KEY

resend.api_key = RESEND_API_KEY


def send_email(user_email: str, user_name: str, token: str):
    html_structure = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f5f5f5; }}
            .container {{ max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            h1 {{ color: #333; margin-bottom: 10px; }}
            p {{ color: #666; font-size: 16px; }}
            .content {{ margin: 20px 0; line-height: 1.6; }}
            .verification-box {{ background-color: #f0f7ff; border-left: 4px solid #0066cc; padding: 15px; margin: 20px 0; }}
            .btn {{ display: inline-block; background-color: black; color: #FFFFFF; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin-top: 15px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Hi {user_name}</h1>
            <p>Welcome to SubDomainLender!</p>
            <div class="content">
                <p>You are one step away from pointing your Application to a custom sub-domain of yours.</p>
                <div class="verification-box">
                    <strong>Verify your email by clicking the link below:</strong><br>
                    <a href="{token}" class="btn">Verify Email</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    params = {
        "from": "SubDomainLender <noreply@amit4218.fun>",
        "to": user_email,
        "subject": "Email Verification! Please verify your email",
        "html": html_structure,
    }

    email = resend.Emails.send(params)  # ty:ignore[invalid-argument-type]

    return email
