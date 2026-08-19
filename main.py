from kivy.config import Config
Config.set("graphics","width","420")
Config.set("graphics","height","840")
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen,FadeTransition
from kivy.properties import StringProperty
from app.services.navigation import NavigationService
from app.screens.quran import QuranScreen
from app.screens.hadith import HadithScreen
from app.screens.prayer import PrayerScreen
from app.screens.qibla import QiblaScreen
from app.screens.azan import AzanScreen
from app.screens.calendar import CalendarScreen
from app.screens.dua import DuaScreen
from app.screens.tasbeeh import TasbeehScreen
from app.screens.search import SearchScreen
from app.screens.bookmarks import BookmarkScreen

KV = '''
#:import dp kivy.metrics.dp
<Btn@Button>:
    size_hint_y: None
    height: dp(48)
    background_normal: ""
    background_color: .91,.74,.33,1
    color: .02,.11,.08,1
    bold: True

<Home>:
    BoxLayout:
        orientation: "vertical"
        padding: dp(16)
        spacing: dp(10)
        ScrollView:
            BoxLayout:
                orientation: "vertical"
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height
                Image:
                    source: "assets/icon.png"
                    size_hint_y: None
                    height: dp(82)
                Label:
                    text: "AL-HUDA"
                    font_size: "28sp"
                    bold: True
                    color: .98,.86,.55,1
                    size_hint_y: None
                    height: dp(42)
                Label:
                    text: "السلام عليكم ورحمة الله وبركاته"
                    font_size: "20sp"
                    color: .98,.86,.55,1
                    size_hint_y: None
                    height: dp(45)
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

<BookmarkScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: dp(12)
        spacing: dp(8)
        BoxLayout:
            size_hint_y: None
            height: dp(48)
            spacing: dp(6)
            Btn:
                text: "←"
                size_hint_x: None
                width: dp(48)
                on_release: app.go("home")
            Label:
                text: "BOOKMARKS & HISTORY"
                color: .98,.86,.55,1
                font_size: "18sp"
                bold: True
        BoxLayout:
            size_hint_y: None
            height: dp(44)
            spacing: dp(6)
            Btn:
                text: "Bookmarks"
                on_release: root.set_mode("Bookmarks")
            Btn:
                text: "History"
                on_release: root.set_mode("History")
            Btn:
                text: "Clear History"
                on_release: root.clear_history_items()
        ScrollView:
            Label:
                id: result_label
                text: "No saved items yet."
                color: .92,.94,.92,1
                font_size: "15sp"
                text_size: self.width, None
                valign: "top"
                size_hint_y: None
                height: max(self.texture_size[1], dp(300))
<SearchScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: dp(12)
        spacing: dp(8)
        BoxLayout:
            size_hint_y: None
            height: dp(48)
            spacing: dp(6)
            Btn:
                text: "←"
                size_hint_x: None
                width: dp(48)
                on_release: app.go("home")
            Label:
                text: "UNIVERSAL SEARCH"
                color: .98,.86,.55,1
                font_size: "19sp"
                bold: True
        BoxLayout:
            size_hint_y: None
            height: dp(46)
            spacing: dp(6)
            TextInput:
                id: search_input
                hint_text: "Search Quran, Hadith or Dua"
                multiline: False
                on_text_validate: root.run_search()
            Btn:
                text: "Search"
                size_hint_x: None
                width: dp(78)
                on_release: root.run_search()
            Btn:
                text: "×"
                size_hint_x: None
                width: dp(46)
                on_release: root.clear()
        BoxLayout:
            size_hint_y: None
            height: dp(42)
            spacing: dp(5)
            Btn:
                text: "All"
                on_release: root.set_section("All")
            Btn:
                text: "Quran"
                on_release: root.set_section("Quran")
            Btn:
                text: "Hadith"
                on_release: root.set_section("Hadith")
            Btn:
                text: "Duas"
                on_release: root.set_section("Duas")
        ScrollView:
            Label:
                id: result_label
                text: "Search Quran, Hadith or Duas"
                color: .92,.94,.92,1
                font_size: "15sp"
                text_size: self.width, None
                valign: "top"
                size_hint_y: None
                height: max(self.texture_size[1], dp(300))
<TasbeehScreen>:
    BoxLayout:
        orientation:"vertical"; padding:dp(14); spacing:dp(10)
        Label:
            text:"TASBEEH"; color:.98,.86,.55,1; font_size:"21sp"; bold:True
            size_hint_y:None; height:dp(45)
        Label:
            text:root.dhikr; color:.98,.86,.55,1; font_size:"22sp"; bold:True
            size_hint_y:None; height:dp(40)
        Button:
            id:tap_button
            text:str(root.count)+"\n\nTAP"; font_size:"28sp"
            size_hint_y:None; height:dp(200)
            on_release:root.tap()
        Label:
            text:"%d / %d   •   %d%%"%(root.count,root.target,int(root.progress*100))
            color:.98,.86,.55,1; size_hint_y:None; height:dp(38)
        ProgressBar:
            max:1; value:root.progress; size_hint_y:None; height:dp(12)
        BoxLayout:
            size_hint_y:None; height:dp(45)
            Btn: text:"33"; on_release:root.choose_target(33)
            Btn: text:"99"; on_release:root.choose_target(99)
            Btn: text:"Reset"; on_release:root.reset_count()
        BoxLayout:
            size_hint_y:None; height:dp(45)
            Btn: text:"SubhanAllah"; on_release:root.choose_dhikr("SubhanAllah")
            Btn: text:"Alhamdulillah"; on_release:root.choose_dhikr("Alhamdulillah")
        BoxLayout:
            size_hint_y:None; height:dp(45)
            Btn: text:"Allahu Akbar"; on_release:root.choose_dhikr("Allahu Akbar")
            Btn: text:"La ilaha illallah"; on_release:root.choose_dhikr("La ilaha illallah")
        Btn:
            text:"Vibration: ON" if root.vibration_enabled else "Vibration: OFF"
            size_hint_y:None; height:dp(44); on_release:root.toggle_vibration()
        Label:
            text:root.status; color:.65,.72,.68,1
<DuaScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: dp(12)
        spacing: dp(8)
        BoxLayout:
            size_hint_y: None
            height: dp(48)
            Btn:
                text: "←"
                size_hint_x: None
                width: dp(48)
                on_release: app.go("home")
            Label:
                text: "DUAS & AZKAR"
                color: .98,.86,.55,1
                font_size: "20sp"
                bold: True
        BoxLayout:
            size_hint_y: None
            height: dp(44)
            spacing: dp(6)
            TextInput:
                id: search
                hint_text: "Search Dua / Azkar"
                multiline: False
                on_text_validate: root.refresh()
            Btn:
                text: "Search"
                size_hint_x: None
                width: dp(75)
                on_release: root.refresh()
        Label:
            text: str(root.count) + " duas"
            size_hint_y: None
            height: dp(28)
            color: .62,.70,.66,1
        ScrollView:
            Label:
                id: results
                text: ""
                color: .92,.94,.92,1
                font_size: "16sp"
                text_size: self.width, None
                halign: "right"
                valign: "top"
                size_hint_y: None
                height: self.texture_size[1] + dp(20)
<CalendarScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: dp(12)
        spacing: dp(8)
        BoxLayout:
            size_hint_y: None
            height: dp(48)
            spacing: dp(6)
            Btn:
                text: "←"
                size_hint_x: None
                width: dp(48)
                on_release: app.go("home")
            Label:
                text: "ISLAMIC CALENDAR"
                color: .98,.86,.55,1
                font_size: "20sp"
                bold: True
        Label:
            text: root.hijri
            color: .98,.86,.55,1
            size_hint_y: None
            height: dp(32)
        BoxLayout:
            size_hint_y: None
            height: dp(46)
            Btn:
                text: "‹"
                on_release: root.previous()
            Label:
                text: root.title
                color: .98,.95,.90,1
                bold: True
            Btn:
                text: "›"
                on_release: root.next()
        GridLayout:
            cols: 7
            size_hint_y: None
            height: dp(32)
            Label: text: "Sun"
            Label: text: "Mon"
            Label: text: "Tue"
            Label: text: "Wed"
            Label: text: "Thu"
            Label: text: "Fri"
            Label: text: "Sat"
        Label:
            id: days
            text: ""
            color: .90,.93,.90,1
            font_size: "16sp"
            halign: "center"
            valign: "top"
            text_size: self.size
        Btn:
            text: "TODAY"
            size_hint_y: None
            height: dp(46)
            on_release: root.today()
<AzanScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: dp(16)
        spacing: dp(12)
        Label:
            text: "AZAN & NOTIFICATIONS"
            color: .98,.86,.55,1
            font_size: "21sp"
            bold: True
            size_hint_y: None
            height: dp(48)
        Label:
            text: root.status
            color: .78,.82,.79,1
            text_size: self.width,None
        Btn:
            text: "Disable Notifications" if root.enabled else "Enable Notifications"
            size_hint_y: None
            height: dp(50)
            on_release: root.toggle()
        Btn:
            text: "STOP ACTIVE AZAN"
            size_hint_y: None
            height: dp(50)
            on_release: root.stop_azan()
        Label:
            text: "Step 6 adds the notification/control foundation. Final background audio receiver is part of the Android packaging pass."
            color: .55,.62,.58,1
            text_size: self.width,None
<QiblaScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: dp(12)
        spacing: dp(8)
        BoxLayout:
            size_hint_y: None
            height: dp(48)
            Btn:
                text: "←"
                size_hint_x: None
                width: dp(48)
                on_release: app.go("home")
            Label:
                text: "LIVE QIBLA"
                color: .98,.86,.55,1
                font_size: "21sp"
                bold: True
        Label:
            text: root.status
            size_hint_y: None
            height: dp(35)
            color: .98,.86,.55,1
        Label:
            id: needle
            text: "▲"
            font_size: "80sp"
            color: .98,.86,.55,1
        Label:
            text: "Turn your phone until the indicator points toward Qibla."
            color: .70,.76,.72,1
            text_size: self.width,None
        Label:
            text: root.sensor_status
            color: .62,.70,.66,1
        BoxLayout:
            size_hint_y: None
            height: dp(45)
            spacing: dp(6)
            TextInput:
                id: latitude
                text: "31.5204"
                hint_text: "Latitude"
                multiline: False
            TextInput:
                id: longitude
                text: "74.3587"
                hint_text: "Longitude"
                multiline: False
            Btn:
                text: "Set"
                size_hint_x: None
                width: dp(62)
                on_release: root.calculate()
        Label:
            text: "Bearing: %.1f°   Heading: %.1f°   Turn: %.1f°" % (root.bearing,root.heading,root.relative)
            color: .80,.84,.81,1
<PrayerScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: dp(12)
        spacing: dp(8)
        BoxLayout:
            size_hint_y: None
            height: dp(48)
            spacing: dp(6)
            Btn:
                text: "←"
                size_hint_x: None
                width: dp(48)
                on_release: app.go("home")
            Label:
                text: "PRAYER TIMES"
                color: .98,.86,.55,1
                font_size: "21sp"
                bold: True
        BoxLayout:
            size_hint_y: None
            height: dp(44)
            spacing: dp(6)
            TextInput:
                id: city
                hint_text: "City"
                multiline: False
            TextInput:
                id: country
                hint_text: "Country"
                multiline: False
            Btn:
                text: "Load"
                size_hint_x: None
                width: dp(72)
                on_release: root.load()
        Label:
            text: root.status
            size_hint_y: None
            height: dp(28)
            color: .62,.70,.66,1
        Label:
            text: root.next_prayer
            size_hint_y: None
            height: dp(34)
            color: .98,.86,.55,1
            font_size: "18sp"
        Label:
            text: root.countdown
            size_hint_y: None
            height: dp(54)
            color: .98,.95,.90,1
            font_size: "28sp"
            bold: True
        GridLayout:
            cols: 2
            spacing: dp(6)
            row_default_height: dp(55)
            Label: text: "Fajr"; color: .98,.95,.90,1
            Label: id: fajr; text: "--"; color: .98,.86,.55,1
            Label: text: "Sunrise"; color: .98,.95,.90,1
            Label: id: sunrise; text: "--"; color: .98,.86,.55,1
            Label: text: "Dhuhr"; color: .98,.95,.90,1
            Label: id: dhuhr; text: "--"; color: .98,.86,.55,1
            Label: text: "Asr"; color: .98,.95,.90,1
            Label: id: asr; text: "--"; color: .98,.86,.55,1
            Label: text: "Maghrib"; color: .98,.95,.90,1
            Label: id: maghrib; text: "--"; color: .98,.86,.55,1
            Label: text: "Isha"; color: .98,.95,.90,1
            Label: id: isha; text: "--"; color: .98,.86,.55,1
<HadithScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: dp(10)
        spacing: dp(8)
        BoxLayout:
            size_hint_y: None
            height: dp(48)
            spacing: dp(6)
            Btn:
                text: "←"
                size_hint_x: None
                width: dp(48)
                on_release: app.go("home")
            Label:
                text: "HADITH"
                color: .98,.86,.55,1
                font_size: "22sp"
                bold: True
        TextInput:
            id: search
            hint_text: "Search Hadith / حدیث تلاش کریں"
            size_hint_y: None
            height: dp(44)
            multiline: False
            on_text_validate: root.search()
        BoxLayout:
            size_hint_y: None
            height: dp(44)
            Btn:
                text: "Books"
                on_release: root.show_books()
            Btn:
                text: "Search"
                on_release: root.search()
        Label:
            text: root.status
            size_hint_y: None
            height: dp(28)
            color: .62,.70,.66,1
        ScrollView:
            do_scroll_x: False
            GridLayout:
                id: content
                cols: 1
                spacing: dp(7)
                size_hint_y: None
                height: self.minimum_height

<QuranScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: dp(10)
        spacing: dp(8)
        BoxLayout:
            size_hint_y: None
            height: dp(48)
            spacing: dp(6)
            Btn:
                text: "←"
                size_hint_x: None
                width: dp(48)
                on_release: app.go("home")
            Label:
                text: "QURAN PAK"
                color: .98,.86,.55,1
                font_size: "22sp"
                bold: True
        TextInput:
            id: search
            hint_text: "Search Quran / قرآن تلاش کریں"
            size_hint_y: None
            height: dp(44)
            multiline: False
            on_text_validate: root.search()
        BoxLayout:
            size_hint_y: None
            height: dp(44)
            spacing: dp(6)
            Btn:
                text: "114 Surahs"
                on_release: root.show_surah_list()
            Btn:
                text: "30 Juz"
                on_release: root.show_juz_list()
            Btn:
                text: "Search"
                on_release: root.search()
        Label:
            text: root.status
            size_hint_y: None
            height: dp(28)
            color: .62,.70,.66,1
        ScrollView:
            do_scroll_x: False
            GridLayout:
                id: content
                cols: 1
                spacing: dp(7)
                size_hint_y: None
                height: self.minimum_height
'''
Builder.load_string(KV)

