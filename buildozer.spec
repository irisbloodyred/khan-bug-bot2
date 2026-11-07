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

[buildozer]
log_level = 2
warn_on_root = 1
