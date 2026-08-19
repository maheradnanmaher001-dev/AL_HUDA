from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from app.services.account_service import register_local, login_local, logout, current_user

class AccountScreen(Screen):
    mode=StringProperty("login")
    message=StringProperty("")
    logged_in=BooleanProperty(False)
    user_name=StringProperty("")
    user_email=StringProperty("")

    def on_enter(self):
        u=current_user()
        self.logged_in=bool(u)
        if u:
            self.user_name=u["name"]; self.user_email=u["email"]

    def set_mode(self, mode):
        self.mode=mode; self.message=""

    def submit(self):
        try:
            name=self.ids.name_input.text.strip()
            email=self.ids.email_input.text.strip()
            password=self.ids.password_input.text
            if self.mode=="register":
                u=register_local(name,email,password)
            else:
                u=login_local(email,password)
            self.logged_in=True; self.user_name=u["name"]; self.user_email=u["email"]
            self.message="Account ready. Email verification is handled in Step 13."
        except Exception as e:
            self.message=str(e)

    def sign_out(self):
        logout()
        self.logged_in=False; self.user_name=""; self.user_email=""
        self.message="Signed out."
