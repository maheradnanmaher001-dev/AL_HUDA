import hashlib, json, secrets, time
from pathlib import Path

CODE_TTL=600
MAX_ATTEMPTS=5

def _file():
    try:
        from kivy.app import App
        return Path(App.get_running_app().user_data_dir)/"verification_state.json"
    except Exception:
        return Path.home()/".al_huda_verification_state.json"

def _load():
    try:
        return json.loads(_file().read_text(encoding="utf-8"))
    except Exception:
        return {"verification": {}, "reset": {}}

def _save(data):
    p=_file(); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data),encoding="utf-8")

def _hash(code, salt):
    return hashlib.sha256((salt+code).encode()).hexdigest()

def create_code(email, kind):
    if kind not in ("verification","reset"):
        raise ValueError("Invalid code type.")
    code=f"{secrets.randbelow(1000000):06d}"
    salt=secrets.token_hex(16)
    data=_load()
    data[kind][email.strip().lower()] = {
        "hash": _hash(code,salt), "salt": salt,
        "expires": time.time()+CODE_TTL, "attempts": 0
    }
    _save(data)
    # The code is returned to the email-delivery layer, never persisted plaintext.
    return code

def verify_code(email, code, kind):
    data=_load(); key=email.strip().lower()
    entry=data.get(kind,{}).get(key)
    if not entry: return False, "No active code."
    if time.time()>entry["expires"]: return False, "Code expired."
    if int(entry.get("attempts",0))>=MAX_ATTEMPTS: return False, "Too many attempts."
    entry["attempts"]=int(entry.get("attempts",0))+1
    ok=secrets.compare_digest(_hash(str(code).strip(),entry["salt"]),entry["hash"])
    if ok:
        del data[kind][key]
        _save(data)
        return True, "Verified."
    _save(data)
    return False, "Invalid code."

def email_subject(kind):
    return "AL-HUDA email verification code" if kind=="verification" else "AL-HUDA password reset code"

def email_body(code, kind):
    action="verify your AL-HUDA account" if kind=="verification" else "reset your AL-HUDA password"
    return f"Your AL-HUDA code is: {code}\n\nUse this code to {action}. It expires in 10 minutes.\n\nThis is an automated no-reply message. Please do not reply."
