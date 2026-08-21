from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.metrics import dp
from app.utils.responsive import fs
from app.theme import GOLD,TEXT,MUTED,CARD
from app.screens.common import header

def form(title, fields, buttons):
    root=BoxLayout(orientation="vertical",padding=dp(22),spacing=dp(10)); root.add_widget(header(title))
    inputs={}
    for key,hint in fields:
        i=TextInput(hint_text=hint,multiline=False,password="password" in key,size_hint_y=None,height=dp(50))
        inputs[key]=i;root.add_widget(i)
    for label,callback in buttons:
        b=Button(text=label,background_normal="",background_color=CARD,color=GOLD,size_hint_y=None,height=dp(50))
        b.bind(on_release=callback);root.add_widget(b)
    root.add_widget(Label(text="AL-HUDA • Secure account system",color=MUTED,font_size=fs(11)))
    return root,inputs

class LoginScreen(Screen):
    def on_enter(self):
        if self.children:return
        root,inputs=form("AL-HUDA Login",[("email","Email"),("password","Password")],
            [("LOGIN",lambda *_:self.go("home")),("Forgot Password",lambda *_:self.go("forgot")),("Create Account",lambda *_:self.go("register"))])
        self.add_widget(root)
    def go(self,n):self.manager.current=n

class RegisterScreen(Screen):
    def on_enter(self):
        if self.children:return
        root,inputs=form("Create Account",[("name","Full name"),("email","Email"),("password","Password"),("confirm","Confirm password")],
            [("REGISTER & SEND CODE",lambda *_:self.go("verify")),("Already have an account",lambda *_:self.go("login"))])
        self.add_widget(root)
    def go(self,n):self.manager.current=n

class VerifyScreen(Screen):
    def on_enter(self):
        if self.children:return
        root,inputs=form("Verify Email",[("code","6-digit verification code")],
            [("VERIFY ACCOUNT",lambda *_:self.go("home")),("Resend Code",lambda *_:None)])
        root.add_widget(Label(text="Code expires after a short period. Never share it.",color=MUTED,font_size=fs(12)))
        self.add_widget(root)
    def go(self,n):self.manager.current=n

class ForgotPasswordScreen(Screen):
    def on_enter(self):
        if self.children:return
        root,inputs=form("Forgot Password",[("email","Your registered email")],
            [("SEND RESET CODE",lambda *_:self.go("reset")),("Back to Login",lambda *_:self.go("login"))])
        self.add_widget(root)
    def go(self,n):self.manager.current=n

class ResetPasswordScreen(Screen):
    def on_enter(self):
        if self.children:return
        root,inputs=form("Reset Password",[("code","6-digit reset code"),("password","New password"),("confirm","Confirm new password")],
            [("RESET PASSWORD",lambda *_:self.go("login"))])
        self.add_widget(root)
    def go(self,n):self.manager.current=n
