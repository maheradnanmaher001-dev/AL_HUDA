import hashlib, json, os, re, secrets
from pathlib import Path

EMAIL_RE=re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def _file():
    try:
        from kivy.app import App
        return Path(App.get_running_app().user_data_dir)/"account.json"
    except Exception:
        return Path.home()/".al_huda_account.json"

def _hash_password(password, salt=None):
    if not isinstance(password,str) or len(password)<8:
        raise ValueError("Password must contain at least 8 characters.")
    salt=salt or secrets.token_hex(16)
    digest=hashlib.pbkdf2_hmac("sha256",password.encode(),bytes.fromhex(salt),120000).hex()
    return salt,digest

def validate_email(email):
    return bool(EMAIL_RE.match((email or "").strip()))

def register_local(name,email,password):
    email=(email or "").strip().lower()
    if not name.strip(): raise ValueError("Name is required.")
    if not validate_email(email): raise ValueError("Enter a valid email.")
    p=_file()
    if p.exists():
        raise ValueError("An account is already configured on this device.")
    salt,digest=_hash_password(password)
    data={"name":name.strip(),"email":email,"salt":salt,"password_hash":digest,
          "logged_in":True,"session_token":secrets.token_urlsafe(32)}
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data),encoding="utf-8")
    return {"name":data["name"],"email":email}

def login_local(email,password):
    p=_file()
    if not p.exists(): raise ValueError("No account found.")
    data=json.loads(p.read_text(encoding="utf-8"))
    salt,digest=_hash_password(password)
    if data.get("email")!=email.strip().lower() or digest!=data.get("password_hash"):
        raise ValueError("Invalid email or password.")
    data["logged_in"]=True
    data["session_token"]=secrets.token_urlsafe(32)
    p.write_text(json.dumps(data),encoding="utf-8")
    return {"name":data["name"],"email":data["email"]}

def logout():
    p=_file()
    if not p.exists(): return
    data=json.loads(p.read_text(encoding="utf-8"))
    data["logged_in"]=False
    data["session_token"]=""
    p.write_text(json.dumps(data),encoding="utf-8")

def current_user():
    p=_file()
    if not p.exists(): return None
    data=json.loads(p.read_text(encoding="utf-8"))
    if not data.get("logged_in"): return None
    return {"name":data.get("name",""),"email":data.get("email","")}
