[app]
title = Xpense
package.name = xpense
package.domain = org.example.xpense
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy==2.1.0,kivymd==1.1.1
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.api = 30
android.minapi = 21
android.ndk = 23b
android.private_storage = True
android.skip_update = False
android.accept_sdk_license = True
android.arch = armeabi-v7a
