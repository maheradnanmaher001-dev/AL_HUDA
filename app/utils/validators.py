import re
EMAIL_RE=re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
def valid_email(v): return bool(EMAIL_RE.match(v or ""))
def strong_password(v):
    return len(v)>=8 and any(c.isupper() for c in v) and any(c.isdigit() for c in v)
