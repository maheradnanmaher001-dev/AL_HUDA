from kivy.config import Config
Config.set("graphics","width","420")
Config.set("graphics","height","840")
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import StringProperty
from app.services.navigation import NavigationService

KV = '''
#:import dp kivy.metrics.dp
<Btn@Button>:
    size_hint_y: None
    height: dp(50)
    background_normal: ""
    background_color: .91,.74,.33,1
    color: .02,.11,.08,1
    bold: True

<Home>:
    BoxLayout:
        orientation: "vertical"
        padding: dp(18)
        spacing: dp(12)
        ScrollView:
            BoxLayout:
                orientation: "vertical"
                spacing: dp(12)
                size_hint_y: None
                height: self.minimum_height
                Image:
                    source: "assets/icon.png"
                    size_hint_y: None
                    height: dp(90)
                Label:
                    text: "AL-HUDA"
                    font_size: "28sp"
                    bold: True
                    color: .98,.86,.55,1
                    size_hint_y: None
                    height: dp(45)
                Label:
                    text: "السلام عليكم ورحمة الله وبركاته"
                    font_size: "21sp"
                    color: .98,.86,.55,1
                    size_hint_y: None
                    height: dp(48)
                Label:
                    text: "Your complete Islamic companion"
                    color: .96,.95,.90,1
                    size_hint_y: None
                    height: dp(32)
                Btn:
                    text: "📖  Quran Pak"
                    on_release: app.go("quran")
                Btn:
                    text: "📚  Hadith"
                    on_release: app.go("hadith")
                Btn:
                    text: "🕌  Prayer Times"
                    on_release: app.go("prayer")
                Btn:
                    text: "🧭  Qibla Compass"
                    on_release: app.go("qibla")
                Btn:
                    text: "🔎  Universal Search"
                    on_release: app.go("search")
                Btn:
                    text: "🤲  Dua & Azkar"
                    on_release: app.go("dua")
                Btn:
                    text: "📿  Tasbeeh"
                    on_release: app.go("tasbeeh")
                Btn:
                    text: "📅  Islamic & Gregorian Calendar"
                    on_release: app.go("calendar")
                Btn:
                    text: "👤  Login / Register"
                    on_release: app.go("account")
                Btn:
                    text: "⚙️  Settings"
                    on_release: app.go("settings")
'''
Builder.load_string(KV)

class Home(Screen):
    pass

class Feature(Screen):
    title_text=StringProperty("")
    description=StringProperty("")

class ALHudaApp(App):
    title="AL-HUDA"
    def build(self):
        sm=ScreenManager(transition=FadeTransition(duration=.22))
        sm.add_widget(Home(name="home"))
        pages={
            "quran":("Quran Pak","114 Surahs • 30 Paras/Juz • Arabic/Urdu/English foundation"),
            "hadith":("Hadith","Book-wise collections and metadata foundation"),
            "prayer":("Prayer Times","Calculation, countdown and notification foundation"),
            "qibla":("Qibla Compass","GPS and phone-sensor integration foundation"),
            "search":("Universal Search","Quran and Hadith search foundation"),
            "dua":("Dua & Azkar","Islamic supplications foundation"),
            "tasbeeh":("Tasbeeh","Digital counter foundation"),
            "calendar":("Islamic & Gregorian Calendar","Hijri and Gregorian calendar foundation"),
            "account":("Account","Register, email verification, login and reset foundation"),
            "settings":("Settings","Theme, language and notification settings foundation")
        }
        for name,(title,desc) in pages.items():
            s=Feature(name=name,title_text=title,description=desc)
            from kivy.uix.boxlayout import BoxLayout
            from kivy.uix.label import Label
            from kivy.uix.button import Button
            box=BoxLayout(orientation="vertical",padding=18,spacing=16)
            box.add_widget(Label(text=title,color=(.98,.86,.55,1),font_size="27sp"))
            box.add_widget(Label(text=desc,color=(.96,.95,.90,1)))
            box.add_widget(Label(text="Foundation screen — next phase will add real functionality.",
                                 color=(.62,.70,.66,1)))
            box.add_widget(Button(text="← Home",size_hint_y=None,height=50,
                                  background_normal="",background_color=(.91,.74,.33,1),
                                  color=(.02,.11,.08,1),
                                  on_release=lambda *_: self.go("home")))
            s.add_widget(box)
            sm.add_widget(s)
        NavigationService.manager=sm
        return sm
    def go(self,name):
        NavigationService.go(name)

if __name__=="__main__":
    ALHudaApp().run()
