import os, sqlite3, secrets, hashlib, smtplib
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from argon2 import PasswordHasher
import jwt

APP=FastAPI(title="AL-HUDA API",version="1.0.0")
DB=os.getenv("ALHUDA_DB","alhuda_users.db")
SECRET=os.getenv("ALHUDA_SECRET_KEY","CHANGE_ME_IN_PRODUCTION")
TTL=int(os.getenv("CODE_TTL_MINUTES","10"))
PH=PasswordHasher()

def con(): return sqlite3.connect(DB)
def init():
    with con() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS users(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,email TEXT UNIQUE NOT NULL,
          password_hash TEXT NOT NULL,verified INTEGER DEFAULT 0,
          created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS codes(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id INTEGER,email TEXT NOT NULL,code_hash TEXT NOT NULL,
          purpose TEXT NOT NULL,expires_at TEXT NOT NULL,used INTEGER DEFAULT 0
        );
        """)
init()

class RegisterIn(BaseModel):
    name:str=Field(min_length=2,max_length=100)
    email:EmailStr
    password:str=Field(min_length=8,max_length=128)

class CodeIn(BaseModel):
    email:EmailStr
    code:str=Field(min_length=6,max_length=6)

class LoginIn(BaseModel):
    email:EmailStr
    password:str

class ResetIn(BaseModel):
    email:EmailStr
    code:str=Field(min_length=6,max_length=6)
    new_password:str=Field(min_length=8,max_length=128)

def hash_code(code): return hashlib.sha256(code.encode()).hexdigest()
def send_code(email,code,purpose):
    host=os.getenv("SMTP_HOST")
    if not host:
        # Development mode: do not expose codes in production logs.
        return
    msg=EmailMessage()
    msg["Subject"]="AL-HUDA — Email Verification" if purpose=="verify" else "AL-HUDA — Password Reset"
    msg["From"]=os.getenv("SMTP_FROM","no-reply@example.com")
    msg["To"]=email
    msg["Reply-To"]="no-reply@example.com"
    msg.set_content(f"Your AL-HUDA {purpose} code is: {code}\n\nThis code expires in {TTL} minutes. Do not share it. This mailbox does not accept replies.")
    with smtplib.SMTP(host,int(os.getenv("SMTP_PORT","587"))) as s:
        s.starttls(); s.login(os.getenv("SMTP_USERNAME"),os.getenv("SMTP_PASSWORD")); s.send_message(msg)

def issue_code(user_id,email,purpose):
    code=f"{secrets.randbelow(1000000):06d}"
    exp=datetime.now(timezone.utc)+timedelta(minutes=TTL)
    with con() as c:
        c.execute("INSERT INTO codes(user_id,email,code_hash,purpose,expires_at) VALUES(?,?,?,?,?)",
                  (user_id,email,hash_code(code),purpose,exp.isoformat()))
    send_code(email,code,purpose)

@APP.post("/api/register")
def register(x:RegisterIn):
    with con() as c:
        if c.execute("SELECT 1 FROM users WHERE email=?",(x.email,)).fetchone():
            raise HTTPException(409,"Email already registered")
        cur=c.execute("INSERT INTO users(name,email,password_hash) VALUES(?,?,?)",
                      (x.name,x.email,PH.hash(x.password)))
        uid=cur.lastrowid
    issue_code(uid,x.email,"verify")
    return {"ok":True,"message":"Verification code sent"}

@APP.post("/api/verify")
def verify(x:CodeIn):
    with con() as c:
        row=c.execute("""SELECT id,user_id FROM codes WHERE email=? AND purpose='verify'
                         AND code_hash=? AND used=0 AND expires_at>? ORDER BY id DESC LIMIT 1""",
                      (x.email,hash_code(x.code),datetime.now(timezone.utc).isoformat())).fetchone()
        if not row: raise HTTPException(400,"Invalid or expired code")
        c.execute("UPDATE codes SET used=1 WHERE id=?",(row[0],))
        c.execute("UPDATE users SET verified=1 WHERE id=?",(row[1],))
    return {"ok":True}

@APP.post("/api/login")
def login(x:LoginIn):
    with con() as c: row=c.execute("SELECT id,password_hash,verified FROM users WHERE email=?",(x.email,)).fetchone()
    if not row: raise HTTPException(401,"Invalid credentials")
    try: PH.verify(row[1],x.password)
    except Exception: raise HTTPException(401,"Invalid credentials")
    if not row[2]: raise HTTPException(403,"Email not verified")
    token=jwt.encode({"sub":str(row[0]),"exp":datetime.now(timezone.utc)+timedelta(days=7)},SECRET,algorithm="HS256")
    return {"ok":True,"access_token":token}

@APP.post("/api/request-reset")
def request_reset(email:EmailStr):
    with con() as c: row=c.execute("SELECT id FROM users WHERE email=?",(email,)).fetchone()
    # Always return the same response to avoid account enumeration.
    if row: issue_code(row[0],email,"reset")
    return {"ok":True,"message":"If the account exists, a reset code has been sent"}

@APP.post("/api/reset")
def reset(x:ResetIn):
    with con() as c:
        row=c.execute("""SELECT id,user_id FROM codes WHERE email=? AND purpose='reset'
                         AND code_hash=? AND used=0 AND expires_at>? ORDER BY id DESC LIMIT 1""",
                      (x.email,hash_code(x.code),datetime.now(timezone.utc).isoformat())).fetchone()
        if not row: raise HTTPException(400,"Invalid or expired code")
        c.execute("UPDATE codes SET used=1 WHERE id=?",(row[0],))
        c.execute("UPDATE users SET password_hash=? WHERE id=?",(PH.hash(x.new_password),row[1]))
    return {"ok":True}

@APP.get("/api/health")
def health(): return {"ok":True,"service":"AL-HUDA"}
