# AL-HUDA Email API contract (Step 13)
#
# Recommended deployment: a private HTTPS backend. The Android app must never
# contain SMTP username/password or an email-provider API secret.
#
# POST /auth/send-verification
# body: {"email":"user@example.com"}
# response: {"ok":true}
#
# POST /auth/verify-email
# body: {"email":"user@example.com","code":"123456"}
#
# POST /auth/send-reset
# body: {"email":"user@example.com"}
#
# POST /auth/reset-password
# body: {"email":"user@example.com","code":"123456","new_password":"..."}
#
# The backend should call email_verification.create_code(), then
# email_mailer.send_code(). Do not return the code in an HTTP response.
#
# Production requirements:
# - HTTPS only
# - rate limiting
# - generic responses for unknown emails
# - short-lived, single-use codes
# - secrets stored in server environment/secret manager
# - audit logging without storing passwords or verification codes