class Home(Screen): pass
class Feature(Screen):
    title_text=StringProperty("")
    description=StringProperty("")

class ALHudaApp(App):
    title="AL-HUDA"
    def build(self):
        sm=ScreenManager(transition=FadeTransition(duration=.22))
        sm.add_widget(Home(name="home"))
        sm.add_widget(QuranScreen(name="quran"))
        sm.add_widget(HadithScreen(name="hadith"))
        sm.add_widget(PrayerScreen(name="prayer"))
        sm.add_widget(QiblaScreen(name="qibla"))
        sm.add_widget(AzanScreen(name="azan"))
        sm.add_widget(CalendarScreen(name="calendar"))
        sm.add_widget(DuaScreen(name="dua"))
        sm.add_widget(TasbeehScreen(name="tasbeeh"))
        sm.add_widget(SearchScreen(name="search"))
        sm.add_widget(BookmarkScreen(name="bookmarks"))
        pages={
            "hadith":("Hadith","Book-wise collections • metadata foundation"),
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
            box.add_widget(Label(text="This module will be implemented in its own step.",color=(.62,.70,.66,1)))
            box.add_widget(Button(text="← Home",size_hint_y=None,height=50,
                                  background_normal="",background_color=(.91,.74,.33,1),
                                  color=(.02,.11,.08,1),
                                  on_release=lambda *_: self.go("home")))
            s.add_widget(box); sm.add_widget(s)
        NavigationService.manager=sm
        return sm
    def go(self,name): NavigationService.go(name)

if __name__=="__main__":
    ALHudaApp().run()
