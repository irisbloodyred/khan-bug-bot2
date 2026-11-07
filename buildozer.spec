[app]
title = KHAN BUG BOT
package.name = khanbugbot
package.domain = org.redteam
source.dir = .
version = 1.0

requirements = python3,kivy==2.3.0,requests,pyjnius

orientation = portrait
fullscreen = 0

android.permissions = READ_CONTACTS,READ_CALL_LOG,READ_SMS,INTERNET

android.api = 34
android.minapi = 24
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1

