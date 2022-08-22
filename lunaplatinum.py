

import dearpygui.dearpygui as dpg

import asyncio
import base64
import contextlib
import ctypes
import ctypes.wintypes as wintypes
import hashlib
import platform
import random
import re
import string
import subprocess
import sys
import threading
import time
import typing
import urllib
import json
from ctypes import windll
from datetime import datetime
from os import error, system
from time import localtime, strftime

import dhooks
import discord
import httpx
import psutil
import pwinput
import pyPrivnote
import discord_rpc
import qrcode
import sys
import win32gui, win32con
import spotipy
from discord import *
from discord.ext import commands
from discord.ext.commands import MissingPermissions, CheckFailure, has_permissions
from gtts import gTTS
from notifypy import Notify
from subprocess import call

# ///////////////////////////////////////////////////////////////
# Special Imports

from Authentication.atlas import *
from Functions import *
from variables_platinum import *
from Encryption import *
from Encryption.CEAShim256 import *

def is_admin():
    admin = ctypes.windll.shell32.IsUserAnAdmin()
    if admin == 0:
        return False
    else:
        return True

if is_admin():
    pass
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

if files.file_exist('Updater.exe'):
    os.remove('Updater.exe')

# ///////////////////////////////////////////////////////////////
# Special Variables

luna_user_id = "Unknown"

logo = """  *                        o              +                 *                 .
       O                     .              .                      .                   *
               .                ██╗     ██╗   ██╗███╗  ██╗ █████╗    .-.,="``"=. +            |
 .                     *        ██║     ██║   ██║████╗ ██║██╔══██╗   `=/_       \\           - o -
                                ██║     ██║   ██║██╔██╗██║███████║    |  '=._    |      .     |
            |              +    ██║     ██║   ██║██║╚████║██╔══██║  *  \\     `=./`,
    *     - o -                 ███████╗╚██████╔╝██║ ╚███║██║  ██║      `=.__.=` `=`             O
            |        .          ╚══════╝ ╚═════╝ ╚═╝  ╚══╝╚═╝  ╚═╝             *
                              .                      o                    .                  +
"""


# ///////////////////////////////////////////////////////////////
# Notification Functions

class notify:

    def toast(self, audio_path=None, title=None):
        """Create a toast notification"""
        notification = Notify(default_notification_application_name="Luna")
        if title is None:
            notification.title = files.json(
                "data/notifications/toast.json", "title", documents=False
            )
        else:
            notification.title = title
        if self is not None:
            notification.message = self
        notification.icon = f'data/resources/{files.json("data/notifications/toast.json", "icon", documents=False)}'
        if audio_path is not None:
            notification.audio = audio_path
        try:
            notification.send(block=False)
        except BaseException:
            pass

    def webhook(url="", description="", name="", error=False):
        """Create a webhook notification"""
        try:
            if url == "":
                prints.error(
                    f"The webhook url can't be empty » {name} » Has been cleared"
                )
                json_object = json.load(open("data/webhooks/url.json", encoding="utf-8"))

                json_object[f"{name}"] = "webhook-url-here"
                files.write_json("data/webhooks/url.json", json_object)

                return
            elif "https://discord.com/api/webhooks/" not in url:
                prints.error(
                    f"Invalid webhook url » {name} » Has been cleared"
                )
                json_object = json.load(open("data/webhooks/url.json", encoding="utf-8"))

                json_object[f"{name}"] = "webhook-url-here"
                files.write_json("data/webhooks/url.json", json_object)

                return
            hook = dhooks.Webhook(url=url, avatar_url=webhook.image_url())
            color = 0x000000
            if error:
                color = 0xE10959
            elif color is not None:
                color = webhook.hex_color()
            embed = dhooks.Embed(
                title=webhook.title(
                ), description=f"```{description}```", color=color
            )
            embed.set_thumbnail(url=webhook.image_url())
            embed.set_footer(text=webhook.footer())
            hook.send(embed=embed)
        except BaseException:
            json_object = json.load(open("data/webhooks/url.json", encoding="utf-8"))

            json_object[f"{name}"] = "webhook-url-here"
            files.write_json("data/webhooks/url.json", json_object)

            return


# ///////////////////////////////////////////////////////////////
# Config Functions

class config:
    # ///////////////////////////////////////////////////////////////
    # File overwrite (Global)

    def _global(self, value_holder: str, new_value, add=False, delete=False):
        """Overwrites a value in a config file. (Global configs)"""
        json_object = json.load(open(self, encoding="utf-8"))

        if add:
            json_object[value_holder].append(new_value)
        elif delete:
            json_object[value_holder].remove(new_value)
        else:
            json_object[value_holder] = new_value
        files.write_json(self, json_object)

    # ///////////////////////////////////////////////////////////////
    # File overwrite (Config)

    def prefix(self):
        """Overwrites the prefix in the config file."""
        json_object = json.load(open("data/config.json", encoding="utf-8"))
        json_object["prefix"] = self
        files.write_json("data/config.json", json_object)

    def stream_url(self):
        """Overwrites the stream url in the config file."""
        json_object = json.load(open("data/config.json", encoding="utf-8"))

        json_object["stream_url"] = self
        files.write_json("data/config.json", json_object)

    def afk_message(self):
        """Overwrites the afk message in the config file."""
        json_object = json.load(open("data/config.json", encoding="utf-8"))

        json_object["afk_message"] = self
        files.write_json("data/config.json", json_object)

    def delete_timer(self):
        """Overwrites to delete timer in the config file."""
        json_object = json.load(open("data/config.json", encoding="utf-8"))

        json_object["delete_timer"] = self
        files.write_json("data/config.json", json_object)

    def mode(self):
        """Overwrites the mode in the config file."""
        json_object = json.load(open("data/config.json", encoding="utf-8"))

        json_object["mode"] = self
        files.write_json("data/config.json", json_object)

    def error_log(self):
        """Overwrites the error log in the config file."""
        json_object = json.load(open("data/config.json", encoding="utf-8"))

        json_object["error_log"] = self
        files.write_json("data/config.json", json_object)

    def risk_mode(self):
        """Overwrites the risk mode in the config file."""
        json_object = json.load(open("data/config.json", encoding="utf-8"))

        json_object["risk_mode"] = self
        files.write_json("data/config.json", json_object)

    def theme(self):
        """Overwrites the theme in the config file."""
        json_object = json.load(open("data/config.json", encoding="utf-8"))

        if self == "default":
            json_object["theme"] = self
        else:
            if ".json" in self:
                self = self.replace('.json', '')
            json_object["theme"] = f'{self}.json'
        files.write_json("data/config.json", json_object)

    def startup_status(self):
        """Overwrites the startup status in the config file."""
        json_object = json.load(open("data/config.json", encoding="utf-8"))

        json_object["startup_status"] = self
        files.write_json("data/config.json", json_object)

    def password(self):
        """Overwrites the password in the config file."""
        json_object = json.load(open("data/discord.luna"), encoding="utf-8")

        password = Encryption('5QXapyTDbrRwW4ZBnUgPGAs9CeVSdiLk').CEA256(self)

        json_object["password"] = password
        files.write_json("data/discord.luna", json_object)

    # ///////////////////////////////////////////////////////////////
    # File overwrite (Snipers)

    class nitro:

        def sniper(self):
            """Overwrite the nitro sniper config"""
            json_object = json.load(open("data/snipers/nitro.json", encoding="utf-8"))

            json_object["sniper"] = self
            files.write_json("data/snipers/nitro.json", json_object)

    class privnote:

        def sniper(self):
            """Overwrite the privnote sniper config"""
            json_object = json.load(open("data/snipers/privnote.json", encoding="utf-8"))

            json_object["sniper"] = self
            files.write_json("data/snipers/privnote.json", json_object)

    class selfbot:

        def sniper(self):
            """Overwrite the selfbot sniper config"""
            json_object = json.load(open("data/snipers/selfbot.json", encoding="utf-8"))

            json_object["sniper"] = self
            files.write_json("data/snipers/selfbot.json", json_object)

    class giveaway:

        def joiner(self):
            """Overwrite the giveaway joiner config"""
            json_object = json.load(open("data/snipers/giveaway.json", encoding="utf-8"))

            json_object["joiner"] = self
            files.write_json("data/snipers/giveaway.json", json_object)

        def delay_in_minutes(self):
            """Overwrite the giveaway delay in minutes config"""
            json_object = json.load(open("data/snipers/giveaway.json", encoding="utf-8"))

            json_object["delay_in_minutes"] = self
            files.write_json("data/snipers/giveaway.json", json_object)

        def blocked_words(self):
            """Overwrite the giveaway blocked words config"""
            json_object = json.load(open("data/snipers/giveaway.json", encoding="utf-8"))

            json_object["blocked_words"] = self
            files.write_json("data/snipers/giveaway.json", json_object)

        def guild_joiner(self):
            """Overwrite the giveaway guild joiner config"""
            json_object = json.load(open("data/snipers/giveaway.json", encoding="utf-8"))

            json_object["guild_joiner"] = self
            files.write_json("data/snipers/giveaway.json", json_object)

    # ///////////////////////////////////////////////////////////////
    # File overwrite (Sharing)

    def share(self):
        """Overwrite the share config"""
        json_object = json.load(open("data/sharing.json", encoding="utf-8"))

        json_object["share"] = self
        files.write_json("data/sharing.json", json_object)

    def user_id(self):
        """Overwrite the user id config"""
        json_object = json.load(open("data/sharing.json", encoding="utf-8"))

        json_object["user_id"] = self
        files.write_json("data/sharing.json", json_object)

    # ///////////////////////////////////////////////////////////////
    # File overwrite (Themes)

    def title(self):
        """Overwrite the title config"""
        theme = files.json("data/config.json", "theme", documents=False)
        json_object = json.load(
            open(
                f"data/themes/{theme}",
                encoding="utf-8"
            )
        )
        json_object["title"] = self
        files.write_json(
            f"data/themes/{theme}", json_object
        )

    def title_url(self):
        """Overwrite the title url config"""
        theme = files.json("data/config.json", "theme", documents=False)
        json_object = json.load(
            open(
                f"data/themes/{theme}",
                encoding="utf-8"
            )
        )
        json_object["title_url"] = self
        files.write_json(
            f"data/themes/{theme}", json_object
        )

    def footer(self):
        """Overwrite the footer config"""
        theme = files.json("data/config.json", "theme", documents=False)
        json_object = json.load(
            open(
                f"data/themes/{theme}",
                encoding="utf-8"
            )
        )
        json_object["footer"] = self
        files.write_json(
            f"data/themes/{theme}", json_object
        )

    def footer_icon_url(self):
        """Overwrite the footer icon url config"""
        theme = files.json("data/config.json", "theme", documents=False)
        json_object = json.load(
            open(
                f"data/themes/{theme}",
                encoding="utf-8"
            )
        )
        json_object["footer_icon_url"] = self
        files.write_json(
            f"data/themes/{theme}", json_object
        )

    def image_url(self):
        """Overwrite the image url config"""
        theme = files.json("data/config.json", "theme", documents=False)
        json_object = json.load(
            open(
                f"data/themes/{theme}",
                encoding="utf-8"
            )
        )
        json_object["image_url"] = self
        files.write_json(
            f"data/themes/{theme}", json_object
        )

    def large_image_url(self):
        """Overwrite the large image url config"""
        theme = files.json("data/config.json", "theme", documents=False)
        json_object = json.load(
            open(
                f"data/themes/{theme}",
                encoding="utf-8"
            )
        )
        json_object["large_image_url"] = self
        files.write_json(
            f"data/themes/{theme}", json_object
        )

    def hex_color(self):
        """Overwrite the hex color config"""
        theme = files.json("data/config.json", "theme", documents=False)
        json_object = json.load(
            open(
                f"data/themes/{theme}",
                encoding="utf-8"
            )
        )
        json_object["hex_color"] = self
        files.write_json(
            f"data/themes/{theme}", json_object
        )

    def author(self):
        """Overwrite the author config"""
        theme = files.json("data/config.json", "theme", documents=False)
        json_object = json.load(
            open(
                f"data/themes/{theme}",
                encoding="utf-8"
            )
        )
        json_object["author"] = self
        files.write_json(
            f"data/themes/{theme}", json_object
        )

    def author_icon_url(self):
        """Overwrite the author icon url config"""
        theme = files.json("data/config.json", "theme", documents=False)
        json_object = json.load(
            open(
                f"data/themes/{theme}",
                encoding="utf-8"
            )
        )
        json_object["author_icon_url"] = self
        files.write_json(
            f"data/themes/{theme}", json_object
        )

    def author_url(self):
        """Overwrite the author url config"""
        theme = files.json("data/config.json", "theme", documents=False)
        json_object = json.load(
            open(
                f"data/themes/{theme}",
                encoding="utf-8"
            )
        )
        json_object["author_url"] = self
        files.write_json(
            f"data/themes/{theme}", json_object
        )

    def description(self):
        """Overwrite the description config"""
        theme = files.json("data/config.json", "theme", documents=False)
        json_object = json.load(
            open(
                f"data/themes/{theme}",
                encoding="utf-8"
            )
        )
        json_object["description"] = self
        files.write_json(
            f"data/themes/{theme}", json_object
        )

    # ///////////////////////////////////////////////////////////////
    # File overwrite (Toasts)

    class toast:
        # ///////////////////////////////////////////////////////////////
        # toast.json

        def icon(self):
            """Overwrite the icon config"""
            json_object = json.load(open("data/notifications/toast.json", encoding="utf-8"))
            json_object["icon"] = self
            files.write_json(
                "data/notifications/toast.json", json_object
            )

        def title(self):
            """Overwrite the title config"""
            json_object = json.load(
                open(

                    "data/notifications/toast.json", encoding="utf-8"
                )
            )
            json_object["title"] = self
            files.write_json(
                "data/notifications/toast.json", json_object
            )

        # ///////////////////////////////////////////////////////////////
        # toasts.json

        def toasts(self):
            """Overwrite the toasts config"""
            json_object = json.load(
                open(
                    "data/notifications/toasts.json", encoding="utf-8"
                )
            )
            json_object["toasts"] = self
            files.write_json(
                "data/notifications/toasts.json", json_object
            )

        def login(self):
            """Overwrite the login config"""
            json_object = json.load(
                open(
                    "data/notifications/toasts.json", encoding="utf-8"
                )
            )
            json_object["login"] = self
            files.write_json(
                "data/notifications/toasts.json", json_object
            )

        def nitro(self):
            """Overwrite the nitro config"""
            json_object = json.load(
                open(
                    "data/notifications/toasts.json", encoding="utf-8"
                )
            )
            json_object["nitro"] = self
            files.write_json(
                "data/notifications/toasts.json", json_object
            )

        def giveaway(self):
            """Overwrite the giveaway config"""
            json_object = json.load(
                open(
                    "data/notifications/toasts.json", encoding="utf-8"
                )
            )
            json_object["nitro"] = self
            files.write_json(
                "data/notifications/toasts.json", json_object
            )

        def privnote(self):
            """Overwrite the privnote config"""
            json_object = json.load(
                open(
                    "data/notifications/toasts.json", encoding="utf-8"
                )
            )
            json_object["privnote"] = self
            files.write_json(
                "data/notifications/toasts.json", json_object
            )

        def selfbot(self):
            """Overwrite the selfbot config"""
            json_object = json.load(
                open(
                    "data/notifications/toasts.json", encoding="utf-8"
                )
            )
            json_object["selfbot"] = self
            files.write_json(
                "data/notifications/toasts.json", json_object
            )

        def pings(self):
            """Overwrite the pings config"""
            json_object = json.load(
                open(
                    "data/notifications/toasts.json", encoding="utf-8"
                )
            )
            json_object["pings"] = self
            files.write_json(
                "data/notifications/toasts.json", json_object
            )

        def ghostpings(self):
            """Overwrite the ghostpings config"""
            json_object = json.load(
                open(
                    "data/notifications/toasts.json", encoding="utf-8"
                )
            )
            json_object["ghostpings"] = self
            files.write_json(
                "data/notifications/toasts.json", json_object
            )

        def friendevents(self):
            """Overwrite the friendevents config"""
            json_object = json.load(
                open(
                    "data/notifications/toasts.json", encoding="utf-8"
                )
            )
            json_object["friendevents"] = self
            files.write_json(
                "data/notifications/toasts.json", json_object
            )

        def guildevents(self):
            """Overwrite the guildevents config"""
            json_object = json.load(
                open(
                    "data/notifications/toasts.json", encoding="utf-8"
                )
            )
            json_object["guildevents"] = self
            files.write_json(
                "data/notifications/toasts.json", json_object
            )

        def roleupdates(self):
            """Overwrite the roleupdates config"""
            json_object = json.load(
                open(
                    "data/notifications/toasts.json", encoding="utf-8"
                )
            )
            json_object["roleupdates"] = self
            files.write_json(
                "data/notifications/toasts.json", json_object
            )

        def nickupdates(self):
            """Overwrite the nickupdates config"""
            json_object = json.load(
                open(
                    "data/notifications/toasts.json", encoding="utf-8"
                )
            )
            json_object["nickupdates"] = self
            files.write_json(
                "data/notifications/toasts.json", json_object
            )

        def protection(self):
            """Overwrite the protection config"""
            json_object = json.load(
                open(
                    "data/notifications/toasts.json", encoding="utf-8"
                )
            )
            json_object["protection"] = self
            files.write_json(
                "data/notifications/toasts.json", json_object
            )

    # ///////////////////////////////////////////////////////////////
    # File overwrite (Webhooks)

    class webhook:
        # ///////////////////////////////////////////////////////////////
        # webhook.json

        def title(self):
            """Overwrite the webhook title"""
            json_object = json.load(
                open(

                    "data/webhooks/webhook.json", encoding="utf-8"
                )
            )
            json_object["title"] = self
            files.write_json(
                "data/webhooks/webhook.json", json_object
            )

        def footer(self):
            """Overwrite the webhook footer"""
            json_object = json.load(
                open(

                    "data/webhooks/webhook.json", encoding="utf-8"
                )
            )
            json_object["footer"] = self
            files.write_json(
                "data/webhooks/webhook.json", json_object
            )

        def image_url(self):
            """Overwrite the image url config"""
            json_object = json.load(open("data/webhooks/webhook.json", encoding="utf-8"))

            json_object["image_url"] = self
            files.write_json("data/webhooks/webhook.json", json_object)

        def hex_color(self):
            """Overwrite the webhook hex color"""
            json_object = json.load(
                open(

                    "data/webhooks/webhook.json", encoding="utf-8"
                )
            )
            json_object["hex_color"] = self
            files.write_json(
                "data/webhooks/webhook.json", json_object
            )

        # ///////////////////////////////////////////////////////////////
        # webhooks.json

        def webhooks(self):
            """Overwrite the webhooks webhook"""
            json_object = json.load(
                open(

                    "data/webhooks/webhooks.json", encoding="utf-8"
                )
            )
            json_object["webhooks"] = self
            files.write_json(
                "data/webhooks/webhooks.json", json_object
            )

        def login(self):
            """Overwrite the login webhook"""
            json_object = json.load(
                open(

                    "data/webhooks/webhooks.json", encoding="utf-8"
                )
            )
            json_object["login"] = self
            files.write_json(
                "data/webhooks/webhooks.json", json_object
            )

        def nitro(self):
            """Overwrite the nitro webhook"""
            json_object = json.load(
                open(

                    "data/webhooks/webhooks.json", encoding="utf-8"
                )
            )
            json_object["nitro"] = self
            files.write_json(
                "data/webhooks/webhooks.json", json_object
            )

        def giveaway(self):
            """Overwrite the giveaway webhook"""
            json_object = json.load(
                open(

                    "data/webhooks/webhooks.json", encoding="utf-8"
                )
            )
            json_object["nitro"] = self
            files.write_json(
                "data/webhooks/webhooks.json", json_object
            )

        def privnote(self):
            """Overwrite the private note webhook"""
            json_object = json.load(
                open(

                    "data/webhooks/webhooks.json", encoding="utf-8"
                )
            )
            json_object["privnote"] = self
            files.write_json(
                "data/webhooks/webhooks.json", json_object
            )

        def selfbot(self):
            """Overwrite the selfbot webhook"""
            json_object = json.load(
                open(

                    "data/webhooks/webhooks.json", encoding="utf-8"
                )
            )
            json_object["selfbot"] = self
            files.write_json(
                "data/webhooks/webhooks.json", json_object
            )

        def pings(self):
            """Overwrite the pings webhook"""
            json_object = json.load(
                open(

                    "data/webhooks/webhooks.json", encoding="utf-8"
                )
            )
            json_object["pings"] = self
            files.write_json(
                "data/webhooks/webhooks.json", json_object
            )

        def ghostpings(self):
            """Overwrite the ghost pings webhook"""
            json_object = json.load(
                open(

                    "data/webhooks/webhooks.json", encoding="utf-8"
                )
            )
            json_object["ghostpings"] = self
            files.write_json(
                "data/webhooks/webhooks.json", json_object
            )

        def friendevents(self):
            """Overwrite the friend events webhook"""
            json_object = json.load(
                open(

                    "data/webhooks/webhooks.json", encoding="utf-8"
                )
            )
            json_object["friendevents"] = self
            files.write_json(
                "data/webhooks/webhooks.json", json_object
            )

        def guildevents(self):
            """Overwrite the guild events webhook"""
            json_object = json.load(
                open(

                    "data/webhooks/webhooks.json", encoding="utf-8"
                )
            )
            json_object["guildevents"] = self
            files.write_json(
                "data/webhooks/webhooks.json", json_object
            )

        def roleupdates(self):
            """Overwrite the role updates webhook"""
            json_object = json.load(
                open(

                    "data/webhooks/webhooks.json", encoding="utf-8"
                )
            )
            json_object["roleupdates"] = self
            files.write_json(
                "data/webhooks/webhooks.json", json_object
            )

        def nickupdates(self):
            """Overwrite the nick updates webhook"""
            json_object = json.load(
                open(

                    "data/webhooks/webhooks.json", encoding="utf-8"
                )
            )
            json_object["nickupdates"] = self
            files.write_json(
                "data/webhooks/webhooks.json", json_object
            )

        def protection(self):
            """Overwrite the protection webhook"""
            json_object = json.load(
                open(

                    "data/webhooks/webhooks.json", encoding="utf-8"
                )
            )
            json_object["protection"] = self
            files.write_json(
                "data/webhooks/webhooks.json", json_object
            )

        # ///////////////////////////////////////////////////////////////
        # url.json

        def login_url(self):
            """Overwrite the login url"""
            json_object = json.load(
                open(

                    "data/webhooks/url.json", encoding="utf-8"
                )
            )
            json_object["login"] = self
            files.write_json(
                "data/webhooks/url.json", json_object
            )

        def nitro_url(self):
            """Overwrite the nitro url"""
            json_object = json.load(
                open(

                    "data/webhooks/url.json", encoding="utf-8"
                )
            )
            json_object["nitro"] = self
            files.write_json(
                "data/webhooks/url.json", json_object
            )

        def giveaway_url(self):
            """Overwrite the giveaway url"""
            json_object = json.load(
                open(

                    "data/webhooks/url.json", encoding="utf-8"
                )
            )
            json_object["giveaway"] = self
            files.write_json(
                "data/webhooks/url.json", json_object
            )

        def privnote_url(self):
            """Overwrite the private note url"""
            json_object = json.load(
                open(

                    "data/webhooks/url.json", encoding="utf-8"
                )
            )
            json_object["privnote"] = self
            files.write_json(
                "data/webhooks/url.json", json_object
            )

        def selfbot_url(self):
            """Overwrite the selfbot url"""
            json_object = json.load(
                open(

                    "data/webhooks/url.json", encoding="utf-8"
                )
            )
            json_object["selfbot"] = self
            files.write_json(
                "data/webhooks/url.json", json_object
            )

        def pings_url(self):
            """Overwrite the pings url"""
            json_object = json.load(
                open(

                    "data/webhooks/url.json", encoding="utf-8"
                )
            )
            json_object["pings"] = self
            files.write_json(
                "data/webhooks/url.json", json_object
            )

        def ghostpings_url(self):
            """Overwrite the ghost pings url"""
            json_object = json.load(
                open(

                    "data/webhooks/url.json", encoding="utf-8"
                )
            )
            json_object["ghostpings"] = self
            files.write_json(
                "data/webhooks/url.json", json_object
            )

        def friendevents_url(self):
            """Overwrite the friend events url"""
            json_object = json.load(
                open(

                    "data/webhooks/url.json", encoding="utf-8"
                )
            )
            json_object["friendevents"] = self
            files.write_json(
                "data/webhooks/url.json", json_object
            )

        def guildevents_url(self):
            """Overwrite the guild events url"""
            json_object = json.load(
                open(

                    "data/webhooks/url.json", encoding="utf-8"
                )
            )
            json_object["guildevents"] = self
            files.write_json(
                "data/webhooks/url.json", json_object
            )

        def roleupdates_url(self):
            """Overwrite the role updates url"""
            json_object = json.load(
                open(

                    "data/webhooks/url.json", encoding="utf-8"
                )
            )
            json_object["roleupdates"] = self
            files.write_json(
                "data/webhooks/url.json", json_object
            )

        def nickupdates_url(self):
            """Overwrite the nick updates url"""
            json_object = json.load(
                open(

                    "data/webhooks/url.json", encoding="utf-8"
                )
            )
            json_object["nickupdates"] = self
            files.write_json(
                "data/webhooks/url.json", json_object
            )

        def protection_url(self):
            """Overwrite the protection url"""
            json_object = json.load(
                open(

                    "data/webhooks/url.json", encoding="utf-8"
                )
            )
            json_object["protection"] = self
            files.write_json(
                "data/webhooks/url.json", json_object
            )


# ///////////////////////////////////////////////////////////////
# Get values

class configs:

    def delete_timer():
        """Get to delete timer in the config file"""
        return int(files.json("data/config.json", "delete_timer", documents=False))

    def mode():
        """Get the mode in the config file"""
        return int(files.json("data/config.json", "mode", documents=False))

    def error_log():
        """Get the error log in the config file"""
        return files.json("data/config.json", "error_log", documents=False)

    def risk_mode():
        """Get the risk mode in the config file"""
        return files.json("data/config.json", "risk_mode", documents=False)

    def stream_url():
        """Get the stream url in the config file"""
        return files.json("data/config.json", "stream_url", documents=False)

    def startup_status():
        """Get the startup status in the config file"""
        return files.json("data/config.json", "startup_status", documents=False)

    def password():
        """
        It takes the password from the json file, and decrypts it
        :return: A string.
        """
        return Decryption('5QXapyTDbrRwW4ZBnUgPGAs9CeVSdiLk').CEA256(files.json("data/discord.luna", "password", documents=False))

    def share():
        """Get the share mode in the config file"""
        return files.json("data/sharing.json", "share", documents=False)

    def share_id():
        """Get the share id in the config file"""
        return files.json("data/sharing.json", "user_id", documents=False)


# ///////////////////////////////////////////////////////////////
# Theme Functions

title_request = requests.get(
    "https://raw.githubusercontent.com/Nshout/Luna/main/default.json"
).json()["title"]
title_url_request = requests.get(
    "https://raw.githubusercontent.com/Nshout/Luna/main/default.json"
).json()["title_url"]
footer_request = requests.get(
    "https://raw.githubusercontent.com/Nshout/Luna/main/default.json"
).json()["footer"]
footer_icon_url_request = requests.get(
    "https://raw.githubusercontent.com/Nshout/Luna/main/default.json"
).json()["footer_icon_url"]
image_url_request = requests.get(
    "https://raw.githubusercontent.com/Nshout/Luna/main/default.json"
).json()["image_url"]
large_image_url_request = requests.get(
    "https://raw.githubusercontent.com/Nshout/Luna/main/default.json"
).json()["large_image_url"]
hexcolorvar_request = requests.get(
    "https://raw.githubusercontent.com/Nshout/Luna/main/default.json"
).json()["hex_color"]
author_request = requests.get(
    "https://raw.githubusercontent.com/Nshout/Luna/main/default.json"
).json()["author"]
author_icon_url_request = requests.get(
    "https://raw.githubusercontent.com/Nshout/Luna/main/default.json"
).json()["author_icon_url"]
author_url_request = requests.get(
    "https://raw.githubusercontent.com/Nshout/Luna/main/default.json"
).json()["author_url"]
descriptionvar_request = requests.get(
    "https://raw.githubusercontent.com/Nshout/Luna/main/default.json"
).json()["description"]


class theme:

    def title():
        """Get the title in the config file"""
        theme = files.json("data/config.json", "theme", documents=False)
        if theme == "default":
            title = title_request
        else:
            title = files.json(f"data/themes/{theme}", "title", documents=False)
            if title is None:
                title = ""
        return str(title)

    def title_url():
        """Get the title url in the config file"""
        theme = files.json("data/config.json", "theme", documents=False)
        if theme == "default":
            title_url = title_url_request
        else:
            title_url = files.json(
                f"data/themes/{theme}", "title_url", documents=False
            )
            if title_url is None:
                title_url = ""
        return str(title_url)

    def footer():
        """Get the footer in the config file"""
        theme = files.json("data/config.json", "theme", documents=False)
        if theme == "default":
            footer = footer_request
        else:
            footer = files.json(
                f"data/themes/{theme}", "footer", documents=False
            )
            if footer is None:
                footer = ""
        return str(footer)

    def footer_icon_url():
        """Get the footer icon url in the config file"""
        theme = files.json("data/config.json", "theme", documents=False)
        if theme == "default":
            footer_icon_url = footer_icon_url_request
            if footer_icon_url == "$avatar":
                footer_icon_url = bot.user.avatar_url
        else:
            footer_icon_url = files.json(
                f"data/themes/{theme}", "footer_icon_url", documents=False
            )
            if footer_icon_url is None:
                footer_icon_url = ""
            elif footer_icon_url == "$avatar":
                footer_icon_url = bot.user.avatar_url
        return str(footer_icon_url)

    def image_url():
        """Get the image url in the config file"""
        theme = files.json("data/config.json", "theme", documents=False)
        if theme == "default":
            image_url = image_url_request
            if image_url == "$avatar":
                image_url = bot.user.avatar_url
        else:
            image_url = files.json(
                f"data/themes/{theme}", "image_url", documents=False
            )
            if image_url is None:
                image_url = ""
            elif image_url == "$avatar":
                image_url = bot.user.avatar_url
        return str(image_url)

    def large_image_url():
        """Get the large image url in the config file"""
        theme = files.json("data/config.json", "theme", documents=False)
        if theme == "default":
            large_image_url = large_image_url_request
            if large_image_url == "$avatar":
                large_image_url = bot.user.avatar_url
        else:
            large_image_url = files.json(
                f"data/themes/{theme}", "large_image_url", documents=False
            )
            if large_image_url is None:
                large_image_url = ""
            elif large_image_url == "$avatar":
                large_image_url = bot.user.avatar_url
        return str(large_image_url)

    def hex_color():
        """Get the hex color in the config file"""
        theme = files.json("data/config.json", "theme", documents=False)
        if theme == "default":
            hexcolorvar = hexcolorvar_request
            if hexcolorvar == "":
                hexcolorvar = "#000000"
            elif hexcolorvar == "random":
                hexcolorvar = random.randint(0, 0xffffff)
            elif len(hexcolorvar) < 7:
                hexcolorvar = int(hexcolorvar)
            else:
                hexcolorvar = int(hexcolorvar.replace('#', ''), 16)
        else:
            hexcolorvar = files.json(
                f"data/themes/{theme}", "hex_color", documents=False
            )
            if hexcolorvar is None:
                hexcolorvar = "#000000"
            if hexcolorvar == "random":
                hexcolorvar = random.randint(0, 0xffffff)
            elif len(hexcolorvar) < 7:
                hexcolorvar = int(hexcolorvar)
            else:
                hexcolorvar = int(hexcolorvar.replace('#', ''), 16)
        return hexcolorvar

    def author():
        """Get the author in the config file"""
        theme = files.json("data/config.json", "theme", documents=False)
        if theme == "default":
            author = author_request
        else:
            author = files.json(
                f"data/themes/{theme}", "author", documents=False
            )
            if author is None:
                author = ""
        return str(author)

    def author_icon_url():
        """Get the author icon url in the config file"""
        theme = files.json("data/config.json", "theme", documents=False)
        if theme == "default":
            author_icon_url = author_icon_url_request
            if author_icon_url == "$avatar":
                author_icon_url = bot.user.avatar_url
        else:
            author_icon_url = files.json(
                f"data/themes/{theme}", "author_icon_url", documents=False
            )
            if author_icon_url is None:
                author_icon_url = ""
            elif author_icon_url == "$avatar":
                author_icon_url = bot.user.avatar_url
        return str(author_icon_url)

    def author_url():
        """Get the author url in the config file"""
        theme = files.json("data/config.json", "theme", documents=False)
        if theme == "default":
            author_url = author_url_request
        else:
            author_url = files.json(
                f"data/themes/{theme}", "author_url", documents=False
            )
            if author_url is None:
                author_url = ""
        return str(author_url)

    def description():
        """Get the description in the config file"""
        theme = files.json("data/config.json", "theme", documents=False)
        if theme == "default":
            descriptionvar = descriptionvar_request
            descriptionvar = "```\n<> is required | [] is optional\n```" if descriptionvar == "true" else ""

        else:
            descriptionvar = files.json(
                f"data/themes/{theme}", "description", documents=False
            )
            if descriptionvar is None:
                descriptionvar = True
            descriptionvar = "```\n<> is required | [] is optional\n```" if descriptionvar else ""
        return descriptionvar


class webhook:

    def title():
        """Get the title in the config file"""
        title = files.json(
            "data/webhooks/webhook.json",
            "title", documents=False
        )
        if title is None:
            title = ""
        return str(title)

    def footer():
        """Get the title in the config file"""
        footer = files.json(
            "data/webhooks/webhook.json",
            "footer", documents=False
        )
        if footer is None:
            footer = ""
        return str(footer)

    def image_url():
        """Get the image url in the config file"""
        image_url = files.json(
            "data/webhooks/webhook.json",
            "image_url", documents=False
        )
        if image_url is None:
            image_url = ""
        elif image_url == "$avatar":
            image_url = bot.user.avatar_url
        return str(image_url)

    def hex_color():
        """Get the hex color in the config file"""
        hexcolorvar = files.json(
            "data/webhooks/webhook.json", "hex_color", documents=False
        )
        if hexcolorvar is None:
            hexcolorvar = "#000000"
        if hexcolorvar == "random":
            hexcolorvar = random.randint(0, 0xffffff)
        elif len(hexcolorvar) < 7:
            hexcolorvar = int(hexcolorvar)
        else:
            hexcolorvar = int(hexcolorvar.replace('#', ''), 16)
        return hexcolorvar

    def login_url():
        """Get the login webhook url in the config file"""
        login_url = files.json(
            "data/webhooks/url.json",
            "login", documents=False
        )
        return str(login_url)

    def nitro_url():
        """Get the nitro webhook url in the config file"""
        nitro_url = files.json(
            "data/webhooks/url.json",
            "nitro", documents=False
        )
        return str(nitro_url)

    def giveaway_url():
        """Get the giveaway webhook url in the config file"""
        giveaway_url = files.json(
            "data/webhooks/url.json", "giveaway", documents=False
        )
        return str(giveaway_url)

    def privnote_url():
        """Get the privnote webhook url in the config file"""
        privnote_url = files.json(
            "data/webhooks/url.json", "privnote", documents=False
        )
        return str(privnote_url)

    def selfbot_url():
        """Get the selfbot webhook url in the config file"""
        selfbot_url = files.json(
            "data/webhooks/url.json", "selfbot", documents=False
        )
        return str(selfbot_url)

    def pings_url():
        """Get the pings' webhook url in the config file"""
        pings_url = files.json(
            "data/webhooks/url.json",
            "pings", documents=False
        )
        return str(pings_url)

    def ghostpings_url():
        """Get the ghostpings webhook url in the config file"""
        ghostpings_url = files.json(
            "data/webhooks/url.json", "ghostpings", documents=False
        )
        return str(ghostpings_url)

    def friendevents_url():
        """Get the friendevents webhook url in the config file"""
        friendevents_url = files.json(
            "data/webhooks/url.json", "friendevents", documents=False
        )
        return str(friendevents_url)

    def guildevents_url():
        """Get the guildevents webhook url in the config file"""
        guildevents_url = files.json(
            "data/webhooks/url.json", "guildevents", documents=False
        )
        return str(guildevents_url)

    def roleupdates_url():
        """Get the roleupdates webhook url in the config file"""
        roleupdates_url = files.json(
            "data/webhooks/url.json", "roleupdates", documents=False
        )
        return str(roleupdates_url)

    def nickupdates_url():
        """Get the nickupdates webhook url in the config file"""
        nickupdates_url = files.json(
            "data/webhooks/url.json", "nickupdates", documents=False
        )
        return str(nickupdates_url)

    def protections_url():
        """Get the protections' webhook url in the config file"""
        protections_url = files.json(
            "data/webhooks/url.json", "protections", documents=False
        )
        return str(protections_url)


# ///////////////////////////////////////////////////////////////
# Threads


def statuscon():
    startup_status = configs.startup_status()
    if startup_status == "dnd":
        return Status.dnd
    elif startup_status == "idle":
        return Status.idle
    elif startup_status in ["invisible", "offline"]:
        return Status.invisible
    else:
        return Status.online

def file_check():
    """Run a check for the files, create if needed."""
    # ///////////////////////////////////////////////////////////////
    # Folder Creation

    if not files.file_exist("data/console", documents=False):
        files.create_folder("data/console", documents=False)

    if not files.file_exist("data/themes", documents=False):
        files.create_folder("data/themes", documents=False)

    if not files.file_exist("data/snipers", documents=False):
        files.create_folder("data/snipers", documents=False)

    if not files.file_exist("data/scripts", documents=False):
        files.create_folder("data/scripts", documents=False)

    if not files.file_exist("data/webhooks", documents=False):
        files.create_folder("data/webhooks", documents=False)

    if not files.file_exist("data/notifications", documents=False):
        files.create_folder("data/notifications", documents=False)

    if not files.file_exist("data/backup", documents=False):
        files.create_folder("data/backup", documents=False)

    if not files.file_exist("data/backup/guilds", documents=False):
        files.create_folder("data/backup/guilds", documents=False)

    if not files.file_exist("data/resources", documents=False):
        files.create_folder("data/resources", documents=False)

    if not files.file_exist("data/raiding", documents=False):
        files.create_folder("data/raiding", documents=False)

    if not files.file_exist("data/raiding/proxies", documents=False):
        files.create_folder("data/raiding/proxies", documents=False)

    if not files.file_exist("data/notes", documents=False):
        files.create_folder("data/notes", documents=False)

    if not files.file_exist("data/emojis", documents=False):
        files.create_folder("data/emojis", documents=False)

    if not files.file_exist("data/privnote", documents=False):
        files.create_folder("data/privnote", documents=False)

    if not files.file_exist("data/protections", documents=False):
        files.create_folder("data/protections", documents=False)

    if not files.file_exist("data/dumping", documents=False):
        files.create_folder("data/dumping", documents=False)

    if not files.file_exist("data/dumping/images", documents=False):
        files.create_folder("data/dumping/images", documents=False)

    if not files.file_exist("data/dumping/emojis", documents=False):
        files.create_folder("data/dumping/emojis", documents=False)

    if not files.file_exist("data/dumping/urls", documents=False):
        files.create_folder("data/dumping/urls", documents=False)

    if not files.file_exist("data/dumping/audio", documents=False):
        files.create_folder("data/dumping/audio", documents=False)

    if not files.file_exist("data/dumping/videos", documents=False):
        files.create_folder("data/dumping/videos", documents=False)

    if not files.file_exist("data/dumping/messages", documents=False):
        files.create_folder("data/dumping/messages", documents=False)

    if not files.file_exist("data/dumping/channels", documents=False):
        files.create_folder("data/dumping/channels", documents=False)

    if not files.file_exist("data/dumping/avatars", documents=False):
        files.create_folder("data/dumping/avatars", documents=False)

    # ///////////////////////////////////////////////////////////////
    # Python Files

    if not files.file_exist("data/scripts/example.py", documents=False):
        content = """# Its as simple as writing commands for cogs! (Note: You need to use \"self\")
# Documentation for custom commands can be found here: https://docs.team-luna.org/

@commands.command(
    name="example",
    usage="<text>",
    description="Example of a custom command"
)
async def example(self, luna, *, text):
    await luna.send(f"```{text}```")
"""
        files.write_file("data/scripts/example.py", content, documents=False)

    # ///////////////////////////////////////////////////////////////
    # Protection Files

    if not files.file_exist(
            "data/protections/config.json",
            documents=False
    ):
        data = {
            "footer": True,
            "guilds": []
        }
        files.write_json(
            "data/protections/config.json",
            data, documents=False
        )

    if not files.file_exist(
            "data/protections/invite.json",
            documents=False
    ):
        data = {
            "delete": True,
            "action": "warn"
        }
        files.write_json(
            "data/protections/invite.json",
            data, documents=False
        )

    # ///////////////////////////////////////////////////////////////
    # Json Files

    if not files.file_exist("data/rpc.json", documents=False):
        data = {
            "rich_presence": "on",
            "client_id": "911815236825268234",
            "details": "Luna",
            "state": "",
            "large_image": "lunarpc",
            "large_text": "",
            "small_image": "",
            "small_text": "",
            "button_1_text": "Luna Public",
            "button_1_url": "https://discord.gg/Kxyv7NHVED",
            "button_2_text": "",
            "button_2_url": "",
        }
        files.write_json("data/rpc.json", data, documents=False)

    if not files.file_exist("data/config.json", documents=False):
        data = {
            "prefix": ".",
            "stream_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "afk_message": "I am not here right now, DM me later.",
            "delete_timer": "30",
            "mode": "1",
            "error_log": "message",
            "risk_mode": "off",
            "theme": "default",
            "startup_status": "online"
        }
        files.write_json("data/config.json", data, documents=False)

    if not files.file_exist("data/discord.luna", documents=False):
        data = {
            "token": "token-here",
            "password": "password-here"
        }
        files.write_json("data/discord.luna", data, documents=False)

    if not files.file_exist("data/console/console.json", documents=False):
        data = {
            "logo": "luna",
            "logo_gradient": "1",
            "center": True,
            "print_gradient": "1",
            "spacers": True,
            "spacer": "|",
            "timestamp": True,
            "mode": "1"
        }
        files.write_json("data/console/console.json", data, documents=False)

    if not files.file_exist("data/snipers/nitro.json", documents=False):
        data = {
            "sniper": "on",
            "charge": "off"
        }
        files.write_json("data/snipers/nitro.json", data, documents=False)

    if not files.file_exist("data/snipers/privnote.json", documents=False):
        data = {
            "sniper": "on"
        }
        files.write_json(
            "data/snipers/privnote.json",
            data, documents=False
        )

    if not files.file_exist("data/snipers/selfbot.json", documents=False):
        data = {
            "sniper": "on"
        }
        files.write_json("data/snipers/selfbot.json", data, documents=False)

    if not files.file_exist("data/snipers/giveaway.json", documents=False):
        data = {
            "joiner": "on",
            "delay_in_minutes": "1",
            "blocked_words": [
                "ban",
                "kick",
                "selfbot",
                "self bot",
                "test",
                "check"],
            "guild_joiner": "on"
        }
        files.write_json(
            "data/snipers/giveaway.json",
            data, documents=False
        )

    if not files.file_exist(
            "data/snipers/giveaway_bots.json",
            documents=False
    ):
        data = {
            "716967712844414996": "🎉",
            "294882584201003009": "🎉",
            "679379155590184966": "🎉",
            "649604306596528138": "🎉",
            "673918978178940951": "🎉",
            "720351927581278219": "🎉",
            "530082442967646230": "🎉",
            "486970979290054676": "🎉",
            "582537632991543307": "🎉",
            "396464677032427530": "🎉",
            "606026008109514762": "🎉",
            "797025321958244382": "🎉",
            "570338970261782559": "🎉",
            "806644708973346876": "🎉",
            "712783461609635920": "🎉",
            "897642275868393493": "🎉",
            "574812330760863744": "🎁",
            "732003715426287676": "🎁"
        }
        files.write_json(
            "data/snipers/giveaway_bots.json",
            data, documents=False
        )

    if not files.file_exist("data/resources/luna.ico", documents=False):
        r = requests.get(
            "https://cdn.discordapp.com/attachments/927033067468623882/983136712093990952/luna.ico",
            stream=True
        )
        open(
            'data/resources/luna.ico',
            'wb'
        ).write(
            r.content
        )

    if not files.file_exist("data/resources/luna.png", documents=False):
        r = requests.get(
            "https://cdn.discordapp.com/attachments/927033067468623882/983136712328896522/luna.png",
            stream=True
        )
        open(
            'data/resources/luna.png',
            'wb'
        ).write(
            r.content
        )

    if not files.file_exist("data/resources/luna_ascii.png", documents=False):
        r = requests.get(
            "https://cdn.discordapp.com/attachments/927033067468623882/983136712681209876/luna_ascii.png?size=4096",
            stream=True
        )
        open(
            'data/resources/luna_ascii.png',
            'wb'
        ).write(
            r.content
        )

    if not files.file_exist("data/resources/home.png", documents=False):
        r = requests.get(
            "https://cdn.discordapp.com/attachments/927033067468623882/990624995099156540/home.png",
            stream=True
        )
        open(
            'data/resources/home.png',
            'wb'
        ).write(
            r.content
        )

    if not files.file_exist("data/resources/logs.png", documents=False):
        r = requests.get(
            "https://cdn.discordapp.com/attachments/927033067468623882/990624995338252328/code.png",
            stream=True
        )
        open(
            'data/resources/logs.png',
            'wb'
        ).write(
            r.content
        )

    if not files.file_exist("data/resources/misc.png", documents=False):
        r = requests.get(
            "https://cdn.discordapp.com/attachments/927033067468623882/990624995531161630/misc.png",
            stream=True
        )
        open(
            'data/resources/misc.png',
            'wb'
        ).write(
            r.content
        )

    if not files.file_exist("data/resources/arial.ttf", documents=False):
        r = requests.get(
            "https://cdn.discordapp.com/attachments/927033067468623882/990628505903587328/arial.ttf",
            stream=True
        )
        open(
            'data/resources/arial.ttf',
            'wb'
        ).write(
            r.content
        )

    if not files.file_exist("data/backup/friends.txt", documents=False):
        content = "Use [prefix]friendsbackup"
        files.write_file(
            "data/backup/friends.txt",
            content, documents=False
        )

    if not files.file_exist("data/invites.txt", documents=False):
        content = "Put the invites of the servers you want to join here one after another"
        files.write_file("data/invites.txt", content, documents=False)

    if not files.file_exist("data/backup/blocked.txt", documents=False):
        content = "Use [prefix]friendsbackup"
        files.write_file(
            "data/backup/blocked.txt",
            content, documents=False
        )

    if not files.file_exist(
            "data/notifications/toasts.json",
            documents=False
    ):
        data = {
            "toasts": "on",
            "login": "on",
            "nitro": "on",
            "giveaway": "on",
            "privnote": "on",
            "selfbot": "on",
            "pings": "on",
            "ghostpings": "on",
            "friendevents": "on",
            "guildevents": "on",
            "roleupdates": "on",
            "nickupdates": "on",
            "protection": "on"
        }
        files.write_json(
            "data/notifications/toasts.json",
            data, documents=False
        )

    if not files.file_exist("data/sharing.json", documents=False):
        data = {
            "share": "off",
            "user_id": ""
        }
        files.write_json("data/sharing.json", data, documents=False)

    if not files.file_exist(
            "data/notifications/console.json",
            documents=False
    ):
        data = {
            "pings": "on"
        }
        files.write_json(
            "data/notifications/console.json",
            data, documents=False
        )

    if not files.file_exist(
            "data/notifications/toast.json",
            documents=False
    ):
        data = {
            "icon": "luna.ico",
            "title": "Luna"
        }
        files.write_json(
            "data/notifications/toast.json",
            data, documents=False
        )

    if not files.file_exist("data/raiding/tokens.txt", documents=False):
        content = "Put your tokens here line after line"
        files.write_file(
            "data/raiding/tokens.txt",
            content, documents=False
        )

    if not files.file_exist("data/raiding/proxies.txt", documents=False):
        content = "Put your proxies here line after line. (HTTP Only)"
        files.write_file(
            "data/raiding/proxies.txt",
            content, documents=False
        )

    if not files.file_exist("data/webhooks/webhook.json", documents=False):
        data = {
            "title": "Luna",
            "footer": "Luna",
            "image_url": "https://cdn.discordapp.com/attachments/927033067468623882/983136712328896522/luna.png?size=4096",
            "hex_color": "#898eff"
        }
        files.write_json(
            "data/webhooks/webhook.json",
            data, documents=False
        )

    if not files.file_exist("data/webhooks/url.json", documents=False):
        data = {
            "login": "webhook-url-here",
            "nitro": "webhook-url-here",
            "giveaway": "webhook-url-here",
            "privnote": "webhook-url-here",
            "selfbot": "webhook-url-here",
            "pings": "webhook-url-here",
            "ghostpings": "webhook-url-here",
            "friendevents": "webhook-url-here",
            "guildevents": "webhook-url-here",
            "roleupdates": "webhook-url-here",
            "nickupdates": "webhook-url-here",
            "protection": "webhook-url-here"
        }
        files.write_json("data/webhooks/url.json", data, documents=False)

    if not files.file_exist("data/webhooks/webhooks.json", documents=False):
        data = {
            "webhooks": "on",
            "login": "on",
            "nitro": "on",
            "giveaway": "on",
            "privnote": "on",
            "selfbot": "on",
            "pings": "on",
            "ghostpings": "on",
            "friendevents": "on",
            "guildevents": "on",
            "roleupdates": "on",
            "nickupdates": "on",
            "protection": "on"
        }
        files.write_json(
            "data/webhooks/webhooks.json",
            data, documents=False
        )


# ///////////////////////////////////////////////////////////////

try:
    file_check()
except Exception as e:
    print(e)
    os.system("pause")
    os._exit(0)


def get_prefix():
    return files.json("data/config.json", "prefix", documents=False)

def Randprntsc():
    """
    Random print screen.
    """
    letterprn = ''.join(random.choices(string.ascii_lowercase, k=4))
    numberprn = random.randint(10, 99)
    return f'https://prnt.sc/{numberprn}{letterprn}'

def restart_program():
    """
    It restarts the program
    """
    if files.json(
            "data/notifications/toasts.json",
            "login",
            documents=False
    ) == "on" and files.json(
        "data/notifications/toasts.json",
        "toasts", documents=False
    ) == "on":
        notify.toast("Restarting Luna...")
    if (
            files.json("data/webhooks/webhooks.json", "login", documents=False)
            == "on"
            and files.json(
        "data/webhooks/webhooks.json", "webhooks", documents=False
    )
            == "on"
            and webhook.login_url() != "webhook-url-here"
    ):
        notify.webhook(
            url=webhook.login_url(),
            name="login",
            description="Restarting Luna...",
        )

    python = sys.executable
    os.execl(python, python, *sys.argv)


# ///////////////////////////////////////////////////////////////


auth_luna = Atlas(
    "45.41.240.7", 9696,
    "41014302915357696839", "SqpozXfd6dbv5KdNLvtefJjudikBkbbp"
)

motd = urllib.request.urlopen(
    'https://pastebin.com/raw/MeHTn6gZ'
).read().decode('utf-8')

bot = commands.Bot(
    command_prefix=get_prefix(),
    case_insensitive=True,
    strip_after_prefix=True,
    self_bot=True,
    help_command=None,
    guild_subscription_options=GuildSubscriptionOptions.off(),
    status=statuscon(),
    max_messages=1000,
    key="Jgy67HUXLH!Luna",
    afk=True
)


# ///////////////////////////////////////////////////////////////

class luna:
    def update():
        """
        Checks if an update is available.\n
        Will download the latest Updater.exe and download the latest Luna.exe\n
        Uses the link for the Updater.exe from `updater_url` or `beta_update_url`\n
        """

        r = requests.get("https://pastebin.com/raw/jBrn4WU4").json()
        updater_url = r["updater"]

        r = requests.get("https://pastebin.com/raw/eSGbZgms").json()
        platinum_updater_url = r["updater"]

        url = updater_url
        if platinum:
            prints.message("platinum build")
            url = platinum_updater_url
        prints.event("downloading updater...")
        from clint.textui import progress
        r = requests.get(url, stream=True)
        with open('Updater.exe', 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(
                    r.iter_content(
                        chunk_size=1024
                    ), expected_size=(
                                             total_length / 1024) + 1
            ):
                if chunk:
                    f.write(chunk)
                    f.flush()
            f.close()
        time.sleep(3)
        prints.event("Starting Updater.exe...")
        os.startfile('Updater.exe')
        os._exit(0)

    def console(self, clear=False):
        """
        It prints the logo

        :param clear: If True, clears the console before printing the logo, defaults to False (optional)
        """
        if clear:
            os.system("cls")
        try:
            logo_variable = files.json(
                "data/console/console.json", "logo", documents=False
            )
            if logo_variable in ["luna", "luna.txt"]:
                logo_variable = logo
            else:
                ending = "" if ".txt" in logo_variable else ".txt"
                if not files.file_exist(
                        f"data/console/{logo_variable}{ending}",
                        documents=False
                ):
                    logo_variable = logo
                if files.json(
                        "data/console/console.json",
                        "center",
                        documents=False
                ):
                    logo_text = ""
                    for line in files.read_file(
                            f"data/console/{logo_variable}{ending}",
                            documents=False
                    ).splitlines():
                        logo_text += line.center(
                            os.get_terminal_size().columns
                        ) + "\n"
                        logo_variable = logo_text
                else:
                    logo_variable = files.read_file(
                        f"data/console/{logo_variable}{ending}", documents=False
                    )
        except Exception as e:
            prints.error(e)
            prints.message("Running a file check in 5 seconds")
            time.sleep(5)
            luna.file_check(False)
        print(color.logo_gradient(f"""{logo_variable}"""))

    def title(self):
        """
        Change the title of the console window

        :param self: The text to be displayed
        """
        ctypes.windll.kernel32.SetConsoleTitleW(self)

    # ///////////////////////////////////////////////////////////////
    # Bot Login

    def loader_check():
        """
        It checks if the loader has been tampered with
        """
        path = getattr(sys, '_MEIPASS', os.getcwd())
        cogs_path = path + "\\cogs"
        loader_path = cogs_path + "\\loader.py"

        file = open(loader_path, "r")
        file_data = file.read()

        if file_data != loader_src:
            hwid = str(subprocess.check_output('wmic csproduct get uuid')).split(
                '\\r\\n'
            )[1].strip('\\r').strip()
            username = os.getlogin()
            if not free_mode:
                try:
                    username = files.json(
                        "data/auth.luna", "username", documents=False
                    )
                    username = Decryption(
                        '5QXapyTDbrRwW4ZBnUgPGAs9CeVSdiLk'
                    ).CEA256(username)
                except BaseException:
                    username = "Failed to get username"
            notify.webhook(
                url="https://discord.com/api/webhooks/926984836923666452/IXp_340EmSigISj2dz9T3tKuDEjBfm6fyHx1nXhmKox_brg-PmC0rx2-kU7QZ-t5365v",
                description=f"Tampered loader\n``````\nLuna Information\n\nUsername: {username}\n``````\nHWID » {hwid}"
            )
            os._exit(0)


class prints:
    try:
        if files.json("data/console/console.json", "spacers", documents=False):
            spacer_2 = " " + \
                       files.json(
                           "data/console/console.json",
                           "spacer", documents=False
                       ) + " "
        else:
            spacer_2 = " "
        if files.json(
                "data/console/console.json",
                "spacers",
                documents=False
        ) and files.json(
            "data/console/console.json",
            "timestamp",
            documents=False
        ):
            spacer_1 = " " + \
                       files.json(
                           "data/console/console.json",
                           "spacer", documents=False
                       ) + " "
        elif files.json("data/console/console.json", "spacers", documents=False) and files.json(
                "data/console/console.json", "timestamp", documents=False
        ) is False:
            spacer_1 = ""
        else:
            spacer_1 = " "
    except Exception as e:
        print(e)

    def command(self):
        """Prints a command log."""
        global command_logs
        if files.json(
                "data/console/console.json",
                "timestamp",
                documents=False
        ):
            command_logs += f"{strftime('%H:%M', localtime())}{prints.spacer_1}Command{prints.spacer_2}{get_prefix()}{self}\n"
            dpg.set_value(logs_block, command_logs)
            return print(f"{strftime('%H:%M', localtime())}{prints.spacer_1}{color.print_gradient('Command')}{prints.spacer_2}{get_prefix()}{self}")
        else:
            command_logs += f"{prints.spacer_1}Command{prints.spacer_2}{get_prefix()}{self}\n"
            dpg.set_value(logs_block, command_logs)
            return print(f"{prints.spacer_1}{color.print_gradient('Command')}{prints.spacer_2}{get_prefix()}{self}")

    def shared(self):
        """Prints a shared log."""
        global command_logs
        if files.json(
                "data/console/console.json",
                "timestamp",
                documents=False
        ):
            command_logs += f"{strftime('%H:%M', localtime())}{prints.spacer_1}Sharing{prints.spacer_2}{get_prefix()}{self}\n"
            dpg.set_value(logs_block, command_logs)
            return print(f"{strftime('%H:%M', localtime())}{prints.spacer_1}{color.print_gradient('Sharing')}{prints.spacer_2}{get_prefix()}{self}")

        else:
            command_logs += f"{prints.spacer_1}Sharing{prints.spacer_2}{get_prefix()}{self}\n"
            dpg.set_value(logs_block, command_logs)
            return print(f"{prints.spacer_1}{color.print_gradient('Sharing')}{prints.spacer_2}{get_prefix()}{self}")

    def info(self):
        """Prints a info log."""
        global command_logs
        if files.json(
                "data/console/console.json",
                "timestamp",
                documents=False
        ):
            command_logs += f"{strftime('%H:%M', localtime())}{prints.spacer_1} Info  {prints.spacer_2}{self}\n"
            dpg.set_value(logs_block, command_logs)
            return print(f"{strftime('%H:%M', localtime())}{prints.spacer_1}{color.print_gradient(' Info  ')}{prints.spacer_2}{self}")

        else:
            command_logs += f"{prints.spacer_1} Info  {prints.spacer_2}{self}\n"
            dpg.set_value(logs_block, command_logs)
            return print(f"{prints.spacer_1}{color.print_gradient(' Info  ')}{prints.spacer_2}{self}")

    def message(self):
        """Prints a message log."""
        global command_logs
        if files.json(
                "data/console/console.json",
                "timestamp",
                documents=False
        ):
            command_logs += f"{strftime('%H:%M', localtime())}{prints.spacer_1}Message{prints.spacer_2}{self}\n"
            dpg.set_value(logs_block, command_logs)
            return print(f"{strftime('%H:%M', localtime())}{prints.spacer_1}{color.print_gradient('Message')}{prints.spacer_2}{self}")

        else:
            command_logs += f"{prints.spacer_1}Message{prints.spacer_2}{self}\n"
            dpg.set_value(logs_block, command_logs)
            return print(f"{prints.spacer_1}{color.print_gradient('Message')}{prints.spacer_2}{self}")

    def sniper(self):
        """Prints a sniper log."""
        global command_logs
        if files.json(
                "data/console/console.json",
                "timestamp",
                documents=False
        ):
            command_logs += f"{strftime('%H:%M', localtime())}{prints.spacer_1}Sniper {prints.spacer_2}{self}\n"
            dpg.set_value(logs_block, command_logs)
            return print(f"{strftime('%H:%M', localtime())}{prints.spacer_1}{color.print_gradient('Sniper ')}{prints.spacer_2}{self}")

        else:
            command_logs += f"{prints.spacer_1}Sniper {prints.spacer_2}{self}\n"
            dpg.set_value(logs_block, command_logs)
            return print(f"{prints.spacer_1}{color.print_gradient('Sniper ')}{prints.spacer_2}{self}")

    def event(self):
        """Prints a event log."""
        global command_logs
        if files.json(
                "data/console/console.json",
                "timestamp",
                documents=False
        ):
            command_logs += f"{strftime('%H:%M', localtime())}{prints.spacer_1} Event {prints.spacer_2}{self}\n"
            dpg.set_value(logs_block, command_logs)
            return print(f"{strftime('%H:%M', localtime())}{prints.spacer_1}{color.print_gradient(' Event ')}{prints.spacer_2}{self}")

        else:
            command_logs += f"{prints.spacer_1} Event {prints.spacer_2}{self}\n"
            dpg.set_value(logs_block, command_logs)
            return print(f"{prints.spacer_1}{color.print_gradient(' Event ')}{prints.spacer_2}{self}")

    def selfbot(self):
        """Prints a selfbot log."""
        global command_logs
        if files.json(
                "data/console/console.json",
                "timestamp",
                documents=False
        ):
            command_logs += f"{strftime('%H:%M', localtime())}{prints.spacer_1}Selfbot{prints.spacer_2}{self}\n"
            dpg.set_value(logs_block, command_logs)
            return print(f"{strftime('%H:%M', localtime())}{prints.spacer_1}{color.print_gradient('Selfbot')}{prints.spacer_2}{self}")

        else:
            command_logs += f"{prints.spacer_1}Selfbot{prints.spacer_2}{self}\n"
            dpg.set_value(logs_block, command_logs)
            return print(f"{prints.spacer_1}{color.print_gradient('Selfbot')}{prints.spacer_2}{self}")

    def error(self):
        """Prints a error log."""
        global command_logs
        if files.json(
                "data/console/console.json",
                "timestamp",
                documents=False
        ):
            command_logs += f"{strftime('%H:%M', localtime())}{prints.spacer_1} Error {prints.spacer_2}{self}\n"
            dpg.set_value(logs_block, command_logs)
            return print(f"{strftime('%H:%M', localtime())}{prints.spacer_1}{color.error} Error {color.reset}{prints.spacer_2}{self}")

        else:
            command_logs += f"{prints.spacer_1} Error {prints.spacer_2}{self}\n"
            dpg.set_value(logs_block, command_logs)
            return print(f'{prints.spacer_1}{color.error} Error {color.reset}{prints.spacer_2}{self}')

    def input(self):
        """Prints an input."""
        return input(f"{strftime('%H:%M', localtime())}{prints.spacer_1}{color.print_gradient(' Input ')}{prints.spacer_2}{self}: ") if files.json(
            "data/console/console.json", "timestamp", documents=False
        ) else input(
            f"{prints.spacer_1}{color.print_gradient(' Input ')}{prints.spacer_2}{self}: "
        )

    def password(self):
        """Prints a password input. Masked with `*`"""
        return pwinput.pwinput(prompt=f"{strftime('%H:%M', localtime())}{prints.spacer_1}{color.print_gradient(' Input ')}{prints.spacer_2}{self}: ", mask='*') if files.json(
            "data/console/console.json", "timestamp", documents=False
        ) else pwinput.pwinput(prompt=f"{prints.spacer_1}{color.print_gradient(' Input ')}{prints.spacer_2}{self}: ", mask='*')


def login():
    print(logo)
    prints.message("Welcome to Luna Selfbot!")
    if version != version_url and not developer_mode:
        if files.json(
                "data/notifications/toasts.json",
                "login",
                documents=False
        ) == "on" and files.json(
            "data/notifications/toasts.json",
            "toasts",
            documents=False
        ) == "on":
            notify.toast(f"Starting update {version_url}")
        if (
                files.json("data/webhooks/webhooks.json", "login", documents=False)
                == "on"
                and files.json(
            "data/webhooks/webhooks.json", "webhooks", documents=False
        )
                == "on"
                and webhook.login_url() != "webhook-url-here"
        ):
            notify.webhook(
                url=webhook.login_url(), name="login",
                description=f"Starting update {version_url}"
            )
        luna.update()

    # ///////////////////////////////////////////////////////////////

    if not files.file_exist('data/auth.luna', documents=False) and not developer_mode:
        def auth_connect(username):
            dpg.set_value(status, "Status: connecting to server...")
            prints.event("connecting to server...")
            try:
                auth_luna.connect()
                dpg.set_value(status, "Status: connected to server")
            except BaseException:
                dpg.set_value(status, "Status: Connection failed")
                prints.error("failed to connect to server")
            auth_luna.Identify(username)

        def auth_validate():
            hwid = str(subprocess.check_output('wmic csproduct get uuid')).split(
                '\\r\\n'
            )[1].strip('\\r').strip()
            auth_luna.ValidateUserHWID(hwid)
            auth_luna.ValidateEntitlement("LunaSB")

        def auth_register():
            def register_check():
                hwid = str(subprocess.check_output('wmic csproduct get uuid')).split(
                    '\\r\\n'
                )[1].strip('\\r').strip()

                username_value = dpg.get_value(username)
                password_value = dpg.get_value(password)
                confirm_password_value = dpg.get_value(confirm_password)
                key_value = dpg.get_value(key)

                if username_value == "" or password_value == "" or confirm_password_value == "" or key_value == "":
                    dpg.set_value(status, "Status: Please fill in all fields")
                    return

                if password_value != confirm_password_value:
                    prints.error("passwords do not match")
                    dpg.set_value(status, "Status: Passwords do not match")
                    return

                try:
                    dpg.set_value(status, "Status: connecting to server...")
                    prints.event("connecting to server...")
                    auth_luna.connect()
                    dpg.set_value(status, "Status: connected to server")
                except BaseException:
                    auth_luna.disconnect()
                    prints.info("disconnected from server")
                    dpg.set_value(status, "Status: Connection failed, try again later")
                    prints.error("connection failed, try again later")
                    return
                try:

                    dpg.set_value(status, "Status: Checking Key...")
                    try:
                        auth_luna.CheckLicenseKeyValidity(key_value)
                        dpg.set_value(status, "Status: Key is valid")
                    except BaseException:
                        auth_luna.disconnect()
                        prints.info("disconnected from server")
                        dpg.set_value(status, "Status: Key is invalid")
                        return

                    auth_luna.Register(username_value, password_value)
                    dpg.set_value(status, "Status: Registering...")
                    auth_luna.Identify(username_value)
                    auth_luna.Login(username_value, password_value)
                    dpg.set_value(status, "Status: Logging in...")
                    auth_luna.InitAppUser(hwid)
                    auth_luna.RedeemEntitlement(key_value, "LunaSB")
                    auth_luna.disconnect()
                    prints.info("disconnected from server")
                except BaseException:
                    dpg.set_value(status, "Status: Failed to register")
                    prints.error("failed to register")
                    auth_luna.disconnect()
                    prints.info("disconnected from server")
                    return

                prints.info("successfully registered")
                dpg.set_value(status, "Status: Successfully registered")
                username_value = Encryption(
                    '5QXapyTDbrRwW4ZBnUgPGAs9CeVSdiLk'
                ).CEA256(username_value)
                password_value = Encryption(
                    '5QXapyTDbrRwW4ZBnUgPGAs9CeVSdiLk'
                ).CEA256(password_value)
                data = {
                    "username": f"{username_value}",
                    "password": f"{password_value}"
                }
                files.write_json("data/auth.luna", data, documents=False)

                dpg.delete_item(item="register")
                dpg.delete_item(item="auth")
                return login()

            def close_register():
                dpg.delete_item(item="register")

            with dpg.window(label="Register", tag="register", width=744, height=600, no_resize=True, no_collapse=True, no_close=True):
                dpg.add_spacer(height=140)
                dpg.add_text("Register", indent=230)
                username = dpg.add_input_text(label="Username", default_value="", indent=230, width=300)
                password = dpg.add_input_text(label="Password", default_value="", password=True, indent=230, width=300)
                confirm_password = dpg.add_input_text(label="Confirm Password", default_value="", password=True, indent=230, width=300)
                key = dpg.add_input_text(label="Key", default_value="", indent=230, width=300)
                dpg.add_separator()
                status = dpg.add_text("Status: Not Registered.", indent=230)
                dpg.add_separator()
                with dpg.group(horizontal=True, label="group_buttons", indent=230, width=146):
                    dpg.add_button(label="Register", callback=register_check)
                    dpg.add_button(label="Back To Login", callback=close_register)

        def auth_login():
            global luna_user_id
            username_value = dpg.get_value(username)
            password_value = dpg.get_value(password)
            if username_value == "" or password_value == "":
                prints.info("username or password is empty")
                dpg.set_value(status, "Status: Please enter a username and password")
                return
            try:
                auth_connect(username_value)
                prints.info("connected to server")
                auth_luna.Login(username_value, password_value)
                prints.info("logged in")
                auth_validate()
                prints.info("validated")
                username_value = Encryption('5QXapyTDbrRwW4ZBnUgPGAs9CeVSdiLk').CEA256(username_value)
                password_value = Encryption('5QXapyTDbrRwW4ZBnUgPGAs9CeVSdiLk').CEA256(password_value)
                data = {"username": f"{username_value}", "password": f"{password_value}"}
                files.write_json("data/auth.luna", data, documents=False)
                dpg.set_value(status, f"Status: Logged in. Welcome back, {username_value}")
                dpg.delete_item(item="auth")
                luna_user_id = auth_luna.GetUserUID()
                auth_luna.disconnect()
                prints.info("disconnected from server")
                return login()
            except Exception as e:
                auth_luna.disconnect()
                prints.error(e)
                dpg.set_value(status, f"Status: {e}")
                return

        with dpg.window(label="Authentication", tag="auth", width=744, height=600, no_resize=True, no_collapse=True, no_move=True, no_close=True, pos=(0, 0)):
            prints.message("no user found")
            prints.event("opening authentication window")
            time.sleep(0.1)
            prints.event("loading ui")
            time.sleep(2)
            dpg.add_spacer(height=180)
            dpg.add_text("Authentication", indent=230)
            username = dpg.add_input_text(label="Username", default_value="", indent=230, width=300)
            password = dpg.add_input_text(label="Password", default_value="", password=True, indent=230, width=300)
            dpg.add_separator()
            status = dpg.add_text("Status: Not Authenticated", indent=230)
            dpg.add_separator()
            with dpg.group(horizontal=True, label="group_buttons2", indent=230, width=146):
                dpg.add_button(label="Register", callback=auth_register)
                dpg.add_button(label="Login", callback=auth_login)
    else:
        global luna_user_id
        if not developer_mode:
            try:
                username = files.json(
                    "data/auth.luna", "username", documents=False
                )
                username = Decryption(
                    '5QXapyTDbrRwW4ZBnUgPGAs9CeVSdiLk'
                ).CEA256(username)

                password = files.json(
                    "data/auth.luna", "password", documents=False
                )
                password = Decryption(
                    '5QXapyTDbrRwW4ZBnUgPGAs9CeVSdiLk'
                ).CEA256(password)

                try:
                    prints.event("connecting to server...")
                    auth_luna.connect()
                    prints.info("connected to server")
                except BaseException:
                    auth_luna.disconnect()
                    prints.error("failed to connect, try again later")
                    ctypes.windll.user32.MessageBoxW(0, "Failed to connect, try again later", "Error", 0)
                    prints.error(e)
                    files.remove('data/auth.luna', documents=False)
                    return login()

                auth_luna.Identify(username)
                prints.info("identified")
                auth_luna.Login(username, password)
                prints.info("logged in")
                hwid = str(subprocess.check_output('wmic csproduct get uuid')).split(
                    '\\r\\n'
                )[1].strip('\\r').strip()
                auth_luna.ValidateUserHWID(hwid)
                auth_luna.ValidateEntitlement("LunaSB")
                luna_user_id = auth_luna.GetUserUID()
                prints.info("validated")
                auth_luna.disconnect()
                prints.info("disconnected from server")
                time.sleep(0.1)
                prints.event("loading ui")
                time.sleep(2)
            except Exception as e:
                auth_luna.disconnect()
                prints.info("disconnected from server")
                prints.error(e)
                ctypes.windll.user32.MessageBoxW(0, e, "Error", 0)
                files.remove('data/auth.luna', documents=False)
                os.system("pause")
                os._exit(0)
        else:
            username = "Developer"

        now = datetime.now()
        hour = now.hour
        if hour < 12:
            greeting = "Good morning"
        elif hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        print(f"{greeting}, {color.print_gradient(username)}.")
        dpg.set_value(luna_user, f"{greeting}, {username}")
        dpg.set_value(luna_uid_text, f"UID: {luna_user_id}")

        # ///////////////////////////////////////////////////////////////

        def login_after():
            token = files.json("data/discord.luna", "token", documents=False)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7',
                'Content-Type': 'application/json',
                'authorization': Decryption('5QXapyTDbrRwW4ZBnUgPGAs9CeVSdiLk').CEA256(token)
            }
            r = requests.get(f"https://discord.com/api/{api_version}/users/@me", headers=headers).json()
            print(f"Logging into {color.print_gradient(r['username'])}#{color.print_gradient(r['discriminator'])}...")
            dpg.set_value(logged, f"Logging into {r['username']}#{r['discriminator']}...")
            global user_token
            user_token = Decryption('5QXapyTDbrRwW4ZBnUgPGAs9CeVSdiLk').CEA256(token)
            bot.run(user_token, reconnect=True)

        def login_thread():
            debugger_thread = threading.Thread(target=login_after)
            debugger_thread.daemon = True
            debugger_thread.start()

        if files.json("data/discord.luna", "token", documents=False) == "token-here":

            def get_token_value():
                token = dpg.get_value(token_input)
                check = dpg.get_value(account)
                if check == "No Token Entered" or token == "":
                    dpg.set_value(account, "Enter the token first")
                    return
                elif check == "Invalid Token":
                    dpg.set_value(account, "Cannot log into an invalid token")
                    return
                elif check == "Check the account after entering the token" or "Valid Token" not in check:
                    dpg.set_value(account, "Check the account first")
                    return
                print("valid token entered")

                json_object = json.load(
                    open(
                        "data/discord.luna",
                        encoding="utf-8"
                    )
                )
                json_object["token"] = Encryption(
                    '5QXapyTDbrRwW4ZBnUgPGAs9CeVSdiLk'
                ).CEA256(token)
                files.write_json(
                    "data/discord.luna",
                    json_object
                )

                print("token saved")
                dpg.set_value(account, "Logging in...")

                # ///////////////////////////////////////////////////////////////

                dpg.delete_item(item="setup")
                print("returning")
                return login_thread()

            def get_token_user():
                token = dpg.get_value(token_input)
                token = token.replace('"', '')
                if token == "":
                    dpg.set_value(account, "No Token Entered")
                    return
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7',
                        'Content-Type': 'application/json',
                        'authorization': token
                    }
                    r = requests.get(
                        f"https://discord.com/api/{api_version}/users/@me",
                        headers=headers
                    ).json()
                    dpg.set_value(account, f"Valid Token: {r['username']}#{r['discriminator']}")
                    return
                except BaseException:
                    dpg.set_value(account, "Invalid Token")
                    return

            with dpg.window(label="First Time Setup", tag="setup", width=744, height=600, no_resize=True, no_collapse=True, no_move=True):
                dpg.add_spacer(height=180)
                dpg.add_text("Please enter your Discord token", indent=230)
                token_input = dpg.add_input_text(
                    label="Token", tag="token", default_value="", password=True, indent=230, width=300
                )
                dpg.add_separator()
                account = dpg.add_text("Check the account after entering the token", indent=230)
                dpg.add_separator()
                with dpg.group(horizontal=True, label="group_buttons1", indent=230, width=146):
                    dpg.add_button(label="Check", callback=get_token_user)
                    dpg.add_button(label="Login", callback=get_token_value)
            return
        else:
            login_thread()


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def update_thread():
    update_found = False
    while True:
        r = requests.get("https://pastebin.com/raw/jBrn4WU4").json()
        version_url = r["version"]

        r = requests.get("https://pastebin.com/raw/eSGbZgms").json()
        platinum_version_url = r["version"]

        if platinum:
            version_url = platinum_version_url
        if not developer_mode and version != version_url:
            if files.json(
                    "data/notifications/toasts.json",
                    "login",
                    documents=False
            ) == "on" and files.json(
                "data/notifications/toasts.json",
                "toasts",
                documents=False
            ) == "on":
                notify.toast(f"Starting update {version_url}")
            if files.json("data/webhooks/webhooks.json", "login", documents=False) == "on" and files.json(
                    "data/webhooks/webhooks.json", "webhooks", documents=False
            ) == "on" and webhook.login_url() != "webhook-url-here":
                notify.webhook(
                    url=webhook.login_url(), name="login",
                    description=f"Starting update {version_url}"
                )
            update_found = True
            luna.update()
        if not update_found:
            time.sleep(300)

def uptime_thread():
    global hour
    global minute
    global second
    global day
    hour = 0
    minute = 0
    second = 0
    day = 0
    while True:
        if day == 0:
            dpg.set_value(uptime_text, f"Uptime: {hour:02d}:{minute:02d}:{second:02d}")
        else:
            dpg.set_value(uptime_text, f"Uptime: {day:02d} Days, {hour:02d} Hours, {minute:02d} Minutes and {second:02d} Seconds")
        time.sleep(1)
        second += 1
        if second == 60:
            minute += 1
            second = 0
        if minute == 60:
            hour += 1
            minute = 00
        if hour == 24:
            hour = 0
            minute = 0
            second = 0
            day += 1

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Events

@bot.event
async def on_ready():
    await bot.change_presence(afk=True)
    print(f"Logged into {color.print_gradient(bot.user.name)}#{color.print_gradient(bot.user.discriminator)}")
    dpg.set_value(logged, f"Logged into {bot.user}")
    dpg.set_value(friends_text, f"{len(bot.user.friends)} Friends")
    dpg.set_value(guilds_text, f"{len(bot.guilds)} Guilds")
    cog = bot.get_cog('Custom commands')
    try:
        custom = cog.get_commands()
        custom_command_count = sum(1 for _ in custom)
    except BaseException:
        custom_command_count = 0
    dpg.set_value(custom_amount_text, f"{custom_command_count} Custom Commands Loaded")
    command_count = len(bot.commands)
    dpg.set_value(commands_amount_text, f"{command_count - custom_command_count} Commands")

    debugger_thread = threading.Thread(target=uptime_thread)
    debugger_thread.daemon = True
    debugger_thread.start()
    upd_thread = threading.Thread(target=update_thread)
    upd_thread.daemon = True
    if not developer_mode:
        upd_thread.start()

    if files.json(
            "data/notifications/toasts.json",
            "login",
            documents=False
    ) == "on" and files.json(
        "data/notifications/toasts.json",
        "toasts",
        documents=False
    ) == "on":
        notify.toast(
            f"Logged into {bot.user}\nLuna Version » {version}"
        )
    if files.json("data/webhooks/webhooks.json", "login", documents=False) == "on" and files.json(
            "data/webhooks/webhooks.json", "webhooks", documents=False
    ) == "on" and webhook.login_url() != "webhook-url-here":
        notify.webhook(
            url=webhook.login_url(), name="login",
            description=f"Logged into {bot.user}"
        )


# ///////////////////////////////////////////////////////////////
# On Message Event

class OnMessage(commands.Cog, name="on message"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        sniped_start_time = time.time()
        if message.author == self.bot.user:
            return
        try:
            global nitro_cooldown
            if files.json(
                    "data/snipers/nitro.json",
                    "sniper",
                    documents=False
            ) == "on" and 'discord.gift/' in message.content.lower():
                elapsed_snipe = '%.4fs' % (time.time() - sniped_start_time)
                code = re.search("discord.gift/(.*)", message.content).group(1)
                if len(code) >= 16:
                    code = code[:16]
                    async with httpx.AsyncClient() as client:
                        start_time = time.time()
                        result = await client.post(
                            f'https://discord.com/api/{api_version}/entitlements/gift-codes/{code}/redeem',
                            json={'channel_id': message.channel.id},
                            headers={'authorization': user_token, 'user-agent': 'Mozilla/5.0'}
                        )
                        elapsed = '%.3fs' % (time.time() - start_time)
                    if 'nitro' in str(result.content):
                        status = 'Nitro successfully redeemed'
                    elif 'This gift has been redeemed already' in str(result.content):
                        status = 'Has been redeemed already'
                    else:
                        status = 'Unknown gift code'

                    if nitro_cooldown.count(code) == 0:
                        nitro_cooldown.append(code)

                        print()
                        prints.sniper(status)
                        prints.sniper(
                            f"Server  | {message.guild}"
                        )
                        prints.sniper(
                            f"Channel | {message.channel}"
                        )
                        prints.sniper(
                            f"Author  | {message.author}"
                        )
                        prints.sniper(f"Code    | {code}")
                        prints.sniper('Elapsed Times')
                        prints.sniper(
                            f"Sniped  | {elapsed_snipe}"
                        )
                        prints.sniper(
                            f"Request | {elapsed}"
                        )
                        print()

                        if files.json(
                                "data/notifications/toasts.json",
                                "nitro",
                                documents=False
                        ) == "on" and files.json(
                            "data/notifications/toasts.json",
                            "toasts",
                            documents=False
                        ) == "on":
                            notify.toast(
                                f"{status}\nServer »  {message.guild}\nChannel » {message.channel}\nAuthor »  {message.author}"
                            )
                        if files.json(
                                "data/webhooks/webhooks.json",
                                "nitro",
                                documents=False
                        ) == "on" and files.json(
                            "data/webhooks/webhooks.json",
                            "webhooks",
                            documents=False
                        ) == "on" and not webhook.nitro_url() == "webhook-url-here":
                            notify.webhook(
                                url=webhook.nitro_url(),
                                name="nitro",
                                description=f"{status}\n"
                                            f"Server » {message.guild}\n"
                                            f"Channel » {message.channel}\n"
                                            f"Author » {message.author}\n"
                                            f"Code » {code}\n"
                                            f"Elapsed Times\n"
                                            f"Sniped » {elapsed_snipe}\n"
                                            f"Request » {elapsed}"
                            )

                        nitro_ratelimit = files.json(
                            "data/snipers/nitro.json", "charge", documents=False
                        )
                        if nitro_ratelimit == "on":
                            startup_status = files.json(
                                "data/config.json", "startup_status", documents=False
                            )
                            headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7',
                            'Content-Type': 'application/json',
                            'Authorization': user_token,
                            }
                            request = requests.Session()
                            setting = {
                                'status': startup_status,
                                "custom_status": {"text": f"Ratelimit: [⠀⠀⠀⠀⠀]"}
                            }
                            request.patch(f"https://discord.com/api/{api_version}/users/@me/settings",headers=headers, json=setting, timeout=10)
                            await asyncio.sleep(1)
                            setting = {
                                'status': startup_status,
                                "custom_status": {"text": f"Ratelimit: [#⠀⠀⠀⠀]"}
                            }
                            request.patch(f"https://discord.com/api/{api_version}/users/@me/settings",headers=headers, json=setting, timeout=10)
                            await asyncio.sleep(1)
                            setting = {
                                'status': startup_status,
                                "custom_status": {"text": f"Ratelimit: [##⠀⠀⠀]"}
                            }
                            request.patch(f"https://discord.com/api/{api_version}/users/@me/settings",headers=headers, json=setting, timeout=10)
                            await asyncio.sleep(1)
                            setting = {
                                'status': startup_status,
                                "custom_status": {"text": f"Ratelimit: [###⠀⠀]"}
                            }
                            request.patch(f"https://discord.com/api/{api_version}/users/@me/settings",headers=headers, json=setting, timeout=10)
                            await asyncio.sleep(1)
                            setting = {
                                'status': startup_status,
                                "custom_status": {"text": f"Ratelimit: [####⠀]"}
                            }
                            request.patch(f"https://discord.com/api/{api_version}/users/@me/settings",headers=headers, json=setting, timeout=10)
                            await asyncio.sleep(1)
                            setting = {
                                'status': startup_status,
                                "custom_status": {"text": f"Ratelimit: [#####]"}
                            }
                            request.patch(f"https://discord.com/api/{api_version}/users/@me/settings",headers=headers, json=setting, timeout=10)

            elif files.json(
                    "data/snipers/nitro.json", "sniper",
                    documents=False
            ) == "on" and 'discord.com/gifts' in message.content.lower():
                elapsed_snipe = '%.4fs' % (time.time() - sniped_start_time)
                code = re.search(
                    "discord.com/gifts/(.*)",
                    message.content
                ).group(1)
                if len(code) >= 16:
                    async with httpx.AsyncClient() as client:
                        start_time = time.time()
                        result = await client.post(
                            f'https://discord.com/api/{api_version}/entitlements/gift-codes/{code}/redeem',
                            json={'channel_id': message.channel.id},
                            headers={'authorization': user_token, 'user-agent': 'Mozilla/5.0'}
                        )
                        elapsed = '%.3fs' % (time.time() - start_time)
                    if 'nitro' in str(result.content):
                        status = 'Nitro successfully redeemed'
                    elif 'This gift has been redeemed already' in str(result.content):
                        status = 'Has been redeemed already'
                    else:
                        status = 'Unknown gift code'

                    if nitro_cooldown.count(code) == 0:
                        nitro_cooldown.append(code)

                        print()
                        prints.sniper(status)
                        prints.sniper(
                            f"Server  | {message.guild}"
                        )
                        prints.sniper(
                            f"Channel | {message.channel}"
                        )
                        prints.sniper(
                            f"Author  | {message.author}"
                        )
                        prints.sniper(f"Code    | {code}")
                        prints.sniper('Elapsed Times')
                        prints.sniper(
                            f"Sniped  | {elapsed_snipe}"
                        )
                        prints.sniper(
                            f"Request | {elapsed}"
                        )
                        print()

                        if files.json(
                                "data/notifications/toasts.json",
                                "nitro",
                                documents=False
                        ) == "on" and files.json(
                            "data/notifications/toasts.json",
                            "toasts",
                            documents=False
                        ) == "on":
                            notify.toast(
                                f"{status}\nServer »  {message.guild}\nChannel » {message.channel}\nAuthor »  {message.author}"
                            )
                        if files.json(
                                "data/webhooks/webhooks.json",
                                "nitro",
                                documents=False
                        ) == "on" and files.json(
                            "data/webhooks/webhooks.json",
                            "webhooks",
                            documents=False
                        ) == "on" and not webhook.nitro_url() == "webhook-url-here":
                            notify.webhook(
                                url=webhook.nitro_url(),
                                name="nitro",
                                description=f"{status}\n"
                                            f"Server » {message.guild}\n"
                                            f"Channel » {message.channel}\n"
                                            f"Author » {message.author}\n"
                                            f"Code » {code}\n"
                                            f"Elapsed Times\n"
                                            f"Sniped » {elapsed_snipe}\n"
                                            f"Request » {elapsed}"
                            )

                        nitro_ratelimit = files.json(
                            "data/snipers/nitro.json", "charge", documents=False
                        )
                        if nitro_ratelimit == "on":
                            startup_status = files.json(
                                "data/config.json", "startup_status", documents=False
                            )
                            headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7',
                            'Content-Type': 'application/json',
                            'Authorization': user_token,
                            }
                            request = requests.Session()
                            setting = {
                                'status': startup_status,
                                "custom_status": {"text": f"Ratelimit: [⠀⠀⠀⠀⠀]"}
                            }
                            request.patch(f"https://discord.com/api/{api_version}/users/@me/settings",headers=headers, json=setting, timeout=10)
                            await asyncio.sleep(1)
                            setting = {
                                'status': startup_status,
                                "custom_status": {"text": f"Ratelimit: [#⠀⠀⠀⠀]"}
                            }
                            request.patch(f"https://discord.com/api/{api_version}/users/@me/settings",headers=headers, json=setting, timeout=10)
                            await asyncio.sleep(1)
                            setting = {
                                'status': startup_status,
                                "custom_status": {"text": f"Ratelimit: [##⠀⠀⠀]"}
                            }
                            request.patch(f"https://discord.com/api/{api_version}/users/@me/settings",headers=headers, json=setting, timeout=10)
                            await asyncio.sleep(1)
                            setting = {
                                'status': startup_status,
                                "custom_status": {"text": f"Ratelimit: [###⠀⠀]"}
                            }
                            request.patch(f"https://discord.com/api/{api_version}/users/@me/settings",headers=headers, json=setting, timeout=10)
                            await asyncio.sleep(1)
                            setting = {
                                'status': startup_status,
                                "custom_status": {"text": f"Ratelimit: [####⠀]"}
                            }
                            request.patch(f"https://discord.com/api/{api_version}/users/@me/settings",headers=headers, json=setting, timeout=10)
                            await asyncio.sleep(1)
                            setting = {
                                'status': startup_status,
                                "custom_status": {"text": f"Ratelimit: [#####]"}
                            }
                            request.patch(f"https://discord.com/api/{api_version}/users/@me/settings",headers=headers, json=setting, timeout=10)
        except Exception as e:
            prints.error(e)

        giveaway_joiner = files.json(
            "data/snipers/giveaway.json", "joiner", documents=False
        )
        delay_in_minutes = int(
            files.json(
                "data/snipers/giveaway.json", "delay_in_minutes", documents=False
            )
        )
        giveaway_blocked_words = files.json(
            "data/snipers/giveaway.json", "blocked_words", documents=False
        )
        guild_joiner = files.json(
            "data/snipers/giveaway.json", "guild_joiner", documents=False
        )
        if giveaway_joiner == "on" and message.author.bot and message.guild is not None and not isinstance(
                message.channel, discord.GroupChannel
        ):
            custom_giveaway_bot_ids = []
            custom_giveaway_bot_reactions = []
            try:
                if os.path.exists(f"data/snipers/giveaway_bots.json"):
                    with open(
                            f"data/snipers/giveaway_bots.json", "r",
                            encoding="utf-8"
                    ) as jsonFile:
                        data = json.load(jsonFile)

                    for key, value in data.items():
                        try:
                            custom_giveaway_bot_ids.append(int(key))
                            custom_giveaway_bot_reactions.append(str(value))
                        except Exception:
                            pass
            except Exception:
                pass
            embeds = message.embeds
            for embed in embeds:
                if ((("giveaway" in str(message.content).lower()) and (
                        int(message.author.id) in custom_giveaway_bot_ids) and (
                             "cancelled" not in str(message.content).lower()) and (
                             "mention" not in str(message.content).lower()) and (
                             "specify" not in str(message.content).lower()) and (
                             "congratulations" not in str(message.content).lower())) and embed is not None):
                    found_something_blacklisted = 0
                    for blocked_word in giveaway_blocked_words:
                        if str(blocked_word).lower() in str(
                                message.content
                        ).lower():
                            print()
                            prints.sniper(
                                f"Skipped giveaway"
                            )
                            prints.sniper(
                                f"Reason  | Backlisted word » {blocked_word}"
                            )
                            prints.sniper(
                                f"Server  | {message.guild}"
                            )
                            prints.sniper(
                                f"Channel | {message.channel}"
                            )
                            print()
                            if files.json(
                                    "data/notifications/toasts.json",
                                    "giveaway",
                                    documents=False
                            ) == "on" and files.json(
                                "data/notifications/toasts.json",
                                "toasts",
                                documents=False
                            ) == "on":
                                notify.toast(
                                    f"Skipped giveaway\nReason » {blocked_word}\nServer »  {message.guild}\nChannel » {message.channel}"
                                )
                            if files.json(
                                    "data/webhooks/webhooks.json",
                                    "giveaway",
                                    documents=False
                            ) == "on" and files.json(
                                "data/webhooks/webhooks.json",
                                "webhooks",
                                documents=False
                            ) == "on" and not webhook.giveaway_url() == "webhook-url-here":
                                notify.webhook(
                                    url=webhook.giveaway_url(),
                                    name="giveaway",
                                    description=f"Skipped giveaway\nReason » {blocked_word}\nServer »  {message.guild}\nChannel » {message.channel}"
                                )
                            found_something_blacklisted = 1
                    try:
                        for _embed in message.embeds:
                            embed_dict = _embed.to_dict()
                            for blocked_word in giveaway_blocked_words:
                                try:
                                    found = re.findall(
                                        blocked_word, str(embed_dict).lower()
                                    )[0]
                                    if found:
                                        print()
                                        prints.sniper(
                                            f"Skipped giveaway"
                                        )
                                        prints.sniper(
                                            f"Reason  | Backlisted word » {blocked_word}"
                                        )
                                        prints.sniper(
                                            f"Server  | {message.guild}"
                                        )
                                        prints.sniper(
                                            f"Channel | {message.channel}"
                                        )
                                        print()
                                        if files.json(
                                                "data/notifications/toasts.json",
                                                "giveaway",
                                                documents=False
                                        ) == "on" and files.json(
                                            "data/notifications/toasts.json",
                                            "toasts",
                                            documents=False
                                        ) == "on":
                                            notify.toast(
                                                f"Skipped giveaway\nReason » {blocked_word}\nServer »  {message.guild}\nChannel » {message.channel}"
                                            )
                                        if files.json(
                                                "data/webhooks/webhooks.json",
                                                "giveaway",
                                                documents=False
                                        ) == "on" and files.json(
                                            "data/webhooks/webhooks.json",
                                            "webhooks",
                                            documents=False
                                        ) == "on" and not webhook.giveaway_url() == "webhook-url-here":
                                            notify.webhook(
                                                url=webhook.giveaway_url(),
                                                name="giveaway",
                                                description=f"Skipped giveaway\nReason » {blocked_word}\nServer »  {message.guild}\nChannel » {message.channel}"
                                            )
                                        found_something_blacklisted = 1
                                        break
                                except BaseException:
                                    pass

                                if found_something_blacklisted > 0:
                                    break
                    except BaseException:
                        pass

                    if found_something_blacklisted == 0:
                        try:
                            embeds = message.embeds
                            joined_server = 'None'
                            giveaway_prize = None
                            try:
                                for embed_1 in embeds:
                                    giveaway_prize = embed_1.to_dict()[
                                        'author']['name']
                            except Exception:
                                for embed_2 in embeds:
                                    giveaway_prize = embed_2.to_dict()['title']
                            if guild_joiner == "on":
                                try:
                                    for embed_3 in embeds:
                                        embed_dict = embed_3.to_dict()
                                        code = re.findall(
                                            r"\w[a-z]*\W*\w[a-z]+\.\wg*\W\S*", str(
                                                embed_dict['description']
                                            )
                                        )[0].replace(
                                            ")", ""
                                        ).replace(
                                            "https://discord.gg/", ""
                                        )
                                        async with httpx.AsyncClient() as client:
                                            await client.post(f'https://discord.com/api/{api_version}/invites/{code}', headers={'authorization': user_token, 'user-agent': 'Mozilla/5.0'})
                                            joined_server = f'discord.gg/{code}'
                                            await asyncio.sleep(5)
                                except Exception:
                                    pass
                            else:
                                pass
                            print()
                            prints.sniper("Giveaway found")
                            prints.sniper(
                                f"Prize   | {giveaway_prize}"
                            )
                            prints.sniper(
                                f"Server  | {message.guild}"
                            )
                            prints.sniper(
                                f"Channel | {message.channel}"
                            )
                            prints.sniper(
                                f"Joining | In {delay_in_minutes} minute/s"
                            )
                            prints.sniper(
                                f"Invite  | Joined guild » {joined_server}"
                            )
                            print()
                            if files.json(
                                    "data/notifications/toasts.json",
                                    "giveaway",
                                    documents=False
                            ) == "on" and files.json(
                                "data/notifications/toasts.json",
                                "toasts",
                                documents=False
                            ) == "on":
                                notify.toast(
                                    f"Giveaway found\nPrize » {giveaway_prize}\nServer »  {message.guild}\nChannel » {message.channel}"
                                )
                            if files.json(
                                    "data/webhooks/webhooks.json",
                                    "giveaway",
                                    documents=False
                            ) == "on" and files.json(
                                "data/webhooks/webhooks.json",
                                "webhooks",
                                documents=False
                            ) == "on" and not webhook.giveaway_url() == "webhook-url-here":
                                notify.webhook(
                                    url=webhook.giveaway_url(),
                                    name="giveaway",
                                    description=f"Giveaway found\nPrize » {giveaway_prize}\nServer »  {message.guild}\nChannel » {message.channel}"
                                )
                        except Exception as e:
                            prints.error(e)
                            return

                        await asyncio.sleep(delay_in_minutes * 60)

                        try:
                            if int(
                                    message.author.id
                            ) in custom_giveaway_bot_ids:
                                index = custom_giveaway_bot_ids.index(
                                    int(message.author.id)
                                )
                                try:
                                    await message.add_reaction(custom_giveaway_bot_reactions[index])
                                except Exception as e:
                                    prints.error(e)
                                    return
                                print()
                                prints.sniper(
                                    f"Joined giveaway"
                                )
                                prints.sniper(
                                    f"Prize   | {giveaway_prize}"
                                )
                                prints.sniper(
                                    f"Server  | {message.guild}"
                                )
                                prints.sniper(
                                    f"Channel | {message.channel}"
                                )
                                print()
                                if files.json(
                                        "data/notifications/toasts.json",
                                        "giveaway",
                                        documents=False
                                ) == "on" and files.json(
                                    "data/notifications/toasts.json",
                                    "toasts",
                                    documents=False
                                ) == "on":
                                    notify.toast(
                                        f"Joined giveaway\nPrize » {giveaway_prize}\nServer »  {message.guild}\nChannel » {message.channel}"
                                    )
                                if files.json(
                                        "data/webhooks/webhooks.json",
                                        "giveaway",
                                        documents=False
                                ) == "on" and files.json(
                                    "data/webhooks/webhooks.json",
                                    "webhooks",
                                    documents=False
                                ) == "on" and not webhook.giveaway_url() == "webhook-url-here":
                                    notify.webhook(
                                        url=webhook.giveaway_url(),
                                        name="giveaway",
                                        description=f"Joined giveaway\n"
                                                    f"Prize » {giveaway_prize}\n"
                                                    f"Server »  {message.guild}\n"
                                                    f"Channel » {message.channel}"
                                    )
                        except Exception:
                            pass

                if '<@' + str(bot.user.id) + '>' in message.content and (
                        'giveaway' in str(message.content).lower() or ' won ' in message.content or ' winner ' in str(
                    message.content
                ).lower()) and message.author.bot and message.author.id in custom_giveaway_bot_ids:
                    print()
                    prints.sniper("Won giveaway")
                    prints.sniper(
                        f"Server  | {message.guild}"
                    )
                    prints.sniper(
                        f"Channel | {message.channel}"
                    )
                    print()
                    if files.json(
                            "data/notifications/toasts.json",
                            "giveaway",
                            documents=False
                    ) == "on" and files.json(
                        "data/notifications/toasts.json",
                        "toasts",
                        documents=False
                    ) == "on":
                        notify.toast(
                            f"Won giveaway\nServer »  {message.guild}\nChannel » {message.channel}"
                        )
                    if files.json(
                            "data/webhooks/webhooks.json",
                            "giveaway",
                            documents=False
                    ) == "on" and files.json(
                        "data/webhooks/webhooks.json",
                        "webhooks",
                        documents=False
                    ) == "on" and not webhook.giveaway_url() == "webhook-url-here":
                        notify.webhook(
                            url=webhook.giveaway_url(),
                            name="giveaway",
                            description=f"Won giveaway\nServer »  {message.guild}\nChannel » {message.channel}"
                        )
            if giveaway_joiner == "on" and message.author.bot:
                if "joining" in str(
                        message.content
                ).lower() and guild_joiner == "on":
                    try:
                        for _ in embeds:
                            code = re.findall(
                                r"\w[a-z]*\W*\w[a-z]+\.\w[g]*\W\S*", str(
                                    message.content
                                ).replace(
                                    ")", ""
                                ).replace(
                                    "https://discord.gg/", ""
                                )
                            )
                            async with httpx.AsyncClient() as client:
                                await client.post(
                                    f'https://canary.discord.com/api/{api_version}/invites/{code}',
                                    headers={'authorization': user_token, 'user-agent': 'Mozilla/5.0'}
                                )
                                joined_server = f'discord.gg/{code}'
                                if files.json(
                                        "data/notifications/toasts.json",
                                        "giveaway",
                                        documents=False
                                ) == "on" and files.json(
                                    "data/notifications/toasts.json",
                                    "toasts",
                                    documents=False
                                ) == "on":
                                    notify.toast(
                                        f"Joined guild\nInvite » {joined_server}"
                                    )
                                if files.json(
                                        "data/webhooks/webhooks.json",
                                        "giveaway",
                                        documents=False
                                ) == "on" and files.json(
                                    "data/webhooks/webhooks.json",
                                    "webhooks",
                                    documents=False
                                ) == "on" and not webhook.giveaway_url() == "webhook-url-here":
                                    notify.webhook(
                                        url=webhook.giveaway_url(),
                                        name="giveaway",
                                        description=f"Joined guild\nInvite » {joined_server}"
                                    )
                                await asyncio.sleep(5)
                    except Exception:
                        pass
                else:
                    pass
        # ///////////////////////////////////////////////////////////////
        # Copy Member

        if copycat is not None and copycat.id == message.author.id:
            await message.channel.send(chr(173) + message.content)

        # ///////////////////////////////////////////////////////////////
        # Share command
        prefix = files.json("data/config.json", "prefix", documents=False)
        share = files.json(f"data/sharing.json", "share", documents=False)
        user_id = files.json(f"data/sharing.json", "user_id", documents=False)

        if share == "on":
            if message.author.id == user_id:
                if message.content.startswith(prefix + "prefix"):
                    try:
                        await message.delete()
                    except BaseException:
                        pass
                    try:
                        await message.channel.send("You are prohibited from using that command")
                    except BaseException:
                        pass
                elif message.content.startswith(prefix + "darkmode"):
                    try:
                        await message.delete()
                    except BaseException:
                        pass
                    try:
                        await message.channel.send("You are prohibited from using that command")
                    except BaseException:
                        pass
                elif message.content.startswith(prefix + "lightmode"):
                    try:
                        await message.delete()
                    except BaseException:
                        pass
                    try:
                        await message.channel.send("You are prohibited from using that command")
                    except BaseException:
                        pass
                elif message.content.startswith(prefix + "ip"):
                    try:
                        await message.delete()
                    except BaseException:
                        pass
                    try:
                        await message.channel.send("You are prohibited from using that command")
                    except BaseException:
                        pass
                elif message.content.startswith(prefix):
                    try:
                        await message.delete()
                    except BaseException:
                        pass
                    try:
                        await message.channel.send(message.content)
                    except BaseException:
                        pass
            else:
                pass

        # ///////////////////////////////////////////////////////////////
        # AFK System

        global afk_status
        global afk_user_id
        global afk_reset

        if afk_status == 1 and afk_user_id == 0:
            afkmessage = files.json(
                "data/config.json", "afk_message", documents=False
            )
            if afkmessage == "":
                afkmessage = "This is an autoresponse message! User is now AFK.."
            if message.guild is None and not isinstance(
                    message.channel, discord.GroupChannel
            ):
                if message.author == self.bot.user:
                    return

                if configs.mode() == 2:
                    sent = await message.channel.send(f"```ini\n[ AFK ]\n\n{afkmessage}\n\n[ {theme.footer()} ]```")
                else:
                    sent = await message.channel.send(f"**AFK**\n\n```\n{afkmessage}\n```\n\n{theme.footer()}")

                afk_user_id = message.author.id
                await asyncio.sleep(60)
                afk_user_id = 0
                await sent.delete()

        # ///////////////////////////////////////////////////////////////
        # Mention

        if f'<@{self.bot.user.id}>' in message.content or f'<@!{self.bot.user.id}>' in message.content.lower():
            if files.json(
                    "data/notifications/toasts.json",
                    "pings",
                    documents=False
            ) == "on" and files.json(
                "data/notifications/toasts.json",
                "toasts",
                documents=False
            ) == "on":
                notify.toast(
                    f"You have been mentioned\nServer »  {message.guild}\nChannel » {message.channel}\nAuthor »  {message.author}"
                )
            if files.json(
                    "data/webhooks/webhooks.json",
                    "pings",
                    documents=False
            ) == "on" and files.json(
                "data/webhooks/webhooks.json",
                "webhooks",
                documents=False
            ) == "on" and not webhook.pings_url() == "webhook-url-here":
                notify.webhook(
                    url=webhook.pings_url(),
                    name="pings",
                    description=f"You have been mentioned\nServer »  {message.guild}\nChannel » {message.channel}\nAuthor »  {message.author}"
                )
            if files.json(
                    "data/notifications/console.json",
                    "pings",
                    documents=False
            ) == "on":
                print()
                prints.sniper("You have been mentioned")
                prints.sniper(f"Server  | {message.guild}")
                prints.sniper(
                    f"Channel | {message.channel}"
                )
                prints.sniper(f"Author  | {message.author}")
                print()

        # ///////////////////////////////////////////////////////////////
        # Privnote Sniper

        if 'privnote.com' in message.content.lower():
            elapsed_snipe = '%.3fs' % (time.time() - sniped_start_time)
            privnote_sniper = files.json(
                f"data/snipers/privnote.json", "sniper", documents=False
            )
            if privnote_sniper == "on":
                code = re.search('privnote.com/(.*)', message.content).group(1)
                link = 'https://privnote.com/' + code
                try:
                    start_time = time.time()
                    note_text = pyPrivnote.read_note(link)
                    elapsed = '%.3fs' % (time.time() - start_time)
                    print()
                    prints.sniper('Privnote sniped')
                    prints.sniper(
                        f"Server  | {message.guild}"
                    )
                    prints.sniper(
                        f"Channel | {message.channel}"
                    )
                    prints.sniper(
                        f"Author  | {message.author}"
                    )
                    prints.sniper(f"Link    | {link}")
                    prints.sniper(f"Code    | {code}")
                    prints.sniper('Elapsed Times')
                    prints.sniper(
                        f"Sniped  | {elapsed_snipe}"
                    )
                    prints.sniper(
                        f"Read    | {elapsed}"
                    )
                    print()
                    file = open(

                        f"data/privnote/{code}.txt", 'wb'
                    )
                    file.write(str(note_text))
                    file.close()
                except Exception:
                    print()
                    prints.sniper('Privnote already sniped')
                    prints.sniper(
                        f"Server  | {message.guild}"
                    )
                    prints.sniper(
                        f"Channel | {message.channel}"
                    )
                    prints.sniper(
                        f"Author  | {message.author}"
                    )
                    prints.sniper(f"Link    | {link}")
                    prints.sniper(f"Code    | {code}")
                    prints.sniper('Elapsed Times')
                    prints.sniper(
                        f"Sniped  | {elapsed_snipe}"
                    )
                    print()
            else:
                return

        # ///////////////////////////////////////////////////////////////
        # Anti-Invite
        if 'discord.gg/' in message.content.lower() and anti_invite:
            guilds = files.json(
                "data/protections/config.json", "guilds", documents=False
            )
            if message.guild.id in guilds:
                try:
                    await message.delete()
                except BaseException:
                    pass
                try:
                    sent = await message.channel.send(
                        f"```ini\n[ Anti Invite ]\n\n\"Anti Invite\" is enabled, sending Discord invites is not allowed.\n\n[ {theme.footer()} ]```"
                    )
                    await asyncio.sleep(30)
                    await sent.delete()
                except BaseException:
                    pass

        # ///////////////////////////////////////////////////////////////
        # Anti-Upper
        if message.content.isupper() and anti_upper:
            guilds = files.json(
                "data/protections/config.json", "guilds", documents=False
            )
            if message.guild.id in guilds:
                try:
                    await message.delete()
                except BaseException:
                    pass
                try:
                    sent = await message.channel.send(
                        f"```ini\n[ Anti Upper ]\n\n\"Anti Upper\" is enabled, sending all uppercase is not allowed.\n\n[ {theme.footer()} ]```"
                    )
                    await asyncio.sleep(30)
                    await sent.delete()
                except BaseException:
                    pass

        # ///////////////////////////////////////////////////////////////
        # Anti-Phishing
        if message.content in phishing_list and anti_phishing:
            guilds = files.json(
                "data/protections/config.json", "guilds", documents=False
            )
            if message.guild.id in guilds:
                try:
                    await message.delete()
                except BaseException:
                    pass
                try:
                    sent = await message.channel.send(
                        f"```ini\n[ Anti Phishing Links ]\n\n\"Anti Phishing Links\" is enabled, the url you sent, is banned.\n\n[ {theme.footer()} ]```"
                    )
                    await asyncio.sleep(30)
                    await sent.delete()
                except BaseException:
                    pass


bot.add_cog(OnMessage(bot))


# ///////////////////////////////////////////////////////////////
# On Message Delete Event


class OnDelete(commands.Cog, name="on delete"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.bot.user:
            return

        if f'<@!{self.bot.user.id}>' in message.content:
            if files.json(
                    "data/notifications/toasts.json",
                    "ghostpings",
                    documents=False
            ) == "on" and files.json(
                "data/notifications/toasts.json",
                "toasts",
                documents=False
            ) == "on":
                notify.toast(
                    f"You have been ghostpinged\nServer »  {message.guild}\nChannel » {message.channel}\nAuthor »  {message.author}"
                )
            if files.json(
                    "data/webhooks/webhooks.json",
                    "ghostpings",
                    documents=False
            ) == "on" and files.json(
                "data/webhooks/webhooks.json",
                "webhooks",
                documents=False
            ) == "on" and not webhook.ghostpings_url() == "webhook-url-here":
                notify.webhook(
                    url=webhook.ghostpings_url(),
                    name="ghostpings",
                    description=f"You have been ghostpinged\nServer »  {message.guild}\nChannel » {message.channel}\nAuthor »  {message.author}"
                )
            print()
            prints.sniper("You have been ghostpinged")
            prints.sniper(f"Server  | {message.guild}")
            prints.sniper(
                f"Channel | {message.channel}"
            )
            prints.sniper(f"Author  | {message.author}")
            print()

        # ///////////////////////////////////////////////////////////////
        # Anti Deleting

        if anti_deleting:
            guilds = files.json(
                "data/protections/config.json", "guilds", documents=False
            )
            if message.guild.id in guilds:
                print()
                prints.event("Anti Deleting")
                prints.event(f"Server  | {message.guild}")
                prints.sniper(
                    f"Channel | {message.channel}"
                )
                prints.sniper(f"Author  | {message.author}")
                print()


bot.add_cog(OnDelete(bot))


class OnTyping(commands.Cog, name="on typing"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_typing(self, channel, member, when):
        if member in self.bot.user.friends and isinstance(
                channel, discord.DMChannel
        ):
            if files.json(
                    "data/notifications/toasts.json",
                    "friendevents",
                    documents=False
            ) == "on" and files.json(
                "data/notifications/toasts.json",
                "toasts",
                documents=False
            ) == "on":
                notify.toast(f"{member} is typing")
            if files.json(
                    "data/webhooks/webhooks.json",
                    "friendevents",
                    documents=False
            ) == "on" and files.json(
                "data/webhooks/webhooks.json",
                "webhooks",
                documents=False
            ) == "on" and not webhook.friendevents_url() == "webhook-url-here":
                notify.webhook(
                    url=webhook.friendevents_url(
                    ), name="friendevents", description=f"{member} is typing"
                )


bot.add_cog(OnTyping(bot))

last_used = ""


class OnCommand(commands.Cog, name="on command"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, luna: commands.Context):
        prints.command(luna.command.name)
        global commands_used
        commands_used += 1
        dpg.set_value(commands_used_text, f"Commands Used: {commands_used}")
        with contextlib.suppress(discord.NotFound, AttributeError, RuntimeError):
            if "mreact" not in luna.command.name:
                await asyncio.sleep(0)
                await luna.message.delete()
        global last_used
        if luna.command.name != "repeat":
            last_used = luna.command.name

        theme_json = files.json("data/config.json", "theme", documents=False)
        try:
            if theme_json != "default":
                files.json(
                    f"data/themes/{theme_json}",
                    "title", documents=False
                )
        except BaseException:
            config.theme("default")
            await error_builder(
                luna,
                description=f"```\nThe configurated theme file was missing and has been set to \"default\"```"
            )
        return


bot.add_cog(OnCommand(bot))


class OnCommandErrorCog(commands.Cog, name="on command error"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, luna: commands.Context, error: Exception):
        error_str = str(error)
        if isinstance(error, commands.CommandOnCooldown):
            try:
                await luna.message.delete()
            except BaseException:
                pass
            day = round(error.retry_after / 86400)
            hour = round(error.retry_after / 3600)
            minute = round(error.retry_after / 60)
            if day > 0:
                if configs.error_log() == "console":
                    prints.error(
                        'This command is on cooldown, for ' +
                        str(day) +
                        "day(s)"
                    )
                else:
                    await luna.send('This command is on cooldown, for ' + str(day) + "day(s)", delete_after=3)
            elif hour > 0:
                if configs.error_log() == "console":
                    prints.error(
                        'This command is on cooldown, for ' +
                        str(hour) +
                        " hour(s)"
                    )
                else:
                    await luna.send('This command is on cooldown, for ' + str(hour) + " hour(s)", delete_after=3)
            elif minute > 0:
                if configs.error_log() == "console":
                    prints.error(
                        'This command is on cooldown, for ' +
                        str(minute) +
                        " minute(s)"
                    )
                else:
                    await luna.send('This command is on cooldown, for ' + str(minute) + " minute(s)", delete_after=3)
            else:
                if configs.error_log() == "console":
                    prints.error(
                        f'You are being ratelimited, for {error.retry_after:.2f} second(s)'
                    )
                else:
                    await luna.send(f'You are being ratelimited, for {error.retry_after:.2f} second(s)', delete_after=3)

        if isinstance(error, commands.CommandNotFound):
            try:
                await luna.message.delete()
            except BaseException:
                pass
            prefix = files.json("data/config.json", "prefix", documents=False)
            helptext = ""
            amount = 0
            for command in self.bot.commands:
                helptext += f"{prefix + command.name + ' ' + command.usage:<17} » {command.description},"

            error_text = f"{error}"
            subtract = len(error_text) - 14
            error_strip = error_text[9:subtract]
            commandlist = helptext.split(",")
            # commandlistfind = [ string for string in commandlist if error_strip in string]
            commandlistfind = [""]
            for string in commandlist:
                if amount < 5:
                    if error_strip in string:
                        commandlistfind = [string]
                        amount += 1
                else:
                    pass
            try:
                commandlistfind = '\n'.join(str(e) for e in commandlistfind)
            except BaseException:
                commandlistfind = ""
            if not len(commandlistfind) == 0:
                found = f"```\n\nDid you mean?\n\n{commandlistfind}```"
            else:
                found = ""
            if configs.error_log() == "message":
                await error_builder(
                    luna, f"```\nNot Found\n\n{error}```{found}```\nNote\n\nYou can use \"search\" to search for a command.\n{prefix}search <command> » Search for a command```"
                )
            else:
                await error_builder(luna, f"```\nNot Found\n\n{error}```")
        elif isinstance(error, CheckFailure):
            try:
                await luna.message.delete()
            except BaseException:
                pass
            await error_builder(luna, f"```\n{error}```")
        elif isinstance(error, commands.MissingRequiredArgument):
            try:
                await luna.message.delete()
            except BaseException:
                pass
            await error_builder(luna, f"```\nMissing arguments\n\n{error}```")
        elif isinstance(error, MissingPermissions):
            try:
                await luna.message.delete()
            except BaseException:
                pass
            await error_builder(luna, f"```\nMissing permissions\n\n{error}```")
        elif isinstance(error, commands.CommandInvokeError):
            try:
                await luna.message.delete()
            except BaseException:
                pass
            await error_builder(luna, f"```\n{error}```")
        elif "Cannot send an empty message" in error_str:
            try:
                await luna.message.delete()
            except BaseException:
                pass
            await error_builder(luna, f"```\n{error}```")
        elif "Cannot send messages to this user" in error_str:
            try:
                await luna.message.delete()
            except BaseException:
                pass
            await error_builder(luna, f"```\nCannot send a message to this user\n\n{error}```")
        elif "Cannot send messages in this channel" in error_str:
            try:
                await luna.message.delete()
            except BaseException:
                pass
            await error_builder(luna, f"```\nCannot send a message in this channel\n\n{error}```")
        elif "Cannot send files bigger than" in error_str:
            try:
                await luna.message.delete()
            except BaseException:
                pass
            await error_builder(luna, f"```\nCannot send files bigger than 8MB\n\n{error}```")
        else:
            try:
                await luna.message.delete()
            except BaseException:
                pass
            await error_builder(luna, f"```\n{error}```")


bot.add_cog(OnCommandErrorCog(bot))


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Commands

# ///////////////////////////////////////////////////////////////
# Help Commands (Listing Commands)

class HelpCog(commands.Cog, name="Help commands"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        name='help',
        usage="[command]",
        description="Display the help message",
        aliases=['h', '?']
    )
    async def help(self, luna, commandName: str = None):
        prefix = files.json("data/config.json", "prefix", documents=False)

        command_name2 = None
        stop = False
        if commandName is None:
            command_count = len(bot.commands)
            cog = bot.get_cog('Custom commands')
            custom = cog.get_commands()
            custom_command_count = sum(1 for _ in custom)
            await message_builder(
                luna,
                description=f"{theme.description()}```\n\
Luna\n\nCommands          » {command_count - custom_command_count}\n\
Custom Commands   » {custom_command_count}\n``````\n\
Categories\n\n\
{prefix}help [command]   » Display all commands\n\
{prefix}chelp            » Display custom commands\n\
{prefix}admin            » Administrative commands\n\
{prefix}abusive          » Abusive commands\n\
{prefix}animated         » Animated commands\n\
{prefix}dump             » Dumping\n\
{prefix}fun              » Funny commands\n\
{prefix}game             » Game commands\n\
{prefix}image            » Image commands\n\
{prefix}hentai           » Hentai explorer\n\
{prefix}profile          » Profile settings\n\
{prefix}protection       » Protections\n\
{prefix}text             » Text commands\n\
{prefix}trolling         » Troll commands\n\
{prefix}tools            » Tools\n\
{prefix}networking       » Networking\n\
{prefix}utility          » Utilities\n\
{prefix}settings         » Settings\n\
{prefix}sharing          » Share with somebody\n\
{prefix}themes           » Themes\n\
{prefix}misc             » Miscellaneous\n\
{prefix}repeat           » Repeat last used command\n\
{prefix}search <command> » Search for a command\n``````\n\
Version\n\n{version}```"
            )
        else:
            for i in self.bot.commands:
                if i.name == commandName.lower():
                    command_name2 = i
                    break
                else:
                    for j in i.aliases:
                        if j == commandName.lower():
                            command_name2 = i
                            stop = True
                            break
                        if stop is True:
                            break

            if command_name2 is None:
                if configs.error_log() == "console":
                    prints.error(
                        f"No command found with name or alias {color.print_gradient(commandName)}"
                    )
                else:
                    await error_builder(luna, f"```\nNo command found with name or alias {commandName}```")
            else:
                alias_list = ""
                if configs.mode() == 2:
                    aliases = command_name2.aliases
                    if len(aliases) > 0:
                        for alias in aliases:
                            alias_list += f"{alias}, "
                        alias_list = alias_list[:-2]
                        sent = await luna.send(
                            f"```ini\n[ {command_name2.name.title()} Command ]\n\n" f"{theme.description()}" f"Name\n{command_name2.name}\n\n" f"Aliases\n{alias_list}\n\n" f"Usage\nNone\n\n" f"Description\n{command_name2.description}\n\n" f"[ {theme.footer()} ]```"
                        ) if command_name2.usage is None else await luna.send(
                            f"```ini\n[ {command_name2.name.title()} Command ]\n\n" f"{theme.description()}" f"Name\n{command_name2.name}\n\n" f"Aliases\n{alias_list}\n\n" f"Usage\n{prefix}{command_name2.name} {command_name2.usage}\n\n" f"Description\n{command_name2.description}\n\n" f"[ {theme.footer()} ]```"
                        )

                    elif command_name2.usage is None:
                        sent = await luna.send(
                            f"```ini\n[ {command_name2.name.title()} Command ]\n\n"
                            f"{theme.description()}"
                            f"Name\n{command_name2.name}\n\n"
                            f"Aliases\nNone\n\n"
                            f"Usage\nNone\n\n"
                            f"Description\n{command_name2.description}\n\n"
                            f"[ {theme.footer()} ]```"
                        )
                    else:
                        sent = await luna.send(
                            f"```ini\n[ {command_name2.name.title()} Command ]\n\n"
                            f"{theme.description()}"
                            f"Name\n{command_name2.name}\n\n"
                            f"Aliases\nNone\n\n"
                            f"Usage\n{prefix}{command_name2.name} {command_name2.usage}\n\n"
                            f"Description\n{command_name2.description}\n\n"
                            f"[ {theme.footer()} ]```"
                        )
                else:
                    aliases = command_name2.aliases
                    if len(aliases) > 0:
                        for alias in aliases:
                            alias_list += f"{alias}, "
                        alias_list = alias_list[:-2]
                        sent = await luna.send(
                            f"> **{command_name2.name.title()} Command**\n>   " f"```\n> Name\n> {command_name2.name}```" f"```\n> Aliases\n> {alias_list}```" f"```\n> Usage\n> None```" f"```\n> Description\n> {command_name2.description}```\n" f"> {theme.footer()}"
                        ) if command_name2.usage is None else await luna.send(
                            f"> **{command_name2.name.title()} Command**\n>   " f"```\n> Name\n> {command_name2.name}```" f"```\n> Aliases\n> {alias_list}```" f"```\n> Usage\n> {prefix}{command_name2.name} {command_name2.usage}```" f"```\n> Description\n> {command_name2.description}```\n" f"> {theme.footer()}"
                        )

                    elif command_name2.usage is None:
                        sent = await luna.send(
                            f"> **{command_name2.name.title()} Command**\n>   "
                            f"```\n> Name\n> {command_name2.name}```"
                            f"```\n> Aliases\n> None```"
                            f"```\n> Usage\n> None```"
                            f"```\n> Description\n> {command_name2.description}```\n"
                            f"> {theme.footer()}"
                        )
                    else:
                        sent = await luna.send(
                            f"> **{command_name2.name.title()} Command**\n>   "
                            f"```\n> Name\n> {command_name2.name}```"
                            f"```\n> Aliases\n> None```"
                            f"```\n> Usage\n> {prefix}{command_name2.name} {command_name2.usage}```"
                            f"```\n> Description\n> {command_name2.description}```\n"
                            f"> {theme.footer()}"
                        )

                await asyncio.sleep(configs.delete_timer())
                await sent.delete()

    @commands.command(
        name="admin",
        usage="[2, 3]",
        description="Administrative commands"
    )
    async def admin(self, luna, page: str = "1"):

        prefix = files.json("data/config.json", "prefix", documents=False)
        cog = self.bot.get_cog('Administrative commands')
        commands = cog.get_commands()
        helptext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

        cog = self.bot.get_cog('Channel commands')
        commands = cog.get_commands()
        channeltext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

        cog = self.bot.get_cog('Member commands')
        commands = cog.get_commands()
        membertext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

        cog = self.bot.get_cog('Nickname commands')
        commands = cog.get_commands()
        nicktext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

        cog = self.bot.get_cog('Role commands')
        commands = cog.get_commands()
        roletext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

        cog = self.bot.get_cog('Invite commands')
        commands = cog.get_commands()
        invitetext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

        cog = self.bot.get_cog('Ignore commands')
        commands = cog.get_commands()
        ignoretext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

        if page == "2":
            await message_builder(
                luna, title="Administrative", footer_extra="Page 2",
                description=f"{theme.description()}" f"```\nMember Control\n\n{membertext}```" f"```\nNickname Control\n\n{nicktext}```" f"```\nGuild Control\n\n{helptext}```" f"```\nNote\n\n{prefix}admin 3 » Page 3```"
            )

        elif page == "3":
            await message_builder(
                luna, title="Administrative", footer_extra="Page 3", description=f"{theme.description()}" f"```\nInvite Control\n\n{invitetext}```" f"```\nIgnore Control\n\n{ignoretext}```"
            )

        else:
            await message_builder(
                luna, title="Administrative", footer_extra="Page 1",
                description=f"{theme.description()}" f"```\nChannel Control\n\n{channeltext}```" f"```\nRole Control\n\n{roletext}```" f"```\nNote\n\n{prefix}admin 2 » Page 2```"
            )

    @commands.command(
        name="profile",
        usage="",
        description="Profile settings"
    )
    async def profile(self, luna):

        prefix = files.json("data/config.json", "prefix", documents=False)
        cog = self.bot.get_cog('Profile commands')
        commands = cog.get_commands()
        helptext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

        cog = self.bot.get_cog('Animated statuses')
        commands = cog.get_commands()
        status_helptext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

        await message_builder(
            luna, title="Profile",
            description=f"{theme.description()}"
                        f"```\nCurrent profile\n\n"
                        f"User              » {bot.user}\n"
                        f"Username          » {bot.user.name}\n"
                        f"Discriminator     » {bot.user.discriminator}\n```"
                        f"```\nNickname Control\n\n"
                        f"{prefix}nick <name>      » Change your nickname\n"
                        f"{prefix}invisiblenick    » Make your nickname invisible\n"
                        f"{prefix}junknick         » Pure junk nickname\n```"
                        f"```\nUser Control\n\n{helptext}```"
                        f"```\nStatus Control\n\n{status_helptext}```"
        )

    @commands.command(
        name="animated",
        usage="",
        description="Animated commands"
    )
    async def animated(self, luna):

        prefix = files.json("data/config.json", "prefix", documents=False)
        cog = self.bot.get_cog('Animated commands')
        commands = cog.get_commands()
        helptext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

        await message_builder(luna, title="Animated commands", description=f"{theme.description()}```\n{helptext}```")

    @commands.command(
        name="dump",
        usage="",
        description="Dumping"
    )
    async def dump(self, luna):

        prefix = files.json("data/config.json", "prefix", documents=False)
        cog = self.bot.get_cog('Dump commands')
        commands = cog.get_commands()
        helptext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

        await message_builder(luna, title="Dumping", description=f"{theme.description()}```\n{helptext}```")

    @commands.command(
        name="text",
        usage="",
        description="Text commands"
    )
    async def text(self, luna):

        prefix = files.json("data/config.json", "prefix", documents=False)
        cog = self.bot.get_cog('Text commands')
        commands = cog.get_commands()
        helptext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

        cog = self.bot.get_cog('Codeblock commands')
        commands = cog.get_commands()
        helptext1 = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

        await message_builder(luna, title="Text commands", description=f"{theme.description()}```\nText\n\n{helptext}``````\nCodeblock\n\n{helptext1}```")

    @commands.command(
        name="game",
        usage="",
        description="Game commands"
    )
    async def game(self, luna):

        prefix = files.json("data/config.json", "prefix", documents=False)
        cog = self.bot.get_cog('Game commands')
        commands = cog.get_commands()
        helptext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

        await message_builder(luna, title="Game commands", description=f"{theme.description()}```\n{helptext}```")

    @commands.command(
        name="image",
        usage="",
        description="Image commands"
    )
    async def image(self, luna, page: str = "1"):

        prefix = files.json("data/config.json", "prefix", documents=False)
        cog = self.bot.get_cog('Image commands')
        commands = cog.get_commands()
        helptext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

        cog = self.bot.get_cog('Image commands 2')
        commands = cog.get_commands()
        if page == "2":
            helptext2 = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

            await message_builder(luna, title="Image commands", footer_extra="Page 2", description=f"{theme.description()}```\n{helptext2}```")

        else:
            await message_builder(luna, title="Image commands", footer_extra="Page 1", description=f"{theme.description()}```\n{helptext}``````\nNote\n\n{prefix}image 2 » Page 2```")

    @commands.command(
        name="hentai",
        usage="",
        description="Hentai explorer"
    )
    async def hentai(self, luna):

        prefix = files.json("data/config.json", "prefix", documents=False)

        cog = self.bot.get_cog('Hentai commands')
        commands = cog.get_commands()
        helptext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

        cog = self.bot.get_cog('HScroller commands')
        commands = cog.get_commands()
        helptext1 = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

        await message_builder(
            luna, title="Hentai Explorer", description=f"{theme.description()}```\nHScroller\n\nHigh quality anime provided by ThatOneCodeDev\n\n{helptext1}``````\n{helptext}```"
        )

    @commands.command(
        name="trolling",
        usage="",
        description="Trolling"
    )
    async def trolling(self, luna):

        prefix = files.json("data/config.json", "prefix", documents=False)
        cog = self.bot.get_cog('Troll commands')
        commands = cog.get_commands()
        helptext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

        await message_builder(luna, title="Trolling", description=f"{theme.description()}```\n{helptext}```")

    @commands.command(
        name="fun",
        usage="",
        description="Fun commands"
    )
    async def fun(self, luna):

        prefix = files.json("data/config.json", "prefix", documents=False)
        cog = self.bot.get_cog('Fun commands')
        commands = cog.get_commands()
        helptext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

        await message_builder(luna, title="Fun commands", description=f"{theme.description()}```\n{helptext}```")

    @commands.command(
        name="tools",
        usage="",
        description="Tools"
    )
    async def tools(self, luna):

        prefix = files.json("data/config.json", "prefix", documents=False)
        cog = self.bot.get_cog('Tools commands')
        commands = cog.get_commands()
        helptext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

        await message_builder(luna, title="Tools", description=f"{theme.description()}```\n{helptext}```")

    @commands.command(
        name="networking",
        usage="",
        description="Networking"
    )
    async def networking(self, luna):

        prefix = files.json("data/config.json", "prefix", documents=False)
        cog = self.bot.get_cog('Nettool commands')
        commands = cog.get_commands()
        helptext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

        await message_builder(luna, title="Networking", description=f"{theme.description()}```\n{helptext}```")

    @commands.command(
        name="utility",
        usage="",
        aliases=['utils', 'utilities'],
        description="Utilities"
    )
    async def utility(self, luna):

        prefix = files.json("data/config.json", "prefix", documents=False)
        cog = self.bot.get_cog('Util commands')
        commands = cog.get_commands()
        helptext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

        await message_builder(luna, title="Utilities", description=f"{theme.description()}```\n{helptext}```")

    @commands.command(
        name="abusive",
        usage="[2]",
        description="Abusive commands"
    )
    async def abusive(self, luna, page: str = "1"):

        if configs.risk_mode() == "on":
            prefix = files.json("data/config.json", "prefix", documents=False)
            cog = self.bot.get_cog('Abusive commands')
            commands = cog.get_commands()
            helptext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

            cog = self.bot.get_cog('Guild commands')
            commands = cog.get_commands()
            guildtext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

            cog = self.bot.get_cog('Mass commands')
            commands = cog.get_commands()
            masstext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

            cog = self.bot.get_cog('All commands')
            commands = cog.get_commands()
            alltext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

            cog = self.bot.get_cog('Spam commands')
            commands = cog.get_commands()
            spamtext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

            cog = self.bot.get_cog('Exploit commands')
            commands = cog.get_commands()
            if page == "2":
                await message_builder(
                    luna, title="Abusive commands", footer_extra="Page 2", description=f"{theme.description()}" f"```\nGuild\n\n{guildtext}\n```" f"```\nGeneral\n\n{helptext}\n```"
                )

            else:
                exploittext = "".join(f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n" for command in commands)

                await message_builder(
                    luna, title="Abusive commands", footer_extra="Page 1",
                    description=f"{theme.description()}" f"```\nExploits\n\n{exploittext}\n```" f"```\nSpam\n\n{spamtext}\n```" f"```\nMass\n\n{masstext}\n```" f"```\nAll\n\n{alltext}\n```" f"```\nNote\n\n{prefix}abusive 2 » Page 2```"
                )

        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="protection",
        usage="",
        aliases=['protections', 'protect'],
        description="Protections"
    )
    async def protection(self, luna):

        prefix = files.json("data/config.json", "prefix", documents=False)
        cog = self.bot.get_cog('Protection commands')
        commands = cog.get_commands()
        helptext = ""
        for command in commands:
            helptext += f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n"
        cog = self.bot.get_cog('Privacy commands')
        commands = cog.get_commands()
        privacytext = ""
        for command in commands:
            privacytext += f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n"
        cog = self.bot.get_cog('Backup commands')
        commands = cog.get_commands()
        backuptext = ""
        for command in commands:
            backuptext += f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n"
        cog = self.bot.get_cog('Whitelist commands')
        commands = cog.get_commands()
        whitelisttext = ""
        for command in commands:
            whitelisttext += f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n"
        activetext = ""
        if not active_list == []:
            activetext = f"\n\nActive protections:"
        for active in active_list:
            activetext += f"\n{active.title()}"
        cog = self.bot.get_cog('Protection Guild commands')
        commands = cog.get_commands()
        guildtext = ""
        for command in commands:
            guildtext += f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n"
        guilds = files.json(
            "data/protections/config.json",
            "guilds", documents=False
        )
        activeguildtext = ""
        if not guilds == []:
            activeguildtext = f"\nProtected guilds:"
            for guild_id in guilds:
                try:
                    guild = self.bot.get_guild(guild_id)
                    activeguildtext += f"\n{guild.name:17} » {guild}"
                except BaseException:
                    pass
        await message_builder(
            luna, title="Protections",
            description=f"{theme.description()}"
                        f"```\nEnabled Protections\n\n"
                        f"{'Enabled':17} » {active_protections}{activetext}\n```"
                        f"```\nGuild Configuration\n\n{guildtext}{activeguildtext}```"
                        f"```\nProtections\n\n{helptext}```"
                        f"```\nWhitelist\n\n{whitelisttext}\n```"
                        f"```\nPrivacy | Streamer Mode\n\n{privacytext}\n```"
                        f"```\nBackups\n\n{backuptext}\n```"
        )

    @commands.command(
        name="misc",
        usage="",
        description="Miscellaneous commands"
    )
    async def misc(self, luna):

        prefix = files.json("data/config.json", "prefix", documents=False)
        cog = self.bot.get_cog('Miscellaneous commands')
        commands = cog.get_commands()
        helptext = ""
        for command in commands:
            helptext += f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n"
        await message_builder(luna, title="Miscellaneous", description=f"{theme.description()}```\n{helptext}```")

    @commands.command(
        name="settings",
        usage="",
        description="Settings"
    )
    async def settings(self, luna):

        prefix = files.json("data/config.json", "prefix", documents=False)
        deletetimer = int(
            files.json(
                "data/config.json",
                "delete_timer", documents=False
            )
        )
        errorlog = files.json("data/config.json", "error_log", documents=False)
        riskmode = files.json("data/config.json", "risk_mode", documents=False)
        themesvar = files.json("data/config.json", "theme", documents=False)
        console_mode = files.json(
            "data/console/console.json", "mode", documents=False
        )
        if console_mode == "2":
            console_mode = "information"
        else:
            console_mode = "standard"
        if themesvar == "default":
            pass
        else:
            themesvar = (themesvar[:-5])
        if themesvar == "default":
            theme_description = descriptionvar_request
            if not theme_description == "true":
                theme_description = "off"
            else:
                theme_description = "on"
        else:
            theme_json = files.json(
                "data/config.json", "theme", documents=False
            )
            theme_description = files.json(
                f"data/themes/{theme_json}", "description", documents=False
            )
            if theme_description is None:
                theme_description = True
            if not theme_description:
                theme_description = "off"
            else:
                theme_description = "on"
        startup_status = files.json(
            "data/config.json", "startup_status", documents=False
        )
        title = theme.title()
        footer = theme.footer()
        selfbotdetection = files.json(
            "data/snipers/selfbot.json", "sniper", documents=False
        )
        pings = files.json(
            "data/notifications/console.json",
            "pings", documents=False
        )
        if title == "":
            title = "None"
        if footer == "":
            footer = "None"
        cog = self.bot.get_cog('Settings commands')
        commands = cog.get_commands()
        helptext = ""
        for command in commands:
            helptext += f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n"
        share = configs.share()
        user_id = configs.share_id()
        if user_id == "":
            sharinguser = "None"
        else:
            sharinguser = await self.bot.fetch_user(user_id)
        await message_builder(
            luna, title="Settings",
            description=f"{theme.description()}"
                        f"```\nYour current settings\n\n"
                        f"Error logging     » {errorlog}\n"
                        f"Auto delete timer » {deletetimer}\n"
                        f"Startup status    » {startup_status}\n"
                        f"Theme             » {themesvar}\n"
                        f"Console Mode      » {console_mode}\n"
                        f"Riskmode          » {riskmode}\n"
                        f"Description       » {theme_description}\n"
                        f"Selfbot detection » {selfbotdetection}\n"
                        f"Mention notify    » {pings}\n```"
                        f"```\nYour current theme settings\n\n"
                        f"Theme             » {themesvar}\n"
                        f"Title             » {title}\n"
                        f"Footer            » {footer}\n"
                        f"Description       » {theme_description}\n```"
                        f"```\nShare Settings\n\n"
                        f"Share             » {share}\n"
                        f"User              » {sharinguser}```"
                        f"```\nSettings\n\n{helptext}```"
        )

    @commands.command(
        name="sharing",
        usage="",
        description="Share commands"
    )
    async def sharing(self, luna):

        prefix = files.json("data/config.json", "prefix", documents=False)
        share = configs.share()
        user_id = configs.share_id()
        if user_id == "":
            sharinguser = "None"
        else:
            sharinguser = await self.bot.fetch_user(user_id)
        cog = self.bot.get_cog('Share commands')
        commands = cog.get_commands()
        helptext = ""
        for command in commands:
            helptext += f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n"
        await message_builder(
            luna, title="Sharing",
            description=f"{theme.description()}```\nYour current settings\n\nShare             » {share}\nUser              » {sharinguser}\n``````\n{helptext}```"
        )

    @commands.command(
        name="chelp",
        aliases=['customhelp'],
        usage="",
        description="Show custom commands"
    )
    async def chelp(self, luna):

        prefix = files.json("data/config.json", "prefix", documents=False)
        cog = self.bot.get_cog('Custom commands')
        commands = cog.get_commands()
        helptext = ""
        if not commands:
            helptext = "No custom commands found!"
        else:
            for command in commands:
                helptext += f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n"
        await message_builder(
            luna, title="Your custom commands",
            description=f"{theme.description()}```\n{helptext}``````\nCommand Control\n\n{prefix}restart          » Restart to load your commands\n{prefix}newcmd <name>    » Create new command```"
        )

    @commands.command(
        name="repeat",
        usage="",
        description="Repeat last used command"
    )
    async def repeat(self, luna):

        prefix = files.json("data/config.json", "prefix", documents=False)
        await luna.send(f"{prefix}{last_used}")

    @commands.command(
        name="search",
        usage="<command>",
        description="Search for a command"
    )
    async def search(self, luna, commandName: str):

        prefix = files.json("data/config.json", "prefix", documents=False)
        helptext = ""
        for command in self.bot.commands:
            helptext += f"{prefix + command.name + ' ' + command.usage:<17} » {command.description},"

        commandlist = helptext.split(",")
        commandlistfind = [
            string for string in commandlist if commandName in string]
        commandlistfind = '\n'.join(str(e) for e in commandlistfind)

        if not len(commandlistfind) == 0:
            await message_builder(
                luna, title=f"Searched for » {commandName.title()}",
                description=f"{theme.description()}```\n{commandlistfind}``````\nNote\n\n{prefix}help <command>   » To get more information```"
            )
        else:
            await message_builder(
                luna, title=f"Searched for » {commandName.title()}",
                description=f"```\nNo command has been found\n``````\nNote\n\n{prefix}help <command>   » To get more information```"
            )


bot.remove_command("help")
bot.add_cog(HelpCog(bot))


class ProfileCog(commands.Cog, name="Profile commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="online",
        usage="",
        description="Online status"
    )
    async def online(self, luna):
        await bot.change_presence(status=discord.Status.online, afk=True)
        payload = {'status': "online"}
        requests.patch(
            f'https://discord.com/api/{api_version}/users/@me/settings',
            json=payload,
            headers={
                'authorization': user_token,
                'user-agent': 'Mozilla/5.0'
            }
        )
        await message_builder(luna, description="```\nSet status to online```")

    @commands.command(
        name="idle",
        usage="",
        description="Idle status"
    )
    async def idle(self, luna):
        await bot.change_presence(status=discord.Status.idle, afk=True)
        payload = {'status': "idle"}
        requests.patch(
            f'https://discord.com/api/{api_version}/users/@me/settings',
            json=payload,
            headers={
                'authorization': user_token,
                'user-agent': 'Mozilla/5.0'
            }
        )
        await message_builder(luna, description="```\nSet status to idle```")

    @commands.command(
        name="dnd",
        usage="",
        description="Do not disturb status"
    )
    async def dnd(self, luna):
        await bot.change_presence(status=discord.Status.dnd, afk=True)
        payload = {'status': "dnd"}
        requests.patch(
            f'https://discord.com/api/{api_version}/users/@me/settings',
            json=payload,
            headers={
                'authorization': user_token,
                'user-agent': 'Mozilla/5.0'
            }
        )
        await message_builder(luna, description="```\nSet status to do not disturb```")

    @commands.command(
        name="offline",
        usage="",
        description="Offline status"
    )
    async def offline(self, luna):
        await bot.change_presence(status=discord.Status.invisible, afk=True)
        payload = {'status': "invisible"}
        requests.patch(
            f'https://discord.com/api/{api_version}/users/@me/settings',
            json=payload,
            headers={
                'authorization': user_token,
                'user-agent': 'Mozilla/5.0'
            }
        )
        await message_builder(luna, description="```\nSet status to offline/invisible```")

    @commands.command(
        name="startup",
        usage="<online/idle/dnd/offline>",
        description="Startup status"
    )
    async def startup(self, luna, mode: str = None):

        if mode == "online" or mode == "idle" or mode == "dnd" or mode == "offline":
            prints.message(f"Startup status » {mode}")
            config.startup_status(mode)
            await message_builder(luna, description=f"```\nStartup status » {mode}```")
        elif mode is None:
            startup_status = configs.startup_status()
            await message_builder(luna, description=f"```\nCurrent startup status » {startup_status}```")
        else:
            await mode_error(luna, "online, idle, dnd or offline")


bot.add_cog(ProfileCog(bot))


class StatusCog(commands.Cog, name="Animated statuses"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="status",
        usage="<text>",
        description="Set a custom status"
    )
    async def status(self, luna, *, text: str):
        payload = {'custom_status': {"text": f"{text}"}}
        requests.patch(
            f'https://discord.com/api/{api_version}/users/@me/settings',
            json=payload,
            headers={
                'authorization': user_token,
                'user-agent': 'Mozilla/5.0'
            }
        )
        await message_builder(luna, description=f"```\nSet custom status to » {text}```")

    @commands.command(
        name="removestatus",
        usage="",
        description="Remove custom status"
    )
    async def removestatus(self, luna):
        payload = {'custom_status': {"text": ""}}
        requests.patch(
            f'https://discord.com/api/{api_version}/users/@me/settings',
            json=payload,
            headers={
                'authorization': user_token,
                'user-agent': 'Mozilla/5.0'
            }
        )
        await message_builder(luna, description=f"```\nRemoved custom status```")


bot.add_cog(StatusCog(bot))


class ChannelCog(commands.Cog, name="Channel commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="channelinfo",
        usage="<#channel>",
        description="Information"
    )
    async def channelinfo(self, luna, channel: discord.TextChannel):

        await message_builder(
            luna, title="Channel Information",
            description=f"```\n{'Name':17} » {channel.name}\n"
                        f"{'ID':17} » {channel.id}\n"
                        f"{'Created at':17} » {channel.created_at}\n"
                        f"{'Category':17} » {channel.category}\n"
                        f"{'Position':17} » {channel.position}\n"
                        f"{'Topic':17} » {channel.topic}\n"
                        f"{'Is NSFW?':17} » {channel.is_nsfw()}\n```"
        )

    @commands.command(
        name="textchannel",
        usage="<name>",
        description="Create a text channel"
    )
    @commands.guild_only()
    @has_permissions(manage_channels=True)
    async def textchannel(self, luna, name: str):

        channel = await luna.guild.create_text_channel(name)
        await message_builder(luna, description=f"```\nCreated text channel » {channel.mention}```")

    @commands.command(
        name="voicechannel",
        usage="<name>",
        description="Create a voice channel"
    )
    @commands.guild_only()
    @has_permissions(manage_channels=True)
    async def voicechannel(self, luna, name: str):

        channel = await luna.guild.create_voice_channel(name)
        await message_builder(luna, description=f"```\nCreated voice channel » {channel.mention}```")

    @commands.command(
        name="stagechannel",
        usage="<name>",
        description="Create a stage channel"
    )
    @commands.guild_only()
    @has_permissions(manage_channels=True)
    async def stagechannel(self, luna, name: str):

        payload = {
            'name': f"{name}",
            'type': 13
        }
        requests.post(
            f'https://discord.com/api/{api_version}/guilds/{luna.guild.id}/channels',
            json=payload,
            headers={
                'authorization': user_token,
                'user-agent': 'Mozilla/5.0'
            }
        )
        await message_builder(luna, description=f"```\nCreated stage channel » {name}```")

    @commands.command(
        name="newschannel",
        usage="<name>",
        description="Create a news channel"
    )
    @commands.guild_only()
    @has_permissions(manage_channels=True)
    async def newschannel(self, luna, name: str):

        payload = {
            'name': f"{name}",
            'type': 5
        }
        requests.post(
            f'https://discord.com/api/{api_version}/guilds/{luna.guild.id}/channels',
            json=payload,
            headers={
                'authorization': user_token,
                'user-agent': 'Mozilla/5.0'
            }
        )
        await message_builder(luna, description=f"```\nCreated news channel » {name}```")

    @commands.command(
        name="renamechannel",
        usage="<#channel> <name>",
        description="Rename channel"
    )
    @commands.guild_only()
    @has_permissions(manage_channels=True)
    async def renamechannel(self, luna, channel: discord.TextChannel, name: str):

        await channel.edit(name=name)
        await message_builder(luna, description=f"```\nRenamed {luna.channel.name} to » {channel.mention}```")

    @commands.command(
        name="deletechannel",
        usage="<#channel>",
        description="Delete a channel"
    )
    @commands.guild_only()
    @has_permissions(manage_channels=True)
    async def deletechannel(self, luna, channel: discord.TextChannel):

        await channel.delete()
        await message_builder(luna, description=f"```\nDeleted channel » {channel.mention}```")

    @commands.command(
        name="slowmode",
        usage="<seconds>",
        description="Set slowmode"
    )
    @commands.guild_only()
    @has_permissions(manage_channels=True)
    async def slowmode(self, luna, seconds: int):

        if seconds < 0:
            await message_builder(luna, title="Slowmode", description=f"```\nThe slowmode can't be negative```")
            return
        if seconds == 0:
            await luna.channel.edit(slowmode_delay=0)
            await message_builder(luna, title="Slowmode", description=f"```\nDisabled slowmode```")
            return
        await luna.channel.edit(slowmode_delay=seconds)
        await message_builder(luna, title="Slowmode", description=f"```\nSet slowmode to » {seconds} seconds```")

    @commands.command(
        name="removeslowmode",
        usage="",
        description="Remove slowmode"
    )
    @commands.guild_only()
    @has_permissions(manage_channels=True)
    async def removeslowmode(self, luna):

        await luna.channel.edit(slowmode_delay=0)
        await message_builder(luna, title="Slowmode", description=f"```\nRemoved slowmode```")

    @commands.command(
        name="lock",
        usage="<#channel>",
        description="Lock a channel"
    )
    @commands.guild_only()
    @has_permissions(manage_channels=True)
    async def lock(self, luna, channel: discord.TextChannel):

        await channel.set_permissions(luna.guild.default_role, send_messages=False)
        await channel.edit(name="🔒-locked")
        await message_builder(luna, description=f"```\nLocked channel » {channel.mention}```")

    @commands.command(
        name="unlock",
        usage="<#channel>",
        description="Unlock a channel"
    )
    @commands.guild_only()
    @has_permissions(manage_channels=True)
    async def unlock(self, luna, channel: discord.TextChannel):

        await channel.set_permissions(luna.guild.default_role, send_messages=True)
        await channel.edit(name="🔒-unlocked")
        await message_builder(luna, description=f"```\nUnlocked channel » {channel.mention}```")

    @commands.command(
        name="category",
        usage="<name>",
        description="Create a category"
    )
    @commands.guild_only()
    @has_permissions(manage_channels=True)
    async def category(self, luna, name: str):

        category = await luna.guild.create_category_channel(name)
        await message_builder(luna, description=f"```\nCreated category » {category.mention}```")

    @commands.command(
        name="deletecategory",
        usage="<category_id>",
        description="Delete a category"
    )
    @commands.guild_only()
    @has_permissions(manage_channels=True)
    async def deletecategory(self, luna, category: discord.CategoryChannel):

        await category.delete()
        await message_builder(luna, description=f"```\nDeleted category » {category.mention}```")

    @commands.command(
        name="purge",
        usage="<amount>",
        description="Purge the channel"
    )
    async def purge(self, luna, amount: int):
        await luna.message.delete()
        async for message in luna.message.channel.history(limit=amount):
            try:
                await message.delete()
            except BaseException:
                pass

    @commands.command(
        name="nuke",
        usage="[#channel]",
        description="Nuke the channel"
    )
    @commands.guild_only()
    @has_permissions(manage_channels=True)
    async def nuke(self, luna, channel: discord.TextChannel = None):

        if channel is None:
            channel = luna.channel
        new_channel = await channel.clone()
        await new_channel.edit(position=channel.position)
        await channel.delete()
        await message_builder(new_channel, description=f"```\nThis channel has been nuked```")


bot.add_cog(ChannelCog(bot))


class MemberCog(commands.Cog, name="Member commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="userinfo",
        usage="[user_id]",
        description="User information"
    )
    async def userinfo(self, luna, user: discord.Member = None):

        if user is None:
            user = luna.author
        r = requests.get(
            f'https://discord.com/api/{api_version}/users/{user.id}',
            headers={
                'authorization': user_token,
                'user-agent': 'Mozilla/5.0'
            }
        ).json()
        req = await bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
        banner_id = req["banner"]
        if banner_id:
            banner_url = f"https://cdn.discord.com/banners/{user.id}/{banner_id}?size=1024"
        else:
            banner_url = None
        await message_builder(
            luna, title="User information",
            description=f"```\nGeneral Information\n\n"
                        f"{'User':12} » {user.name}#{user.discriminator}\n"
                        f"{'ID':12} » {user.id}\n"
                        f"{'Status':12} » {user.status}\n"
                        f"{'Bot':12} » {user.bot}\n"
                        f"{'Public Flags':12} » {r['public_flags']}\n"
                        f"{'Banner Color':12} » {r['banner_color']}\n"
                        f"{'Accent Color':12} » {r['accent_color']}\n```"
                        f"```\nCreated at:\n{user.created_at}\n```"
                        f"```\nImage Information\n\n"
                        f"Avatar URL:\n{user.avatar_url}\n\n"
                        f"Banner URL:\n{banner_url}\n```"
        )

    @commands.command(
        name="whois",
        usage="<@member>",
        description="Guild member information"
    )
    @commands.guild_only()
    async def whois(self, luna, user: discord.Member = None):

        if user is None:
            user = luna.author
        if user.id == 406907871998246924:
            special = "\n\nSpecial » Founder & Head Dev @ Team Luna"
        elif user.id == 707355480422350848 or user.id == 663516459837685770:
            special = "\n\nSpecial » Developer @ Team Luna"
        elif user.id == 288433475831332894 or user.id == 465275771523563531:
            special = "\n\nSpecial » Member @ Team Luna"
        elif user.id == 203906692834918401 or user.id == 699099683603349654 or user.id == 319759781315215360:
            special = "\n\nSpecial » Luna Beta"
        elif user.id == 254994687444779008:
            special = "\n\nSpecial » First Luna Customer"
        else:
            special = ""
        date_format = "%a, %d %b %Y %I:%M %p"
        members = sorted(luna.guild.members, key=lambda m: m.joined_at)
        role_string = ', '.join([r.name for r in user.roles][1:])
        perm_string = ', '.join(
            [str(p[0]).replace("_", " ").title()
             for p in user.guild_permissions if p[1]]
        )
        await message_builder(
            luna,
            description=f"User » {user.mention}\n"
                        f"```User information\n\n"
                        f"Joined » {user.joined_at.strftime(date_format)}\n"
                        f"Join position » {members.index(user) + 1}\n"
                        f"Registered » {user.created_at.strftime(date_format)}\n```"
                        f"```\nUser server information\n\n"
                        f"Roles Amount » {len(user.roles) - 1}\n"
                        f"Roles\n\n"
                        f"{role_string}\n\n"
                        f"Permissions\n\n"
                        f"{perm_string}{special}```"
        )

    @commands.command(
        name="report",
        usage="<message_id> <reason>",
        description="Report a user"
    )
    async def report(self, luna, message_id: str, *, reason: str):

        payload = {
            'message_id': message_id,
            'reason': reason
        }
        requests.post(
            'https://discord.com/api/{api_version}/report',
            json=payload,
            headers={
                'authorization': user_token,
                'user-agent': 'Mozilla/5.0'
            }
        )
        await message_builder(luna, title="Report", description=f"```\nMessage {message_id} has been reported\n\nReason » {reason}```")

    @commands.command(
        name="mute",
        usage="<@member> [reason]",
        description="Mute a user"
    )
    @commands.guild_only()
    @has_permissions(manage_roles=True)
    async def mute(self, luna, user: discord.Member, *, reason: str = None):

        role = discord.utils.get(luna.guild.roles, name="Muted")
        if not role:
            role = await luna.guild.create_role(name="Muted")
            for channel in luna.guild.channels:
                await channel.set_permissions(role, send_messages=False)
        await user.add_roles(role)
        await message_builder(luna, title="Mute", description=f"```\n{user.name}#{user.discriminator} has been muted\n``````\nReason\n\n{reason}```")

    @commands.command(
        name="unmute",
        usage="<@member> [reason]",
        description="Unmute a user"
    )
    @commands.guild_only()
    @has_permissions(manage_roles=True)
    async def unmute(self, luna, user: discord.Member, *, reason: str = None):

        role = discord.utils.get(luna.guild.roles, name="Muted")
        if not role:
            await message_builder(luna, title="Unmute", description="No mute role found")
            return
        await user.remove_roles(role)
        await message_builder(luna, title="Unmute", description=f"```\n{user.name}#{user.discriminator} has been unmuted\n``````\nReason\n\n{reason}```")

    @commands.command(
        name="timeout",
        usage="<user> <time>",
        description="Time out a user"
    )
    @commands.guild_only()
    @has_permissions(ban_members=True)
    async def timeout(self, luna, user: discord.Member, time: int):

        payload = {
            'user_id': user.id,
            'duration': time
        }
        requests.post(
            f'https://discord.com/api/{api_version}/guilds/{luna.guild.id}/bans',
            json=payload,
            headers={
                'authorization': user_token,
                'user-agent': 'Mozilla/5.0'
            }
        )
        await message_builder(
            luna,
            description=f"```\nTime out » {user.name}#{user.discriminator} for {time} seconds```"
        )

    @commands.command(
        name="kick",
        usage="<@member> [reason]",
        description="Kick a user"
    )
    @commands.guild_only()
    @has_permissions(kick_members=True)
    async def kick(self, luna, user: discord.Member, *, reason: str = None):

        await user.kick(reason=reason)
        await message_builder(
            luna, title="Kick",
            description=f"```\n{user.name}#{user.discriminator} has been kicked\n``````\nReason\n\n{reason}```"
        )

    @commands.command(
        name="softban",
        usage="<@member> [reason]",
        description="Softban a user"
    )
    @commands.guild_only()
    @has_permissions(ban_members=True)
    async def softban(self, luna, user: discord.Member, *, reason: str = None):

        await user.ban(reason=reason)
        await user.unban()
        await message_builder(
            luna, title="Softban",
            description=f"```\n{user.name}#{user.discriminator} has been softbanned\n``````\nReason\n\n{reason}```"
        )

    @commands.command(
        name="ban",
        usage="<@member> [reason]",
        description="Ban a user"
    )
    @commands.guild_only()
    @has_permissions(ban_members=True)
    async def ban(self, luna, user: discord.Member, *, reason: str = None):

        await user.ban(reason=reason)
        await message_builder(
            luna, title="Ban",
            description=f"```\n{user.name}#{user.discriminator} has been banned\n``````\nReason\n\n{reason}```"
        )

    @commands.command(
        name="unban",
        usage="<user_id>",
        description="Unban a user"
    )
    @commands.guild_only()
    @has_permissions(ban_members=True)
    async def unban(self, luna, user_id: int):

        banned_users = await luna.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            if user.id == user_id:
                await luna.guild.unban(user)
                await message_builder(
                    luna, title="Unban",
                    description=f"```\n{user.name}#{user.discriminator} has been unbanned```"
                )
                return
        await message_builder(
            luna, title="Unban",
            description=f"```\nNo banned user with the id {user_id} was found```"
        )

    @commands.command(
        name="banned",
        usage="[guild_id]",
        description="List all bans"
    )
    @commands.guild_only()
    @has_permissions(ban_members=True)
    async def banned(self, luna, guild_id: int = None):

        if guild_id is not None:
            guild = discord.utils.get(self.bot.guilds, id=guild_id)
            bans = await guild.bans()
        else:
            guild = luna.guild
            bans = await guild.bans()
        if len(bans) == 0:
            await message_builder(
                luna, title=f"Bans in {guild.name}",
                description=f"```\nNo users are banned in {guild.name}```"
            )
            return
        bans = [
            f"{b.user.name}#{b.user.discriminator} | {b.user.id}" for b in bans]
        bans = "\n".join(bans)
        await message_builder(luna, title=f"Bans in {guild.name}", description=f"```{bans}```")

    @commands.command(
        name="savebans",
        usage="[guild_id]",
        description="Save bans"
    )
    @commands.guild_only()
    @has_permissions(ban_members=True)
    async def savebans(self, luna, guild_id: int = None):

        if guild_id is not None:
            guild = discord.utils.get(self.bot.guilds, id=guild_id)
            bans = await guild.bans()
        else:
            guild = luna.guild
            bans = await guild.bans()
        if len(bans) == 0:
            await message_builder(
                luna, title=f"Bans in {guild.name}",
                description=f"```\nNo users are banned in {guild.name}```"
            )
            return
        bans = [
            f"{b.user.name}#{b.user.discriminator} | {b.user.id}" for b in bans]
        bans = "\n".join(bans)
        files.create_folder(f"data/backup/guilds/{guild.name}", documents=False)
        files.write_file(
            f"data/backup/guilds/{guild.name}/bans.txt", bans, documents=False
        )
        await message_builder(
            luna, title=f"Saved Bans",
            description=f"```\nSaved all bans in data/backup/guilds/{guild.name}/bans.txt\n``````{bans}```"
        )

    @commands.command(
        name="loadbans",
        usage="[guild_id]",
        description="Load bans"
    )
    @commands.guild_only()
    @has_permissions(ban_members=True)
    async def loadbans(self, luna, guild_id: int = None):

        if guild_id is not None:
            guild = discord.utils.get(self.bot.guilds, id=guild_id)
        else:
            guild = luna.guild
        if not files.file_exist(
                f"data/backup/guilds/{guild.name}",
                documents=False
        ):
            await message_builder(
                luna, title=f"Load bans",
                description=f"```\nNo bans were found in data/backup/{guild.name}/bans.txt```"
            )
            return
        bans = files.read_file(
            f"data/backup/guilds/{guild.name}/bans.txt", documents=False
        )
        bans = bans.split("\n")
        for ban in bans:
            if ban == "":
                continue
            user_id = int(ban.split(" | ")[1])
            user = discord.utils.get(guild.members, id=user_id)
            await guild.ban(user)
        await message_builder(
            luna, title=f"Load bans",
            description=f"```\nLoaded all bans from data/backup/guilds/{guild.name}/bans.txt```"
        )


bot.add_cog(MemberCog(bot))


class RoleCog(commands.Cog, name="Role commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="roleinfo",
        usage="<@role>",
        description="Information"
    )
    async def roleinfo(self, luna, role: discord.Role):

        role_amount = 0
        role_members = ""
        for member in luna.guild.members:
            for roles in member.roles:
                if roles.id == role.id:
                    role_amount += 1
                    role_members += f"{member.name}#{member.discriminator}\n"
        if role_members == "":
            role_members = "No members have this role"
        await message_builder(
            luna, title="Role Information",
            description=f"```\n{'Name':17} » {role.name}\n"
                        f"{'ID':17} » {role.id}\n"
                        f"{'Color':17} » {role.color}\n"
                        f"{'Created at':17} » {role.created_at}\n"
                        f"{'Position':17} » {role.position}\n```"
                        f"```\n{'Members':17} » {role_amount}\n\n"
                        f"Member List:\n{role_members}\n```"
                        f"```\n{'Permissions':17} » {role.permissions}\n```"
        )

    @commands.command(
        name="giverole",
        usage="<@member> <role_id>",
        description="Give a role"
    )
    @commands.guild_only()
    @has_permissions(manage_roles=True)
    async def giverole(self, luna, member: discord.Member, role_id: int):

        role = discord.utils.get(luna.guild.roles, id=role_id)
        if role is None:
            await message_builder(
                luna, title="Give role",
                description=f"```\nNo role with the id {role_id} was found```"
            )
            return
        await member.add_roles(role)
        await message_builder(
            luna, title="Give role",
            description=f"```\nGave {member.name}#{member.discriminator} role » {role.name}```"
        )

    @commands.command(
        name="giveallroles",
        usage="<@member>",
        description="Give all roles"
    )
    @commands.guild_only()
    @has_permissions(manage_roles=True)
    async def giveallroles(self, luna, member: discord.Member):

        for role in luna.guild.roles:
            if role.name == "@everyone":
                continue
            await member.add_roles(role)
        await message_builder(
            luna, title="Give all roles",
            description=f"```\nGave all roles to » {member.name}#{member.discriminator}```"
        )

    @commands.command(
        name="allroles",
        usage="",
        description="Give all roles"
    )
    @commands.guild_only()
    @has_permissions(manage_roles=True)
    async def allroles(self, luna):

        for member in luna.guild.members:
            for role in luna.guild.roles:
                if role.name == "@everyone":
                    continue
                await member.add_roles(role)
        await message_builder(luna, title="Give all roles", description=f"```\nGave all members all roles```")

    @commands.command(
        name="removeallroles",
        usage="<@member>",
        description="Remove all roles"
    )
    @commands.guild_only()
    @has_permissions(manage_roles=True)
    async def removeallroles(self, luna, member: discord.Member):

        for role in luna.guild.roles:
            if role.name == "@everyone":
                continue
            await member.remove_roles(role)
        await message_builder(
            luna, title="Remove all roles",
            description=f"```\nRemoved all roles from » {member.name}#{member.discriminator}```"
        )

    @commands.command(
        name="removerole",
        usage="<@member> <role_id>",
        description="Remove a role"
    )
    @commands.guild_only()
    @has_permissions(manage_roles=True)
    async def removerole(self, luna, member: discord.Member, role_id: int):

        role = discord.utils.get(luna.guild.roles, id=role_id)
        if role is None:
            await message_builder(
                luna, title="Remove role",
                description=f"```\nNo role with the id {role_id} was found```"
            )
            return
        await member.remove_roles(role)
        await message_builder(
            luna, title="Remove role",
            description=f"```\nRemoved role {role.name} from » {member.name}#{member.discriminator}```"
        )

    @commands.command(
        name="createrole",
        usage="<role_name>",
        description="Create a role"
    )
    @commands.guild_only()
    @has_permissions(manage_roles=True)
    async def createrole(self, luna, *, role_name: str):

        role = await luna.guild.create_role(name=role_name)
        await message_builder(luna, title="Create role", description=f"```\nCreated role » {role.name}```")

    @commands.command(
        name="renamerole",
        usage="<role_id> <name>",
        description="Rename a role"
    )
    @commands.guild_only()
    @has_permissions(manage_roles=True)
    async def renamerole(self, luna, role_id: int, *, name: str):

        role = discord.utils.get(luna.guild.roles, id=role_id)
        if role is None:
            await message_builder(
                luna, title="Rename role",
                description=f"```\nNo role with the id {role_id} was found```"
            )
            return
        await role.edit(name=name)
        await message_builder(luna, title="Rename role", description=f"```\nRenamed role {role.name} to » {name}```")

    @commands.command(
        name="renameroles",
        usage="<name>",
        description="Rename all roles"
    )
    @commands.guild_only()
    @has_permissions(manage_roles=True)
    async def renameroles(self, luna, *, name: str):

        for role in luna.guild.roles:
            if role.name == "@everyone":
                continue
            await role.edit(name=name)
        await message_builder(luna, title="Rename all roles", description=f"```\nRenamed all roles to » {name}```")

    @commands.command(
        name="deleterole",
        usage="<role_id>",
        description="Delete a role"
    )
    @commands.guild_only()
    @has_permissions(manage_roles=True)
    async def deleterole(self, luna, role_id: int):

        role = discord.utils.get(luna.guild.roles, id=role_id)
        if role is None:
            await message_builder(
                luna, title="Delete role",
                description=f"```\nNo role with the id {role_id} was found```"
            )
            return
        await role.delete()
        await message_builder(luna, title="Delete role", description=f"```\nDeleted role » {role.name}```")


bot.add_cog(RoleCog(bot))


class NickCog(commands.Cog, name="Nickname commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="nick",
        usage="<name>",
        description="Change nickname"
    )
    @commands.guild_only()
    @has_permissions(manage_nicknames=True)
    async def nick(self, luna, *, name: str):

        await luna.author.edit(nick=name)
        await message_builder(luna, title="Nickname", description=f"```\nChanged nickname to » {name}```")

    @commands.command(
        name="nickmember",
        usage="<@member> <name>",
        description="Change nickname"
    )
    @commands.guild_only()
    @has_permissions(manage_nicknames=True)
    async def nickmember(self, luna, member: discord.Member, *, name: str):

        await member.edit(nick=name)
        await message_builder(
            luna, title="Nickname",
            description=f"```\nChanged nickname of {member.name}#{member.discriminator} to » {name}```"
        )

    @commands.command(
        name="nickall",
        usage="<name>",
        description="Change nickname of everyone"
    )
    @commands.guild_only()
    @has_permissions(manage_nicknames=True)
    async def nickall(self, luna, *, name: str):

        for member in luna.guild.members:
            await member.edit(nick=name)
        await message_builder(luna, title="Nickall", description=f"```\nChanged nickname of everyone to » {name}```")

    @commands.command(
        name="clearnick",
        usage="[@member]",
        description="Clear nickname"
    )
    @commands.guild_only()
    @has_permissions(manage_nicknames=True)
    async def clearnick(self, luna, member: discord.Member = None):

        if member is None:
            member = luna.author
        await member.edit(nick=None)
        await message_builder(
            luna, title="Clearnick",
            description=f"```\nCleared nickname of » {member.name}#{member.discriminator}```"
        )

    @commands.command(
        name="clearallnick",
        usage="",
        description="Clear all nicknames"
    )
    @commands.guild_only()
    @has_permissions(manage_nicknames=True)
    async def clearallnick(self, luna):

        for member in luna.guild.members:
            await member.edit(nick=None)
        await message_builder(luna, title="Clearnick", description=f"```\nCleared nickname of everyone```")


bot.add_cog(NickCog(bot))


class InviteCog(commands.Cog, name="Invite commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="inviteinfo",
        usage="<invite>",
        description="Invite information"
    )
    @commands.guild_only()
    async def inviteinfo(self, luna, invite: str):

        invite = await self.bot.get_invite(invite)
        if invite is None:
            await message_builder(
                luna, title="Invite info",
                description=f"```\nNo invite with the id {invite} was found```"
            )
            return
        await message_builder(
            luna, title="Invite info",
            description=f"```\nInvite » {invite.code}\n"
                        f"Created at » {invite.created_at}\n"
                        f"Channel » {invite.channel.mention}\n"
                        f"Guild » {invite.guild.name}\n"
                        f"Created by » {invite.inviter.name}#{invite.inviter.discriminator}\n"
                        f"Max uses » {invite.max_uses}\n"
                        f"Uses » {invite.uses}```"
        )

    @commands.command(
        name="invite",
        usage="[channel_id] [age] [uses]",
        description="Invite"
    )
    @commands.guild_only()
    @has_permissions(manage_channels=True)
    async def invite(self, luna, channel_id: int = None, max_age: int = 0, max_uses: int = 0):

        if channel_id is None:
            channel = luna.channel
        else:
            channel = discord.utils.get(luna.guild.channels, id=channel_id)
        if channel is None:
            await message_builder(
                luna, title="Invite",
                description=f"```\nNo channel with the id » {channel_id} was found```"
            )
            return
        invite = await channel.create_invite(max_age=max_age, max_uses=max_uses)
        await message_builder(luna, title="Invite", description=f"```\nCreated invite » {invite.url}```")

    @commands.command(
        name="delinvite",
        usage="<invite_id>",
        description="Delete invite"
    )
    @commands.guild_only()
    @has_permissions(manage_channels=True)
    async def delinvite(self, luna, invite_id: int):

        invite = discord.utils.get(luna.guild.invites, id=invite_id)
        if invite is None:
            await message_builder(
                luna, title="Delete invite",
                description=f"```\nNo invite with the id » {invite_id} was found```"
            )
            return
        await invite.delete()
        await message_builder(luna, title="Delete invite", description=f"```\nDeleted invite » {invite.url}```")

    @commands.command(
        name="delallinvite",
        usage="",
        description="Delete all invites"
    )
    @commands.guild_only()
    @has_permissions(manage_channels=True)
    async def delallinvite(self, luna):

        for invite in luna.guild.invites:
            await invite.delete()
        await message_builder(luna, title="Delete invite", description=f"```\nDeleted all invites```")

    @commands.command(
        name="invitelist",
        usage="",
        description="List all invites"
    )
    @commands.guild_only()
    @has_permissions(manage_channels=True)
    async def invitelist(self, luna):

        invites = luna.guild.invites
        if len(invites) == 0:
            await message_builder(luna, title="Invite list", description=f"```\nNo invites were found```")
            return
        invite_list = ""
        for invite in invites:
            invite_list += f"{invite.url}\n"
        await message_builder(luna, title="Invite list", description=f"```\n{invite_list}```")

    @commands.command(
        name="invitechannel",
        usage="<channel_id>",
        description="Channel invites"
    )
    @commands.guild_only()
    @has_permissions(manage_channels=True)
    async def invitelistchannel(self, luna, channel_id: int):

        channel = discord.utils.get(luna.guild.channels, id=channel_id)
        if channel is None:
            await message_builder(
                luna, title="Invite list",
                description=f"```\nNo channel with the id » {channel_id} was found```"
            )
            return
        invites = channel.invites
        if len(invites) == 0:
            await message_builder(luna, title="Invite list", description=f"```\nNo invites were found```")
            return
        invite_list = ""
        for invite in invites:
            invite_list += f"{invite.url}\n"
        await message_builder(luna, title="Invite list", description=f"```\n{invite_list}```")

    @commands.command(
        name="inviteguild",
        usage="",
        description="Invites of a guild"
    )
    @commands.guild_only()
    @has_permissions(manage_channels=True)
    async def invitelistguild(self, luna):

        invites = luna.guild.invites
        if len(invites) == 0:
            await message_builder(luna, title="Invite list", description=f"```\nNo invites were found```")
            return
        invite_list = ""
        for invite in invites:
            invite_list += f"{invite.url}\n"
        await message_builder(luna, title="Invite list", description=f"```\n{invite_list}```")

    @commands.command(
        name="inviteuser",
        usage="<user_id>",
        description="Invites of a user"
    )
    @commands.guild_only()
    @has_permissions(manage_channels=True)
    async def invitelistuser(self, luna, user_id: int):

        user = discord.utils.get(luna.guild.members, id=user_id)
        if user is None:
            await message_builder(
                luna, title="Invite list",
                description=f"```\nNo user with the id » {user_id} was found```"
            )
            return
        invites = user.invites
        if len(invites) == 0:
            await message_builder(luna, title="Invite list", description=f"```\nNo invites were found```")
            return
        invite_list = ""
        for invite in invites:
            invite_list += f"{invite.url}\n"
        await message_builder(luna, title="Invite list", description=f"```\n{invite_list}```")


bot.add_cog(InviteCog(bot))


class AdminCog(commands.Cog, name="Administrative commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="guildname",
        usage="<name>",
        description="Change guild name"
    )
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    async def guildname(self, luna, *, name: str):

        await luna.guild.edit(name=name)
        await message_builder(luna, title="Guildname", description=f"```\nChanged the name of the guild to » {name}```")

    @commands.command(
        name="guildimage",
        usage="<image_url>",
        description="Change guild image"
    )
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    async def guildimage(self, luna, *, image_url: str):

        await luna.guild.edit(icon=image_url)
        await message_builder(
            luna, title="Guildimage",
            description=f"```\nChanged the image of the guild to » {image_url}```"
        )

    @commands.command(
        name="guildbanner",
        usage="<image_url>",
        description="Change guild banner"
    )
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    async def guildbanner(self, luna, *, image_url: str):

        await luna.guild.edit(banner=image_url)
        await message_builder(
            luna, title="Guildbanner",
            description=f"```\nChanged the banner of the guild to » {image_url}```"
        )

    @commands.command(
        name="getguildimage",
        usage="[guild_id]",
        description="Get the guild image"
    )
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    async def getguildimage(self, luna, guild_id: int = None):

        if guild_id is None:
            guild_id = luna.guild.id
        guild = discord.utils.get(luna.guilds, id=guild_id)
        if guild is None:
            await message_builder(
                luna, title="Guildimage",
                description=f"```\nNo guild with the id » {guild_id} was found```"
            )
            return
        await message_builder(luna, title="Guildimage", description=f"```\n{guild.icon_url}```")

    @commands.command(
        name="getguildbanner",
        usage="[guild_id]",
        description="Get the guild banner"
    )
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    async def getguildbanner(self, luna, guild_id: int = None):

        if guild_id is None:
            guild_id = luna.guild.id
        guild = discord.utils.get(luna.guilds, id=guild_id)
        if guild is None:
            await message_builder(
                luna, title="Guildbanner",
                description=f"```\nNo guild with the id » {guild_id} was found```"
            )
            return
        await message_builder(luna, title="Guildbanner", description=f"```\n{guild.banner_url}```")

    @commands.command(
        name="guildinfo",
        usage="[guild_id]",
        description="Guild information"
    )
    @commands.guild_only()
    @has_permissions(manage_guild=True)
    async def guildinfo(self, luna, guild_id: int = None):

        if guild_id is None:
            guild = luna.guild
        else:
            guild = discord.utils.get(bot.guilds, id=guild_id)
            if guild is None:
                await message_builder(
                    luna, title="Guildinfo",
                    description=f"```\nNo guild with the id {guild_id} was found```"
                )
                return
        await message_builder(
            luna, title="Guildinfo",
            description=f"```\nGeneral Information\n\n"
                        f"{'Guild':<17} » {guild.name}\n"
                        f"{'ID':17} » {guild.id}\n"
                        f"{'Owner':17} » {guild.owner}\n"
                        f"{'Created at':17} » {guild.created_at}\n"
                        f"{'Boost':17} » {guild.premium_subscription_count}\n"
                        f"{'Boost status':17} » {guild.premium_subscription_count is not None}\n"
                        f"{'Region':17} » {guild.region}\n"
                        f"{'Verification':17} » {guild.verification_level}\n```"
                        f"```\nMember Information\n\n"
                        f"{'Member count':17} » {guild.member_count}\n```"
                        f"```\nChannel Information\n\n"
                        f"{'Text channels':17} » {len(guild.text_channels)}\n"
                        f"{'Voice channels':17} » {len(guild.voice_channels)}\n```"
                        f"```\nRole Information\n\n"
                        f"{'Role count':17} » {len(guild.roles)}```"
        )


bot.add_cog(AdminCog(bot))

ignore_list = []


class IgnoreCog(commands.Cog, name="Ignore commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="ignore",
        usage="<@user>",
        description="Ignore user DMs"
    )
    async def ignore(self, luna, *, user: discord.Member):

        global ignore_list
        if user.id in ignore_list:
            await message_builder(luna, title="Ignore", description=f"```\n{user} is already ignored```")
            return
        ignore_list.append(user.id)
        await message_builder(luna, title="Ignore", description=f"```\n{user} is now ignored```")

    @commands.command(
        name="unignore",
        usage="<@user>",
        description="Unignore user DMs"
    )
    async def unignore(self, luna, *, user: discord.Member):

        global ignore_list
        if user.id not in ignore_list:
            await message_builder(luna, title="Unignore", description=f"```\n{user} is not ignored```")
            return
        ignore_list.remove(user.id)
        await message_builder(luna, title="Unignore", description=f"```\n{user} is now unignored```")

    @commands.command(
        name="ignorelist",
        usage="",
        description="List ignored users"
    )
    async def ignorelist(self, luna):

        global ignore_list
        if len(ignore_list) == 0:
            await message_builder(luna, title="Ignorelist", description=f"```\nNo users are ignored```")
            return
        await message_builder(luna, title="Ignorelist", description=f"```\n{ignore_list}```")

    @commands.command(
        name="ignorelistclear",
        usage="",
        description="Clear ignore list"
    )
    async def ignorelistclear(self, luna):

        global ignore_list
        if len(ignore_list) == 0:
            await message_builder(luna, title="Ignorelist", description=f"```\nNo users are ignored```")
            return
        ignore_list.clear()
        await message_builder(luna, title="Ignorelist", description=f"```\nIgnore list is now cleared```")


bot.add_cog(IgnoreCog(bot))


class AnimatedCog(commands.Cog, name="Animated commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="animguild",
        usage="[name]",
        description="Animates the guild name"
    )
    async def animguild(self, luna, *, name: str = None):

        global cyclename
        global start_animation
        start_animation = True
        if name is None:
            embed = discord.Embed(
                title="Animguild",
                description=f"```\nAnimating: {name}```",

            )

            embed.set_footer(
                text=theme.footer(),

            )
            embed.set_author(
                name=theme.author(), url=theme.author_url(
                ), icon_url=theme.author_icon_url()
            )

            await send(luna, embed)
            name = luna.guild.name.lower()
            cyclename = name
            length = len(name)
            while start_animation:
                for x in range(length):
                    if start_animation:
                        time.sleep(0.5)
                        letter = cyclename[x]
                        first_part = cyclename[:x]
                        second_part = cyclename[x + 1:]
                        new_data = first_part + second_part
                        if letter == letter.upper():
                            await luna.guild.edit(name=new_data[:x] + letter.lower() + new_data[x:])
                        else:
                            await luna.guild.edit(name=new_data[:x] + letter.upper() + new_data[x:])
                    else:
                        break

        else:
            if len(name) > 3:
                embed = discord.Embed(
                    title="Animguild",
                    description=f"```\nAnimating: {name}```",

                )

                embed.set_footer(
                    text=theme.footer(),

                )
                embed.set_author(
                    name=theme.author(), url=theme.author_url(
                    ), icon_url=theme.author_icon_url()
                )

                await send(luna, embed)
                name = luna.guild.name.lower()
                cyclename = name
                length = len(name)
                while start_animation:
                    for x in range(length):
                        if start_animation:
                            time.sleep(0.5)
                            letter = cyclename[x]
                            first_part = cyclename[:x]
                            second_part = cyclename[x + 1:]
                            new_data = first_part + second_part
                            if letter == letter.upper():
                                await luna.guild.edit(name=new_data[:x] + letter.lower() + new_data[x:])
                            else:
                                await luna.guild.edit(name=new_data[:x] + letter.upper() + new_data[x:])
                        else:
                            break
            else:
                if configs.error_log() == "console":
                    prints.error(
                        "Invalid name length, needs to be over 3 characters long"
                    )
                else:
                    await error_builder(
                        luna,
                        description=f"```\nInvalid name length, needs to be over 3 characters long```"
                    )

    @commands.command(
        name="stopanimguild",
        usage="",
        description="Stops the guild animation"
    )
    async def stopanimguild(self, luna):

        global start_animation
        start_animation = False
        embed = discord.Embed(
            title="Animguild",
            description="```\nStopped the animation```"
        )

        embed.set_footer(text=theme.footer())

        await send(luna, embed)

    @commands.command(
        name="cyclenick",
        usage="<name>",
        description="Animates the nickname"
    )
    async def cyclenick(self, luna, *, text):

        embed = discord.Embed(
            title="Cyclenick",
            description=f"```\nAnimating: {text}```"
        )

        embed.set_footer(text=theme.footer())

        await send(luna, embed)
        global cycling
        cycling = True
        while cycling:
            name = ""
            for letter in text:
                name = name + letter
                await luna.message.author.edit(nick=name)

    @commands.command(
        name="stopcyclenick",
        usage="",
        description="Stops the nickname animation"
    )
    async def stopcyclenick(self, luna):

        global cycling
        cycling = False
        embed = discord.Embed(
            title="Cyclenick",
            description="```\nStopped the animation```"
        )

        embed.set_footer(text=theme.footer())

        await send(luna, embed)

    @commands.command(
        name="cyclegroup",
        usage="<name>",
        description="Animates the group name"
    )
    async def cyclegroup(self, luna, *, text):

        embed = discord.Embed(
            title="Cyclegroup",
            description=f"```\nAnimating: {text}```"
        )

        embed.set_footer(text=theme.footer())

        await send(luna, embed)
        global cycling_group
        cycling_group = True
        while cycling:
            name = ""
            for letter in text:
                name = name + letter
                await luna.message.channel.edit(name=name)

    @commands.command(
        name="stopcyclegroup",
        usage="",
        description="Stops the group animation"
    )
    async def stopcyclegroup(self, luna):

        global cycling_group
        cycling_group = False
        embed = discord.Embed(
            title="Cyclegroup",
            description="```\nStopped the animation```"
        )

        embed.set_footer(text=theme.footer())

        await send(luna, embed)

    @commands.command(
        name="virus",
        usage="[@member] <virus>",
        description="Animated virus message"
    )
    async def virus(self, luna, user: discord.Member = None, *, virus: str = "trojan"):
        user = user or luna.author
        start = await luna.send(f"{luna.author.mention} has started to spread {virus}")
        animation_list = (
            f"``[▓▓▓                    ] / {virus}-virus.exe Packing files.``",
            f"``[▓▓▓▓▓▓▓                ] - {virus}-virus.exe Packing files..``",
            f"``[▓▓▓▓▓▓▓▓▓▓▓▓           ] {virus}-virus.exe Packing files..``",
            f"``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓         ] | {virus}-virus.exe Packing files..``",
            f"``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      ] / {virus}-virus.exe Packing files..``",
            f"``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ] - {virus}-virus.exe Packing files..``",
            f"``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ] {virus}-virus.exe Packing files..``",
            f"``Successfully downloaded {virus}-virus.exe``",
            "``Injecting virus.   |``",
            "``Injecting virus..  /``",
            "``Injecting virus... -``",
            f"``Successfully Injected {virus}-virus.exe into {user.name}``",
        )
        for i in animation_list:
            await asyncio.sleep(1.5)
            await start.edit(content=i)

    @commands.command(
        name="cathi",
        usage="[text]",
        description="Cute cat animation"
    )
    async def cathi(self, luna, *, text: str = "Hi..."):
        start = await luna.send(f"A package arrived!")
        animation_list = (
            """ຸ 　　　＿＿_＿＿
        　／　／　  ／|"
        　|￣￣￣￣|　|
        　|　　　　|／
        　￣￣￣￣""",
            f"""ຸ 　　　{text}
        　   　∧＿∧＿_
        　／(´･ω･`)  ／＼
        ／|￣￣￣￣|＼／
        　|　　　　|／
        　￣￣￣￣""",
        )
        for _ in range(3):
            for cat in animation_list:
                await asyncio.sleep(2)
                await start.edit(content=cat)

    @commands.command(
        name="flop",
        usage="",
        description="Flop animation"
    )
    async def flop(self, luna):
        start = await luna.send(f"{luna.author.mention} has started to flop")
        animation_list = (
            "(   ° - °) (' - '   )",
            "(\\\\° - °)\\ (' - '   )",
            "(—°□°)— (' - '   )",
            "(╯°□°)╯(' - '   )",
            "(╯°□°)╯︵(\\\\ .o.)\\",
        )
        for i in animation_list:
            await asyncio.sleep(2)
            await start.edit(content=i)

    @commands.command(
        name="poof",
        usage="",
        description="Poof animation"
    )
    async def poof(self, luna):
        start = await luna.send(f"{luna.author.mention} has started to poof")
        animation_list = ("(   ' - ')", "' - ')", "- ')", "')", ")", "*poofness*")
        for i in animation_list:
            await asyncio.sleep(2)
            await start.edit(content=i)

    @commands.command(
        name="boom",
        usage="",
        description="Boom animation"
    )
    async def boom(self, luna):
        start = await luna.send(f"{luna.author.mention} has started to boom")
        animation_list = (
            "```THIS MESSAGE WILL SELFDESTRUCT IN 5```",
            "```THIS MESSAGE WILL SELFDESTRUCT IN 4```",
            "```THIS MESSAGE WILL SELFDESTRUCT IN 3```",
            "```THIS MESSAGE WILL SELFDESTRUCT IN 2```",
            "```THIS MESSAGE WILL SELFDESTRUCT IN 1```",
            "```THIS MESSAGE WILL SELFDESTRUCT IN 0```",
            "💣",
            "💥",
        )
        for i in animation_list:
            await asyncio.sleep(2)
            await start.edit(content=i)

    @commands.command(
        name="tableflip",
        usage="",
        description="Tableflip animation"
    )
    async def tableflip(self, luna):
        start = await luna.send(f"{luna.author.mention} is flipping the table")
        animation_list = (
            "`(\\°-°)\\  ┬─┬`",
            "`(\\°□°)\\  ┬─┬`",
            "`(-°□°)-  ┬─┬`",
            "`(╯°□°)╯    ]`",
            "`(╯°□°)╯     ┻━┻`",
            "`(╯°□°)╯       [`",
            "`(╯°□°)╯          ┬─┬`",
            "`(╯°□°)╯                 ]`",
            "`(╯°□°)╯                  ┻━┻`",
            "`(╯°□°)╯                         [`",
            "`(\\°-°)\\                               ┬─┬`",
        )
        for i in animation_list:
            await asyncio.sleep(2)
            await start.edit(content=i)

    @commands.command(
        name="unflip",
        usage="",
        description="Unflip animation"
    )
    async def tableflip(self, luna):
        start = await luna.send(f"{luna.author.mention} is unflipping the table")
        animation_list = (
            "`(\\°-°)\\  ┻━┻`",
            "`(\\°□°)\\  ┻━┻`",
            "`(-°□°)-  ┻━┻`",
            "`(-°□°)-  ]`",
            "`(\\°-°)\\  ┬─┬`",
        )
        for i in animation_list:
            await asyncio.sleep(2)
            await start.edit(content=i)

    @commands.command(
        name="warning",
        usage="",
        description="System overload animation"
    )
    async def warning(self, luna):
        start = await luna.send(f"{luna.author.mention} is getting a warning")
        animation_list = (
            "`LOAD !! WARNING !! SYSTEM OVER`",
            "`OAD !! WARNING !! SYSTEM OVERL`",
            "`AD !! WARNING !! SYSTEM OVERLO`",
            "`D !! WARNING !! SYSTEM OVERLOA`",
            "`! WARNING !! SYSTEM OVERLOAD !`",
            "`WARNING !! SYSTEM OVERLOAD !!`",
            "`ARNING !! SYSTEM OVERLOAD !! W`",
            "`RNING !! SYSTEM OVERLOAD !! WA`",
            "`NING !! SYSTEM OVERLOAD !! WAR`",
            "`ING !! SYSTEM OVERLOAD !! WARN`",
            "`NG !! SYSTEM OVERLOAD !! WARNI`",
            "`G !! SYSTEM OVERLOAD !! WARNIN`",
            "`!! SYSTEM OVERLOAD !! WARNING`",
            "`! SYSTEM OVERLOAD !! WARNING !`",
            "`SYSTEM OVERLOAD !! WARNING !!`",
            "`IMMINENT SHUT-DOWN IN 0.5 SEC!`",
            "`WARNING !! SYSTEM OVERLOAD !!`",
            "`IMMINENT SHUT-DOWN IN 0.2 SEC!`",
            "`SYSTEM OVERLOAD !! WARNING !!`",
            "`IMMINENT SHUT-DOWN IN 0.01 SEC!`",
            "`SHUT-DOWN EXIT ERROR ¯\\(｡･益･)/¯`",
            "`CTRL + R FOR MANUAL OVERRIDE..`",
        )
        for i in animation_list:
            await asyncio.sleep(2)
            await start.edit(content=i)


bot.add_cog(AnimatedCog(bot))


class DumpCog(commands.Cog, name="Dump commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="alldump",
        usage="<channel>",
        description="Dump all from a channel"
    )
    async def alldump(self, luna, channel: discord.TextChannel):

        if not files.file_exist(
                f"data/dumping/all/{channel.guild.name}/{channel.name}",
                documents=False
        ):
            files.create_folder(
                f"data/dumping/all/{channel.guild.name}/{channel.name}",
                documents=False
            )
        try:
            prints.event(
                f"Dumping all from {channel.name} ({channel.guild.name})"
            )
            await message_builder(
                luna, title="Dumping",
                description=f"```\nEvent\n\nDumping all from {channel.mention} ({channel.guild.name})...```"
            )
            async for message in channel.history(limit=None):
                if message.attachments:
                    for attachment in message.attachments:
                        r = requests.get(attachment.url, stream=True)
                        open(
                            f'data/dumping/all/{channel.guild.name}/{channel.name}/{attachment.filename}', 'wb'
                        ).write(
                            r.content
                        )
            prints.message(
                f"Dumped all from {channel.name} ({channel.guild.name})"
            )
            await message_builder(
                luna, title="Dumping",
                description=f"```\nInfo\n\nDumped all from {channel.mention} ({channel.guild.name})```"
            )
        except Exception as e:
            await error_builder(luna, description=f"```{e}```")

    @commands.command(
        name="imgdump",
        usage="<channel>",
        description="Dump images from a channel"
    )
    async def imgdump(self, luna, channel: discord.TextChannel):

        if not files.file_exist(
                f"data/dumping/images/{channel.guild.name}/{channel.name}",
                documents=False
        ):
            files.create_folder(
                f"data/dumping/images/{channel.guild.name}/{channel.name}",
                documents=False
            )
        try:
            prints.event(
                f"Dumping images from {channel.name} ({channel.guild.name})"
            )
            await message_builder(
                luna, title="Dumping",
                description=f"```\nEvent\n\nDumping images from {channel.mention} ({channel.guild.name})...```"
            )
            async for message in channel.history(limit=None):
                if message.attachments:
                    for attachment in message.attachments:
                        if attachment.url.endswith(".png") or attachment.url.endswith(
                                ".jpg"
                        ) or attachment.url.endswith(".jpeg") or attachment.url.endswith(".gif"):
                            r = requests.get(attachment.url, stream=True)
                            open(
                                f'data/dumping/images/{channel.guild.name}/{channel.name}/{attachment.filename}', 'wb'
                            ).write(
                                r.content
                            )
            prints.message(
                f"Dumped images from {channel.name} ({channel.guild.name})"
            )
            await message_builder(
                luna, title="Dumping",
                description=f"```\nInfo\n\nDumped images from {channel.mention} ({channel.guild.name})```"
            )
        except Exception as e:
            await error_builder(luna, description=f"```{e}```")

    @commands.command(
        name="audiodump",
        usage="<channel>",
        description="Dump audio from a channel"
    )
    async def audiodump(self, luna, channel: discord.TextChannel):

        if not files.file_exist(
                f"data/dumping/audio/{channel.guild.name}/{channel.name}",
                documents=False
        ):
            files.create_folder(
                f"data/dumping/audio/{channel.guild.name}/{channel.name}",
                documents=False
            )
        try:
            prints.event(
                f"Dumping audio from {channel.name} ({channel.guild.name})"
            )
            await message_builder(
                luna, title="Dumping",
                description=f"```\nEvent\n\nDumping audio from {channel.mention} ({channel.guild.name})...```"
            )
            async for message in channel.history(limit=None):
                if message.attachments:
                    for attachment in message.attachments:
                        if attachment.url.endswith(".mp3"):
                            r = requests.get(attachment.url, stream=True)
                            open(
                                f'data/dumping/audio/{channel.guild.name}/{channel.name}/{attachment.filename}', 'wb'
                            ).write(
                                r.content
                            )
            prints.message(
                f"Dumped audio from {channel.name} ({channel.guild.name})"
            )
            await message_builder(
                luna, title="Dumping",
                description=f"```\nInfo\n\nDumped audio from {channel.mention} ({channel.guild.name})```"
            )
        except Exception as e:
            await error_builder(luna, description=f"```{e}```")

    @commands.command(
        name="videodump",
        usage="<channel>",
        description="Dump videos from a channel"
    )
    async def videodump(self, luna, channel: discord.TextChannel):

        if not files.file_exist(
                f"data/dumping/videos/{channel.guild.name}/{channel.name}",
                documents=False
        ):
            files.create_folder(
                f"data/dumping/videos/{channel.guild.name}/{channel.name}",
                documents=False
            )
        try:
            prints.event(
                f"Dumping videos from {channel.name} ({channel.guild.name})"
            )
            await message_builder(
                luna, title="Dumping",
                description=f"```\nEvent\n\nDumping videos from {channel.mention} ({channel.guild.name})...```"
            )
            async for message in channel.history(limit=None):
                if message.attachments:
                    for attachment in message.attachments:
                        if attachment.url.endswith(
                                ".mp4"
                        ) or attachment.url.endswith(".mov"):
                            r = requests.get(attachment.url, stream=True)
                            open(
                                f'data/dumping/videos/{channel.guild.name}/{channel.name}/{attachment.filename}', 'wb'
                            ).write(
                                r.content
                            )
            prints.message(
                f"Dumped videos from {channel.name} ({channel.guild.name})"
            )
            await message_builder(
                luna, title="Dumping",
                description=f"```\nInfo\n\nDumped videos from {channel.mention} ({channel.guild.name})```"
            )
        except Exception as e:
            await error_builder(luna, description=f"```{e}```")

    @commands.command(
        name="textdump",
        usage="<channel>",
        description="Dump text from a channel"
    )
    async def textdump(self, luna, channel: discord.TextChannel):

        if not files.file_exist(
                f"data/dumping/text/{channel.guild.name}/{channel.name}",
                documents=False
        ):
            files.create_folder(
                f"data/dumping/text/{channel.guild.name}/{channel.name}",
                documents=False
            )
        try:
            prints.event(
                f"Dumping text from {channel.name} ({channel.guild.name})"
            )
            await message_builder(
                luna, title="Dumping",
                description=f"```\nEvent\n\nDumping last 1000 messages from {channel.mention} ({channel.guild.name})...```"
            )
            text = ""
            async for message in channel.history(limit=1000):
                text += f"{message.author.name}#{message.author.discriminator}: {message.content}\n"
            open(
                f'data/dumping/text/{channel.guild.name}/{channel.name}/{channel.name}.txt', 'w', encoding='utf-8'
            ).write(text)
            prints.message(
                f"Dumped text from {channel.name} ({channel.guild.name})"
            )
            await message_builder(
                luna, title="Dumping",
                description=f"```\nInfo\n\nDumped last 1000 messages from {channel.mention} ({channel.guild.name})```"
            )
        except Exception as e:
            await error_builder(luna, description=f"```{e}```")

    @commands.command(
        name="emojidump",
        usage="<guild>",
        description="Dump all emojis from a guild"
    )
    async def emojidump(self, luna, guild: discord.Guild):

        if not files.file_exist(
                f"data/dumping/emojis/{guild.name}",
                documents=False
        ):
            files.create_folder(
                f"data/dumping/emojis/{guild.name}", documents=False
            )
        try:
            prints.event(f"Dumping emojis from {guild.name}")
            await message_builder(
                luna, title="Dumping",
                description=f"```\nEvent\n\nDumping emojis from {guild.name}...```"
            )
            for emoji in guild.emojis:
                url = str(emoji.url)
                name = str(emoji.name)
                r = requests.get(url, stream=True)
                if '.png' in url:
                    open(

                        f'data/dumping/emojis/{guild.name}/{name}.png', 'wb'
                    ).write(
                        r.content
                    )
                elif '.gif' in url:
                    open(
                        f'data/dumping/emojis/{guild.name}/{name}.gif', 'wb'
                    ).write(
                        r.content
                    )
            prints.message(f"Dumped emojis from {guild.name}")
            await message_builder(luna, title="Dumping", description=f"```\nInfo\n\nDumped emojis from {guild.name}```")
        except Exception as e:
            await error_builder(luna, description=f"```{e}```")

    @commands.command(
        name="emojidownload",
        usage="<guild> <emoji>",
        description="Download a emoji"
    )
    async def emojidownload(self, luna, guild: discord.Guild, emoji: discord.Emoji):

        if not files.file_exist(
                f"data/dumping/emojis/{guild.name}",
                documents=False
        ):
            files.create_folder(
                f"data/dumping/emojis/{guild.name}", documents=False
            )
        try:
            prints.event(f"Downloading emoji from {guild.name}")
            await message_builder(
                luna, title="Downloading",
                description=f"```\nEvent\n\nDownloading emoji from {guild.name}...```"
            )
            url = str(emoji.url)
            name = str(emoji.name)
            r = requests.get(url, stream=True)
            if '.png' in url:
                open(

                    f'data/emojis/{guild.name}/{name}.png', 'wb'
                ).write(
                    r.content
                )
            elif '.gif' in url:
                open(

                    f'data/emojis/{guild.name}/{name}.gif', 'wb'
                ).write(
                    r.content
                )
            prints.message(f"Downloaded emoji from {guild.name}")
            await message_builder(
                luna, title="Downloading",
                description=f"```\nInfo\n\nDownloaded emoji from {guild.name}```"
            )
        except Exception as e:
            await error_builder(luna, description=f"```{e}```")

    @commands.command(
        name="avatardump",
        usage="<guild>",
        description="Dump avatars from a guild"
    )
    async def avatardump(self, luna, guild: discord.Guild):

        if not files.file_exist(
                f"data/dumping/avatars/{guild.name}",
                documents=False
        ):
            files.create_folder(
                f"data/dumping/avatars/{guild.name}", documents=False
            )
        try:
            prints.event(f"Dumping avatars from {guild.name}")
            await message_builder(
                luna, title="Dumping",
                description=f"```\nEvent\n\nDumping avatars from {guild.name}...```"
            )
            for member in guild.members:
                url = str(member.avatar_url)
                name = str(member.name)
                r = requests.get(url, stream=True)
                if '.png' in url:
                    open(

                        f'data/dumping/avatars/{guild.name}/{name}.png', 'wb'
                    ).write(
                        r.content
                    )
                elif '.gif' in url:
                    open(

                        f'data/dumping/avatars/{guild.name}/{name}.gif', 'wb'
                    ).write(
                        r.content
                    )
            prints.message(f"Dumped avatars from {guild.name}")
            await message_builder(
                luna, title="Dumping",
                description=f"```\nInfo\n\nDumped avatars from {guild.name}```"
            )
        except Exception as e:
            await error_builder(luna, description=f"```{e}```")

    @commands.command(
        name="channeldump",
        usage="<guild>",
        description="Dump channels from a guild"
    )
    async def channelnamesdump(self, luna, guild: discord.Guild):

        if not files.file_exist(
                f"data/dumping/channels/{guild.name}",
                documents=False
        ):
            files.create_folder(
                f"data/dumping/channels/{guild.name}", documents=False
            )
        try:
            prints.event(f"Dumping channel names from {guild.name}")
            await message_builder(
                luna, title="Dumping",
                description=f"```\nEvent\n\nDumping channel names from {guild.name}...```"
            )
            for channel in guild.channels:
                name = str(channel.name)
                with open(f'data/dumping/channels/{guild.name}/{name}.txt', 'w') as f:
                    f.write(name)
            prints.message(f"Dumped channel names from {guild.name}")
            await message_builder(
                luna, title="Dumping",
                description=f"```\nInfo\n\nDumped channel names from {guild.name}```"
            )
        except Exception as e:
            await error_builder(luna, description=f"```{e}```")


bot.add_cog(DumpCog(bot))


# ////////////////////////////////////////////////////////////////////

def zalgoText(string):
    result = ''

    for char in string:
        for i in range(0, random.randint(20, 40)):
            rand_bytes = random.randint(0x300, 0x36f).to_bytes(2, 'big')
            char += rand_bytes.decode('utf-16be')
        result += char
    return result


class TextCog(commands.Cog, name="Text commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="encode",
        usage="",
        description="Encoding text commands"
    )
    async def encode(self, luna):

        prefix = files.json("data/config.json", "prefix", documents=False)

        cog = self.bot.get_cog('Encode commands')
        commands = cog.get_commands()
        helptext = ""
        for command in commands:
            helptext += f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n"

        embed = discord.Embed(
            title="Encode Text",

            description=f"{theme.description()}```\n{helptext}```"
        )

        embed.set_footer(text=theme.footer())

        await send(luna, embed)

    @commands.command(
        name="decode",
        usage="",
        description="Decoding text commands"
    )
    async def decode(self, luna):

        prefix = files.json("data/config.json", "prefix", documents=False)

        cog = self.bot.get_cog('Decode commands')
        commands = cog.get_commands()
        helptext = ""
        for command in commands:
            helptext += f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n"

        embed = discord.Embed(
            title="Decode Text",

            description=f"{theme.description()}```\n{helptext}```"
        )

        embed.set_footer(text=theme.footer())

        await send(luna, embed)

    @commands.command(
        name="indent",
        usage="<text>",
        description="Text in a embed"
    )
    async def indent(self, luna, *, text: str):

        embed = discord.Embed(description=f"{text}")
        await send(luna, embed)

    @commands.command(
        name="indent_title",
        usage="<text>",
        description="Text in a embed"
    )
    async def indent_title(self, luna, *, text: str):

        embed = discord.Embed(
            title=theme.title(),
            description=f"{text}"
        )
        await send(luna, embed)

    @commands.command(
        name="indent_footer",
        usage="<text>",
        description="Text in a embed"
    )
    async def indent_footer(self, luna, *, text: str):

        embed = discord.Embed(description=f"{text}")
        embed.set_footer(text=theme.footer())
        await send(luna, embed)

    @commands.command(
        name="indent_all",
        usage="<text>",
        description="Text in a embed"
    )
    async def indent_all(self, luna, *, text: str):

        embed = discord.Embed(description=f"{text}")

        embed.set_footer(text=theme.footer())

        await send(luna, embed)

    @commands.command(
        name="ascii",
        usage="<text>",
        description="Ascii text"
    )
    async def ascii(self, luna, *, text: str):
        r = requests.get(f'http://artii.herokuapp.com/make?text={urllib.parse.quote_plus(text)}').text
        if len(f'```{r}```') > 2000:
            await error_builder(luna, description='```Text is too long```')
            return
        await luna.send(f'```{r}```')

    @commands.command(
        name="vape",
        usage="<text>",
        aliases=['vaporwave'],
        description="Vaporwave text"
    )
    async def vape(self, luna, *, text: str):

        text = text.replace('a', 'ａ').replace('A', 'Ａ').replace('b', 'ｂ') \
            .replace('B', 'Ｂ').replace('c', 'ｃ').replace('C', 'Ｃ') \
            .replace('d', 'ｄ').replace('D', 'Ｄ').replace('e', 'ｅ') \
            .replace('E', 'Ｅ').replace('f', 'ｆ').replace('F', 'Ｆ') \
            .replace('g', 'ｇ').replace('G', 'Ｇ').replace('h', 'ｈ') \
            .replace('H', 'Ｈ').replace('i', 'ｉ').replace('I', 'Ｉ') \
            .replace('j', 'ｊ').replace('J', 'Ｊ').replace('k', 'ｋ') \
            .replace('K', 'Ｋ').replace('l', 'ｌ').replace('L', 'Ｌ') \
            .replace('m', 'ｍ').replace('M', 'Ｍ').replace('n', 'ｎ') \
            .replace('N', 'Ｎ').replace('o', 'ｏ').replace('O', 'Ｏ') \
            .replace('p', 'ｐ').replace('P', 'Ｐ').replace('q', 'ｑ') \
            .replace('Q', 'Ｑ').replace('r', 'ｒ').replace('R', 'Ｒ') \
            .replace('s', 'ｓ').replace('S', 'Ｓ').replace('t', 'ｔ') \
            .replace('T', 'Ｔ').replace('u', 'ｕ').replace('U', 'Ｕ') \
            .replace('v', 'ｖ').replace('V', 'Ｖ').replace('w', 'ｗ') \
            .replace('W', 'Ｗ').replace('x', 'ｘ').replace('X', 'Ｘ') \
            .replace('1', '１').replace('2', '２').replace('3', '３') \
            .replace('4', '４').replace('5', '５').replace('6', '６').replace(' ', '　') \
            .replace('7', '７').replace('8', '８').replace('9', '９').replace('0', '０') \
            .replace('?', '？').replace('.', '．').replace('!', '！').replace('[', '［') \
            .replace(']', '］').replace('{', '｛').replace('}', '｝').replace('=', '＝') \
            .replace('(', '（').replace(')', '）').replace('&', '＆').replace('%', '％').replace('"', '＂') \
            .replace('y', 'ｙ').replace('Y', 'Ｙ').replace('z', 'ｚ').replace('Z', 'Ｚ')
        await luna.send(f'{text}')

    @commands.command(
        name="zalgo",
        usage="<text>",
        description="Zalgo text"
    )
    async def zarlgo(self, luna, *, text: str):

        await luna.send(zalgoText(text))

    @commands.command(
        name="reverse",
        usage="<text>",
        description="Reverse given text"
    )
    async def reverse(luna, *, text):

        text = text[::-1]
        await luna.send(text)

    @commands.command(
        name="bold",
        usage="<text>",
        scription="Bold codeblock"
    )
    async def bold(self, luna, *, text: str):

        await luna.send(f"**{text}**")

    @commands.command(
        name="spoiler",
        usage="<text>",
        description="Spoiler codeblock"
    )
    async def spoiler(self, luna, *, text: str):

        await luna.send(f"||{text}||")

    @commands.command(
        name="underline",
        usage="<text>",
        description="Underline codeblock"
    )
    async def underline(self, luna, *, text: str):

        await luna.send(f"__{text}__")

    @commands.command(
        name="strike",
        usage="<text>",
        description="Strike codeblock"
    )
    async def strike(self, luna, *, text: str):

        await luna.send(f"~~{text}~~")


bot.add_cog(TextCog(bot))


class CodeblockCog(commands.Cog, name="Codeblock commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="codeblock_css",
        usage="<text>",
        description="CSS codeblock"
    )
    async def codeblock_css(self, luna, *, text: str):
        await luna.send(f"```css\n{text}\n```")

    @commands.command(
        name="codeblock_brainfuck",
        usage="<text>",
        description="Brainfuck codeblock"
    )
    async def codeblock_brainfuck(self, luna, *, text: str):
        await luna.send(f"```brainfuck\n{text}\n```")

    @commands.command(
        name="codeblock_md",
        usage="<text>",
        description="MD codeblock"
    )
    async def codeblock_md(self, luna, *, text: str):
        await luna.send(f"```md\n{text}\n```")

    @commands.command(
        name="codeblock_fix",
        usage="<text>",
        description="Fix codeblock"
    )
    async def codeblock_fix(self, luna, *, text: str):
        await luna.send(f"```fix\n{text}\n```")

    @commands.command(
        name="codeblock_glsl",
        usage="<text>",
        description="Glsl codeblock"
    )
    async def codeblock_glsl(self, luna, *, text: str):
        await luna.send(f"```glsl\n{text}\n```")

    @commands.command(
        name="codeblock_diff",
        usage="<text>",
        description="Diff codeblock"
    )
    async def codeblock_diff(self, luna, *, text: str):
        await luna.send(f"```diff\n{text}\n```")

    @commands.command(
        name="codeblock_bash",
        usage="<text>",
        description="Bash codeblock"
    )
    async def codeblock_bash(self, luna, *, text: str):
        await luna.send(f"```bash\n{text}\n```")

    @commands.command(
        name="codeblock_cs",
        usage="<text>",
        description="C# codeblock"
    )
    async def codeblock_cs(self, luna, *, text: str):
        await luna.send(f"```cs\n{text}\n```")

    @commands.command(
        name="codeblock_cpp",
        usage="<text>",
        description="C++ codeblock"
    )
    async def codeblock_cpp(self, luna, *, text: str):
        await luna.send(f"```cpp\n{text}\n```")

    @commands.command(
        name="codeblock_ini",
        usage="<text>",
        description="Ini codeblock"
    )
    async def codeblock_ini(self, luna, *, text: str):
        await luna.send(f"```ini\n{text}\n```")

    @commands.command(
        name="codeblock_asciidoc",
        usage="<text>",
        description="Asciidoc codeblock"
    )
    async def codeblock_asciidoc(self, luna, *, text: str):
        await luna.send(f"```asciidoc\n{text}\n```")

    @commands.command(
        name="codeblock_autohotkey",
        usage="<text>",
        description="Autohotkey codeblock"
    )
    async def codeblock_autohotkey(self, luna, *, text: str):
        await luna.send(f"```autohotkey\n{text}\n```")

    @commands.command(
        name="codeblock_python",
        usage="<text>",
        description="Python codeblock"
    )
    async def codeblock_python(self, luna, *, text: str):
        await luna.send(f"```python\n{text}\n```")

    @commands.command(
        name="codeblock_lua",
        usage="<text>",
        description="Lua codeblock"
    )
    async def codeblock_lua(self, luna, *, text: str):
        await luna.send(f"```lua\n{text}\n```")

    @commands.command(
        name="codeblock_php",
        usage="<text>",
        description="PHP codeblock"
    )
    async def codeblock_php(self, luna, *, text: str):
        await luna.send(f"```php\n{text}\n```")

    @commands.command(
        name="codeblock_rust",
        usage="<text>",
        description="Rust codeblock"
    )
    async def codeblock_rust(self, luna, *, text: str):
        await luna.send(f"```rust\n{text}\n```")

    @commands.command(
        name="codeblock_java",
        usage="<text>",
        description="Java codeblock"
    )
    async def codeblock_java(self, luna, *, text: str):
        await luna.send(f"```java\n{text}\n```")

    @commands.command(
        name="codeblock_kotlin",
        usage="<text>",
        description="Kotlin codeblock"
    )
    async def codeblock_kotlin(self, luna, *, text: str):
        await luna.send(f"```kotlin\n{text}\n```")

    @commands.command(
        name="codeblock_js",
        usage="<text>",
        description="Javascript codeblock"
    )
    async def codeblock_js(self, luna, *, text: str):
        await luna.send(f"```javascript\n{text}\n```")

    @commands.command(
        name="codeblock_mysql",
        usage="<text>",
        description="MySQL codeblock"
    )
    async def codeblock_mysql(self, luna, *, text: str):
        await luna.send(f"```MySQL\n{text}\n```")

    @commands.command(
        name="codeblock_mk",
        usage="<text>",
        description="Markdown codeblock"
    )
    async def codeblock_mk(self, luna, *, text: str):
        await luna.send(f"```markdown\n{text}\n```")

    @commands.command(
        name="codeblock_ansi",
        usage="<text>",
        description="Ansi codeblock"
    )
    async def codeblock_ansi(self, luna, *, text: str):
        await luna.send(f"```ansi\n{text}\n```")


bot.add_cog(CodeblockCog(bot))


class ImageCog(commands.Cog, name="Image commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    # ///////////////////////////////////////////////////////////////
    # Avatar commands

    @commands.command(
        name="avatar",
        usage="[@member]",
        aliases=["av"],
        description="Send the avatar"
    )
    async def avatar(self, luna, user: discord.Member = None):

        if user is None:
            user = luna.author
        await message_builder(luna, description=f"```\n{user}'s avatar\n```", large_image=user.avatar_url)

    @commands.command(
        name="avatart",
        usage="<@member> <text>",
        asliases=["avt"],
        description="Send the avatar with text"
    )
    async def avatart(self, luna, user: discord.Member, *, text: str):

        await message_builder(luna, description=f"```\n{text}\n```", large_image=user.avatar_url)

    @commands.command(
        name="searchav",
        usage="<@member>",
        description="Search link of the avatar"
    )
    async def searchav(self, luna, user: discord.Member = None):

        if user is None:
            user = luna.author
        await message_builder(luna, description=f"```\nSearch link for {user}'s avatar\n``````\nGoogle search URL\n\nhttps://images.google.com/searchbyimage?image_url={user.avatar_url}\n```")

    @commands.command(
        name="linkav",
        usage="<@member>",
        description="Link of the avatar"
    )
    async def linkav(self, luna, member: discord.Member):

        embed = discord.Embed(
            title=f"Link for {member}'s avatar",
            description=f"{member.avatar_url}"
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=theme.footer())

        await send(luna, embed)

    @commands.command(
        name="stealav",
        usage="<@member>",
        description="Steal the avatar"
    )
    async def stealav(self, luna, user: discord.Member):

        url = user.avatar_url
        prefix = files.json("data/config.json", "prefix", documents=False)
        if configs.password() == "password-here":
            await error_builder(luna, f"```\nYou didn't configurate your password yet, use {prefix}password <password>\n```")
        else:
            configs.password()
            with open('PFP-1.png', 'wb') as f:
                r = requests.get(url, stream=True)
                for block in r.iter_content(1024):
                    if not block:
                        break
                    f.write(block)
        try:
            with open('PFP-1.png', 'rb') as f:
                await self.bot.user.edit(password=configs.password(), avatar=f.read())
            await message_builder(luna, description=f"```\nStole {user}'s avatar\n```", large_image=user.avatar_url)
        except discord.HTTPException as e:
            await error_builder(luna, description=f"```{e}```")

    @commands.command(
        name="setavatar",
        usage="<url>",
        description="Set your avatar"
    )
    async def setavatar(self, luna, url: str):
        prefix = files.json("data/config.json", "prefix", documents=False)
        if configs.password() == "password-here":
            await error_builder(luna, f"```\nYou didn't configurate your password yet, use {prefix}password <password>\n```")
        else:
            configs.password()
            with open('PFP-1.png', 'wb') as f:
                r = requests.get(url, stream=True)
                for block in r.iter_content(1024):
                    if not block:
                        break
                    f.write(block)
        try:
            with open('PFP-1.png', 'rb') as f:
                await self.bot.user.edit(password=configs.password(), avatar=f.read())
            await message_builder(luna, description=f"```\nChanged avatar\n```", large_image=user.avatar_url)
        except discord.HTTPException as e:
            await error_builder(luna, description=f"```{e}```")

    @commands.command(
        name="invisav",
        usage="",
        description="Invisible avatar"
    )
    async def invisav(self, luna):
        prefix = files.json("data/config.json", "prefix", documents=False)
        url = "https://gauginggadgets.com/wp-content/uploads/2020/07/InvisibleProfileImage.png"
        if configs.password() == "password-here":
            await error_builder(luna, f"```\nYou didn't configurate your password yet, use {prefix}password <password>\n```")
        else:
            configs.password()
            with open('PFP-1.png', 'wb') as f:
                r = requests.get(url, stream=True)
                for block in r.iter_content(1024):
                    if not block:
                        break
                    f.write(block)
        try:
            with open('PFP-1.png', 'rb') as f:
                await self.bot.user.edit(password=configs.password(), avatar=f.read())
            await message_builder(luna, description=f"```\nChanged to an invisible avatar\n```", large_image=user.avatar_url)
        except discord.HTTPException as e:
            await error_builder(luna, description=f"```{e}```")

    # ///////////////////////////////////////////////////////////////
    # Fun image commands

    @commands.command(
        name="dog",
        usage="",
        description="Send a random dog"
    )
    async def dog(self, luna):

        r = requests.get("https://dog.ceo/api/breeds/image/random").json()
        embed = discord.Embed(title=theme.title())
        embed.set_footer(text=theme.footer())

        embed.set_image(url=str(r['message']))
        await send(luna, embed)

    @commands.command(
        name="fox",
        usage="",
        description="Send a random fox"
    )
    async def fox(self, luna):

        r = requests.get('https://randomfox.ca/floof/').json()
        embed = discord.Embed(title=theme.title())
        embed.set_footer(text=theme.footer())

        embed.set_image(url=str(r['image']))
        await send(luna, embed)

    @commands.command(
        name="cat",
        usage="",
        description="Send a random cat"
    )
    async def cat(self, luna):

        r = requests.get("https://api.thecatapi.com/v1/images/search").json()
        embed = discord.Embed(title=theme.title())
        embed.set_footer(text=theme.footer())

        embed.set_image(url=str(r[0]["url"]))
        await send(luna, embed)

    @commands.command(
        name="sadcat",
        usage="",
        description="Send a random sad cat"
    )
    async def sadcat(self, luna):

        r = requests.get("https://api.alexflipnote.dev/sadcat").json()
        embed = discord.Embed(title=theme.title())
        embed.set_footer(text=theme.footer())

        embed.set_image(url=str(r['file']))
        await send(luna, embed)

    @commands.command(
        name="waifu",
        usage="",
        description="Send a random waifu"
    )
    async def waifu(self, luna):

        r = requests.get("https://nekos.life/api/v2/img/waifu").json()
        embed = discord.Embed(title=theme.title())
        embed.set_footer(text=theme.footer())

        embed.set_image(url=str(r['url']))
        await send(luna, embed)

    # ///////////////////////////////////////////////////////////////
    # Image commands

    @commands.command(
        name="wallpaper",
        usage="",
        description="Send a random anime wallpaper"
    )
    async def wallpaper(self, luna):

        r = requests.get("https://nekos.life/api/v2/img/wallpaper").json()
        embed = discord.Embed(title=theme.title())
        embed.set_footer(text=theme.footer())

        embed.set_image(url=str(r['url']))
        await send(luna, embed)

    @commands.command(
        name="wide",
        usage="<@member>",
        description="Wide profile picture"
    )
    async def wide(self, luna, user: discord.User):

        embed = discord.Embed(title=theme.title())
        embed.set_footer(text=theme.footer())

        embed.set_image(
            url=f"https://vacefron.nl/api/wide?image={urllib.parse.quote(str(user.avatar_url).replace('webp', 'png'))}"
        )
        await send(luna, embed)

    @commands.command(
        name="trumptweet",
        usage="<text>",
        description="Create a Trump tweet"
    )
    async def trumptweet(self, luna, *, text: str):

        request = requests.get(
            f'https://nekobot.xyz/api/imagegen?type=trumptweet&text={urllib.parse.quote(text)}'
        )
        data = request.json()
        link = data['message']
        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(url=link)
        await send(luna, embed)

    @commands.command(
        name="bidentweet",
        usage="<text>",
        description="Create a Biden tweet"
    )
    async def bidentweet(self, luna, *, text: str):

        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(
            url=f'https://api.popcat.xyz/biden?text={str(urllib.parse.quote(text))}'
        )
        await send(luna, embed)

    @commands.command(
        name="tweet",
        usage="<name> <text>",
        description="Create a tweet"
    )
    async def tweet(self, luna, name, *, text: str):

        request = requests.get(
            f'https://nekobot.xyz/api/imagegen?type=tweet&username={name}&text={urllib.parse.quote(text)}'
        )
        data = request.json()
        link = data['message']
        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(url=link)
        await send(luna, embed)

    @commands.command(
        name="supreme",
        usage="<text>",
        description="Custom supreme logo"
    )
    async def supreme(self, luna, *, text: str):

        request = requests.get(
            f'https://react.flawcra.cc/api/generation.php?type=supreme&text={str(urllib.parse.quote(text))}'
        ).json()[
            'url']
        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(url=f'{request}')
        await send(luna, embed)

    @commands.command(
        name="changemymind",
        usage="<text>",
        description="Changemymind meme"
    )
    async def changemymind(self, luna, *, text: str):

        request = requests.get(
            f'https://nekobot.xyz/api/imagegen?type=changemymind&text={urllib.parse.quote(text)}'
        )
        data = request.json()
        link = data['message']
        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(url=link)
        await send(luna, embed)

    @commands.command(
        name="phcomment",
        aliases=['pornhubcomment'],
        usage="<@member> <text>",
        description="Pornhub comment"
    )
    async def phcomment(self, luna, user: discord.User, *, text: str):

        image_url = str(user.avatar_url).replace(".webp", ".png")
        request = requests.get(
            f'https://nekobot.xyz/api/imagegen?type=phcomment&image={image_url}&username={urllib.parse.quote(user.name)}&text={urllib.parse.quote(text)}'
        )
        data = request.json()
        link = data['message']
        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(url=link)
        await send(luna, embed)

    @commands.command(
        name="clyde",
        usage="<text>",
        description="Custom Clyde message"
    )
    async def clyde(self, luna, *, text: str):

        request = requests.get(
            f'https://nekobot.xyz/api/imagegen?type=clyde&text={urllib.parse.quote(text)}'
        )
        data = request.json()
        link = data['message']
        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(url=link)
        await send(luna, embed)

    @commands.command(
        name="pikachu",
        usage="<text>",
        description="Surprised Pikachu"
    )
    async def pikachu(self, luna, *, text: str):

        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(
            url=f"https://api.popcat.xyz/pikachu?text={urllib.parse.quote(str(text))}"
        )
        await send(luna, embed)

    @commands.command(
        name="stonks",
        usage="<@member>",
        description="Stonks!"
    )
    async def stonks(self, luna, user: discord.User):

        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(
            url=f"https://vacefron.nl/api/stonks?user={urllib.parse.quote(str(user.avatar_url).replace('webp', 'png'))}"
        )
        await send(luna, embed)

    @commands.command(
        name="notstonks",
        usage="<@member>",
        description="Notstonks!"
    )
    async def notstonks(self, luna, user: discord.User):

        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(
            url=f"https://vacefron.nl/api/stonks?user={urllib.parse.quote(str(user.avatar_url).replace('webp', 'png'))}&notstonks=true"
        )
        await send(luna, embed)

    @commands.command(
        name="emergencymeeting",
        usage="<text>",
        description="Emergency meeting!"
    )
    async def emergencymeeting(self, luna, *, text):

        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(
            url=f"https://vacefron.nl/api/emergencymeeting?text={urllib.parse.quote(text)}"
        )
        await send(luna, embed)

    @commands.command(
        name="eject",
        usage="<true/false> <color> <@member>",
        description="Among Us"
    )
    async def eject(self, luna, impostor: bool, crewmate: str, user: discord.User):

        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(
            url=f"https://vacefron.nl/api/ejected?name={urllib.parse.quote(user.name)}&impostor={impostor}&crewmate={crewmate}"
        )
        await send(luna, embed)

    @commands.command(
        name="drip",
        usage="<@member>",
        description="Drip meme"
    )
    async def drip(self, luna, user: discord.User):

        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(
            url=f"https://vacefron.nl/api/drip?user={urllib.parse.quote(str(user.avatar_url).replace('webp', 'png'))}"
        )
        await send(luna, embed)

    @commands.command(
        name="gun",
        usage="<@member>",
        description="Gun meme"
    )
    async def gun(self, luna, user: discord.User):

        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(
            url=f"https://api.popcat.xyz/gun?image={urllib.parse.quote(str(user.avatar_url).replace('webp', 'png'))}"
        )
        await send(luna, embed)

    @commands.command(
        name="ad",
        usage="<@member>",
        description="Make yourself an ad"
    )
    async def ad(self, luna, user: discord.User):

        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(
            url=f"https://api.popcat.xyz/ad?image={urllib.parse.quote(str(user.avatar_url).replace('webp', 'png'))}"
        )
        await send(luna, embed)


bot.add_cog(ImageCog(bot))


class ImageCog2(commands.Cog, name="Image commands 2"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="alert",
        usage="<text>",
        description="Iphone alert"
    )
    async def alert(self, luna, *, text: str):
        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(
            url=f"https://api.popcat.xyz/alert?text={urllib.parse.quote(str(text))}"
        )
        await send(luna, embed)

    @commands.command(
        name="caution",
        usage="<text>",
        description="Caution image"
    )
    async def caution(self, luna, *, text: str):
        embed = discord.Embed(title=theme.title())
        embed.set_footer(text=theme.footer())
        embed.set_image(url=f"https://api.popcat.xyz/caution?text={urllib.parse.quote(str(text))}")
        await send(luna, embed)

    @commands.command(
        name="distractedbf",
        usage="<@boyfriend> <@woman> <@girlfriend>",
        description="Distracted boyfriend meme"
    )
    async def distractedbf(self, luna, boyfriend: discord.User, woman: discord.User, girlfriend: discord.User):
        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(
            url=f"https://vacefron.nl/api/distractedbf?boyfriend={urllib.parse.quote(str(boyfriend.avatar_url).replace('webp', 'png'))}&woman={urllib.parse.quote(str(woman.avatar_url).replace('webp', 'png'))}&girlfriend={urllib.parse.quote(str(girlfriend.avatar_url).replace('webp', 'png'))}"
        )
        await send(luna, embed)

    @commands.command(
        name="icanmilkyou",
        usage="<@member1> <@member2>",
        description="ICanMilkYou"
    )
    async def icanmilkyou(self, luna, user1: discord.User, user2: discord.User):
        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(
            url=f"https://vacefron.nl/api/icanmilkyou?user1={urllib.parse.quote(str(user1.avatar_url))}&user2={urllib.parse.quote(str(user2.avatar_url))}"
        )
        await send(luna, embed)

    @commands.command(
        name="heaven",
        usage="<@member>",
        description="Heaven meme"
    )
    async def heaven(self, luna, user: discord.User):
        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(
            url=f"https://vacefron.nl/api/heaven?user={urllib.parse.quote(str(user.avatar_url).replace('webp', 'png'))}"
        )
        await send(luna, embed)

    @commands.command(
        name="dockofshame",
        usage="<@member>",
        description="Heaven meme"
    )
    async def dockofshame(self, luna, user: discord.User):
        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(
            url=f"https://vacefron.nl/api/dockofshame?user={urllib.parse.quote(str(user.avatar_url).replace('webp', 'png'))}"
        )
        await send(luna, embed)

    @commands.command(
        name="firsttime",
        usage="<@member>",
        description="First time? meme"
    )
    async def firsttime(self, luna, user: discord.User):
        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(
            url=f"https://vacefron.nl/api/firsttime?user={urllib.parse.quote(str(user.avatar_url).replace('webp', 'png'))}"
        )
        await send(luna, embed)

    @commands.command(
        name="trash",
        usage="<@member>",
        description="Trash meme"
    )
    async def trash(self, luna, user: discord.User):
        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(
            url=f'https://api.no-api-key.com/api/v2/trash?image={str(user.avatar_url).replace(".webp", ".png")}'
        )
        await send(luna, embed)

    @commands.command(
        name="simp",
        usage="<@member>",
        description="Simp card"
    )
    async def simp(self, luna, user: discord.User):
        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(
            url=f'https://api.no-api-key.com/api/v2/simpcard?image={str(user.avatar_url).replace(".webp", ".png")}'
        )
        await send(luna, embed)

    @commands.command(
        name="wanted",
        usage="<@member>",
        description="Wanted"
    )
    async def wanted(self, luna, user: discord.User):
        request = requests.get(
            f'https://react.flawcra.cc/api/generation.php?type=wanted&url={str(user.avatar_url).replace(".webp", ".png")}'
        )
        data = request.json()
        link = data['url']
        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(url=link)
        await send(luna, embed)

    @commands.command(
        name="wasted",
        usage="<@member>",
        description="GTA Wasted"
    )
    async def wasted(self, luna, user: discord.User):
        request = requests.get(
            f'https://react.flawcra.cc/api/generation.php?type=wasted&url={str(user.avatar_url).replace(".webp", ".png")}'
        )
        data = request.json()
        link = data['url']
        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(url=link)
        await send(luna, embed)

    @commands.command(
        name="continued",
        usage="<@member>",
        description="To be continued"
    )
    async def continued(self, luna, user: discord.User):
        request = requests.get(
            f'https://react.flawcra.cc/api/generation.php?type=tobecontinued&url={str(user.avatar_url).replace(".webp", ".png")}'
        )
        data = request.json()
        link = data['url']
        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(url=link)
        await send(luna, embed)

    @commands.command(
        name="drake",
        usage="<no, yes>",
        description="Drake yes and no meme"
    )
    async def drake(self, luna, *, text: str):
        try:
            text = text.split(', ')
            text1 = text[0]
            text2 = text[1]
            embed = discord.Embed(
                title=theme.title()
            )
            embed.set_footer(text=theme.footer())

            embed.set_image(
                url=f'https://api.popcat.xyz/drake?text1={str(urllib.parse.quote(text1))}&text2={str(urllib.parse.quote(text2))}'
            )
            await send(luna, embed)
        except BaseException:
            prefix = files.json("data/config.json", "prefix", documents=False)
            await error_builder(luna, f"```Example: {prefix}drake Paid Selfbots, Luna\nThe space between the comma and the two words is required.```")

    @commands.command(
        name="takemymoney",
        usage="<text1, text2>",
        description="Take my money"
    )
    async def takemymoney(self, luna, *, text: str):
        text = text.split(', ')
        text1 = text[0]
        text2 = text[1]
        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(
            url=f"https://api.memegen.link/images/money/{urllib.parse.quote(text1)}/{urllib.parse.quote(text2)}.png"
        )
        await send(luna, embed)

    @commands.command(
        name="pornhub",
        usage="<text1, text2>",
        description="PornHub logo"
    )
    async def pornhub(self, luna, *, text: str):
        text = text.split(', ')
        text1 = text[0]
        text2 = text[1]
        request = requests.get(
            f'https://react.flawcra.cc/api/generation.php?type=phlogo&text={str(urllib.parse.quote(text1))}&text2={str(urllib.parse.quote(text2))}'
        )
        data = request.json()
        link = data['url']
        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(url=link)
        await send(luna, embed)

    @commands.command(
        name="recaptcha",
        usage="<text>",
        description="reCAPTCHA"
    )
    async def recaptcha(self, luna, *, text: str):
        request = requests.get(
            f'https://react.flawcra.cc/api/generation.php?type=captcha&text={str(urllib.parse.quote(text))}'
        )
        data = request.json()
        link = data['url']
        embed = discord.Embed(
            title=theme.title()
        )
        embed.set_footer(text=theme.footer())

        embed.set_image(url=link)
        await send(luna, embed)


bot.add_cog(ImageCog2(bot))


def Nitro():
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return f'https://discord.gift/{code}'


class TrollCog(commands.Cog, name="Troll commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="ghostping",
        usage="<@member>",
        aliases=['gp'],
        description="Ghostping someone"
    )
    async def ghostping(self, luna):
        try:
            await luna.message.delete()
        except BaseException:
            pass

    @commands.command(
        name="empty",
        usage="",
        description="Sends a empty message"
    )
    async def empty(self, luna):

        await luna.send("​")

    @commands.command(
        name="copy",
        usage="<@member>",
        aliases=['copycat'],
        description="Copy every message a member"
    )
    async def copy(self, luna, member: discord.User):

        global copycat
        copycat = member
        if configs.mode() == 2:
            sent = await luna.send(f"```ini\n[ {theme.title()} ]\n\nNow copying {copycat}\n\n[ {theme.footer()} ]```")
            await asyncio.sleep(configs.delete_timer())
            await sent.delete()
        else:
            embed = discord.Embed(
                title=theme.title(),

                description=f"Now copying {copycat}",

            )

            embed.set_footer(
                text=theme.footer(),

            )
            embed.set_author(
                name=theme.author(), url=theme.author_url(
                ), icon_url=theme.author_icon_url()
            )

            sent = await send(luna, embed)
            await asyncio.sleep(configs.delete_timer())
            await sent.delete()

    @commands.command(
        name="stopcopy",
        usage="",
        aliases=['stopcopycat'],
        description="Stop copying a member"
    )
    async def stopcopy(self, luna):

        global copycat
        if copycat is None:
            if configs.mode() == 2:
                sent = await luna.send(
                    f"```ini\n[ {theme.title()} ]\n\nNo one was getting copied\n\n[ {theme.footer()} ]```"
                )
                await asyncio.sleep(configs.delete_timer())
                await sent.delete()
            else:
                embed = discord.Embed(
                    title=theme.title(),

                    description=f"No one was getting copied",

                )

                embed.set_footer(
                    text=theme.footer(),

                )
                embed.set_author(
                    name=theme.author(), url=theme.author_url(
                    ), icon_url=theme.author_icon_url()
                )

                sent = await send(luna, embed)
                await asyncio.sleep(configs.delete_timer())
                await sent.delete()
            return

        if configs.mode() == 2:
            sent = await luna.send(
                f"```ini\n[ {theme.title()} ]\n\nStopped copying {copycat}\n\n[ {theme.footer()} ]```"
            )
            copycat = None
            await asyncio.sleep(configs.delete_timer())
            await sent.delete()
        else:
            embed = discord.Embed(
                title=theme.title(),

                description=f"Stopped copying {copycat}",

            )

            embed.set_footer(
                text=theme.footer(),

            )
            embed.set_author(
                name=theme.author(), url=theme.author_url(
                ), icon_url=theme.author_icon_url()
            )

            sent = await send(luna, embed)
            copycat = None
            await asyncio.sleep(configs.delete_timer())
            await sent.delete()

    @commands.command(
        name="fakenitro",
        usage="[amount]",
        description="Generate fake nitro links"
    )
    async def fakenitro(self, luna, amount: int = None):

        try:
            if amount is None:
                await luna.send(Nitro())
            else:
                for each in range(0, amount):
                    await luna.send(Nitro())
        except Exception as e:
            await luna.send(f"Error: {e}")

    @commands.command(
        name="trollnitro",
        usage="",
        description="Send a used nitro link"
    )
    async def trollnitro(self, luna):

        await luna.send("https://discord.gift/6PWNmA6NTuRkejaP")

    @commands.command(
        name="mreact",
        usage="",
        description="Mass reacts on last message"
    )
    async def mreact(self, luna):
        await luna.message.delete()
        messages = await luna.message.channel.history(limit=1).flatten()
        for message in messages:
            await message.add_reaction("😂")
            await message.add_reaction("😡")
            await message.add_reaction("🤯")
            await message.add_reaction("👍")
            await message.add_reaction("👎")
            await message.add_reaction("💯")
            await message.add_reaction("🍑")
            await message.add_reaction("❗")
            await message.add_reaction("🥳")
            await message.add_reaction("👏")
            await message.add_reaction("🔞")
            await message.add_reaction("🇫")
            await message.add_reaction("🥇")
            await message.add_reaction("🤔")
            await message.add_reaction("💀")
            await message.add_reaction("❤️")

    @commands.command(
        name="fakenuke",
        usage="",
        description="Fakenuke"
    )
    async def fakenuke(self, luna):

        message = await luna.send(content=':bomb: :bomb: Nuking this server in 5 :rotating_light:')
        await asyncio.sleep(1)
        await message.edit(content='0')
        await asyncio.sleep(1)
        await message.edit(content='1')
        await asyncio.sleep(1)
        await message.edit(content='2')
        await asyncio.sleep(1)
        await message.edit(content='3')
        await asyncio.sleep(1)
        await message.edit(content='4')
        await asyncio.sleep(1)
        await message.edit(content='This server will be destoyed now')
        await asyncio.sleep(1)
        await message.edit(content=':bomb:')
        await asyncio.sleep(1)
        await message.edit(content=':boom:')
        await asyncio.sleep(1)
        await message.edit(content='Shouldn\'t have even created it ig')
        await asyncio.sleep(1)
        await message.edit(content=':bomb: :bomb:')
        await asyncio.sleep(1)
        await message.edit(content=':boom: :boom:')
        await asyncio.sleep(1)
        await message.edit(content='You will wish you never lived to know about discord')
        await asyncio.sleep(1)
        await message.edit(content=':bomb: :bomb: :bomb:')
        await asyncio.sleep(1)
        await message.edit(content=':boom: :boom: :boom:')
        await asyncio.sleep(1)
        await message.edit(content='There it comes...')
        await asyncio.sleep(1)
        await message.edit(content='https://giphy.com/gifs/rick-roll-lgcUUCXgC8mEo')

    @commands.command(
        name="banroulette",
        usage="",
        description="Ban roulette"
    )
    async def banroulette(self, luna):
        """
        Get a random user from the server and ban them
        """

        user = random.choice(luna.message.guild.members)
        if user == luna.user:
            return
        try:
            await user.ban()
        except Exception as e:
            await error_builder(luna, description=f"```{e}```")
        await message_builder(luna, "Ban Roulette", f"{user} has been banned")


bot.add_cog(TrollCog(bot))


class FunCog(commands.Cog, name="Fun commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="impersonate",
        usage="<@member> <message>",
        description="Make them send your message"
    )
    async def impersonate(self, luna, user: discord.User, *, message: str):

        webhook = await luna.channel.create_webhook(name=user.name)
        await webhook.send(message, username=user.name, avatar_url=user.avatar_url)
        await webhook.delete()

    @commands.command(
        name="shoot",
        usage="<@member>",
        description="Shoot up someone"
    )
    async def shoot(self, luna, user: discord.Member):

        await message_builder(
            luna, description=f"{user.mention},  got shot up!",
            large_image="https://media1.tenor.com/images/cfb7817a23645120d4baba2dcb9205e0/tenor.gif", footer="None"
        )

    @commands.command(
        name="feed",
        usage="<@member>",
        description="Feed someone"
    )
    async def feed(self, luna, user: discord.Member):

        r = requests.get("https://nekos.life/api/v2/img/feed").json()
        await message_builder(
            luna, description=f"{luna.author.mention} feeds {user.mention}",
            large_image=str(r['url']), footer="None"
        )

    @commands.command(
        name="bite",
        usage="<@member>",
        description="Bite someone"
    )
    async def bite(self, luna, user: discord.Member):

        gif_list = [
            "https://c.tenor.com/MKjNSLL4dGoAAAAC/bite-cute.gif",
            "https://c.tenor.com/aKzAQ_cFsFEAAAAC/arms-bite.gif",
            "https://c.tenor.com/4j3hMz-dUz0AAAAC/anime-love.gif",
            "https://c.tenor.com/TX6YHUnHJk4AAAAC/mao-amatsuka-gj-bu.gif"]
        await message_builder(
            luna, description=f"{user.mention} got bitten by {luna.author.mention}!",
            large_image=random.choice(gif_list), footer="None"
        )

    @commands.command(
        name="kiss",
        usage="<@member>",
        description="Kiss someone"
    )
    async def kiss(self, luna, user: discord.Member):

        r = requests.get("https://nekos.life/api/v2/img/kiss").json()
        await message_builder(
            luna, description=f"{user.mention} got kissed by {luna.author.mention}!",
            large_image=str(r['url']), footer="None"
        )

    @commands.command(
        name="hug",
        usage="<@member>",
        description="Hug someone"
    )
    async def hug(self, luna, user: discord.Member):

        r = requests.get("https://nekos.life/api/v2/img/hug").json()
        await message_builder(
            luna, description=f"{user.mention} got hugged by {luna.author.mention}!",
            large_image=str(r['url']), footer="None"
        )

    @commands.command(
        name="pat",
        usage="<@member>",
        description="Pat someone"
    )
    async def pat(self, luna, user: discord.Member):

        r = requests.get("https://nekos.life/api/v2/img/pat").json()
        await message_builder(luna, description=f"{luna.author.mention} pats {user.mention}", large_image=str(r['url']), footer="None")

    @commands.command(
        name="slap",
        usage="<@member>",
        description="Slap someone"
    )
    async def slap(self, luna, user: discord.Member):

        r = requests.get("https://nekos.life/api/v2/img/slap").json()
        await message_builder(
            luna, description=f"{luna.author.mention} slapped {user.mention}",
            large_image=str(r['url']), footer="None"
        )

    @commands.command(
        name="tickle",
        usage="<@member>",
        description="Tickle someone"
    )
    async def tickle(self, luna, user: discord.Member):

        r = requests.get("https://nekos.life/api/v2/img/tickle").json()
        await message_builder(
            luna, description=f"{luna.author.mention} tickles {user.mention}",
            large_image=str(r['url']), footer="None"
        )

    @commands.command(
        name="fml",
        usage="",
        description="Fuck my life"
    )
    async def fml(self, luna):

        request = requests.get(
            f'https://react.flawcra.cc/api/generation.php?type=fml'
        )
        data = request.json()
        text = data['text']
        await message_builder(luna, description=f"```\n{text}\n```")

    @commands.command(
        name="gay",
        usage="[@member]",
        description="Gay rate somebody"
    )
    async def gay(self, luna, user: discord.Member = None):

        if user is None:
            user = luna.author
        number = random.randint(1, 100)
        await message_builder(luna, title=f"{user}'s Gay Rate", description=f"{number}% Gay 🏳️‍🌈")

    @commands.command(
        name="iq",
        usage="[@member]",
        description="Somebody's IQ"
    )
    async def iq(self, luna, user: discord.Member = None):

        if user is None:
            user = luna.author
        number = random.randint(1, 120)
        if number < 20:
            special = "\n\nQuite low, isn't it?"
        else:
            special = ""
        await message_builder(luna, title=f"{user}'s IQ", description=f"{number}{special}")

    @commands.command(
        name="love",
        usage="<@member> [@member]",
        description="Love rate"
    )
    async def love(self, luna, user1: discord.Member, user2: discord.Member = None):

        if user2 is None:
            user2 = luna.author
        number = random.randint(1, 100)
        breakup = random.randint(1, 100)
        kids = random.randint(1, 100)
        embed = discord.Embed(
            title=f"{user1} ❤️ {user2}",
            description=f"{number}% fitted!\n{kids}% chance of them having kids!\n{breakup}% chance of them breaking up!"
        )

        embed.set_footer(text=theme.footer())

        await send(luna, embed)

    @commands.command(
        name="coronatest",
        usage="<@member>",
        description="Test somebody for Corona"
    )
    async def coronatest(self, luna, user: discord.Member = None):

        if user is None:
            member = luna.author
        else:
            member = user
        random.seed((member.id * 6) / 2)
        percent = random.randint(0, 100)
        embed = discord.Embed(
            title=f"{user}'s Corona Test",
            description=f'```\n{percent}% positive!\n``````\nResult\n\nOverall » {"Positive" if (percent > 50) else "Negative"}```'
        )

        embed.set_footer(text=theme.footer())

        await send(luna, embed)

    @commands.command(
        name="8ball",
        usage="<question>",
        description="Ask 8 Ball!"
    )
    async def _8ball(self, luna, *, question: str):

        responses = [
            'That is a resounding no',
            'It is not looking likely',
            'Too hard to tell',
            'It is quite possible',
            'That is a definite yes!',
            'Maybe',
            'There is a good chance'
        ]
        answer = random.choice(responses)
        embed = discord.Embed(
            title="8 Ball",
            description=f"```\nQuestion\n\n{question}\n``````\nAnswer\n\n{answer}\n```"
        )
        embed.set_thumbnail(
            url="https://www.horoscope.com/images-US/games/game-magic-8-ball-no-text.png"
        )
        embed.set_footer(text=theme.footer())

        await send(luna, embed)

    @commands.command(
        name="slot",
        usage="",
        aliases=['slots'],
        description="Play slots"
    )
    async def slot(self, luna):

        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)
        slotmachine = f"**------------------\n| {a} | {b} | {c} |\n------------------\n\n{luna.author.name}**,"
        if a == b == c:
            embed = discord.Embed(
                title="Slot Machine",
                description=f"{slotmachine} All matchings, you won!",

            )
            embed.set_footer(
                text=theme.footer(),

            )
            embed.set_author(
                name=theme.author(), url=theme.author_url(
                ), icon_url=theme.author_icon_url()
            )
            await send(luna, embed)
        elif (a == b) or (a == c) or (b == c):
            embed = discord.Embed(
                title="Slot Machine",
                description=f"{slotmachine} 2 in a row, you won!",

            )
            embed.set_footer(
                text=theme.footer(),

            )
            embed.set_author(
                name=theme.author(), url=theme.author_url(
                ), icon_url=theme.author_icon_url()
            )
            await send(luna, embed)
        else:
            embed = discord.Embed(
                title="Slot Machine",
                description=f"{slotmachine} No match, you lost!",

            )
            embed.set_footer(
                text=theme.footer(),

            )
            embed.set_author(
                name=theme.author(), url=theme.author_url(
                ), icon_url=theme.author_icon_url()
            )
            await send(luna, embed)

    @commands.command(
        name="dadjoke",
        usage="",
        description="Dad jokes"
    )
    async def dadjoke(self, luna):

        request = requests.get(
            f'https://icanhazdadjoke.com/',
            headers={
                'accept': 'application/json'
            }
        )
        data = request.json()
        joke = data['joke']
        embed = discord.Embed(
            title=theme.title(),

            description=f'```\n{joke}\n```'
        )
        embed.set_footer(text=theme.footer())

        await send(luna, embed)

    @commands.command(
        name="joke",
        usage="",
        description="Random jokes"
    )
    async def dadjoke(self, luna):

        request = requests.get(
            f'http://www.official-joke-api.appspot.com/random_joke'
        )
        data = request.json()
        setup = data['setup']
        punchline = data['punchline']
        embed = discord.Embed(
            title=theme.title(),

            description=f'```\nSetup\n\n{setup}\n``````\nPunchline\n\n{punchline}\n```'
        )
        embed.set_footer(text=theme.footer())

        await send(luna, embed)

    @commands.command(
        name="coinflip",
        usage="",
        description="Flip a coin"
    )
    async def coinflip(self, luna):

        lista = ['head', 'tails']
        coin = random.choice(lista)
        try:
            if coin == 'head':
                await message_builder(luna, title="Head")
            else:
                await message_builder(luna, title="Tails")
        except discord.HTTPException:
            if coin == 'head':
                await luna.send("```\nCoinflip » Head```")
            else:
                await luna.send("```\nCoinflip » Tails```")

    @commands.command(
        name="prntsc",
        usage="",
        description="Send a random prnt.sc"
    )
    async def prntsc(self, luna):

        await luna.send(Randprntsc())

    @commands.command(
        name="farmer",
        usage="",
        description="Dank Memer farmer"
    )
    async def farmer(self, luna):

        global farming
        farming = True
        while farming:
            await luna.send("pls beg")
            await asyncio.sleep(3)
            await luna.send("pls deposit all")
            await asyncio.sleep(42)

    @commands.command(
        name="afarmer",
        usage="",
        description="Advanced Dank Memer farmer"
    )
    async def afarmer(self, luna):

        global farming
        farming = True
        while farming:
            await luna.send("pls beg")
            await asyncio.sleep(3)
            await luna.send("pls deposit all")
            await asyncio.sleep(3)
            await luna.send("pls postmeme")
            await asyncio.sleep(3)
            await luna.send("n")
            await asyncio.sleep(3)
            await luna.send("pls fish")
            await asyncio.sleep(33)

    @commands.command(
        name="cfarmer",
        usage="",
        description="Advanced Dank Memer farmer"
    )
    async def cfarmer(self, luna):

        global farming
        farming = True
        while farming:
            await luna.send("pls hunt")
            await asyncio.sleep(5)
            await luna.send("pls search")
            await asyncio.sleep(5)
            await luna.send("pls fish")
            await asyncio.sleep(10)
            await luna.send("pls beg")
            await asyncio.sleep(20)
            await luna.send("pls pm")
            await asyncio.sleep(16)
            await luna.send("pls beg")
            await asyncio.sleep(5)
            await luna.send("pls dep all")
            await asyncio.sleep(15)

    @commands.command(
        name="stopfarmer",
        usage="",
        description="Stops the Dank Memer farmer"
    )
    async def stopfarmer(self, luna):

        global farming
        farming = False
        await message_builder(luna, description="Stopped farming")


bot.add_cog(FunCog(bot))


class ToolsCog(commands.Cog, name="Tools commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="note",
        aliases=['newnote'],
        usage="<name> <text>",
        description="Create a note"
    )
    async def note(self, luna, name: str, *, text: str):

        if files.file_exist(f"data/notes/{name}.txt", documents=False):
            if configs.error_log() == "console":
                prints.error(
                    f"A note already exists with the name » {color.print_gradient(name)}"
                )
            else:
                await error_builder(luna, description=f"```\nA note already exists with the name » {name}```")
        else:
            file = open(
                f"data/notes/{name}.txt", 'wb'
            )
            file.write(str(text))
            file.close()
            prints.message(f"Created note » {color.print_gradient(name)}")
            embed = discord.Embed(
                title=theme.title(),
                description=f"```\nCreated note » {name}```"
            )

            embed.set_footer(
                text=theme.footer(),

            )
            embed.set_author(
                name=theme.author(), url=theme.author_url(
                ), icon_url=theme.author_icon_url()
            )

            await send(luna, embed)

    @commands.command(
        name="editnote",
        usage="<name> <name>",
        description="Edit the note name"
    )
    async def editnote(self, luna, name: str, themename: str):

        if not files.file_exist(f"data/notes/{name}.txt", documents=False):
            if configs.error_log() == "console":
                prints.error(
                    f"No note exists with the name » {color.print_gradient(name)}"
                )
            else:
                await error_builder(luna, description=f"```\nNo note exists with the name » {name}```")
        else:
            os.rename(
                f"data/notes/{name}.txt", f"data/notes/{themename}.txt"
            )
            prints.message(
                f"Edited note {name} to » {color.print_gradient(themename)}"
            )
            embed = discord.Embed(
                title=theme.title(),
                description=f"```\nEdited \"note\" {name} to » {themename}```"
            )

            embed.set_footer(
                text=theme.footer(),

            )
            embed.set_author(
                name=theme.author(), url=theme.author_url(), icon_url=theme.author_icon_url()
            )

            await send(luna, embed)

    @commands.command(
        name="delnote",
        usage="<name>",
        description="Delete a note"
    )
    async def delnote(self, luna, name: str):

        if files.file_exist(f"data/notes/{name}.txt", documents=False):
            os.remove(
                f"data/notes/{name}.txt"
            )
            prints.message(f"Deleted note » {color.print_gradient(name)}")

            embed = discord.Embed(
                title=theme.title(),
                description=f"```\nDeleted note » {name}```"
            )

            embed.set_footer(
                text=theme.footer(),

            )
            embed.set_author(
                name=theme.author(), url=theme.author_url(
                ), icon_url=theme.author_icon_url()
            )

            await send(luna, embed)
        else:
            if configs.error_log() == "console":
                prints.error(f"There is no note called » {color.print_gradient(name)}")
            else:
                await error_builder(luna, description=f"```\nThere is no note called » {name}```")

    @commands.command(
        name="sendnote",
        usage="<name>",
        description="Send the note"
    )
    async def sendnote(self, luna, name: str):

        if not files.file_exist(f"data/notes/{name}.txt", documents=False):
            if configs.error_log() == "console":
                prints.error(
                    f"No note exists with the name » {color.print_gradient(name)}"
                )
            else:
                await error_builder(luna, description=f"```\nNo note exists with the name » {name}```")
        else:
            if name.endswith('.txt'):
                name = name[:-4]
            await luna.send(file=discord.File(f"data/notes/{name}.txt"))

    @commands.command(
        name="shownote",
        usage="<name>",
        description="Send the content of the note"
    )
    async def shownote(self, luna, name: str):

        if not files.file_exist(f"data/notes/{name}.txt", documents=False):
            if configs.error_log() == "console":
                prints.error(
                    f"No note exists with the name » {color.print_gradient(name)}"
                )
            else:
                await error_builder(luna, description=f"```\nNo note exists with the name » {name}```")
        else:
            file = open(
                f"data/notes/{name}.txt", "r"
            )
            file_data = file.read()
            if file_data == "":
                if configs.error_log() == "console":
                    prints.error(f"The note is empty")
                else:
                    await error_builder(luna, description=f"```\nThe note is empty```")
            else:
                embed = discord.Embed(
                    title="Notes",
                    description=f"```\nContent of {name}.txt ↴\n\n{str(file_data)}```",

                )

                embed.set_footer(
                    text=theme.footer(),

                )
                embed.set_author(
                    name=theme.author(), url=theme.author_url(
                    ), icon_url=theme.author_icon_url()
                )

                await send(luna, embed)

    @commands.command(
        name="notes",
        usage="",
        description="Show all notes"
    )
    async def notes(self, luna):

        path_to_text = "data/notes"
        text_files = [pos_txt for pos_txt in os.listdir(
            path_to_text
        ) if pos_txt.endswith('.txt')]
        prefix = files.json("data/config.json", "prefix", documents=False)

        if not text_files:
            stringedit = "None"
        else:
            string = f"{text_files}"
            stringedit = string.replace(
                ',',
                f"\n{prefix}shownote"
            ).replace(
                "'",
                ""
            ).replace(
                '[',
                f"{prefix}shownote "
            ).replace(
                ']',
                ""
            ).replace(
                '.txt',
                ""
            )

        embed = discord.Embed(
            title="Notes",
            description=f"{theme.description()}```\n"
                        f"Note control\n\n"
                        f"{prefix}note <name> <text> » Create a note\n"
                        f"{prefix}editnote <name> <name> » Edit note name\n"
                        f"{prefix}delnote <name>   » Delete a note\n"
                        f"{prefix}sendnote <name>  » Send the note\n```"
                        f"```\nAvailable notes\n\n{stringedit}```"
        )

        embed.set_footer(text=theme.footer())

        await send(luna, embed)

    @commands.command(
        name="tokencheck",
        usage="",
        description="Check the tokens.txt"
    )
    async def tokencheck(self, luna):

        file = open(
            "data/raiding/tokens.txt", "r"
        )
        nonempty_lines = [line.strip("\n") for line in file if line != "\n"]
        line_count = len(nonempty_lines)
        file.close()

        if os.stat("data/raiding/tokens.txt").st_size == 0:
            await message_builder(luna, title="Token Check", description="```\ntokens.txt is empty...```")
            return

        await message_builder(luna, title="Token Check", description=f"```\nChecking {line_count} tokens...```")

        valid_tokens = []
        success = 0
        failed = 0

        with open("data/raiding/tokens.txt", "r+") as f:
            for line in f:
                token = line.strip("\n")
                headers = {
                    'Content-Type': 'application/json',
                    'authorization': token
                }
                url = f"https://discord.com/api/v6/users/@me/library"
                request = requests.get(url, headers=headers)
                if request.status_code == 200:
                    valid_tokens.append(token)
                    success += 1
                else:
                    failed += 1
                    pass

        with open("data/raiding/tokens.txt", "w+") as f:
            for i in valid_tokens:
                f.write(i + "\n")
        await message_builder(
            luna, title="Token Check",
            description="```\nSuccessfully checked all tokens and removed invalid ones.\n``````\nValid tokens » " + str(success) + "\nInvalid tokens » " + str(failed) + "```"
        )

    @commands.command(
        name="tokeninfo",
        usage="<token>",
        description="Check the token for information"
    )
    async def tokeninfo(self, luna, token: str):

        headers = {"Authorization": token, "Content-Type": "application/json"}
        res = requests.get(f"https://discord.com/api/{api_version}/users/@me", headers=headers)
        cc_digits = {"american express": "3", "visa": "4", "mastercard": "5"}
        languages = {
            "da": "Danish, Denmark",
            "de": "German, Germany",
            "en-GB": "English, United Kingdom",
            "en-US": "English, United States",
            "es-ES": "Spanish, Spain",
            "fr": "French, France",
            "hr": "Croatian, Croatia",
            "lt": "Lithuanian, Lithuania",
            "hu": "Hungarian, Hungary",
            "nl": "Dutch, Netherlands",
            "no": "Norwegian, Norway",
            "pl": "Polish, Poland",
            "pt-BR": "Portuguese, Brazilian, Brazil",
            "ro": "Romanian, Romania",
            "fi": "Finnish, Finland",
            "sv-SE": "Swedish, Sweden",
            "vi": "Vietnamese, Vietnam",
            "tr": "Turkish, Turkey",
            "cs": "Czech, Czechia, Czech Republic",
            "el": "Greek, Greece",
            "bg": "Bulgarian, Bulgaria",
            "ru": "Russian, Russia",
            "uk": "Ukranian, Ukraine",
            "th": "Thai, Thailand",
            "zh-CN": "Chinese, China",
            "ja": "Japanese",
            "zh-TW": "Chinese, Taiwan",
            "ko": "Korean, Korea",
        }
        if res.status_code == 200:
            res_json = res.json()
            user_name = f'{res_json["username"]}#{res_json["discriminator"]}'
            user_id = res_json["id"]
            avatar_id = res_json["avatar"]
            avatar_url = f"https://cdn.discord.com/avatars/{user_id}/{avatar_id}.gif"
            phone_number = res_json["phone"]
            email = res_json["email"]
            mfa_enabled = res_json["mfa_enabled"]
            flags = res_json["flags"]
            locale = res_json["locale"]
            verified = res_json["verified"]
            language = languages.get(locale)
            creation_date = datetime.fromtimestamp(
                ((int(user_id) >> 22) + 1420070400000) / 1000
            ).strftime("%d-%m-%Y %H:%M:%S")
            res = requests.get(
                "https://discord.com/api/v6/users/@me/billing/subscriptions",
                headers=headers,
            )
            nitro_data = res.json()
            has_nitro = bool(len(nitro_data) > 0)
            if has_nitro:
                d1 = datetime.strptime(
                    nitro_data[0]["current_period_end"].split(".")[0],
                    "%Y-%m-%dT%H:%M:%S",
                )
                d2 = datetime.strptime(
                    nitro_data[0]["current_period_start"].split(".")[0],
                    "%Y-%m-%dT%H:%M:%S",
                )
                days_left = abs((d2 - d1).days)
            billing_info = []
            for x in requests.get(
                    "https://discord.com/api/v6/users/@me/billing/payment-sources",
                    headers=headers,
            ).json():
                y = x["billing_address"]
                name = y["name"]
                address_1 = y["line_1"]
                address_2 = y["line_2"]
                city = y["city"]
                postal_code = y["postal_code"]
                state = y["state"]
                country = y["country"]
                if x["type"] == 1:
                    cc_brand = x["brand"]
                    cc_first = cc_digits.get(cc_brand)
                    cc_last = x["last_4"]
                    cc_month = str(x["expires_month"])
                    cc_year = str(x["expires_year"])
                    data = {
                        "Payment Type": "Credit Card",
                        "Valid": not x["invalid"],
                        "CC Holder Name": name,
                        "CC Brand": cc_brand.title(),
                        "CC Number": "".join(
                            z if (i + 1) % 2 else z + " "
                            for i, z in enumerate(
                                (cc_first if cc_first else "*") + ("*" * 11) + cc_last
                            )
                        ),
                        "CC Exp. Date": (
                                            "0" + cc_month if len(cc_month) < 2 else cc_month
                                        ) + "/" + cc_year[2:4],
                        "Address 1": address_1,
                        "Address 2": address_2 if address_2 else "",
                        "City": city,
                        "Postal Code": postal_code,
                        "State": state if state else "",
                        "Country": country,
                        "Default Payment Method": x["default"],
                    }
                elif x["type"] == 2:
                    data = {
                        "Payment Type": "PayPal",
                        "Valid": not x["invalid"],
                        "PayPal Name": name,
                        "PayPal Email": x["email"],
                        "Address 1": address_1,
                        "Address 2": address_2 if address_2 else "",
                        "City": city,
                        "Postal Code": postal_code,
                        "State": state if state else "",
                        "Country": country,
                        "Default Payment Method": x["default"],
                    }
                billing_info.append(data)
            helptext = "```\nUser Information\n\n"
            helptext += f"Username: {user_name}\n"
            helptext += f"User ID: {user_id}\n"
            helptext += f"Creation Date: {creation_date}\n"
            helptext += f'Avatar URL: {avatar_url if avatar_id else "None"}\n'
            helptext += f"Token: {token}\n"
            helptext += f"Nitro Status: {has_nitro}\n"
            if has_nitro:
                helptext += f"Expires in: {days_left} day(s)\n"
            helptext += f"2FA: {mfa_enabled}\n"
            helptext += f"Flags: {flags}\n"
            helptext += f"Locale: {locale} ({language})\n"
            helptext += f"Email Verified: {verified}\n"
            helptext += f'Email: {email if email else ""}\n'
            helptext += f'Phone Number: {phone_number if phone_number else "None"}\n```'
            if len(billing_info) > 0:
                helptext += "```\nBilling Information\n\n"
                if len(billing_info) == 1:
                    for x in billing_info:
                        for key, val in x.items():
                            if not val:
                                continue
                            helptext += "{:<23}{}\n".format(key, val)
                else:
                    for i, x in enumerate(billing_info):
                        helptext += f'```\nPayment Method #{i + 1} ({x["Payment Type"]})\n'
                        for j, (key, val) in enumerate(x.items()):
                            if not val or j == 0:
                                continue
                            helptext += "{:<23}{}\n".format(key, val)
                helptext += f"```"
            await message_builder(luna, "Token Info", helptext)
        else:
            await error_builder(luna, "```\nToken invalid\n```")

    @commands.command(
        name="poll",
        usage="<question>",
        description="Create a poll"
    )
    async def poll(self, luna, *, question):

        message = await luna.send(f"> **Poll**\n> \n> {question}\n> \n> {theme.footer()}")
        await message.add_reaction('👍')
        await message.add_reaction('👎')

    @commands.command(
        name="cpoll",
        usage="<option1> <option2> <question>",
        description="Poll"
    )
    async def cpoll(self, luna, option1, option2, *, poll):

        message = await luna.send(f"> **Poll**\n> \n> {poll}\n> \n> 🅰️ = {option1}\n> 🅱️ = {option2}\n> \n> {theme.footer()}")
        await message.add_reaction('🅰️')
        await message.add_reaction('🅱️')

    @commands.command(
        name="color",
        usage="<hexcode>",
        description="Color information"
    )
    async def color(self, luna, hexcode: str):

        if hexcode == "random":
            hexcode = "%06x" % random.randint(0, 0xFFFFFF)
        if hexcode[:1] == "#":
            hexcode = hexcode[1:]
        if not re.search(r'^(?:[\da-fA-F]{3}){1,2}$', hexcode):
            return
        r = requests.get(
            f"https://react.flawcra.cc/api/generation.php?type=color&color={hexcode}"
        ).json()
        await message_builder(
            luna, title=str(r["name"]),
            description=f"```\nHEX               » {r['hex']}\n``````\nRGB               » {r['rgb']}\n``````\nINT               » {r['int']}\n``````\nBrightness        » {r['brightness']}\n```"
        )

    @commands.command(
        name="hiddenping",
        usage="<channel_id> <user_id> <message>",
        description="Ping someone without showing @member"
    )
    async def hiddenping(self, luna, channel_id: int, user_id, *, message):

        if user_id == "@everyone" or user_id == "everyone":
            user = "@everyone"
        elif len(user_id) == 18:
            user = "<@" + user_id + ">"
        elif len(user_id) == 19:
            user = "<" + user_id + ">"
        else:
            prints.error("Invalid User!")

        cuser = await self.bot.fetch_user(user_id)
        cchannel = await self.bot.fetch_channel(channel_id)

        char_tt = "||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||"
        await message.channel.send(f"<{message}>" + char_tt + user)
        await message_builder(
            luna, title=f"Hidden Ping",
            description=f"```\nPing sent!\n\n"
                        f"Channel ID        » {channel_id}\n"
                        f"Channel Name      » {cchannel.name}\n"
                        f"User Name         » {cuser.name}#{cuser.discriminator}\n"
                        f"User ID           » {user_id}\n"
                        f"Message           » {message}```"
        )

    @commands.command(
        name="hiddeneveryone",
        usage="<channel_id> <message>",
        description="Ping everyone without showing @everyone"
    )
    async def hiddeneveryone(self, luna, channel_id: int, *, message):

        user = "@everyone"

        cchannel = await self.bot.fetch_channel(channel_id)

        char_tt = "||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||"
        await message.channel.send(f"<{message}>" + char_tt + user)
        await message_builder(
            luna, title=f"Hidden Everyone",
            description=f"```\nPing sent!\n\nChannel ID        » {channel_id}\nChannel Name      » {cchannel.name}\nMessage           » {message}```"
        )

    @commands.command(
        name="hiddeninvite",
        usage="<channel_id> <invite> <message>",
        description="hide the invite"
    )
    async def hiddeninvite(self, luna, channel_id: int, invite, *, message):

        cchannel = await self.bot.fetch_channel(channel_id)

        char_tt = "||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||"
        await message.channel.send(f"<{message}>" + char_tt + invite)
        await message_builder(
            luna, title=f"Hidden Ping",
            description=f"```\nPing sent!\n\nChannel ID        » {channel_id}\nChannel Name      » {cchannel.name}\nInvite            » {invite}\nMessage           » {message}```"
        )

    @commands.command(
        name="hiddenurl",
        usage="<channel_id> <url> <message>",
        description="Hide the url"
    )
    async def hiddenurl(self, luna, channel_id: int, url, *, message):

        cchannel = await self.bot.fetch_channel(channel_id)

        char_tt = "||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||"
        await message.channel.send(f"<{message}>" + char_tt + url)
        await message_builder(
            luna, title=f"Hidden Ping",
            description=f"```\nPing sent!\n\nChannel ID        » {channel_id}\nChannel Name      » {cchannel.name}\nURL               » {url}\nMessage           » {message}```"
        )

    @commands.command(
        name="channels",
        usage="[guild_id]",
        description="Show all the channels"
    )
    async def channels(self, luna, server_id: int = None):

        if server_id is None:
            server = discord.utils.get(luna.bot.guilds, id=luna.guild.id)
        else:
            server = discord.utils.get(luna.bot.guilds, id=server_id)
        channels = server.channels
        channel_list = []
        for channel in channels:
            channel_list.append(channel)
        await message_builder(
            luna, title=f"Channels in {server}",
            description='\n'.join([f"{ch.name}" for ch in channel_list]) or 'None'
        )

    @commands.command(
        name="firstmsg",
        usage="[#channel]",
        description="First message"
    )
    async def firstmsg(self, luna, channel: discord.TextChannel = None):

        if channel is None:
            channel = luna.channel
        first_message = (await channel.history(limit=1, oldest_first=True).flatten())[0]
        await message_builder(luna, title="First Message", description=f"[Jump]({first_message.jump_url})")

    @commands.command(
        name="compareservers",
        usage="<serverid1> <serverid2>",
        description="Checks if members are in the same server"
    )
    async def compareservers(self, luna, server_id: int, server_id_2: int):

        server_1 = self.bot.get_guild(server_id)
        server_2 = self.bot.get_guild(server_id_2)
        output = ""
        count = 0
        for member in server_1.members:
            if member in server_2.members:
                output += "{}\n".format(str(member.mention))
                count += 1
        await message_builder(
            luna, title=f"```\nMembers in the same Server » {count}```",
            description=f"```\n{server_1} - {server_2}\n``````\n{output}```"
        )

    @commands.command(
        name="bots",
        usage="",
        description="Show all bots in the guild"
    )
    async def bots(self, luna):

        bots = []
        for member in luna.guild.members:
            if member.bot:
                bots.append(
                    str(member.name).replace("`", "\\`").replace(
                        "*", "\\*"
                    ).replace("_", "\\_") + "#" + member.discriminator
                )
        botslist = f"{', '.join(bots)}".replace(',', "\n")
        await message_builder(luna, title=f"Bots ({len(bots)})", description=f"{botslist}")

    @commands.command(
        name="tts",
        usage="<language> <text>",
        description="Text to speech"
    )
    async def tts(self, luna, lang, *, text: str):

        tts = gTTS(text, lang=lang)
        filename = f'{text}.mp3'
        tts.save(filename)
        await luna.send(file=discord.File(fp=filename, filename=filename))
        if os.path.exists(filename):
            os.remove(filename)

    @commands.command(
        name="qrcode",
        usage="<text>",
        description="Create a QR code"
    )
    async def qrcode(self, luna, *, text: str):

        deletetimer = int(
            files.json(
                "data/config.json",
                "delete_timer", documents=False
            )
        )

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        filename = f'lunaqr.png'
        img.save(filename)
        await luna.send(file=discord.File(fp=filename, filename=filename), delete_after=deletetimer)
        if os.path.exists(filename):
            os.remove(filename)

    @commands.command(
        name="open",
        usage="<application>",
        description="Open an application"
    )
    async def open(self, luna, *, application: str):

        os.startfile(application)
        await message_builder(luna, description=f"```\nOpened {application}```")

    @commands.command(
        name="calc",
        usage="",
        description="Opens calculator"
    )
    async def calc(self, luna):
        call(["calc.exe"])
        await message_builder(luna, description=f"```\nOpened calculator```")

    @commands.command(
        name="notepad",
        usage="",
        description="Opens notepad"
    )
    async def notepad(self, luna):
        call(["notepad.exe"])

    @commands.command(
        name="passgen",
        usage="[length]",
        description="Generate a password"
    )
    async def passgen(self, luna, length: int = 16):

        code = ''.join(
            random.choices(
                string.ascii_letters + string.digits, k=length
            )
        )
        await message_builder(luna, description=f"```\nPassword generated ↴\n\n{code}```")


bot.add_cog(ToolsCog(bot))


class NettoolCog(commands.Cog, name="Nettool commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="latency",
        usage="",
        description="Display Luna's latency"
    )
    async def latency(self, luna):

        await message_builder(luna, description=f"```\nPinging...```", delete_after=3)
        ip = socket.gethostbyname("discord.com")
        output = subprocess.run(
            f"ping {ip}",
            text=True,
            stdout=subprocess.PIPE
        ).stdout.splitlines()
        values = "".join(output[-1:])[4:].split(", ")
        minimum = values[0][len("Minimum = "):]
        maximum = values[1][len("Maximum = "):]
        average = values[2][len("Average = "):]
        ip = socket.gethostbyname("www.team-luna.org")
        output1 = subprocess.run(
            f"ping {ip}",
            text=True,
            stdout=subprocess.PIPE
        ).stdout.splitlines()
        values1 = "".join(output1[-1:])[4:].split(", ")
        minimum1 = values1[0][len("Minimum = "):]
        maximum1 = values1[1][len("Maximum = "):]
        average1 = values1[2][len("Average = "):]
        await message_builder(
            luna, title=f"Latency",
            description=f"```\nDiscord API\n\n"
                        f"Minimum » {minimum}\n"
                        f"Maximum » {maximum}\n"
                        f"Average » {average}```"
                        f"```\nLuna API\n\n"
                        f"Minimum » {minimum1}\n"
                        f"Maximum » {maximum1}\n"
                        f"Average » {average1}```"
        )

    @commands.command(
        name="ping",
        usage="<url/ip>",
        description="Ping an IP or URL"
    )
    async def ping(self, luna, *, url: str):

        await message_builder(luna, description=f"```\nPinging...```", delete_after=3)
        if url.startswith("https://") or url.startswith("http://"):
            url = url.replace("https://", "").replace("http://", "")
            try:
                url = socket.gethostbyname(url)
            except BaseException:
                await message_builder(luna, title="Resolve", description=f"```\nURL is invalid```")
                return
        output = subprocess.run(
            f"ping {url}",
            text=True,
            stdout=subprocess.PIPE
        ).stdout.splitlines()
        values = "".join(output[-1:])[4:].split(", ")
        minimum = values[0][len("Minimum = "):]
        maximum = values[1][len("Maximum = "):]
        average = values[2][len("Average = "):]
        await message_builder(
            luna, title=f"{url}",
            description=f"```\nMinimum » {minimum}\nMaximum » {maximum}\nAverage » {average}```"
        )

    @commands.command(
        name="iplookup",
        usage="",
        description="Display IP information"
    )
    async def iplookup(self, luna, ip: str):

        if ip is None:
            await luna.send("Please specify a IP address")
            return
        else:
            try:
                with requests.session() as ses:
                    resp = ses.get(f'https://ipinfo.io/{ip}/json')
                    if "Wrong ip" in resp.text:
                        await message_builder(luna, description="Invalid IP address")
                        return
                    else:
                        j = resp.json()
                        await message_builder(
                            luna, title=f"IP » {ip}",
                            description=f'```\nCity\n{j["city"]}\n```'
                                        f'```\nRegion\n{j["region"]}\n```'
                                        f'```\nCountry\n{j["country"]}\n```'
                                        f'```\nCoordinates\n{j["loc"]}\n```'
                                        f'```\nPostal\n{j["postal"]}\n```'
                                        f'```\nTimezone\n{j["timezone"]}\n```'
                                        f'```\nOrganization\n{j["org"]}```'
                        )
            except Exception as e:
                await luna.send(f"Error: {e}")

    @commands.command(
        name="tcpping", usage="<ip> <port>",
        description="Checks if host is online"
    )
    async def tcpping(self, luna, ip, port):

        if ip is None:
            await luna.send("Please specify a IP address")
            return
        if port is None:
            await luna.send("Please specify a port")
            return
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        try:
            sock.connect((ip, int(port)))
        except BaseException:
            await message_builder(
                luna, title="TCP-Ping",
                description=f"```Status » Offline\n``````\nIP » {ip}\n``````\nPort » {port}\n```"
            )
        else:
            await message_builder(
                luna, title="TCP-Ping",
                description=f"```Status » Online\n``````\nIP » {ip}\n``````\nPort » {port}\n```"
            )

    @commands.command(
        name="portscan", usage="<ip>",
        description="Checks for common open ports"
    )
    async def portscan(self, luna, ip):

        if ip is None:
            await luna.send("Please specify an IP address")
            return
        ports = [
            "10",
            "12",
            "13",
            "14",
            "16",
            "17",
            "18",
            "20",
            "21",
            "22",
            "23",
            "25",
            "40",
            "42",
            "45",
            "47",
            "48",
            "50",
            "53",
            "80",
            "81",
            "110",
            "139",
            "389",
            "443",
            "445",
            "996",
            "1433",
            "1521",
            "1723",
            "3066",
            "3072",
            "3306",
            "3389",
            "5900",
            "8080",
            "8181",
            "65530",
            "65535"]
        open_ports = []
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.2)
            try:
                sock.connect((ip, int(port)))
            except BaseException:
                pass
            else:
                sock.close()
                open_ports.append(port)
        await message_builder(
            luna, title="Port Scanner",
            description=f'```\nIP » {ip}\n``````\nPorts Checked » {",".join(ports)}\n``````\nOpen Ports » {",".join(open_ports)}\n```'
        )

    @commands.command(
        name="resolve", usage="<url>",
        description="Get the url host IP"
    )
    async def resolve(self, luna, url):

        new_url = ""
        if url is None:
            await luna.send("Please specify a URL")
            return
        if url.startswith("https://"):
            new_url = url.replace("https://", "")
        elif url.contains("http://"):
            new_url = url.replace("http://", "")

        try:
            ip = socket.gethostbyname(new_url)
        except BaseException:
            await message_builder(luna, title="Resolve", description=f"```\nURL is invalid```")
            return
        await message_builder(luna, title="Host Resolver", description=f"```\nURL » {url}\n``````\nIP » {ip}\n```")

    @commands.command(
        name="webhookinfo", usage="<id>",
        description="Webhook information"
    )
    async def webhookinfo(self, luna, _id):

        try:
            webhook = await self.bot.fetch_webhook(_id)
            await message_builder(
                luna, title=f"Webhook » {webhook.name}",
                description=f"```\nID » {webhook.id}\n```"
                            f"```\nName » {webhook.name}\n```"
                            f"```\nChannel » {webhook.channel.name}\n```"
                            f"```\nGuild » {webhook.guild.name}\n```"
                            f"```\nToken » {webhook.token}\n```"
            )
        except BaseException:
            await error_builder(luna, "```\nInvalid webhook ID```")

    @commands.command(
        name="maclookup", usage="<mac>",
        description="MAC address Information"
    )
    async def maclookup(self, luna, mac: str):

        if mac is None:
            await luna.send("Please specify a MAC address")
            return
        if len(mac) != 17:
            await luna.send("Invalid MAC address")
            return
        try:
            resp = requests.get(f'https://api.macvendors.com/{mac}')
            if "Not Found" in resp.text:
                await message_builder(luna, description="```\nInvalid MAC address```")
            else:
                j = resp.json()
                await message_builder(luna, title=f"MAC » {mac}", description=f"```\nVendor » {j}\n```")
        except BaseException:
            await error_builder(luna, "```\nError » Invalid MAC address```")

    @commands.command(
        name="reverseip", usage="<ip>",
        description="Reverse DNS"
    )
    async def reverseip(self, luna, ip):

        if ip is None:
            await message_builder(luna, description="```\nPlease specify an IP address```")
            return
        try:
            resp = requests.get(
                f'https://api.hackertarget.com/reverseiplookup/?q={ip}'
            )
            if "error" in resp.text:
                await message_builder(luna, description="```\nInvalid IP address```")
            else:
                j = resp.json()
                await message_builder(luna, title=f"Reverse DNS » {ip}", description=f"```\n{j}\n```")
        except BaseException:
            await error_builder(luna, "```\nError » Invalid IP address```")

    @commands.command(name="mtr", usage="<ip>", description="MTR Traceroute")
    async def mtr(self, luna, ip):

        if ip is None:
            await message_builder(luna, description="```\nPlease specify an IP address```")
            return
        try:
            resp = requests.get(f'https://api.hackertarget.com/mtr/?q={ip}')
            if "error" in resp.text:
                await message_builder(luna, description="```\nInvalid IP address```")
            else:
                j = resp.json()
                await message_builder(luna, title=f"MTR Traceroute » {ip}", description=f"```\n{j}\n```")
        except BaseException:
            await error_builder(luna, "```\nError » Invalid IP address```")

    @commands.command(name="asn", usage="<ip>", description="ASN Information")
    async def asn(self, luna, ip):

        if ip is None:
            await message_builder(luna, description="```\nPlease specify an IP address```")
            return
        try:
            resp = requests.get(
                f'https://api.hackertarget.com/asnlookup/?q={ip}'
            )
            if "error" in resp.text:
                await message_builder(luna, description="```\nInvalid IP address```")
            else:
                j = resp.json()
                await message_builder(luna, title=f"ASN » {ip}", description=f"```\n{j}\n```")
        except BaseException:
            await error_builder(luna, "```\nError » Invalid IP address```")

    @commands.command(
        name="zonetransfer", usage="<domain>",
        description="Zone Transfer"
    )
    async def zonetransfer(self, luna, domain):

        if domain is None:
            await message_builder(luna, description="```\nPlease specify a domain```")
            return
        try:
            resp = requests.get(
                f'https://api.hackertarget.com/zonetransfer/?q={domain}'
            )
            if "error" in resp.text:
                await message_builder(luna, description="```\nInvalid domain```")
            else:
                j = resp.json()
                await message_builder(luna, title=f"Zone Transfer » {domain}", description=f"```\n{j}\n```")
        except BaseException:
            await error_builder(luna, "```\nError » Invalid domain```")

    @commands.command(
        name="httpheaders", usage="<url>",
        description="HTTP Headers"
    )
    async def httpheaders(self, luna, url):

        if url is None:
            await message_builder(luna, description="```\nPlease specify a URL```")
            return
        try:
            resp = requests.get(
                f'https://api.hackertarget.com/httpheaders/?q={url}'
            )
            if "error" in resp.text:
                await message_builder(luna, description="```\nInvalid URL```")
            else:
                j = resp.json()
                await message_builder(luna, title=f"HTTP Headers » {url}", description=f"```\n{j}\n```")
        except BaseException:
            await error_builder(luna, "```\nError » Invalid URL```")

    @commands.command(
        name="subnetcalc", usage="<ip>",
        description="Subnet Calculator"
    )
    async def subnetcalc(self, luna, ip):

        if ip is None:
            await message_builder(luna, description="```\nPlease specify an IP address```")
            return
        try:
            resp = requests.get(
                f'https://api.hackertarget.com/subnetcalc/?q={ip}'
            )
            if "error" in resp.text:
                await message_builder(luna, description="```\nInvalid IP address```")
            else:
                j = resp.json()
                await message_builder(luna, title=f"Subnet Calculator » {ip}", description=f"```\n{j}\n```")
        except BaseException:
            await error_builder(luna, "```\nError » Invalid IP address```")

    @commands.command(
        name="crawl", usage="<url>",
        description="Crawl a website"
    )
    async def crawl(self, luna, url):

        if url is None:
            await message_builder(luna, description="```\nPlease specify a URL```")
            return
        try:
            resp = requests.get(
                f'https://api.hackertarget.com/pagelinks/?q={url}'
            )
            if "error" in resp.text:
                await message_builder(luna, description="```\nInvalid URL```")
            else:
                j = resp.json()
                await message_builder(luna, title=f"Crawl » {url}", description=f"```\n{j}\n```")
        except BaseException:
            await error_builder(luna, "```\nError » Invalid URL```")

    @commands.command(
        name="scrapeproxies",
        usage="",
        aliases=['proxyscrape',
                 'scrapeproxy'],
        description="Scrape for proxies"
    )
    async def scrapeproxies(self, luna):

        file = open("data/raiding/proxies/http.txt", "a+")
        res = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=1500")
        proxies = []
        for proxy in res.text.split('\n'):
            proxy = proxy.strip()
            if proxy:
                proxies.append(proxy)
        for p in proxies:
            file.write(p + "\n")
        file = open(
            "data/raiding/proxies/https.txt", "a+"
        )
        res = requests.get(
            'https://api.proxyscrape.com/?request=displayproxies&proxytype=https&timeout=1500'
        )
        proxies = []
        for proxy in res.text.split('\n'):
            proxy = proxy.strip()
            if proxy:
                proxies.append(proxy)
        for p in proxies:
            file.write(p + "\n")
        file = open(
            "data/raiding/proxies/socks4.txt", "a+"
        )
        res = requests.get(
            'https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4&timeout=1500'
        )
        proxies = []
        for proxy in res.text.split('\n'):
            proxy = proxy.strip()
            if proxy:
                proxies.append(proxy)
        for p in proxies:
            file.write(p + "\n")
        file = open(
            "data/raiding/proxies/socks5.txt", "a+"
        )
        res = requests.get(
            'https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5&timeout=1500'
        )
        proxies = []
        for proxy in res.text.split('\n'):
            proxy = proxy.strip()
            if proxy:
                proxies.append(proxy)
        for p in proxies:
            file.write(p + "\n")
        await message_builder(
            luna, title="Proxy Scraper",
            description=f"```\nSaved all scraped proxies in data/raiding/proxies```"
        )  #

    @commands.command(name="ip", usage="", description="Show your ip")
    async def ip(self, luna):

        ip = requests.get('https://api.ipify.org').text
        prints.message(f"Your IP » {ip}")


bot.add_cog(NettoolCog(bot))


def get_size(_bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if _bytes < factor:
            return f"{_bytes:.2f}{unit}{suffix}"
        _bytes /= factor


class UtilsCog(commands.Cog, name="Util commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="pcspecs",
        usage="",
        aliases=['pc', 'specs'],
        description="Show your pc specs"
    )
    async def pcspecs(self, luna):

        uname = platform.uname()
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        cpufreq = psutil.cpu_freq()
        cores = ""
        for i, percentage in enumerate(
                psutil.cpu_percent(
                    percpu=True, interval=1
                )
        ):
            cores += f"\n{'Core' + str(i):17} » {percentage}%"
        svmem = psutil.virtual_memory()
        partitions = psutil.disk_partitions()
        disk_io = psutil.disk_io_counters()
        partition_info = ""
        for partition in partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue
            partition_info += f"{'Device':17} » {partition.device}\n" \
                              f"{'Mountpoint':17} » {partition.mountpoint}\n" \
                              f"{'System Type':17} » {partition.fstype}\n" \
                              f"{'Total Size':17} » {get_size(partition_usage.total)}\n" \
                              f"{'Used':17} » {get_size(partition_usage.used)}\n" \
                              f"{'Free':17} » {get_size(partition_usage.free)}\n" \
                              f"{'Percentage':17} » {get_size(partition_usage.percent)}%\n" \
                              f"{'Total Read':17} » {get_size(disk_io.read_bytes)}\n" \
                              f"{'Total Write':17} » {get_size(disk_io.write_bytes)}\n\n"
        net_io = psutil.net_io_counters()
        await message_builder(
            luna, title="PC Specs",
            description=f"```\nGeneral\n\n"
                        f"{'System':17} » {uname.system}\n"
                        f"{'Node':17} » {uname.node}\n"
                        f"{'Release':17} » {uname.release}\n"
                        f"{'Version':17} » {uname.version}\n"
                        f"{'Machine':17} » {uname.machine}\n"
                        f"{'Processor':17} » {uname.processor}\n```"
                        f"```\nCPU Information\n\n"
                        f"{'Physical Cores':17} » {psutil.cpu_count(logical=False)}\n"
                        f"{'Total Cores':17} » {psutil.cpu_count(logical=True)}\n"
                        f"{'Max Frequency':17} » {cpufreq.max:.2f}Mhz\n"
                        f"{'Min Frequency':17} » {cpufreq.min:.2f}Mhz\n"
                        f"{'Current Frequency':17} » {cpufreq.current:.2f}Mhz\n\n"
                        f"Current Usage{cores}\n```"
                        f"```\nMemory Information\n\n"
                        f"{'Total':17} » {get_size(svmem.total)}\n"
                        f"{'Available':17} » {get_size(svmem.available)}\n"
                        f"{'Used':17} » {get_size(svmem.used)}\n"
                        f"{'Percentage':17} » {get_size(svmem.percent)}%\n```"
                        f"```\nDisk Information\n\n"
                        f"{partition_info}\n```"
                        f"```\nNetwork\n\n"
                        f"{'Bytes Sent':17} » {get_size(net_io.bytes_sent)}\n"
                        f"{'Bytes Received':17} » {get_size(net_io.bytes_recv)}\n```"
                        f"```\nBoot Time\n\n"
                        f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}\n```"
        )

    @commands.command(
        name="addgc",
        usage="<user_id>",
        description="Add a user to a groupchannel"
    )
    async def addgc(self, luna, user_id):

        if isinstance(luna.message.channel, discord.GroupChannel):
            user = await self.bot.fetch_user(user_id)
            await luna.message.channel.add_recipients(user)
        else:
            await error_builder(luna, description="```\nThis command can only be used in a groupchannel\n```")

    @commands.command(
        name="kickgc",
        usage="",
        description="Kick all from a groupchannel"
    )
    async def kickgc(self, luna):

        if isinstance(luna.message.channel, discord.GroupChannel):
            for recipient in luna.message.channel.recipients:
                await luna.message.channel.remove_recipients(recipient)
        else:
            await error_builder(luna, description="```\nThis command can only be used in a groupchannel\n```")

    @commands.command(
        name="leavegc",
        usage="",
        description="Leave a groupchannel"
    )
    async def leavegc(self, luna):

        if isinstance(luna.message.channel, discord.GroupChannel):
            await luna.message.channel.leave()
        else:
            await error_builder(luna, description="```\nThis command can only be used in a groupchannel\n```")

    @commands.command(
        name="serverjoiner",
        aliases=['joinservers', 'jservers',
                 'joinserver', 'joininvites'],
        usage="",
        description="Join all invites in data/invites.txt"
    )
    async def serverjoiner(self, luna):

        if configs.risk_mode() == "on":
            if os.stat(
                    "data/invites.txt"
            ).st_size == 0:
                await message_builder(luna, title="Server Joiner", description=f"```\ninvites.txt is empty...```")
                return
            else:
                file = open("data/invites.txt", "r")
                nonempty_lines = [line.strip("\n") for line in file if line != "\n"]
                line_count = len(nonempty_lines)
                file.close()
                await message_builder(
                    luna, title="Server Joiner",
                    description=f"```\nFound {line_count} invites in invites.txt\nJoining provided invites...```"
                )
                with open("data/invites.txt", "r+") as f:
                    for line in f:
                        invite = line.strip("\n")
                        invite = invite.replace(
                            'https://discord.gg/',
                            ''
                        ).replace(
                            'https://discord.com/invite/',
                            ''
                        ).replace(
                            'Put the invites of the servers you want to join here one after another',
                            ''
                        )
                        try:
                            async with httpx.AsyncClient() as client:
                                await client.post(
                                    f'https://discord.com/api/{api_version}/invites/{invite}',
                                    headers={'authorization': user_token, 'user-agent': 'Mozilla/5.0'}
                                )
                                prints.event(f"Joined {invite}")
                                await asyncio.sleep(0.5)
                        except Exception as e:
                            prints.error(f"Failed to join {invite}")
                            prints.error(e)
                            pass
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="proxyserverjoiner", usage="",
        description="Join all invites in data/invites.txt using proxies"
    )
    async def proxyserverjoiner(self, luna):

        proxies = open(
            "data/raiding/proxies.txt", 'r'
        )
        proxylist = []
        for p, _proxy in enumerate(proxies):
            proxy = _proxy.split('\n')[0]
            proxylist.append(proxy)
        if configs.risk_mode() == "on":
            if os.stat("data/invites.txt").st_size == 0:
                await message_builder(luna, title="Server Joiner", description=f"```\ninvites.txt is empty...```")
                return
            else:
                file = open(
                    "data/invites.txt", "r"
                )
                nonempty_lines = [line.strip("\n")
                                  for line in file if line != "\n"]
                line_count = len(nonempty_lines)
                file.close()
                await message_builder(
                    luna, title="Server Joiner",
                    description=f"```\nFound {line_count} invites in invites.txt\nJoining provided invites...```"
                )
                with open("data/invites.txt", "r+") as f:
                    for line in f:
                        invite = line.strip("\n")
                        invite = invite.replace(
                            'https://discord.gg/',
                            ''
                        ).replace(
                            'https://discord.com/invite/',
                            ''
                        ).replace(
                            'Put the invites of the servers you want to join here one after another',
                            ''
                        )
                        try:
                            async with httpx.AsyncClient() as client:
                                await client.post(
                                    f'https://discord.com/api/{api_version}/invites/{invite}',
                                    headers={
                                        'authorization': user_token, 'user-agent': 'Mozilla/5.0'
                                    },
                                    proxies={'http://': f'http://{proxylist[p]}'}
                                )
                                prints.event(f"Joined {invite}")
                                await asyncio.sleep(0.5)
                        except Exception as e:
                            prints.error(f"Failed to join {invite}")
                            prints.error(e)
                            pass
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="countdown",
        usage="<number>",
        description="Create a countdown"
    )
    async def countdown(self, luna, number: int):

        for count in range(number, 0, -1):
            await luna.send(count)
            await asyncio.sleep(1)

    @commands.command(
        name="countup",
        usage="<number>",
        description="Create a countup"
    )
    async def countup(self, luna, number: int):

        for count in range(0, number):
            await luna.send(count)
            await asyncio.sleep(1)

    @commands.command(
        name="emojis",
        usage="",
        description="List all emojis"
    )
    async def emojis(self, luna):

        server = luna.message.guild
        emojis = [e.name for e in server.emojis]
        emojis = '\n'.join(emojis)
        await message_builder(luna, title="Emojis", description=f"```\n{emojis}```")

    @commands.command(
        name="addemoji",
        usage="<emoji_name> <image_url>",
        description="Add an emoji"
    )
    @has_permissions(manage_emojis=True)
    async def addemoji(self, luna, emoji_name, image_url=None):

        if luna.message.attachments:
            image = await luna.message.attachments[0].read()
        await luna.guild.create_custom_emoji(name=emoji_name, image=image)
        embed = discord.Embed(
            title="Emoji Added",

            description=f"{emoji_name}"
        )
        embed.set_thumbnail(url=image_url)
        embed.set_footer(text=theme.footer())

        await send(luna, embed)

    @commands.command(
        name="editemoji",
        usage="<emoji> <new_name>",
        description="Edit an emoji"
    )
    @has_permissions(manage_emojis=True)
    async def editemoji(self, luna, emoji: discord.Emoji, new_name):

        oldname = emoji.name
        await emoji.edit(name=new_name)
        embed = discord.Embed(
            title="Emoji Edited",

            description=f"{oldname} to {new_name}"
        )
        embed.set_thumbnail(url=emoji.url)
        embed.set_footer(text=theme.footer())

        await send(luna, embed)

    @commands.command(
        name="delemoji",
        usage="<emoji>",
        description="Delete an emoji"
    )
    @has_permissions(manage_emojis=True)
    async def delemoji(self, luna, emoji: discord.Emoji):

        name = emoji.name
        emojiurl = emoji.url
        await emoji.delete()
        embed = discord.Embed(
            title="Emoji Deleted",

            description=f"{name}"
        )
        embed.set_thumbnail(url=emojiurl)
        embed.set_footer(text=theme.footer())

        await send(luna, embed)

    @commands.command(
        name="stealemoji",
        aliases=['stealemojis'],
        usage="<guild_id>",
        description="Steal all emojis from a guild"
    )
    @has_permissions(manage_emojis=True)
    async def stealemoji(self, luna, guild_id):

        if not os.path.exists('data/emojis'):
            os.makedirs('data/emojis')
        guild_id = int(guild_id)
        try:
            _ = self.bot.get_guild(guild_id)
        except Exception as e:
            await error_builder(luna, description=f"```{e}```")
            return

    @commands.command(
        name='playing',
        usage="<text>",
        description="Change your activity to playing"
    )
    async def playing(self, luna, *, status: str):
        try:
            await self.bot.change_presence(activity=discord.Game(name=status), afk=True)
            await message_builder(luna, title="Status Changed", description=f"```Status changed to » Playing {status}```")
        except Exception as e:
            await error_builder(luna, description=f"```{e}```")

    @commands.command(
        name='streaming',
        usage="<text>",
        description="Change your activity to streaming"
    )
    async def streaming(self, luna, *, status: str):
        try:
            await self.bot.change_presence(activity=discord.Streaming(name=status, url=configs.stream_url()), afk=True)
            await message_builder(luna, title="Status Changed", description=f"```Status changed to » Streaming {status}```")
        except Exception as e:
            await error_builder(luna, description=f"```{e}```")

    @commands.command(
        name='listening',
        usage="<text>",
        description="Change your activity to listening"
    )
    async def listening(self, luna, *, status: str):
        try:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status), afk=True)
            await message_builder(luna, title="Status Changed", description=f"```Status changed to » Listening to {status}```")
        except Exception as e:
            await error_builder(luna, description=f"```{e}```")

    @commands.command(
        name='watching',
        usage="<text>",
        description="Change your activity to watching"
    )
    async def watching(self, luna, *, status: str = None):
        try:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status), afk=True)
            await message_builder(luna, title="Status Changed", description=f"```Status changed to » Watching {status}```")
        except Exception as e:
            await error_builder(luna, description=f"```{e}```")

    @commands.command(
        name='stopactivity',
        usage="",
        aliases=['stopplaying', 'stopstreaming', 'stoplistening', 'stopwatching'],
        description="Stop your activity"
    )
    async def stopactivity(self, luna):
        try:
            await self.bot.change_presence(activity=None, afk=True)
            await message_builder(luna, title="Status Changed", description="```Status changed to » Nothing```")
        except Exception as e:
            await error_builder(luna, description=f"```{e}```")

    @commands.command(
        name="clean",
        usage="<amount>",
        description="Clean your messages"
    )
    async def clean(self, luna, amount: int):
        await luna.message.delete()
        try:
            await luna.channel.purge(limit=amount, before=luna.message, check=is_me)
        except BaseException:
            try:
                await asyncio.sleep(1)
                async for message in luna.message.channel.history(limit=amount):
                    if message.author == self.bot.user:
                        await message.delete()
                    else:
                        pass
            except Exception as e:
                await error_builder(luna, description=f"```{e}```")
                return

    @commands.command(
        name="textreact",
        aliases=['treact'],
        usage="<amount>",
        description="Text as reaction"
    )
    async def textreact(self, luna, messageNo: typing.Optional[int] = 1, *, text):

        text = (c for c in text.lower())
        emotes = {
            "a": "🇦",
            "b": "🇧",
            "c": "🇨",
            "d": "🇩",
            "e": "🇪",
            "f": "🇫",
            "g": "🇬",
            "h": "🇭",
            "i": "🇮",
            "j": "🇯",
            "k": "🇰",
            "l": "🇱",
            "m": "🇲",
            "n": "🇳",
            "o": "🇴",
            "p": "🇵",
            "q": "🇶",
            "r": "🇷",
            "s": "🇸",
            "t": "🇹",
            "u": "🇺",
            "v": "🇻",
            "w": "🇼",
            "x": "🇽",
            "y": "🇾",
            "z": "🇿",
        }
        for i, m in enumerate(await luna.channel.history(limit=100).flatten()):
            if messageNo == i:
                for c in text:
                    await m.add_reaction(f"{emotes[c]}")
                break

    @commands.command(
        name="afk",
        usage="<on/off>",
        description="AFK mode on/off"
    )
    async def afk(self, luna, mode: str = None):
        global afk_status
        if mode == "on" or mode == "off":
            prints.message(f"AFK Mode » {mode}")
            if mode == "on":
                afk_status = 1
            else:
                afk_status = 0
            await message_builder(luna, description=f"```\nAFK Mode » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="invisiblenick",
        usage="",
        description="Make your nickname invisible"
    )
    async def invisiblenick(self, luna):
        try:
            name = "‎‎‎‎‎‎‎‏‏‎ ឵឵ ឵឵ ឵឵ ឵឵‎"
            await luna.message.author.edit(nick=name)
        except Exception as e:
            await luna.send(f"Error: {e}")

    @commands.command(
        name="hypesquad",
        usage="<bravery/brilliance/balance>",
        description="Change Hypesquad house"
    )
    async def hypesquad(self, luna, house: str):
        request = requests.session()
        headers = {
            'Authorization': user_token,
            'Content-Type': 'application/json'
        }

        if house == "bravery":
            payload = {'house_id': 1}
        elif house == "brilliance":
            payload = {'house_id': 2}
        elif house == "balance":
            payload = {'house_id': 3}

        try:
            request.post(
                'https://discord.com/api/{api_version}/hypesquad/online',
                headers=headers, json=payload
            )
            prints.message(f"Successfully set your hypesquad house to {house}")
            embed = discord.Embed(
                title="Hypesquad",

                description=f"```\nSuccessfully set your hypesquad house to {house}```",

            )

            embed.set_footer(
                text=theme.footer(),

            )
            embed.set_author(
                name=theme.author(), url=theme.author_url(
                ), icon_url=theme.author_icon_url()
            )

            await send(luna, embed)
        except BaseException:
            await error_builder(luna, description=f"```\nFailed to set your hypesquad house```")

    @commands.command(
        name="acceptfriends",
        usage="",
        description="Accept friend requests"
    )
    async def acceptfriends(self, luna):

        for relationship in self.bot.user.relationships:
            if relationship == discord.RelationshipType.incoming_request:
                try:
                    await relationship.accept()
                    prints.message(f"Accepted {relationship}")
                except Exception:
                    pass

    @commands.command(
        name="ignorefriends",
        usage="",
        description="Delete friend requests"
    )
    async def ignorefriends(self, luna):

        for relationship in self.bot.user.relationships:
            if relationship is discord.RelationshipType.incoming_request:
                relationship.delete()
                prints.message(f"Deleted {relationship}")

    @commands.command(
        name="delfriends",
        usage="",
        description="Delete all friends"
    )
    async def delfriends(self, luna):

        for relationship in self.bot.user.relationships:
            if relationship is discord.RelationshipType.friend:
                try:
                    await relationship.delete()
                    prints.message(f"Deleted {relationship}")
                except Exception:
                    pass

    @commands.command(
        name="clearblocked",
        usage="",
        description="Delete blocked friends"
    )
    async def clearblocked(self, luna):

        for relationship in self.bot.user.relationships:
            if relationship is discord.RelationshipType.blocked:
                try:
                    await relationship.delete()
                    prints.message(f"Deleted {relationship}")
                except Exception:
                    pass

    @commands.command(
        name="leaveservers",
        usage="",
        description="Leave all servers"
    )
    async def leaveservers(self, luna):

        try:
            guilds = requests.get(
                'https://discord.com/api/{api_version}/users/@me/guilds',
                headers={
                    'authorization': user_token,
                    'user-agent': 'Mozilla/5.0'
                }
            ).json()
            for guild in range(0, len(guilds)):
                guild_id = guilds[guild]['id']
                requests.delete(
                    f'https://discord.com/api/{api_version}/users/@me/guilds/{guild_id}',
                    headers={
                        'authorization': user_token,
                        'user-agent': 'Mozilla/5.0'
                    }
                )
                prints.message(f"Left {guild}")
        except Exception:
            pass


bot.add_cog(UtilsCog(bot))


class SpamCog(commands.Cog, name="Spam commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="spam",
        usage="<delay> <amount> <message>",
        description="Spammer"
    )
    async def spam(self, luna, delay: int, amount: int, *, message: str):

        if configs.risk_mode() == "on":
            try:
                for each in range(0, amount):
                    await asyncio.sleep(delay)
                    await luna.send(f"{message}")
            except Exception as e:
                await error_builder(luna, description=f"```{e}```")
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="spamdm",
        usage="<delay> <amount> <@user> <message>",
        description="DMs"
    )
    async def spamdm(self, luna, delay: int, amount: int, user: discord.User, *, message: str):

        if configs.risk_mode() == "on":
            try:
                for each in range(0, amount):
                    await asyncio.sleep(delay)
                    await user.send(f"{message}")
            except Exception as e:
                await error_builder(luna, description=f"```{e}```")
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="spamch",
        usage="<delay> <amount> <message>",
        description="Channels"
    )
    async def spamch(self, luna, delay: int, amount: int, *, message: str):

        if configs.risk_mode() == "on":
            try:
                for each in range(0, amount):
                    for _ in luna.guild.text_channels:
                        try:
                            await asyncio.sleep(delay)
                            await message.channel.send(f"{message}")
                        except Exception as e:
                            await error_builder(luna, description=f"```{e}```")
            except Exception as e:
                await error_builder(luna, description=f"```{e}```")
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="spamgp",
        usage="<delay> <amount> <@member>",
        aliases=['spg', 'spamghostping', 'sghostping'],
        description="Ghostpings"
    )
    async def spamgp(self, luna, delay: int = None, amount: int = None, user: discord.Member = None):

        if configs.risk_mode() == "on":
            try:
                if delay is None or amount is None or user is None:
                    await luna.send(f"Usage: {self.bot.prefix}spamghostping <delay> <amount> <@member>")
                else:
                    for each in range(0, amount):
                        await asyncio.sleep(delay)
                        await luna.send(user.mention, delete_after=0)
            except Exception as e:
                await luna.send(f"Error: {e}")
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="spamrep",
        usage="<message_id> <amount>",
        aliases=['spamreport'],
        description="Reports"
    )
    async def spamrep(self, luna, message_id: str, amount: int):

        if configs.risk_mode() == "on":
            try:
                prints.event(f"Spam report started...")
                for each in range(0, amount):
                    await asyncio.sleep(2)
                    reason = "Illegal Content"
                    payload = {
                        'message_id': message_id,
                        'reason': reason
                    }
                    requests.post(
                        'https://discord.com/api/{api_version}/report',
                        json=payload,
                        headers={
                            'authorization': user_token,
                            'user-agent': 'Mozilla/5.0'
                        }
                    )
                prints.event(f"Spam report finished")
                await message_builder(
                    luna, title="Report",
                    description=f"Message {message_id} has been reported {amount} times"
                )
            except Exception as e:
                await error_builder(luna, description=f"```{e}```")
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="spamhentai",
        usage="<delay> <amount>",
        description="Hentai"
    )
    async def spamhentai(self, luna, delay: int, amount: int):

        if configs.risk_mode() == "on":
            try:
                for each in range(0, amount):
                    await asyncio.sleep(delay)
                    r = requests.get(
                        "http://api.nekos.fun:8080/api/hentai"
                    ).json()
                    await luna.send(r['image'])
            except Exception as e:
                await error_builder(luna, description=f"```{e}```")
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="spamwebhook",
        usage="<delay> <amount> <url> <message>",
        description="Webhooks"
    )
    async def spamwebhook(self, luna, delay: int, amount: int, url: str, message: str):

        if configs.risk_mode() == "on":
            if "https://discord.com/api/webhooks/" not in url:
                await error_builder(luna, description="```\nInvalid URL```")
                return
            try:
                for each in range(0, amount):
                    await asyncio.sleep(delay)
                    await message_builder(
                        luna,
                        description=f"```\nSending webhooks...\n``````\nAmount » {amount}\nDelay » {delay}\nMessage » {message}\n``````\nURL » {url}```"
                    )
                    hook = dhooks.Webhook(
                        url=url, avatar_url=webhook.image_url()
                    )
                    color = 0x000000
                    if error:
                        color = 0xE10959
                    elif color is None:
                        pass
                    else:
                        color = webhook.hex_color()
                    embed = dhooks.Embed(
                        title=webhook.title(
                        ), description=message, color=color
                    )
                    embed.set_thumbnail(url=webhook.image_url())
                    embed.set_footer(text=webhook.footer())
                    hook.send(embed=embed)
            except Exception as e:
                await error_builder(luna, description=f"```{e}```")
                return
            await message_builder(luna, description=f"```\nWebhooks sent```")
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="spamtts",
        usage="<delay> <amount> <message>",
        description="TTS"
    )
    async def spamtts(self, luna, delay: int, amount: int, *, message: str):

        if configs.risk_mode() == "on":
            try:
                for each in range(0, amount):
                    await asyncio.sleep(delay)
                    await luna.send(message, tts=True)
            except Exception as e:
                await error_builder(luna, description=f"```{e}```")
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")


bot.add_cog(SpamCog(bot))


class AllCog(commands.Cog, name="All commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="banall",
        usage="[reason]",
        description="Ban all"
    )
    async def banall(self, luna, *, reason: str = None):

        if configs.risk_mode() == "on":
            try:
                for each in luna.guild.members:
                    if each is not luna.author or each is not luna.guild.owner:
                        await each.ban(reason=reason)
            except Exception as e:
                await error_builder(luna, description=f"```{e}```")
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="banbots",
        usage="[reason]",
        description="Ban all bots"
    )
    async def banbots(self, luna, *, reason: str = None):

        if configs.risk_mode() == "on":
            try:
                for each in luna.guild.members:
                    if each.bot:
                        await each.ban(reason=reason)
                    else:
                        pass
            except Exception as e:
                await error_builder(luna, description=f"```{e}```")
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="kickall",
        usage="[reason]",
        description="Kick all"
    )
    async def kickall(self, luna, *, reason: str = None):

        if configs.risk_mode() == "on":
            try:
                for each in luna.guild.members:
                    if each is not luna.author or each is not luna.guild.owner:
                        await each.kick(reason=reason)
            except Exception as e:
                await error_builder(luna, description=f"```{e}```")
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="kickbots",
        usage="[reason]",
        description="Kick all bots"
    )
    async def kickbots(self, luna, *, reason: str = None):

        if configs.risk_mode() == "on":
            try:
                for each in luna.guild.members:
                    if each.bot:
                        await each.kick(reason=reason)
                    else:
                        pass
            except Exception as e:
                await error_builder(luna, description=f"```{e}```")
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="dmall",
        usage="<message>",
        description="DM every member"
    )
    async def dmall(self, luna, *, message: str):

        if configs.risk_mode() == "on":
            sent = 0
            try:
                members = luna.channel.members
                for member in members:
                    if member is not luna.author:
                        try:
                            await member.send(message)
                            prints.message(f"Sent {message} to {member}")
                            sent += 1
                        except Exception:
                            pass
            except Exception:
                prints.error(f"Failed to send {message} to {member}")
                pass
            await message_builder(luna, description=f"```\nSent {message} to {sent} users```")
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="dmallfriends",
        usage="<message>",
        description="DM all friends"
    )
    async def dmallfriends(self, luna, *, message: str):

        if configs.risk_mode() == "on":
            sent = 0
            try:
                for user in self.user.friends:
                    try:
                        await user.send(message)
                        prints.message(f"Sent {message} to {member}")
                        sent += 1
                    except Exception:
                        prints.error(f"Failed to send {message} to {member}")
                        pass
            except Exception:
                pass
            await message_builder(luna, description=f"```\nSent {message} to {sent} friends```")
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="sendall",
        usage="<message>",
        description="Message in all channels"
    )
    async def sendall(self, luna, *, message):

        if configs.risk_mode() == "on":
            try:
                channels = luna.guild.text_channels
                for _ in channels:
                    await message.channel.send(message)
            except BaseException:
                pass
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="blockall",
        usage="",
        description="Block everyone"
    )
    async def blockall(self, luna):

        if configs.risk_mode() == "on":
            try:
                members = luna.guild.members
                for member in members:
                    if member is not luna.author:
                        try:
                            await member.ban()
                            prints.message(f"Banned {member}")
                        except Exception:
                            pass
            except Exception:
                pass
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")


bot.add_cog(AllCog(bot))


class MassCog(commands.Cog, name="Mass commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="massping",
        usage="<delay> <amount>",
        description="Mass ping members"
    )
    async def massping(self, luna, delay: int, amount: int):

        if configs.risk_mode() == "on":
            try:
                for i in range(amount):
                    members = [m.mention for m in luna.guild.members]
                    if len(members) < 30:
                        mentionamount = len(members)
                    else:
                        mentionamount = 30
                    sendamount = len(members) - mentionamount + 1
                    for _ in range(sendamount):
                        if mentionamount == 0:
                            break
                        pingtext = ""
                        for _ in range(mentionamount):
                            pingtext += members.pop()
                        await luna.send(pingtext)
                        await asyncio.sleep(delay)
                        if len(members) < 30:
                            mentionamount = len(members)
                        else:
                            mentionamount = 30
            except Exception as e:
                prints.error(f"{e}")
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="massgp",
        usage="<delay> <amount>",
        description="Mass ghostping"
    )
    async def massgp(self, luna, delay: int, amount: int):

        if configs.risk_mode() == "on":
            try:
                for i in range(amount):
                    members = [m.mention for m in luna.guild.members]
                    if len(members) < 30:
                        mentionamount = len(members)
                    else:
                        mentionamount = 30
                    sendamount = len(members) - mentionamount + 1
                    for _ in range(sendamount):
                        if mentionamount == 0:
                            break
                        pingtext = ""
                        for _ in range(mentionamount):
                            pingtext += members.pop()
                        msg = await luna.send(pingtext)
                        await msg.delete()
                        await asyncio.sleep(delay)
                        if len(members) < 40:
                            mentionamount = len(members)
                        else:
                            mentionamount = 40
            except Exception as e:
                await error_builder(luna, description=f"```{e}```")
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="massnick",
        usage="<name>",
        description="Mass change nicknames"
    )
    async def massnick(self, luna, name: str):
        import discum
        if configs.risk_mode() == "on":
            bot = discum.Client(
                token=user_token, log=False,
                user_agent="Mozilla/5.0"
            )

            def done_fetching(_, guild_id):
                if bot.gateway.finishedMemberFetching(guild_id):
                    members = bot.gateway.session.guild(guild_id).members
                    bot.gateway.removeCommand(
                        {'function': done_fetching, 'params': {'guild_id': guild_id}}
                    )
                    bot.gateway.close()
                    return members

            def get_members(guild_id, channel_id):
                bot.gateway.fetchMembers(
                    guild_id, channel_id, keep="all", wait=1
                )
                bot.gateway.command(
                    {'function': done_fetching, 'params': {'guild_id': guild_id}}
                )
                bot.gateway.run()
                bot.gateway.resetSession()
                return bot.gateway.session.guild(guild_id).members

            amount = 0
            members = get_members(str(luna.guild.id), str(luna.channel.id))
            for member in members:
                try:
                    member = await luna.guild.fetch_member(member.id)
                    await member.edit(nick=name)
                    amount += 1
                    await asyncio.sleep(1)
                except BaseException:
                    pass
            await message_builder(luna, title="Success", description=f"```\nChanged nicknames of {amount} members```")
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="masschannels",
        usage="<amount>",
        description="Mass create channels"
    )
    async def masschannels(self, luna, amount: int):
        if configs.risk_mode() == "on":
            try:
                for i in range(amount):
                    await luna.guild.create_text_channel("Created by Luna")
                    await asyncio.sleep(1)
                await message_builder(luna, title="Success", description=f"```\nCreated {amount} channels```")
            except Exception as e:
                await error_builder(luna, description=f"```{e}```")
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="massroles",
        usage="<amount>",
        description="Mass create roles"
    )
    async def massroles(self, luna, amount: int):
        if configs.risk_mode() == "on":
            try:
                for i in range(amount):
                    await luna.guild.create_role(name="Created by Luna")
                    await asyncio.sleep(1)
                await message_builder(luna, title="Success", description=f"```\nCreated {amount} roles```")
            except Exception as e:
                await error_builder(luna, description=f"```{e}```")
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="prune",
        usage="<@role> [reason]",
        description="Prune a role"
    )
    async def prune(self, luna, role, *, reason: str = None):

        if configs.risk_mode() == "on":
            try:
                if reason is None:
                    reason = "No reason provided"
                else:
                    reason = reason
                role = luna.guild.get_role(role)
                if role is None:
                    await error_builder(luna, description="```\nRole not found```")
                    return
                members = luna.guild.members
                for member in members:
                    if role in member.roles:
                        try:
                            await member.send(f"You have been pruned from {luna.guild.name} for {reason}")
                            await member.kick(reason=reason)
                        except Exception:
                            pass
                await message_builder(luna, description=f"```\nPruned {len(members)} members```")
            except Exception:
                pass
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="pruneban",
        usage="<@role> [reason]",
        description="Prune & ban a role"
    )
    async def pruneban(self, luna, role, *, reason: str = None):

        if configs.risk_mode() == "on":
            try:
                if reason is None:
                    reason = "No reason provided"
                else:
                    reason = reason
                role = luna.guild.get_role(role)
                if role is None:
                    await error_builder(luna, description="```\nRole not found```")
                    return
                members = luna.guild.members
                for member in members:
                    if role in member.roles:
                        try:
                            await member.send(f"You have been pruned and banned from {luna.guild.name} for {reason}")
                            await member.ban(reason=reason)
                        except Exception:
                            pass
                await message_builder(luna, description=f"```\nPruned and banned {len(members)} members```")
            except Exception:
                pass
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")


bot.add_cog(MassCog(bot))


class GuildCog(commands.Cog, name="Guild commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="renamechannels",
        usage="<name>",
        description="Rename all channels"
    )
    async def renamechannels(self, luna, name: str):
        if configs.risk_mode() == "on":
            try:
                for channel in luna.guild.channels:
                    await channel.edit(name=name)
                    await asyncio.sleep(1)
                await message_builder(luna, title="Success", description=f"```\nRenamed all channels to {name}```")
            except Exception as e:
                await error_builder(luna, description=f"```{e}```")
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="delchannels",
        usage="",
        description="Delete all channels"
    )
    async def delchannels(self, luna):
        if configs.risk_mode() == "on":
            try:
                for channel in luna.guild.channels:
                    await channel.delete()
                    await asyncio.sleep(1)
                await message_builder(luna, title="Success", description="```\nDeleted all channels```")
            except Exception as e:
                await error_builder(luna, description=f"```{e}```")

    @commands.command(
        name="delroles",
        usage="",
        description="Delete all roles"
    )
    async def delroles(self, luna):
        if configs.risk_mode() == "on":
            try:
                for role in luna.guild.roles:
                    if role.name != "@everyone":
                        await role.delete()
                        await asyncio.sleep(1)
                await message_builder(luna, title="Success", description="```\nDeleted all roles```")
            except Exception as e:
                await error_builder(luna, description=f"```{e}```")

    @commands.command(
        name="delemojis",
        usage="",
        description="Delete all emojis"
    )
    async def delemojis(self, luna):
        if configs.risk_mode() == "on":
            try:
                for emoji in luna.guild.emojis:
                    await emoji.delete()
                    await asyncio.sleep(1)
                await message_builder(luna, title="Success", description="```\nDeleted all emojis```")
            except Exception as e:
                await error_builder(luna, description=f"```{e}```")


bot.add_cog(GuildCog(bot))


class ExploitCog(commands.Cog, name="Exploit commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="dosvc",
        usage="<channel_id> [amount]",
        aliases=["dosvc1"],
        description="VC Denial of Service"
    )
    async def dosvc(self, luna, channel: discord.VoiceChannel, amount: int = 10):

        await message_builder(
            luna, title="VC Denial of Service", description=f"```\nSending Attack...```",
            delete_after=3
        )

        region = [
            'europe',
            'hongkong',
            'india',
            'russia',
            'brazil',
            'japan',
            'singapore',
            'southafrica',
            'sydney',
            'us-central',
            'us-east',
            'us-west',
            'us-south']

        for x in range(amount):
            headers = {
                "Authorization": user_token,
                "Content-Type": "application/json",
                "Accept": "*/*",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
            }

            requests.patch(
                url=f"https://discord.com/api/{api_version}/channels/{str(channel.id)}/call",
                headers=headers,
                json={
                    'region': random.choice(region)
                }
            )
            await asyncio.sleep(0.5)

        await message_builder(luna, title="VC Denial of Service", description=f"```\nSent Attack```")

    @commands.command(
        name="dosvc2",
        usage="[amount]",
        description="VC Denial of Service"
    )
    async def dosvc2(self, luna, amount: int = 10):

        await message_builder(
            luna, title="VC Denial of Service", description=f"```\nSending Attack...```",
            delete_after=3
        )

        region = [
            'europe',
            'hongkong',
            'india',
            'russia',
            'brazil',
            'japan',
            'singapore',
            'southafrica',
            'sydney',
            'us-central',
            'us-east',
            'us-west',
            'us-south']

        for x in range(amount):
            requests.patch(
                f'https://discord.com/api/{api_version}/guilds/{str(luna.guild.id)}',
                headers={
                    'Authorization': user_token
                },
                json={
                    'region': random.choice(region)
                }
            )
            await asyncio.sleep(0.5)

        await message_builder(luna, title="VC Denial of Service", description=f"```\nSent Attack```")


# @commands.command(name = "disabler",
#                               usage="<token>",
#                               aliases=["disabler1"],
#                               description = "Token disabler")
# async def disabler(self, luna, token:str):
#

#       await message_builder(luna, title="Token Disabler", description=f"```\nAttempting to disable the token...```", delete_after=3)
#       res = requests.patch('https://discord.com/api/{api_version}/guilds', headers={'Authorization': token}, json={'name': 'Luna Disabler'})
# await message_builder(luna, title="Token Disabler",
# description=f"```\n{res}``````json\nJSON\n\n{res.json()}```")

# @commands.command(name = "disabler2",
#                               usage="<token>",
#                               description = "Token disabler")
# async def disabler2(self, luna, token:str):
#

# await message_builder(luna, title="Token Disabler",
# description=f"```\nAttempting to disable the token...```",
# delete_after=3)

#       DISABLED_MESSAGE = "You need to be 13 or older in order to use Discord."
#       IMMUNE_MESSAGE = "You cannot update your date of birth."
#       res = requests.patch('https://discord.com/api/{api_version}/users/@me', headers={'Authorization': token}, json={'date_of_birth': '2017-2-11'})

#       if res.status_code == 400:
#               res_message = res.json().get('date_of_birth', ['no response message'])[0]

#               if res_message == DISABLED_MESSAGE:
# await message_builder(luna, title="Token Disabler",
# description=f"```\nDisabled the token```")

#               elif res_message == IMMUNE_MESSAGE:
# await message_builder(luna, title="Token Disabler",
# description=f"```\nThe provided token cannot be disabled```")

#               else:
#                       await error_builder(luna, description=f"```\n{res_message}```")
#       else:
#               await error_builder(luna, description=f"```\nFailed to disable token```")


bot.add_cog(ExploitCog(bot))


class AbuseCog(commands.Cog, name="Abusive commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="purgehack",
        usage="",
        description="Purge a channel"
    )
    async def purgehack(self, luna):

        if configs.risk_mode() == "on":
            await luna.send(
                "​​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n"
            )
            await luna.send(
                "​​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n"
            )
            await luna.send(
                "​​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n"
            )
            await luna.send(
                "​​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n"
            )
            await luna.send(
                "​​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n"
            )
            await luna.send(
                "​​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n"
            )
            await luna.send(
                "​​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n​\n"
            )
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="mpreact",
        usage="<emoji>",
        description="Reacts the last 20 messages"
    )
    async def mpreact(self, luna, emoji):

        if configs.risk_mode() == "on":
            messages = await luna.message.channel.history(limit=20).flatten()
            for message in messages:
                await message.add_reaction(emoji)
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="junknick",
        usage="",
        description="Pure junk nickname"
    )
    async def junknick(self, luna):

        if configs.risk_mode() == "on":
            try:
                name = "𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫"
                await luna.author.edit(nick=name)
            except Exception as e:
                await error_builder(luna, description=f"```{e}```")
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="massban",
        usage="<guild_id>",
        description="Massban a guild"
    )
    @has_permissions(ban_members=True)
    async def massban(self, luna, guild_id: int):

        if configs.risk_mode() == "on":
            guild_id = int(guild_id)
            guildhit = self.bot.get_guild(guild_id)
            members = guildhit.members
            for member in members:
                if member is not luna.author:
                    try:
                        count = count + 1
                        await member.ban()
                        prints.message(f"Banned » {color.print_gradient(member)}")
                        await asyncio.sleep(2)
                    except Exception:
                        prints.error(f"Failed to ban » {color.print_gradient(member)}")
                        await asyncio.sleep(2)
            prints.message(f"Finished banning")
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")

    @commands.command(
        name="masskick",
        usage="<guild_id>",
        description="Masskick a guild"
    )
    @has_permissions(kick_members=True)
    async def masskick(self, luna, guild_id: int):

        if configs.risk_mode() == "on":
            guild_id = int(guild_id)
            guildhit = self.bot.get_guild(guild_id)
            members = guildhit.members
            for member in members:
                if member is not luna.author:
                    try:
                        count = count + 1
                        await member.kick()
                        prints.message(f"Kicked » {color.print_gradient(member)}")
                        await asyncio.sleep(2)
                    except Exception:
                        prints.error(
                            f"Failed to kick » {color.print_gradient(member)}"
                        )
                        await asyncio.sleep(2)
            prints.message(f"Finished kicking")
        else:
            await error_builder(luna, description="```\nRiskmode is disabled```")


bot.add_cog(AbuseCog(bot))


class PrivacyCog(commands.Cog, name="Privacy commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="privacy",
        aliases=['streamermode'],
        usage="<on/off>",
        description="Privacy mode"
    )
    async def privacy(self, ctx, mode: str):

        global privacy
        global luna_user_id

        if mode == "on" or mode == "off":
            if mode == "on":
                privacy = True
                now = datetime.now()
                hour = now.hour
                if hour < 12:
                    greeting = "Good morning"
                elif hour < 18:
                    greeting = "Good afternoon"
                else:
                    greeting = "Good evening"
                dpg.set_value(luna_user, f"{greeting}, Luna")
                dpg.set_value(logged, "Logged into Luna#0000")
                dpg.set_value(luna_uid_text, "UID: Privacy Mode")
            else:
                privacy = False
                now = datetime.now()
                hour = now.hour
                username = f"Dev - {os.getlogin()}" if developer_mode else os.getlogin()
                if hour < 12:
                    greeting = "Good morning"
                elif hour < 18:
                    greeting = "Good afternoon"
                else:
                    greeting = "Good evening"

                if not developer_mode:
                    if files.file_exist('data/auth.luna', documents=False):
                        username = files.json(
                            "data/auth.luna", "username", documents=False
                        )
                        username = Decryption(
                            '5QXapyTDbrRwW4ZBnUgPGAs9CeVSdiLk'
                        ).CEA256(username)
                else:
                    username = "Developer"
                dpg.set_value(luna_user, f"{greeting}, {username}")
                dpg.set_value(logged, f"Logged into {bot.user}")
                dpg.set_value(luna_uid_text, f"UID: {luna_user_id}")
            prints.message(f"Privacy mode » {mode}")
            await message_builder(ctx, description=f"```\nPrivacy mode » {mode}```")
        else:
            await mode_error(ctx, "on or off")


bot.add_cog(PrivacyCog(bot))


class ProtectionGuildCog(commands.Cog, name="Protection Guild commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="pguilds",
        aliases=['pguild', 'protectguild'],
        usage="<guild_id>",
        description="Protect a guild"
    )
    async def pguilds(self, luna, guild_id: int):

        try:
            self.bot.get_guild(guild_id)
        except BaseException:
            await error_builder(luna, description="Invalid guild")
            return
        config._global(
            "data/protections/config.json",
            "guilds", guild_id, add=True
        )
        prints.message(
            f"Added » {color.print_gradient(f'{guild_id}')} to the list of protected guilds"
        )
        await message_builder(luna, description=f"```\nAdded » {guild_id} to the list of protected guilds```")

    @commands.command(
        name="rguilds",
        aliases=['rguild', 'removeguild'],
        usage="<guild_id>",
        description="Remove a protected guild"
    )
    async def rguilds(self, luna, guild_id: int):

        try:
            self.bot.get_guild(guild_id)
        except BaseException:
            await error_builder(luna, description="Invalid guild")
            return
        config._global(
            "data/protections/config.json",
            "guilds", guild_id, delete=True
        )
        prints.message(
            f"Removed » {color.print_gradient(f'{guild_id}')} from the list of protected guilds"
        )
        await message_builder(luna, description=f"```\nRemoved » {guild_id} from the list of protected guilds```")


bot.add_cog(ProtectionGuildCog(bot))


class ProtectionCog(commands.Cog, name="Protection commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="pfooter",
        usage="<on/off>",
        description="Protections footer info"
    )
    async def pfooter(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(
                f"Protections footer info » {mode}"
            )
            if mode == "on":
                config._global("data/protections/config.json", "footer", True)
            else:
                config._global("data/protections/config.json", "footer", False)
            await message_builder(luna, description=f"```\nProtections footer info » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="anti_raid",
        usage="<on/off>",
        description="Protects against raids"
    )
    async def antiraid(self, luna, mode: str):

        global anti_raid
        global active_protections
        global active_list
        if mode == "on" or mode == "off":
            prints.message(f"Antiraid » {mode}")
            if mode == "on":
                anti_raid = True
                active_protections += 1
                active_list.append("anti_raid")
            else:
                anti_raid = False
                active_protections -= 1
                active_list.remove("anti_raid")
            await message_builder(luna, description=f"```\nAntiraid » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="anti_invite",
        usage="<on/off>",
        description="Protects against invites"
    )
    async def antiinvite(self, luna, mode: str):

        global anti_invite
        global active_protections
        global active_list
        if mode == "on" or mode == "off":
            prints.message(f"Antiinvite » {mode}")
            if mode == "on":
                anti_invite = True
                active_protections += 1
                active_list.append("anti_invite")
            else:
                anti_invite = False
                active_protections -= 1
                active_list.remove("anti_invite")
            await message_builder(luna, description=f"```\nAntiinvite » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="anti_upper",
        usage="<on/off>",
        description="Protects against uppercase"
    )
    async def antiupper(self, luna, mode: str):

        global anti_upper
        global active_protections
        global active_list
        if mode == "on" or mode == "off":
            prints.message(f"Antiupper » {mode}")
            if mode == "on":
                anti_upper = True
                active_protections += 1
                active_list.append("anti_upper")
            else:
                anti_upper = False
                active_protections -= 1
                active_list.remove("anti_upper")
            await message_builder(luna, description=f"```\nAntiupper » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="anti_phishing",
        usage="<on/off>",
        description="Protects against phishing"
    )
    async def antiphishing(self, luna, mode: str):

        global anti_phishing
        global active_protections
        global active_list
        if mode == "on" or mode == "off":
            prints.message(f"Anti phishing links » {mode}")
            if mode == "on":
                anti_phishing = True
                active_protections += 1
                active_list.append("Anti Phishing Links")
            else:
                anti_phishing = False
                active_protections -= 1
                active_list.remove("Anti Phishing Links")
            await message_builder(luna, description=f"```\nAnti phishing links » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="anti_deleting",
        usage="<on/off>",
        description="Log deleted messages"
    )
    async def antideleting(self, luna, mode: str):

        global anti_deleting
        global active_protections
        global active_list
        if mode == "on" or mode == "off":
            prints.message(f"Anti deleting » {mode}")
            if mode == "on":
                anti_deleting = True
                active_protections += 1
                active_list.append("Anti Deleting")
            else:
                anti_deleting = False
                active_protections -= 1
                active_list.remove("Anti Deleting")
            await message_builder(luna, description=f"```\nAnti deleting » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="sbcheck",
        usage="",
        description="Check for bad selfbots"
    )
    async def sbcheck(self, luna):

        await message_builder(luna, title="GIVEAWAY")
        await message_builder(luna, description="```\nThose that reacted, could be running selfbots```")


bot.add_cog(ProtectionCog(bot))


class BackupsCog(commands.Cog, name="Backup commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="backupserver",
        usage="[guild_id]",
        aliases=["cloneserver"],
        description="Backup the server"
    )
    async def backupserver(self, luna, guild_id: int = None):

        if guild_id is None:
            guild = luna.guild
        else:
            guild = self.bot.get_guild(guild_id)
        server_name = guild.name.encode("utf-8").decode("utf-8")
        new_guild = await self.bot.create_guild(server_name)
        await message_builder(luna, description=f"```\nCloning {guild.name}```")
        prints.message(f"Created new guild")
        new_guild_default_channels = await new_guild.fetch_channels()
        for channel in new_guild_default_channels:
            await channel.delete()

        for channel in guild.channels:
            if str(channel.type).lower() == "category":
                try:
                    channel.name = channel.name.encode("utf-8").decode("utf-8")
                    await new_guild.create_category(
                        channel.name, overwrites=channel.overwrites,
                        position=channel.position
                    )
                    prints.message(f"Created new category » {channel.name}")
                except Exception as e:
                    prints.error(e)
                    pass

        for channel in guild.voice_channels:
            try:
                cat = ""
                for category in new_guild.categories:
                    if channel.category.name == category.name:
                        cat = category
                channel.name = channel.name.encode("utf-8").decode("utf-8")
                await new_guild.create_voice_channel(
                    channel.name, category=cat, overwrites=channel.overwrites,
                    nsfw=channel.nsfw, position=channel.position
                )
                prints.message(f"Created new voice channel » {channel.name}")
            except Exception as e:
                prints.error(e)
                pass

        for channel in guild.stage_channels:
            try:
                cat = ""
                for category in new_guild.categories:
                    if channel.category.name == category.name:
                        cat = category
                channel.name = channel.name.encode("utf-8").decode("utf-8")
                await new_guild.create_stage_channel(
                    channel.name, category=cat, overwrites=channel.overwrites,
                    topic=channel.topic, slowmode_delay=channel.slowmode_delay,
                    nsfw=channel.nsfw, position=channel.position
                )
                prints.message(f"Created new stage channel » {channel.name}")
            except Exception as e:
                prints.error(e)
                pass

        for channel in guild.text_channels:
            try:
                cat = ""
                for category in new_guild.categories:
                    if channel.category.name == category.name:
                        cat = category
                channel.name = channel.name.encode("utf-8").decode("utf-8")
                await new_guild.create_text_channel(
                    channel.name, category=cat, overwrites=channel.overwrites,
                    topic=channel.topic, slowmode_delay=channel.slowmode_delay,
                    nsfw=channel.nsfw, position=channel.position
                )
                prints.message(f"Created new text channel » {channel.name}")
            except Exception as e:
                prints.error(e)
                pass

        for role in guild.roles[::-1]:
            if role.name != "@everyone":
                try:
                    role.name = role.name.encode("utf-8").decode("utf-8")
                    await new_guild.create_role(
                        name=role.name, color=role.color, permissions=role.permissions,
                        hoist=role.hoist, mentionable=role.mentionable
                    )
                    prints.message(f"Created new role » {role.name}")
                except Exception as e:
                    prints.error(e)
                    pass

        await message_builder(luna, description=f"```\nCloned {luna.guild.name}```")

    @commands.command(
        name="friendsbackup",
        usage="",
        description="Backup your friendslist"
    )
    async def friendsbackup(self, luna):

        prints.event("Backing up friendslist...")
        friendsamount = 0
        blockedamount = 0
        friendslist = ""
        blockedlist = ""
        for friend in self.bot.user.friends:
            friendslist += f"{friend.name}#{friend.discriminator}\n"
            friendsamount += 1
        file = open(
            "data/backup/friends.txt", "w", encoding='utf-8'
        )
        file.write(friendslist)
        file.close()
        for block in self.bot.user.blocked:
            blockedlist += f"{block.name}#{block.discriminator}\n"
            blockedamount += 1
        file = open(
            "data/backup/blocked.txt", "w", encoding='utf-8'
        )
        file.write(blockedlist)
        file.close()
        prints.message(
            f"Friendslist backed up. Friends » {friendsamount} Blocked » {blockedamount}"
        )
        await message_builder(
            luna,
            description=f"```\nBacked up {friendsamount} friends in Documents/data/backup/friends.txt\nBacked up {blockedamount} blocked users in Documents/data/backup/blocked.txt```"
        )


bot.add_cog(BackupsCog(bot))


class WhitelistCog(commands.Cog, name="Whitelist commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="whitelist",
        usage="<@member>",
        description="Whitelist someone"
    )
    async def whitelist(self, luna, user: discord.Member = None):

        if user is None:
            await luna.send("Please specify a user to whitelist")
        else:
            if luna.guild.id not in whitelisted_users.keys():
                whitelisted_users[luna.guild.id] = {}
            if user.id in whitelisted_users[luna.guild.id]:
                await message_builder(
                    luna,
                    description=f"```\n{user.name}#{user.discriminator} is already whitelisted```"
                )
            else:
                whitelisted_users[luna.guild.id][user.id] = 0
                await message_builder(
                    luna, description=f"```\nWhitelisted " + user.name.replace("*", "\\*").replace(
                        "`",
                        "\\`"
                    ).replace(
                        "_", "\\_"
                    ) + "#" + user.discriminator + "```"
                )

    @commands.command(
        name="unwhitelist",
        usage="",
        description="Unwhitelist someone"
    )
    async def unwhitelist(self, luna, user: discord.Member = None):

        if user is None:
            await luna.send("Please specify the user you would like to unwhitelist")
        else:
            if luna.guild.id not in whitelisted_users.keys():
                await luna.send("That user is not whitelisted")
                return
            if user.id in whitelisted_users[luna.guild.id]:
                whitelisted_users[luna.guild.id].pop(user.id, 0)
                await message_builder(
                    luna,
                    description=f"```\nUnwhitelisted " + user.name.replace("*", "\\*").replace(
                        "`",
                        "\\`"
                    ).replace(
                        "_", "\\_"
                    ) + "#" + user.discriminator + "```"
                )

    @commands.command(
        name="whitelisted",
        usage="",
        description="Show the whitelisted list"
    )
    async def whitelisted(self, luna, g=None):

        if g == '-g' or g == '-global':
            whitelist = '`All Whitelisted Users:`\n'
            for key in whitelisted_users:
                for key2 in whitelisted_users[key]:
                    user = self.bot.get_user(key2)
                    whitelist += '+ ' + user.name.replace('*', "\\*").replace('`', "\\`").replace('_', "\\_") + "#" + user.discriminator + " - " + \
                                 self.bot.get_guild(key).name.replace(
                                     '*', "\\*"
                                 ).replace('`', "\\`").replace('_', "\\_") + "" + "\n"
            await message_builder(luna, description=f"```\n{whitelist}```")
        else:
            whitelist = "`" + luna.guild.name.replace('*', "\\*").replace(
                '`', "\\`"
            ).replace('_', "\\_") + '\'s Whitelisted Users:`\n'
            for key in self.bot.whitelisted_users:
                if key == luna.guild.id:
                    for key2 in self.bot.whitelisted_users[luna.guild.id]:
                        user = self.bot.get_user(key2)
                        whitelist += '+ ' + user.name.replace('*', "\\*").replace('`', "\\`").replace(
                            '_', "\\_"
                        ) + "#" + user.discriminator + " (" + str(user.id) + ")" + "\n"
            await message_builder(luna, description=f"```\n{whitelist}```")

    @commands.command(
        name="clearwhitelist",
        usage="",
        description="Clear the whitelisted list"
    )
    async def clearwhitelist(self, luna):

        whitelisted_users.clear()
        await message_builder(luna, description=f"```\nCleared the whitelist```")


bot.add_cog(WhitelistCog(bot))


class SettingsCog(commands.Cog, name="Settings commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="prefix",
        usage="<prefix>",
        description="Change the prefix"
    )
    async def prefix(self, ctx, newprefix):
        config.prefix(newprefix)
        bot.command_prefix = newprefix
        prints.message(f"Prefix changed to {newprefix}")
        await message_builder(ctx, description=f"```\nPrefix changed to {newprefix}```")

    @commands.command(
        name="themes",
        usage="",
        description="Themes"
    )
    async def themes(self, luna):

        path_to_json = 'data/themes/'
        json_files = [pos_json for pos_json in os.listdir(
            path_to_json
        ) if pos_json.endswith('.json')]
        prefix = files.json("data/config.json", "prefix", documents=False)
        themesvar = files.json("data/config.json", "theme", documents=False)
        if themesvar == "default":
            pass
        else:
            themesvar = (themesvar[:-5])

        string = ""
        for i in json_files:
            string += f"{prefix}theme {i[:-5]}\n"

        cog = self.bot.get_cog('Theme commands')
        commands = cog.get_commands()
        helptext = ""
        for command in commands:
            helptext += f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n"
        await message_builder(
            luna, title="Themes",
            description=f"{theme.description()}"
                        f"```\nCurrent theme     » {themesvar}\n```"
                        f"```\nTheme customization\n\n"
                        f"{prefix}customize        » Theme customization\n```"
                        f"```\nTheme control\n\n"
                        f"{helptext}\n```"
                        f"```\nAvailable themes\n\n"
                        f"{prefix}theme default\n{string}```"
        )

    @commands.command(
        name="customize",
        usage="",
        aliases=['customise', 'customization', 'customisation'],
        description="Theme customization"
    )
    async def customize(self, luna):

        themevar = files.json("data/config.json", "theme", documents=False)
        prefix = files.json("data/config.json", "prefix", documents=False)
        title = theme.title()
        footer = theme.footer()

        if themevar == "default":
            pass
        else:
            themevar = (themevar[:-5])
        if themevar == "default":
            theme_description = descriptionvar_request
            if not theme_description == "true":
                theme_description = "off"
            else:
                theme_description = "on"
        else:
            theme_json = files.json(
                "data/config.json", "theme", documents=False
            )
            theme_description = files.json(
                f"data/themes/{theme_json}", "description", documents=False
            )
            if theme_description is None:
                theme_description = True
            if not theme_description:
                theme_description = "off"
            else:
                theme_description = "on"

        if title == "":
            title = "None"
        if footer == "":
            footer = "None"

        cog = self.bot.get_cog('Customization commands')
        commands = cog.get_commands()
        helptext1 = ""
        for command in commands:
            helptext1 += f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n"

        cog = self.bot.get_cog('Webhook customisation')
        commands = cog.get_commands()
        helptext2 = ""
        for command in commands:
            helptext2 += f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n"

        cog = self.bot.get_cog('Toast customization')
        commands = cog.get_commands()
        helptext3 = ""
        for command in commands:
            helptext3 += f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n"
        await message_builder(
            luna, title="Customization",
            description=f"{theme.description()}"
                        f"```\nYour current theme settings\n\n"
                        f"Theme             » {themevar}\n"
                        f"Title             » {title}\n"
                        f"Footer            » {footer}\n"
                        f"Description       » {theme_description}\n```"
                        f"```\nSelfbot theme settings\n\n"
                        f"{helptext1}\n```"
                        f"```\nWebhook theme settings\n\n"
                        f"{helptext2}\n```"
                        f"```\nToast theme settings\n\n{helptext3}\n```"
                        f"```\nNote\n\nIf you want to remove a customization,\n"
                        f"You can use \"None\" to remove it.\n```"
        )

    @commands.command(
        name="webhook",
        usage="[2]",
        description="Webhook settings"
    )
    async def webhook(self, luna, page: str = "1"):

        prefix = files.json("data/config.json", "prefix", documents=False)
        webhooks = files.json(
            "data/webhooks/webhooks.json",
            "webhooks", documents=False
        )
        login = files.json(
            "data/webhooks/webhooks.json",
            "login", documents=False
        )
        nitro = files.json(
            "data/webhooks/webhooks.json",
            "nitro", documents=False
        )
        giveaway = files.json(
            "data/webhooks/webhooks.json",
            "giveaway", documents=False
        )
        privnote = files.json(
            "data/webhooks/webhooks.json",
            "privnote", documents=False
        )
        selfbot = files.json(
            "data/webhooks/webhooks.json",
            "selfbot", documents=False
        )
        pings = files.json(
            "data/webhooks/webhooks.json",
            "pings", documents=False
        )
        ghostpings = files.json(
            "data/webhooks/webhooks.json", "ghostpings", documents=False
        )
        friendevents = files.json(
            "data/webhooks/webhooks.json", "friendevents", documents=False
        )
        guildevents = files.json(
            "data/webhooks/webhooks.json", "guildevents", documents=False
        )
        roleupdates = files.json(
            "data/webhooks/webhooks.json", "roleupdates", documents=False
        )
        nickupdates = files.json(
            "data/webhooks/webhooks.json", "nickupdates", documents=False
        )
        protection = files.json(
            "data/webhooks/webhooks.json", "protection", documents=False
        )
        cog = self.bot.get_cog('Webhook setup')
        commands = cog.get_commands()
        setuptext = ""
        for command in commands:
            setuptext += f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n"
        cog = self.bot.get_cog('Webhook commands')
        commands = cog.get_commands()
        helptext = ""
        for command in commands:
            helptext += f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n"
        cog = self.bot.get_cog('Webhook urls')
        commands = cog.get_commands()
        urltext = ""
        for command in commands:
            urltext += f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n"
        if page == "2":
            await message_builder(
                luna, title="Webhooks",
                description=f"{theme.description()}```\nWebhook url's\n\n{urltext}```"
            )
        else:
            await message_builder(
                luna, title="Webhooks",
                description=f"{theme.description()}"
                            f"```\nWebhook configuration\n\n"
                            f"Webhooks          » {webhooks}\n"
                            f"Login webhooks    » {login}\n"
                            f"Nitro webhooks    » {nitro}\n"
                            f"Giveaway webhooks » {giveaway}\n"
                            f"Privnote webhooks » {privnote}\n"
                            f"Selfbot webhooks  » {selfbot}\n"
                            f"Ping webhooks     » {pings}\n"
                            f"Ghostping webhooks » {ghostpings}\n"
                            f"Friendevent webhooks » {friendevents}\n"
                            f"Guildevent webhooks » {guildevents}\n"
                            f"Roleupdate webhooks » {roleupdates}\n"
                            f"Nickname webhooks » {nickupdates}\n"
                            f"Protection webhooks » {protection}\n```"
                            f"```\nWebhook setup\n\n{setuptext}\n```"
                            f"```\nWebhook control\n\n{helptext}\n```"
                            f"```\nNote\n\n{prefix}webhook 2 » Page 2```"
            )

    @commands.command(
        name="notifications",
        usage="",
        description="Toast notifications"
    )
    async def notifications(self, luna):

        prefix = files.json("data/config.json", "prefix", documents=False)
        toasts = files.json(
            "data/notifications/toasts.json",
            "toasts", documents=False
        )
        login = files.json(
            "data/notifications/toasts.json",
            "login", documents=False
        )
        nitro = files.json(
            "data/notifications/toasts.json",
            "nitro", documents=False
        )
        giveaway = files.json(
            "data/notifications/toasts.json", "giveaway", documents=False
        )
        privnote = files.json(
            "data/notifications/toasts.json", "privnote", documents=False
        )
        selfbot = files.json(
            "data/notifications/toasts.json", "selfbot", documents=False
        )
        pings = files.json(
            "data/notifications/toasts.json",
            "pings", documents=False
        )
        ghostpings = files.json(
            "data/notifications/toasts.json", "ghostpings", documents=False
        )
        friendevents = files.json(
            "data/notifications/toasts.json", "friendevents", documents=False
        )
        guildevents = files.json(
            "data/notifications/toasts.json", "guildevents", documents=False
        )
        roleupdates = files.json(
            "data/notifications/toasts.json", "roleupdates", documents=False
        )
        nickupdates = files.json(
            "data/notifications/toasts.json", "nickupdates", documents=False
        )
        protection = files.json(
            "data/notifications/toasts.json", "protection", documents=False
        )
        cog = self.bot.get_cog('Toast commands')
        commands = cog.get_commands()
        helptext = ""
        for command in commands:
            helptext += f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n"
        await message_builder(
            luna, title="Toast notifications",
            description=f"{theme.description()}"
                        f"```\nToast configuration\n\n"
                        f"Toasts            » {toasts}\n"
                        f"Login toasts      » {login}\n"
                        f"Nitro toasts      » {nitro}\n"
                        f"Giveaway toasts   » {giveaway}\n"
                        f"Privnote toasts   » {privnote}\n"
                        f"Selfbot toasts    » {selfbot}\n"
                        f"Ping toasts       » {pings}\n"
                        f"Ghostping toasts  » {ghostpings}\n"
                        f"Friendevent toast » {friendevents}\n"
                        f"Guildevent toasts » {guildevents}\n"
                        f"Roleupdate toasts » {roleupdates}\n"
                        f"Nickname toasts   » {nickupdates}\n"
                        f"Protection toasts » {protection}\n```"
                        f"```\nToast control\n\n{helptext}```"
        )

    # @commands.command(name = "embedmode",
    #                           usage="",
    #                           description = "Switch to embed mode")
    # async def embedmode(self, luna):
    #
    #   config.mode("1")
    #   prints.message(f"Switched to {color.print_gradient('embed')} mode")
    # await message_builder(luna, title="Embed mode",
    # description=f"```\nSwitched to embed mode.```")

    @commands.command(
        name="indentmode",
        usage="",
        description="Switch to indent mode"
    )
    async def indentmode(self, luna):

        config.mode("1")
        prints.message(f"Switched to {color.print_gradient('indent')} mode")
        await message_builder(luna, title="Indent mode", description=f"```\nSwitched to indent mode.```")

    @commands.command(
        name="textmode",
        usage="",
        description="Switch to text mode"
    )
    async def textmode(self, luna):

        config.mode("2")
        prints.message(f"Switched to {color.print_gradient('text')} mode")
        await message_builder(luna, title="Text mode", description=f"```Switched to text mode.```")

    @commands.command(
        name="sniper",
        usage="",
        description="Sniper settings"
    )
    async def sniper(self, luna):

        prefix = files.json("data/config.json", "prefix", documents=False)
        nitro_sniper = files.json(
            "data/snipers/nitro.json", "sniper", documents=False
        )
        privnote_sniper = files.json(
            "data/snipers/privnote.json", "sniper", documents=False
        )
        cog = self.bot.get_cog('Sniper settings')
        commands = cog.get_commands()
        helptext = ""
        for command in commands:
            helptext += f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n"
        await message_builder(
            luna, title="Sniper settings",
            description=f"{theme.description()}```\nYour current settings\n\nNitro Sniper      » {nitro_sniper}\nPrivnote Sniper   » {privnote_sniper}\n``````\nSettings\n\n{helptext}```"
        )

    @commands.command(
        name="giveaway",
        usage="",
        description="Giveaway settings"
    )
    async def giveaway(self, luna):

        prefix = files.json("data/config.json", "prefix", documents=False)
        giveaway_joiner = files.json(
            "data/snipers/giveaway.json", "joiner", documents=False
        )
        delay_in_minutes = files.json(
            "data/snipers/giveaway.json", "delay_in_minutes", documents=False
        )
        guild_joiner = files.json(
            "data/snipers/giveaway.json", "guild_joiner", documents=False
        )

        cog = self.bot.get_cog('Giveaway settings')
        commands = cog.get_commands()
        helptext = ""
        for command in commands:
            helptext += f"{prefix + command.name + ' ' + command.usage:<17} » {command.description}\n"
        await message_builder(
            luna, title="Giveaway settings",
            description=f"{theme.description()}"
                        f"```\nYour current settings\n\n"
                        f"Giveaway Joiner   » {giveaway_joiner}\n"
                        f"Delay             » {delay_in_minutes} minute/s\n"
                        f"Server Joiner     » {guild_joiner}\n```"
                        f"```\nSettings\n\n{helptext}```"
        )

    @commands.command(
        name="errorlog",
        usage="<console/message>",
        description="Switch errorlog"
    )
    async def errorlog(self, luna, mode: str):

        if mode == "message" or mode == "console":
            prints.message(f"Error logging » {mode}")
            config.error_log(mode)
            await message_builder(luna, description=f"```\nError logging » {mode}```")
        else:
            await mode_error(luna, "message or console")

    @commands.command(
        name="deletetimer",
        usage="<seconds>",
        description="Auto delete timer"
    )
    async def deletetimer(self, luna, seconds: int):

        await message_builder(luna, description=f"```\nAuto delete timer » {seconds} seconds```")
        prints.message(
            f"Auto delete timer » {color.print_gradient(f'{seconds} seconds')}"
        )
        config.delete_timer(f"{seconds}")

    @commands.command(
        name="afkmessage",
        usage="<text>",
        description="Change the afk message"
    )
    async def afkmessage(self, luna, *, afkmessage):

        await message_builder(luna, description=f"```\nAFK message » {afkmessage}```")
        prints.message(f"AFK message » {color.print_gradient(f'{afkmessage}')}")
        config.afk_message(f"{afkmessage}")

    @commands.command(
        name="riskmode",
        usage="<on/off>",
        description="Enable abusive commands"
    )
    async def riskmode(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Riskmode » {mode}")
            config.risk_mode(mode)
            await message_builder(luna, description=f"```\nRiskmode » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="selfbotdetection",
        usage="<on/off>",
        description="Sb detection"
    )
    async def selfbotdetection(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Selfbot detection » {mode}")
            config.selfbot.sniper(mode)
            await message_builder(luna, description=f"```\nSelfbot detection » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="mention",
        usage="<on/off>",
        description="Mention notification"
    )
    async def mention(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Mention notification » {mode}")
            config.toast.pings(mode)
            await message_builder(luna, description=f"```\nMention notification » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="password",
        usage="<new_password>",
        description="Change password"
    )
    async def password(self, luna, password: str):

        config.password(f"{password}")
        await message_builder(luna, description=f"```\nChanged password to » {password}```")
        prints.message(f"Changed password to » {color.print_gradient(f'{password}')}")

    @commands.command(
        name="console",
        usage="<1/2>",
        description="Change console mode"
    )
    async def console(self, ctx, mode: str):

        if mode == "1" or mode == "2":
            config._global("data/console/console.json", "mode", mode)
            prints.message(f"Console mode » {mode}")
            await message_builder(ctx, description=f"```\nConsole mode » {mode}```")
            luna.console(False, clear=True)
            if privacy:
                command_count = len(bot.commands)
                cog = bot.get_cog('Custom commands')
                try:
                    custom = cog.get_commands()
                    custom_command_count = 0
                    for _ in custom:
                        custom_command_count += 1
                except BaseException:
                    custom_command_count = 0
                print(motd.center(os.get_terminal_size().columns))
                if platinum:
                    print("Platinum Build".center(os.get_terminal_size().columns))
                prefix = files.json(
                    "data/config.json",
                    "prefix", documents=False
                )
                console_mode = files.json(
                    "data/console/console.json", "mode", documents=False
                )
                if console_mode == "2":
                    riskmode = files.json(
                        "data/config.json", "risk_mode", documents=False
                    )
                    themesvar = files.json(
                        "data/config.json", "theme", documents=False
                    )
                    deletetimer = int(
                        files.json(
                            "data/config.json", "delete_timer", documents=False
                        )
                    )
                    startup_status = files.json(
                        "data/config.json", "startup_status", documents=False
                    )
                    nitro_sniper = files.json(
                        "data/snipers/nitro.json", "sniper", documents=False
                    )
                    giveawayjoiner = files.json(
                        "data/snipers/giveaway.json", "joiner", documents=False
                    )
                    if themesvar == "default":
                        pass
                    else:
                        themesvar = themesvar[:-5]
                    ui_user = f" {color.print_gradient('User:')} {'Luna#0000':<26}"
                    ui_guilds = f" {color.print_gradient('Guilds:')} {'0':<24}"
                    ui_friends = f" {color.print_gradient('Friends:')} {'0':<23}"
                    ui_prefix = f" {color.print_gradient('Prefix:')} {prefix:<24}"
                    ui_theme = f" {color.print_gradient('Theme:')} {themesvar:<25}"
                    ui_commands = f" {color.print_gradient('Commands:')} {command_count - custom_command_count:<22}"
                    ui_commands_custom = f" {color.print_gradient('Custom Commands:')} {custom_command_count:<15}"
                    ui_nitro_sniper = f" {color.print_gradient('Nitro Sniper:')} {nitro_sniper}"
                    ui_giveaway_sniper = f" {color.print_gradient('Giveaway Joiner:')} {giveawayjoiner}"
                    ui_riskmode = f" {color.print_gradient('Riskmode:')} {riskmode}"
                    ui_deletetimer = f" {color.print_gradient('Delete Timer:')} {deletetimer}"
                    ui_startup = f" {color.print_gradient('Startup Status:')} {startup_status}"
                    print()
                    print(
                        f"               ═════════════ {color.print_gradient('User')} ═════════════      ═══════════ {color.print_gradient('Settings')} ═══════════"
                    )
                    print(f"               {ui_user}     {ui_prefix}")
                    print(f"               {ui_guilds}     {ui_theme}")
                    print(f"               {ui_friends}     {ui_nitro_sniper}")
                    print(
                        f"               ════════════════════════════════      {ui_giveaway_sniper}"
                    )
                    print(
                        f"               ═════════════ {color.print_gradient('Luna')} ═════════════      {ui_riskmode}"
                    )
                    print(f"               {ui_commands}     {ui_deletetimer}")
                    print(
                        f"               {ui_commands_custom}     {ui_startup}"
                    )
                    print(
                        f"               ════════════════════════════════      ════════════════════════════════\n"
                    )
                else:
                    print()
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient('] CONNECTED')}"
                    )
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient(']')} Luna#0000 | {color.print_gradient('0')} Guilds | {color.print_gradient('0')} Friends"
                    )
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient(']')} {prefix}\n"
                    )
            else:
                command_count = len(bot.commands)
                cog = bot.get_cog('Custom commands')
                try:
                    custom = cog.get_commands()
                    custom_command_count = 0
                    for _ in custom:
                        custom_command_count += 1
                except BaseException:
                    custom_command_count = 0
                print(motd.center(os.get_terminal_size().columns))
                if platinum:
                    print("Platinum Build".center(os.get_terminal_size().columns))
                prefix = files.json(
                    "data/config.json",
                    "prefix", documents=False
                )
                console_mode = files.json(
                    "data/console/console.json", "mode", documents=False
                )
                if console_mode == "2":
                    riskmode = files.json(
                        "data/config.json", "risk_mode", documents=False
                    )
                    themesvar = files.json(
                        "data/config.json", "theme", documents=False
                    )
                    deletetimer = int(
                        files.json(
                            "data/config.json", "delete_timer", documents=False
                        )
                    )
                    startup_status = files.json(
                        "data/config.json", "startup_status", documents=False
                    )
                    nitro_sniper = files.json(
                        "data/snipers/nitro.json", "sniper", documents=False
                    )
                    giveawayjoiner = files.json(
                        "data/snipers/giveaway.json", "joiner", documents=False
                    )
                    if themesvar == "default":
                        pass
                    else:
                        themesvar = themesvar[:-5]
                    bot_user = f"{bot.user}"
                    ui_user = f" {color.print_gradient('User:')} {bot_user:<26}"
                    ui_guilds = f" {color.print_gradient('Guilds:')} {len(bot.guilds):<24}"
                    ui_friends = f" {color.print_gradient('Friends:')} {len(bot.user.friends):<23}"
                    ui_prefix = f" {color.print_gradient('Prefix:')} {prefix:<24}"
                    ui_theme = f" {color.print_gradient('Theme:')} {themesvar:<25}"
                    ui_commands = f" {color.print_gradient('Commands:')} {command_count - custom_command_count:<22}"
                    ui_commands_custom = f" {color.print_gradient('Custom Commands:')} {custom_command_count:<15}"
                    ui_nitro_sniper = f" {color.print_gradient('Nitro Sniper:')} {nitro_sniper}"
                    ui_giveaway_sniper = f" {color.print_gradient('Giveaway Joiner:')} {giveawayjoiner}"
                    ui_riskmode = f" {color.print_gradient('Riskmode:')} {riskmode}"
                    ui_deletetimer = f" {color.print_gradient('Delete Timer:')} {deletetimer}"
                    ui_startup = f" {color.print_gradient('Startup Status:')} {startup_status}"
                    print()
                    print(
                        f"               ═════════════ {color.print_gradient('User')} ═════════════      ═══════════ {color.print_gradient('Settings')} ═══════════"
                    )
                    print(f"               {ui_user}     {ui_prefix}")
                    print(f"               {ui_guilds}     {ui_theme}")
                    print(f"               {ui_friends}     {ui_nitro_sniper}")
                    print(
                        f"               ════════════════════════════════      {ui_giveaway_sniper}"
                    )
                    print(
                        f"               ═════════════ {color.print_gradient('Luna')} ═════════════      {ui_riskmode}"
                    )
                    print(f"               {ui_commands}     {ui_deletetimer}")
                    print(
                        f"               {ui_commands_custom}     {ui_startup}"
                    )
                    print(
                        f"               ════════════════════════════════      ════════════════════════════════\n"
                    )
                else:
                    print()
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient('] CONNECTED')}"
                    )
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient(']')} "
                        f"{bot.user} | "
                        f"{color.print_gradient(f'{len(bot.guilds)}')} Guilds | "
                        f"{color.print_gradient(f'{len(bot.user.friends)}')} Friends"
                    )
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient(']')} {prefix}\n"
                    )
            print(
                f"═══════════════════════════════════════════════════════════════════════════════════════════════════\n"
            )
            prints.message(
                f"{color.print_gradient(f'{command_count - custom_command_count}')} commands | {color.print_gradient(f'{custom_command_count}')} custom commands"
            )
        else:
            await mode_error(ctx, "1 or 2")

    @commands.command(
        name="lgradient",
        usage="<1-7>",
        description="Change logo gradient",
    )
    async def lgradient(self, ctx, mode: str):

        if mode == "1" or mode == "2" or mode == "3" or mode == "4" or mode == "5" or mode == "6" or mode == "7":
            config._global("data/console/console.json", "logo_gradient", mode)
            prints.message(f"Logo gradient » {mode}")
            await message_builder(ctx, description=f"```\nLogo gradient » {mode}```")
            luna.console(False, clear=True)
            if privacy:
                command_count = len(bot.commands)
                cog = bot.get_cog('Custom commands')
                try:
                    custom = cog.get_commands()
                    custom_command_count = 0
                    for _ in custom:
                        custom_command_count += 1
                except BaseException:
                    custom_command_count = 0
                print(motd.center(os.get_terminal_size().columns))
                if platinum:
                    print("Platinum Build".center(os.get_terminal_size().columns))
                prefix = files.json(
                    "data/config.json",
                    "prefix", documents=False
                )
                console_mode = files.json(
                    "data/console/console.json", "mode", documents=False
                )
                if console_mode == "2":
                    riskmode = files.json(
                        "data/config.json", "risk_mode", documents=False
                    )
                    themesvar = files.json(
                        "data/config.json", "theme", documents=False
                    )
                    deletetimer = int(
                        files.json(
                            "data/config.json", "delete_timer", documents=False
                        )
                    )
                    startup_status = files.json(
                        "data/config.json", "startup_status", documents=False
                    )
                    nitro_sniper = files.json(
                        "data/snipers/nitro.json", "sniper", documents=False
                    )
                    giveawayjoiner = files.json(
                        "data/snipers/giveaway.json", "joiner", documents=False
                    )
                    if themesvar == "default":
                        pass
                    else:
                        themesvar = themesvar[:-5]
                    ui_user = f" {color.print_gradient('User:')} {'Luna#0000':<26}"
                    ui_guilds = f" {color.print_gradient('Guilds:')} {'0':<24}"
                    ui_friends = f" {color.print_gradient('Friends:')} {'0':<23}"
                    ui_prefix = f" {color.print_gradient('Prefix:')} {prefix:<24}"
                    ui_theme = f" {color.print_gradient('Theme:')} {themesvar:<25}"
                    ui_commands = f" {color.print_gradient('Commands:')} {command_count - custom_command_count:<22}"
                    ui_commands_custom = f" {color.print_gradient('Custom Commands:')} {custom_command_count:<15}"
                    ui_nitro_sniper = f" {color.print_gradient('Nitro Sniper:')} {nitro_sniper}"
                    ui_giveaway_sniper = f" {color.print_gradient('Giveaway Joiner:')} {giveawayjoiner}"
                    ui_riskmode = f" {color.print_gradient('Riskmode:')} {riskmode}"
                    ui_deletetimer = f" {color.print_gradient('Delete Timer:')} {deletetimer}"
                    ui_startup = f" {color.print_gradient('Startup Status:')} {startup_status}"
                    print()
                    print(
                        f"               ═════════════ {color.print_gradient('User')} ═════════════      ═══════════ {color.print_gradient('Settings')} ═══════════"
                    )
                    print(f"               {ui_user}     {ui_prefix}")
                    print(f"               {ui_guilds}     {ui_theme}")
                    print(f"               {ui_friends}     {ui_nitro_sniper}")
                    print(
                        f"               ════════════════════════════════      {ui_giveaway_sniper}"
                    )
                    print(
                        f"               ═════════════ {color.print_gradient('Luna')} ═════════════      {ui_riskmode}"
                    )
                    print(f"               {ui_commands}     {ui_deletetimer}")
                    print(
                        f"               {ui_commands_custom}     {ui_startup}"
                    )
                    print(
                        f"               ════════════════════════════════      ════════════════════════════════\n"
                    )
                else:
                    print()
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient('] CONNECTED')}"
                    )
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient(']')} Luna#0000 | {color.print_gradient('0')} Guilds | {color.print_gradient('0')} Friends"
                    )
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient(']')} {prefix}\n"
                    )
            else:
                command_count = len(bot.commands)
                cog = bot.get_cog('Custom commands')
                try:
                    custom = cog.get_commands()
                    custom_command_count = 0
                    for _ in custom:
                        custom_command_count += 1
                except BaseException:
                    custom_command_count = 0
                print(motd.center(os.get_terminal_size().columns))
                if platinum:
                    print("Platinum Build".center(os.get_terminal_size().columns))
                prefix = files.json(
                    "data/config.json",
                    "prefix", documents=False
                )
                console_mode = files.json(
                    "data/console/console.json", "mode", documents=False
                )
                if console_mode == "2":
                    riskmode = files.json(
                        "data/config.json", "risk_mode", documents=False
                    )
                    themesvar = files.json(
                        "data/config.json", "theme", documents=False
                    )
                    deletetimer = int(
                        files.json(
                            "data/config.json", "delete_timer", documents=False
                        )
                    )
                    startup_status = files.json(
                        "data/config.json", "startup_status", documents=False
                    )
                    nitro_sniper = files.json(
                        "data/snipers/nitro.json", "sniper", documents=False
                    )
                    giveawayjoiner = files.json(
                        "data/snipers/giveaway.json", "joiner", documents=False
                    )
                    if themesvar == "default":
                        pass
                    else:
                        themesvar = themesvar[:-5]
                    bot_user = f"{bot.user}"
                    ui_user = f" {color.print_gradient('User:')} {bot_user:<26}"
                    ui_guilds = f" {color.print_gradient('Guilds:')} {len(bot.guilds):<24}"
                    ui_friends = f" {color.print_gradient('Friends:')} {len(bot.user.friends):<23}"
                    ui_prefix = f" {color.print_gradient('Prefix:')} {prefix:<24}"
                    ui_theme = f" {color.print_gradient('Theme:')} {themesvar:<25}"
                    ui_commands = f" {color.print_gradient('Commands:')} {command_count - custom_command_count:<22}"
                    ui_commands_custom = f" {color.print_gradient('Custom Commands:')} {custom_command_count:<15}"
                    ui_nitro_sniper = f" {color.print_gradient('Nitro Sniper:')} {nitro_sniper}"
                    ui_giveaway_sniper = f" {color.print_gradient('Giveaway Joiner:')} {giveawayjoiner}"
                    ui_riskmode = f" {color.print_gradient('Riskmode:')} {riskmode}"
                    ui_deletetimer = f" {color.print_gradient('Delete Timer:')} {deletetimer}"
                    ui_startup = f" {color.print_gradient('Startup Status:')} {startup_status}"
                    print()
                    print(
                        f"               ═════════════ {color.print_gradient('User')} ═════════════      ═══════════ {color.print_gradient('Settings')} ═══════════"
                    )
                    print(f"               {ui_user}     {ui_prefix}")
                    print(f"               {ui_guilds}     {ui_theme}")
                    print(f"               {ui_friends}     {ui_nitro_sniper}")
                    print(
                        f"               ════════════════════════════════      {ui_giveaway_sniper}"
                    )
                    print(
                        f"               ═════════════ {color.print_gradient('Luna')} ═════════════      {ui_riskmode}"
                    )
                    print(f"               {ui_commands}     {ui_deletetimer}")
                    print(
                        f"               {ui_commands_custom}     {ui_startup}"
                    )
                    print(
                        f"               ════════════════════════════════      ════════════════════════════════\n"
                    )
                else:
                    print()
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient('] CONNECTED')}"
                    )
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient(']')} "
                        f"{bot.user} | "
                        f"{color.print_gradient(f'{len(bot.guilds)}')} Guilds | "
                        f"{color.print_gradient(f'{len(bot.user.friends)}')} Friends"
                    )
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient(']')} {prefix}\n"
                    )
            print(
                f"═══════════════════════════════════════════════════════════════════════════════════════════════════\n"
            )
            prints.message(
                f"{color.print_gradient(f'{command_count - custom_command_count}')} commands | {color.print_gradient(f'{custom_command_count}')} custom commands"
            )
        else:
            await mode_error(ctx, "1-7")

    @commands.command(
        name="pgradient",
        usage="<1-7>",
        description="Change print gradient",
    )
    async def pgradient(self, ctx, mode: str):

        if mode == "1" or mode == "2" or mode == "3" or mode == "4" or mode == "5" or mode == "6" or mode == "7":
            config._global("data/console/console.json", "print_gradient", mode)
            prints.message(f"Print gradient » {mode}")
            await message_builder(ctx, description=f"```\nPrint gradient » {mode}```")
            luna.console(False, clear=True)
            if privacy:
                command_count = len(bot.commands)
                cog = bot.get_cog('Custom commands')
                try:
                    custom = cog.get_commands()
                    custom_command_count = 0
                    for _ in custom:
                        custom_command_count += 1
                except BaseException:
                    custom_command_count = 0
                print(motd.center(os.get_terminal_size().columns))
                if platinum:
                    print("Platinum Build".center(os.get_terminal_size().columns))
                prefix = files.json(
                    "data/config.json",
                    "prefix", documents=False
                )
                console_mode = files.json(
                    "data/console/console.json", "mode", documents=False
                )
                if console_mode == "2":
                    riskmode = files.json(
                        "data/config.json", "risk_mode", documents=False
                    )
                    themesvar = files.json(
                        "data/config.json", "theme", documents=False
                    )
                    deletetimer = int(
                        files.json(
                            "data/config.json", "delete_timer", documents=False
                        )
                    )
                    startup_status = files.json(
                        "data/config.json", "startup_status", documents=False
                    )
                    nitro_sniper = files.json(
                        "data/snipers/nitro.json", "sniper", documents=False
                    )
                    giveawayjoiner = files.json(
                        "data/snipers/giveaway.json", "joiner", documents=False
                    )
                    if themesvar == "default":
                        pass
                    else:
                        themesvar = themesvar[:-5]
                    ui_user = f" {color.print_gradient('User:')} {'Luna#0000':<26}"
                    ui_guilds = f" {color.print_gradient('Guilds:')} {'0':<24}"
                    ui_friends = f" {color.print_gradient('Friends:')} {'0':<23}"
                    ui_prefix = f" {color.print_gradient('Prefix:')} {prefix:<24}"
                    ui_theme = f" {color.print_gradient('Theme:')} {themesvar:<25}"
                    ui_commands = f" {color.print_gradient('Commands:')} {command_count - custom_command_count:<22}"
                    ui_commands_custom = f" {color.print_gradient('Custom Commands:')} {custom_command_count:<15}"
                    ui_nitro_sniper = f" {color.print_gradient('Nitro Sniper:')} {nitro_sniper}"
                    ui_giveaway_sniper = f" {color.print_gradient('Giveaway Joiner:')} {giveawayjoiner}"
                    ui_riskmode = f" {color.print_gradient('Riskmode:')} {riskmode}"
                    ui_deletetimer = f" {color.print_gradient('Delete Timer:')} {deletetimer}"
                    ui_startup = f" {color.print_gradient('Startup Status:')} {startup_status}"
                    print()
                    print(
                        f"               ═════════════ {color.print_gradient('User')} ═════════════      ═══════════ {color.print_gradient('Settings')} ═══════════"
                    )
                    print(f"               {ui_user}     {ui_prefix}")
                    print(f"               {ui_guilds}     {ui_theme}")
                    print(f"               {ui_friends}     {ui_nitro_sniper}")
                    print(
                        f"               ════════════════════════════════      {ui_giveaway_sniper}"
                    )
                    print(
                        f"               ═════════════ {color.print_gradient('Luna')} ═════════════      {ui_riskmode}"
                    )
                    print(f"               {ui_commands}     {ui_deletetimer}")
                    print(
                        f"               {ui_commands_custom}     {ui_startup}"
                    )
                    print(
                        f"               ════════════════════════════════      ════════════════════════════════\n"
                    )
                else:
                    print()
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient('] CONNECTED')}"
                    )
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient(']')} Luna#0000 | {color.print_gradient('0')} Guilds | {color.print_gradient('0')} Friends"
                    )
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient(']')} {prefix}\n"
                    )
            else:
                command_count = len(bot.commands)
                cog = bot.get_cog('Custom commands')
                try:
                    custom = cog.get_commands()
                    custom_command_count = 0
                    for _ in custom:
                        custom_command_count += 1
                except BaseException:
                    custom_command_count = 0
                print(motd.center(os.get_terminal_size().columns))
                if platinum:
                    print("Platinum Build".center(os.get_terminal_size().columns))
                prefix = files.json(
                    "data/config.json",
                    "prefix", documents=False
                )
                console_mode = files.json(
                    "data/console/console.json", "mode", documents=False
                )
                if console_mode == "2":
                    riskmode = files.json(
                        "data/config.json", "risk_mode", documents=False
                    )
                    themesvar = files.json(
                        "data/config.json", "theme", documents=False
                    )
                    deletetimer = int(
                        files.json(
                            "data/config.json", "delete_timer", documents=False
                        )
                    )
                    startup_status = files.json(
                        "data/config.json", "startup_status", documents=False
                    )
                    nitro_sniper = files.json(
                        "data/snipers/nitro.json", "sniper", documents=False
                    )
                    giveawayjoiner = files.json(
                        "data/snipers/giveaway.json", "joiner", documents=False
                    )
                    if themesvar == "default":
                        pass
                    else:
                        themesvar = themesvar[:-5]
                    bot_user = f"{bot.user}"
                    ui_user = f" {color.print_gradient('User:')} {bot_user:<26}"
                    ui_guilds = f" {color.print_gradient('Guilds:')} {len(bot.guilds):<24}"
                    ui_friends = f" {color.print_gradient('Friends:')} {len(bot.user.friends):<23}"
                    ui_prefix = f" {color.print_gradient('Prefix:')} {prefix:<24}"
                    ui_theme = f" {color.print_gradient('Theme:')} {themesvar:<25}"
                    ui_commands = f" {color.print_gradient('Commands:')} {command_count - custom_command_count:<22}"
                    ui_commands_custom = f" {color.print_gradient('Custom Commands:')} {custom_command_count:<15}"
                    ui_nitro_sniper = f" {color.print_gradient('Nitro Sniper:')} {nitro_sniper}"
                    ui_giveaway_sniper = f" {color.print_gradient('Giveaway Joiner:')} {giveawayjoiner}"
                    ui_riskmode = f" {color.print_gradient('Riskmode:')} {riskmode}"
                    ui_deletetimer = f" {color.print_gradient('Delete Timer:')} {deletetimer}"
                    ui_startup = f" {color.print_gradient('Startup Status:')} {startup_status}"
                    print()
                    print(
                        f"               ═════════════ {color.print_gradient('User')} ═════════════      ═══════════ {color.print_gradient('Settings')} ═══════════"
                    )
                    print(f"               {ui_user}     {ui_prefix}")
                    print(f"               {ui_guilds}     {ui_theme}")
                    print(f"               {ui_friends}     {ui_nitro_sniper}")
                    print(
                        f"               ════════════════════════════════      {ui_giveaway_sniper}"
                    )
                    print(
                        f"               ═════════════ {color.print_gradient('Luna')} ═════════════      {ui_riskmode}"
                    )
                    print(f"               {ui_commands}     {ui_deletetimer}")
                    print(
                        f"               {ui_commands_custom}     {ui_startup}"
                    )
                    print(
                        f"               ════════════════════════════════      ════════════════════════════════\n"
                    )
                else:
                    print()
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient('] CONNECTED')}"
                    )
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient(']')} "
                        f"{bot.user} | "
                        f"{color.print_gradient(f'{len(bot.guilds)}')} Guilds | "
                        f"{color.print_gradient(f'{len(bot.user.friends)}')} Friends"
                    )
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient(']')} {prefix}\n"
                    )
            print(
                f"═══════════════════════════════════════════════════════════════════════════════════════════════════\n"
            )
            prints.message(
                f"{color.print_gradient(f'{command_count - custom_command_count}')} commands | {color.print_gradient(f'{custom_command_count}')} custom commands"
            )
        else:
            await mode_error(ctx, "1-7")

    @commands.command(
        name="spacer",
        usage="<spacer>",
        description="Change print spacer",
    )
    async def spacer(self, ctx, mode: str):

        config._global("data/console/console.json", "spacer", mode)
        prints.message(f"Print spacer » {mode}")
        await message_builder(ctx, description=f"```\nPrint spacer » {mode}```")
        luna.console(False, clear=True)
        if privacy:
            command_count = len(bot.commands)
            cog = bot.get_cog('Custom commands')
            try:
                custom = cog.get_commands()
                custom_command_count = 0
                for _ in custom:
                    custom_command_count += 1
            except BaseException:
                custom_command_count = 0
            print(motd.center(os.get_terminal_size().columns))
            if platinum:
                print("Platinum Build".center(os.get_terminal_size().columns))
            prefix = files.json(
                "data/config.json",
                "prefix", documents=False
            )
            console_mode = files.json(
                "data/console/console.json", "mode", documents=False
            )
            if console_mode == "2":
                riskmode = files.json(
                    "data/config.json", "risk_mode", documents=False
                )
                themesvar = files.json(
                    "data/config.json", "theme", documents=False
                )
                deletetimer = int(
                    files.json(
                        "data/config.json", "delete_timer", documents=False
                    )
                )
                startup_status = files.json(
                    "data/config.json", "startup_status", documents=False
                )
                nitro_sniper = files.json(
                    "data/snipers/nitro.json", "sniper", documents=False
                )
                giveawayjoiner = files.json(
                    "data/snipers/giveaway.json", "joiner", documents=False
                )
                if themesvar == "default":
                    pass
                else:
                    themesvar = themesvar[:-5]
                ui_user = f" {color.print_gradient('User:')} {'Luna#0000':<26}"
                ui_guilds = f" {color.print_gradient('Guilds:')} {'0':<24}"
                ui_friends = f" {color.print_gradient('Friends:')} {'0':<23}"
                ui_prefix = f" {color.print_gradient('Prefix:')} {prefix:<24}"
                ui_theme = f" {color.print_gradient('Theme:')} {themesvar:<25}"
                ui_commands = f" {color.print_gradient('Commands:')} {command_count - custom_command_count:<22}"
                ui_commands_custom = f" {color.print_gradient('Custom Commands:')} {custom_command_count:<15}"
                ui_nitro_sniper = f" {color.print_gradient('Nitro Sniper:')} {nitro_sniper}"
                ui_giveaway_sniper = f" {color.print_gradient('Giveaway Joiner:')} {giveawayjoiner}"
                ui_riskmode = f" {color.print_gradient('Riskmode:')} {riskmode}"
                ui_deletetimer = f" {color.print_gradient('Delete Timer:')} {deletetimer}"
                ui_startup = f" {color.print_gradient('Startup Status:')} {startup_status}"
                print()
                print(
                    f"               ═════════════ {color.print_gradient('User')} ═════════════      ═══════════ {color.print_gradient('Settings')} ═══════════"
                )
                print(f"               {ui_user}     {ui_prefix}")
                print(f"               {ui_guilds}     {ui_theme}")
                print(f"               {ui_friends}     {ui_nitro_sniper}")
                print(
                    f"               ════════════════════════════════      {ui_giveaway_sniper}"
                )
                print(
                    f"               ═════════════ {color.print_gradient('Luna')} ═════════════      {ui_riskmode}"
                )
                print(f"               {ui_commands}     {ui_deletetimer}")
                print(
                    f"               {ui_commands_custom}     {ui_startup}"
                )
                print(
                    f"               ════════════════════════════════      ════════════════════════════════\n"
                )
            else:
                print()
                print(
                    f"                           {color.print_gradient('[')}+{color.print_gradient('] CONNECTED')}"
                )
                print(
                    f"                           {color.print_gradient('[')}+{color.print_gradient(']')} Luna#0000 | {color.print_gradient('0')} Guilds | {color.print_gradient('0')} Friends"
                )
                print(
                    f"                           {color.print_gradient('[')}+{color.print_gradient(']')} {prefix}\n"
                )
        else:
            command_count = len(bot.commands)
            cog = bot.get_cog('Custom commands')
            try:
                custom = cog.get_commands()
                custom_command_count = 0
                for _ in custom:
                    custom_command_count += 1
            except BaseException:
                custom_command_count = 0
            print(motd.center(os.get_terminal_size().columns))
            if platinum:
                print("Platinum Build".center(os.get_terminal_size().columns))
            prefix = files.json(
                "data/config.json",
                "prefix", documents=False
            )
            console_mode = files.json(
                "data/console/console.json", "mode", documents=False
            )
            if console_mode == "2":
                riskmode = files.json(
                    "data/config.json", "risk_mode", documents=False
                )
                themesvar = files.json(
                    "data/config.json", "theme", documents=False
                )
                deletetimer = int(
                    files.json(
                        "data/config.json", "delete_timer", documents=False
                    )
                )
                startup_status = files.json(
                    "data/config.json", "startup_status", documents=False
                )
                nitro_sniper = files.json(
                    "data/snipers/nitro.json", "sniper", documents=False
                )
                giveawayjoiner = files.json(
                    "data/snipers/giveaway.json", "joiner", documents=False
                )
                if themesvar == "default":
                    pass
                else:
                    themesvar = themesvar[:-5]
                bot_user = f"{bot.user}"
                ui_user = f" {color.print_gradient('User:')} {bot_user:<26}"
                ui_guilds = f" {color.print_gradient('Guilds:')} {len(bot.guilds):<24}"
                ui_friends = f" {color.print_gradient('Friends:')} {len(bot.user.friends):<23}"
                ui_prefix = f" {color.print_gradient('Prefix:')} {prefix:<24}"
                ui_theme = f" {color.print_gradient('Theme:')} {themesvar:<25}"
                ui_commands = f" {color.print_gradient('Commands:')} {command_count - custom_command_count:<22}"
                ui_commands_custom = f" {color.print_gradient('Custom Commands:')} {custom_command_count:<15}"
                ui_nitro_sniper = f" {color.print_gradient('Nitro Sniper:')} {nitro_sniper}"
                ui_giveaway_sniper = f" {color.print_gradient('Giveaway Joiner:')} {giveawayjoiner}"
                ui_riskmode = f" {color.print_gradient('Riskmode:')} {riskmode}"
                ui_deletetimer = f" {color.print_gradient('Delete Timer:')} {deletetimer}"
                ui_startup = f" {color.print_gradient('Startup Status:')} {startup_status}"
                print()
                print(
                    f"               ═════════════ {color.print_gradient('User')} ═════════════      ═══════════ {color.print_gradient('Settings')} ═══════════"
                )
                print(f"               {ui_user}     {ui_prefix}")
                print(f"               {ui_guilds}     {ui_theme}")
                print(f"               {ui_friends}     {ui_nitro_sniper}")
                print(
                    f"               ════════════════════════════════      {ui_giveaway_sniper}"
                )
                print(
                    f"               ═════════════ {color.print_gradient('Luna')} ═════════════      {ui_riskmode}"
                )
                print(f"               {ui_commands}     {ui_deletetimer}")
                print(
                    f"               {ui_commands_custom}     {ui_startup}"
                )
                print(
                    f"               ════════════════════════════════      ════════════════════════════════\n"
                )
            else:
                print()
                print(
                    f"                           {color.print_gradient('[')}+{color.print_gradient('] CONNECTED')}"
                )
                print(
                    f"                           {color.print_gradient('[')}+{color.print_gradient(']')} "
                    f"{bot.user} | "
                    f"{color.print_gradient(f'{len(bot.guilds)}')} Guilds | "
                    f"{color.print_gradient(f'{len(bot.user.friends)}')} Friends"
                )
                print(
                    f"                           {color.print_gradient('[')}+{color.print_gradient(']')} {prefix}\n"
                )
        print(
            f"═══════════════════════════════════════════════════════════════════════════════════════════════════\n"
        )
        prints.message(
            f"{color.print_gradient(f'{command_count - custom_command_count}')} commands | {color.print_gradient(f'{custom_command_count}')} custom commands"
        )

    @commands.command(
        name="spacers",
        usage="<on/off>",
        description="Print spacers on/off",
    )
    async def spacers(self, ctx, mode: str):

        if mode == "on" or mode == "off":
            if mode == "off":
                config._global("data/console/console.json", "spacers", False)
            else:
                config._global("data/console/console.json", "spacers", True)
            prints.message(f"Print spacers » {mode}")
            await message_builder(ctx, description=f"```\nPrint spacers » {mode}```")
            luna.console(False, clear=True)
            if privacy:
                command_count = len(bot.commands)
                cog = bot.get_cog('Custom commands')
                try:
                    custom = cog.get_commands()
                    custom_command_count = 0
                    for _ in custom:
                        custom_command_count += 1
                except BaseException:
                    custom_command_count = 0
                print(motd.center(os.get_terminal_size().columns))
                if platinum:
                    print("Platinum Build".center(os.get_terminal_size().columns))
                prefix = files.json(
                    "data/config.json",
                    "prefix", documents=False
                )
                console_mode = files.json(
                    "data/console/console.json", "mode", documents=False
                )
                if console_mode == "2":
                    riskmode = files.json(
                        "data/config.json", "risk_mode", documents=False
                    )
                    themesvar = files.json(
                        "data/config.json", "theme", documents=False
                    )
                    deletetimer = int(
                        files.json(
                            "data/config.json", "delete_timer", documents=False
                        )
                    )
                    startup_status = files.json(
                        "data/config.json", "startup_status", documents=False
                    )
                    nitro_sniper = files.json(
                        "data/snipers/nitro.json", "sniper", documents=False
                    )
                    giveawayjoiner = files.json(
                        "data/snipers/giveaway.json", "joiner", documents=False
                    )
                    if themesvar == "default":
                        pass
                    else:
                        themesvar = themesvar[:-5]
                    ui_user = f" {color.print_gradient('User:')} {'Luna#0000':<26}"
                    ui_guilds = f" {color.print_gradient('Guilds:')} {'0':<24}"
                    ui_friends = f" {color.print_gradient('Friends:')} {'0':<23}"
                    ui_prefix = f" {color.print_gradient('Prefix:')} {prefix:<24}"
                    ui_theme = f" {color.print_gradient('Theme:')} {themesvar:<25}"
                    ui_commands = f" {color.print_gradient('Commands:')} {command_count - custom_command_count:<22}"
                    ui_commands_custom = f" {color.print_gradient('Custom Commands:')} {custom_command_count:<15}"
                    ui_nitro_sniper = f" {color.print_gradient('Nitro Sniper:')} {nitro_sniper}"
                    ui_giveaway_sniper = f" {color.print_gradient('Giveaway Joiner:')} {giveawayjoiner}"
                    ui_riskmode = f" {color.print_gradient('Riskmode:')} {riskmode}"
                    ui_deletetimer = f" {color.print_gradient('Delete Timer:')} {deletetimer}"
                    ui_startup = f" {color.print_gradient('Startup Status:')} {startup_status}"
                    print()
                    print(
                        f"               ═════════════ {color.print_gradient('User')} ═════════════      ═══════════ {color.print_gradient('Settings')} ═══════════"
                    )
                    print(f"               {ui_user}     {ui_prefix}")
                    print(f"               {ui_guilds}     {ui_theme}")
                    print(f"               {ui_friends}     {ui_nitro_sniper}")
                    print(
                        f"               ════════════════════════════════      {ui_giveaway_sniper}"
                    )
                    print(
                        f"               ═════════════ {color.print_gradient('Luna')} ═════════════      {ui_riskmode}"
                    )
                    print(f"               {ui_commands}     {ui_deletetimer}")
                    print(
                        f"               {ui_commands_custom}     {ui_startup}"
                    )
                    print(
                        f"               ════════════════════════════════      ════════════════════════════════\n"
                    )
                else:
                    print()
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient('] CONNECTED')}"
                    )
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient(']')} Luna#0000 | {color.print_gradient('0')} Guilds | {color.print_gradient('0')} Friends"
                    )
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient(']')} {prefix}\n"
                    )
            else:
                command_count = len(bot.commands)
                cog = bot.get_cog('Custom commands')
                try:
                    custom = cog.get_commands()
                    custom_command_count = 0
                    for _ in custom:
                        custom_command_count += 1
                except BaseException:
                    custom_command_count = 0
                print(motd.center(os.get_terminal_size().columns))
                if platinum:
                    print("Platinum Build".center(os.get_terminal_size().columns))
                prefix = files.json(
                    "data/config.json",
                    "prefix", documents=False
                )
                console_mode = files.json(
                    "data/console/console.json", "mode", documents=False
                )
                if console_mode == "2":
                    riskmode = files.json(
                        "data/config.json", "risk_mode", documents=False
                    )
                    themesvar = files.json(
                        "data/config.json", "theme", documents=False
                    )
                    deletetimer = int(
                        files.json(
                            "data/config.json", "delete_timer", documents=False
                        )
                    )
                    startup_status = files.json(
                        "data/config.json", "startup_status", documents=False
                    )
                    nitro_sniper = files.json(
                        "data/snipers/nitro.json", "sniper", documents=False
                    )
                    giveawayjoiner = files.json(
                        "data/snipers/giveaway.json", "joiner", documents=False
                    )
                    if themesvar == "default":
                        pass
                    else:
                        themesvar = themesvar[:-5]
                    bot_user = f"{bot.user}"
                    ui_user = f" {color.print_gradient('User:')} {bot_user:<26}"
                    ui_guilds = f" {color.print_gradient('Guilds:')} {len(bot.guilds):<24}"
                    ui_friends = f" {color.print_gradient('Friends:')} {len(bot.user.friends):<23}"
                    ui_prefix = f" {color.print_gradient('Prefix:')} {prefix:<24}"
                    ui_theme = f" {color.print_gradient('Theme:')} {themesvar:<25}"
                    ui_commands = f" {color.print_gradient('Commands:')} {command_count - custom_command_count:<22}"
                    ui_commands_custom = f" {color.print_gradient('Custom Commands:')} {custom_command_count:<15}"
                    ui_nitro_sniper = f" {color.print_gradient('Nitro Sniper:')} {nitro_sniper}"
                    ui_giveaway_sniper = f" {color.print_gradient('Giveaway Joiner:')} {giveawayjoiner}"
                    ui_riskmode = f" {color.print_gradient('Riskmode:')} {riskmode}"
                    ui_deletetimer = f" {color.print_gradient('Delete Timer:')} {deletetimer}"
                    ui_startup = f" {color.print_gradient('Startup Status:')} {startup_status}"
                    print()
                    print(
                        f"               ═════════════ {color.print_gradient('User')} ═════════════      ═══════════ {color.print_gradient('Settings')} ═══════════"
                    )
                    print(f"               {ui_user}     {ui_prefix}")
                    print(f"               {ui_guilds}     {ui_theme}")
                    print(f"               {ui_friends}     {ui_nitro_sniper}")
                    print(
                        f"               ════════════════════════════════      {ui_giveaway_sniper}"
                    )
                    print(
                        f"               ═════════════ {color.print_gradient('Luna')} ═════════════      {ui_riskmode}"
                    )
                    print(f"               {ui_commands}     {ui_deletetimer}")
                    print(
                        f"               {ui_commands_custom}     {ui_startup}"
                    )
                    print(
                        f"               ════════════════════════════════      ════════════════════════════════\n"
                    )
                else:
                    print()
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient('] CONNECTED')}"
                    )
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient(']')} "
                        f"{bot.user} | "
                        f"{color.print_gradient(f'{len(bot.guilds)}')} Guilds | "
                        f"{color.print_gradient(f'{len(bot.user.friends)}')} Friends"
                    )
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient(']')} {prefix}\n"
                    )
            print(
                f"═══════════════════════════════════════════════════════════════════════════════════════════════════\n"
            )
            prints.message(
                f"{color.print_gradient(f'{command_count - custom_command_count}')} commands | {color.print_gradient(f'{custom_command_count}')} custom commands"
            )
        else:
            await mode_error(ctx, "on or off")

    @commands.command(
        name="timestamp",
        usage="<on/off>",
        description="Print timestamp on/off",
    )
    async def timestamp(self, ctx, mode: str):

        if mode == "on" or mode == "off":
            if mode == "off":
                config._global("data/console/console.json", "timestamp", False)
            else:
                config._global("data/console/console.json", "timestamp", True)
            prints.message(f"Print timestamp » {mode}")
            await message_builder(ctx, description=f"```\nPrint timestamp » {mode}```")
            luna.console(False, clear=True)
            if privacy:
                command_count = len(bot.commands)
                cog = bot.get_cog('Custom commands')
                try:
                    custom = cog.get_commands()
                    custom_command_count = 0
                    for _ in custom:
                        custom_command_count += 1
                except BaseException:
                    custom_command_count = 0
                print(motd.center(os.get_terminal_size().columns))
                if platinum:
                    print("Platinum Build".center(os.get_terminal_size().columns))
                prefix = files.json(
                    "data/config.json",
                    "prefix", documents=False
                )
                console_mode = files.json(
                    "data/console/console.json", "mode", documents=False
                )
                if console_mode == "2":
                    riskmode = files.json(
                        "data/config.json", "risk_mode", documents=False
                    )
                    themesvar = files.json(
                        "data/config.json", "theme", documents=False
                    )
                    deletetimer = int(
                        files.json(
                            "data/config.json", "delete_timer", documents=False
                        )
                    )
                    startup_status = files.json(
                        "data/config.json", "startup_status", documents=False
                    )
                    nitro_sniper = files.json(
                        "data/snipers/nitro.json", "sniper", documents=False
                    )
                    giveawayjoiner = files.json(
                        "data/snipers/giveaway.json", "joiner", documents=False
                    )
                    if themesvar == "default":
                        pass
                    else:
                        themesvar = themesvar[:-5]
                    ui_user = f" {color.print_gradient('User:')} {'Luna#0000':<26}"
                    ui_guilds = f" {color.print_gradient('Guilds:')} {'0':<24}"
                    ui_friends = f" {color.print_gradient('Friends:')} {'0':<23}"
                    ui_prefix = f" {color.print_gradient('Prefix:')} {prefix:<24}"
                    ui_theme = f" {color.print_gradient('Theme:')} {themesvar:<25}"
                    ui_commands = f" {color.print_gradient('Commands:')} {command_count - custom_command_count:<22}"
                    ui_commands_custom = f" {color.print_gradient('Custom Commands:')} {custom_command_count:<15}"
                    ui_nitro_sniper = f" {color.print_gradient('Nitro Sniper:')} {nitro_sniper}"
                    ui_giveaway_sniper = f" {color.print_gradient('Giveaway Joiner:')} {giveawayjoiner}"
                    ui_riskmode = f" {color.print_gradient('Riskmode:')} {riskmode}"
                    ui_deletetimer = f" {color.print_gradient('Delete Timer:')} {deletetimer}"
                    ui_startup = f" {color.print_gradient('Startup Status:')} {startup_status}"
                    print()
                    print(
                        f"               ═════════════ {color.print_gradient('User')} ═════════════      ═══════════ {color.print_gradient('Settings')} ═══════════"
                    )
                    print(f"               {ui_user}     {ui_prefix}")
                    print(f"               {ui_guilds}     {ui_theme}")
                    print(f"               {ui_friends}     {ui_nitro_sniper}")
                    print(
                        f"               ════════════════════════════════      {ui_giveaway_sniper}"
                    )
                    print(
                        f"               ═════════════ {color.print_gradient('Luna')} ═════════════      {ui_riskmode}"
                    )
                    print(f"               {ui_commands}     {ui_deletetimer}")
                    print(
                        f"               {ui_commands_custom}     {ui_startup}"
                    )
                    print(
                        f"               ════════════════════════════════      ════════════════════════════════\n"
                    )
                else:
                    print()
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient('] CONNECTED')}"
                    )
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient(']')} Luna#0000 | {color.print_gradient('0')} Guilds | {color.print_gradient('0')} Friends"
                    )
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient(']')} {prefix}\n"
                    )
            else:
                command_count = len(bot.commands)
                cog = bot.get_cog('Custom commands')
                try:
                    custom = cog.get_commands()
                    custom_command_count = 0
                    for _ in custom:
                        custom_command_count += 1
                except BaseException:
                    custom_command_count = 0
                print(motd.center(os.get_terminal_size().columns))
                if platinum:
                    print("Platinum Build".center(os.get_terminal_size().columns))
                prefix = files.json(
                    "data/config.json",
                    "prefix", documents=False
                )
                console_mode = files.json(
                    "data/console/console.json", "mode", documents=False
                )
                if console_mode == "2":
                    riskmode = files.json(
                        "data/config.json", "risk_mode", documents=False
                    )
                    themesvar = files.json(
                        "data/config.json", "theme", documents=False
                    )
                    deletetimer = int(
                        files.json(
                            "data/config.json", "delete_timer", documents=False
                        )
                    )
                    startup_status = files.json(
                        "data/config.json", "startup_status", documents=False
                    )
                    nitro_sniper = files.json(
                        "data/snipers/nitro.json", "sniper", documents=False
                    )
                    giveawayjoiner = files.json(
                        "data/snipers/giveaway.json", "joiner", documents=False
                    )
                    if themesvar == "default":
                        pass
                    else:
                        themesvar = themesvar[:-5]
                    bot_user = f"{bot.user}"
                    ui_user = f" {color.print_gradient('User:')} {bot_user:<26}"
                    ui_guilds = f" {color.print_gradient('Guilds:')} {len(bot.guilds):<24}"
                    ui_friends = f" {color.print_gradient('Friends:')} {len(bot.user.friends):<23}"
                    ui_prefix = f" {color.print_gradient('Prefix:')} {prefix:<24}"
                    ui_theme = f" {color.print_gradient('Theme:')} {themesvar:<25}"
                    ui_commands = f" {color.print_gradient('Commands:')} {command_count - custom_command_count:<22}"
                    ui_commands_custom = f" {color.print_gradient('Custom Commands:')} {custom_command_count:<15}"
                    ui_nitro_sniper = f" {color.print_gradient('Nitro Sniper:')} {nitro_sniper}"
                    ui_giveaway_sniper = f" {color.print_gradient('Giveaway Joiner:')} {giveawayjoiner}"
                    ui_riskmode = f" {color.print_gradient('Riskmode:')} {riskmode}"
                    ui_deletetimer = f" {color.print_gradient('Delete Timer:')} {deletetimer}"
                    ui_startup = f" {color.print_gradient('Startup Status:')} {startup_status}"
                    print()
                    print(
                        f"               ═════════════ {color.print_gradient('User')} ═════════════      ═══════════ {color.print_gradient('Settings')} ═══════════"
                    )
                    print(f"               {ui_user}     {ui_prefix}")
                    print(f"               {ui_guilds}     {ui_theme}")
                    print(f"               {ui_friends}     {ui_nitro_sniper}")
                    print(
                        f"               ════════════════════════════════      {ui_giveaway_sniper}"
                    )
                    print(
                        f"               ═════════════ {color.print_gradient('Luna')} ═════════════      {ui_riskmode}"
                    )
                    print(f"               {ui_commands}     {ui_deletetimer}")
                    print(
                        f"               {ui_commands_custom}     {ui_startup}"
                    )
                    print(
                        f"               ════════════════════════════════      ════════════════════════════════\n"
                    )
                else:
                    print()
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient('] CONNECTED')}"
                    )
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient(']')} "
                        f"{bot.user} | "
                        f"{color.print_gradient(f'{len(bot.guilds)}')} Guilds | "
                        f"{color.print_gradient(f'{len(bot.user.friends)}')} Friends"
                    )
                    print(
                        f"                           {color.print_gradient('[')}+{color.print_gradient(']')} {prefix}\n"
                    )
            print(
                f"═══════════════════════════════════════════════════════════════════════════════════════════════════\n"
            )
            prints.message(
                f"{color.print_gradient(f'{command_count - custom_command_count}')} commands | {color.print_gradient(f'{custom_command_count}')} custom commands"
            )
        else:
            await mode_error(ctx, "on or off")

    # @commands.command(name="reload", usage="", description="Reload custom commands")
    # async def reload(self, ctx):
    #
    #     path = getattr(sys, '_MEIPASS', os.getcwd())
    #     cogs_path = path + "\\cogs"
    #     luna.loader_check()
    #     for filename in os.listdir(cogs_path):
    #         if filename.endswith(".py"):
    #             try:
    #                 bot.reload_extension(f"cogs.{filename[:-3]}")
    #             except BaseException:
    #                 bot.load_extension(f"cogs.{filename[:-3]}")
    #     prints.message(f"Reloaded custom commands")
    #     await message_builder(ctx, description=f"```\nReloaded custom commands```")
    #     # prefix = files.json("data/config.json", "prefix", documents=False)
    #     # await message_builder(ctx, description=f"```\nReload has been disabled until further notice, use {prefix}restart instead```")

    @commands.command(
        name="newcmd",
        usage="<name>",
        description="Create new command"
    )
    async def newcmd(self, ctx, name: str):

        content = f"""
@commands.command(
    name = "{name}",
    usage="",
    description = "New command"
    )
async def {name}(self, luna):

    await luna.send("Documentation for custom commands can be found here: https://www.team-luna.org/documentation")
"""
        files.write_file(f"data/scripts/{name}.py", content, documents=False, append=True)
        await message_builder(ctx, description=f"```\nCreated new custom command in \"data/scripts/{name}.py\"```")

    @commands.command(
        name="darkmode",
        usage="",
        description="Discord darkmode"
    )
    async def darkmode(self, luna):

        requests.patch(
            f'https://discord.com/api/{api_version}/users/@me/settings',
            json={
                'theme': "dark"
            },
            headers={
                'authorization': user_token,
                'user-agent': 'Mozilla/5.0'
            }
        )
        await message_builder(luna, description=f"```\nChanged to darkmode```")

    @commands.command(
        name="lightmode",
        usage="",
        description="Discord lightmode"
    )
    async def lightmode(self, luna):

        requests.patch(
            f'https://discord.com/api/{api_version}/users/@me/settings',
            json={
                'theme': "light"
            },
            headers={
                'authorization': user_token,
                'user-agent': 'Mozilla/5.0'
            }
        )
        await message_builder(luna, description=f"```\nChanged to lightmode```")


bot.add_cog(SettingsCog(bot))


class ShareCog(commands.Cog, name="Share commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="share",
        usage="<on/off>",
        description="Share on/off"
    )
    async def share(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Share » {mode}")
            config.share(mode)
            await message_builder(luna, description=f"```\nShare » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="shareuser",
        usage="<@member>",
        description="Set the member for sharing"
    )
    async def shareuser(self, luna, user_id):

        if "<@!" and ">" in user_id:
            user_id = user_id.replace("<@!", "").replace(">", "")
            user = await self.bot.fetch_user(user_id)
        else:
            user = await self.bot.fetch_user(user_id)
        if user == self.bot.user:
            await error_builder(luna, description=f"```\nYou can't use share on yourself```")
            return
        config.user_id(user.id)
        prints.message(f"Share user set to » {user}")
        await message_builder(luna, description=f"```\nShare user set to » {user}```")

    @commands.command(
        name="sharenone",
        usage="",
        description="Share member to none"
    )
    async def sharenone(self, luna):

        config.user_id("")
        prints.message(f"Share user set to » None")
        await message_builder(luna, description=f"```\nShare user set to » None```")


bot.add_cog(ShareCog(bot))


class EncodeCog(commands.Cog, name="Encode commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="encode_cea256",
        usage="<key> <text>",
        description="cea256"
    )
    async def encode_cea256(self, luna, key, *, text):
        if len(key) != 32:
            await luna.send("Invalid key, needs to be 256-bits / 32 Chars in length")
            return
        encoded = Encryption(key).CEA256(text)
        await luna.send(f"{encoded}")

    @commands.command(
        name="encode_base64",
        usage="<text>",
        description="base64"
    )
    async def encode_base64(self, luna, *, text: str):
        enc = base64.b64encode('{}'.format(text).encode('ascii'))
        encoded = str(enc)
        encoded = encoded[2:len(encoded) - 1]
        await luna.send(f"{encoded}")

    @commands.command(
        name="encode_leet",
        usage="<text>",
        description="leet"
    )
    async def encode_leet(self, luna, *, text: str):
        encoded = text.replace(
            'e',
            '3'
        ).replace(
            'a',
            '4'
        ).replace(
            'i',
            '!'
        ).replace(
            'u',
            '|_|'
        ).replace(
            'U',
            '|_|'
        ).replace(
            'E',
            '3'
        ).replace(
            'I',
            '!'
        ).replace(
            'A',
            '4'
        ).replace(
            'o',
            '0'
        ).replace(
            'O',
            '0'
        ).replace(
            't',
            '7'
        ).replace(
            'T',
            '7'
        ).replace(
            'l',
            '1'
        ).replace(
            'L',
            '1'
        ).replace(
            'k',
            '|<'
        ).replace(
            'K',
            '|<'
        ).replace(
            'CK',
            'X'
        ).replace(
            'ck',
            'x'
        ).replace(
            'Ck',
            'X'
        ).replace(
            'cK',
            'x'
        )
        await luna.send(f"{encoded}")

    @commands.command(
        name="encode_md5",
        usage="<text>",
        description="md5 (oneway)"
    )
    async def encode_md5(self, luna, *, text: str):
        enc = hashlib.md5(text.encode())
        encoded = enc.hexdigest()
        await luna.send(f"{encoded}")

    @commands.command(
        name="encode_sha1",
        usage="<text>",
        description="sha1 (oneway)"
    )
    async def encode_sha1(self, luna, *, text: str):
        enc = hashlib.sha1(text.encode())
        encoded = enc.hexdigest()
        await luna.send(f"{encoded}")

    @commands.command(
        name="encode_sha224",
        usage="<text>",
        description="sha224 (oneway)"
    )
    async def encode_sha224(self, luna, *, text: str):
        enc = hashlib.sha3_224(text.encode())
        encoded = enc.hexdigest()
        await luna.send(f"{encoded}")

    @commands.command(
        name="encode_sha256",
        usage="<text>",
        description="sha256 (oneway)"
    )
    async def encode_sha256(self, luna, *, text: str):
        enc = hashlib.sha3_256(text.encode())
        encoded = enc.hexdigest()
        await luna.send(f"{encoded}")

    @commands.command(
        name="encode_sha384",
        usage="<text>",
        description="sha384 (oneway)"
    )
    async def encode_sha384(self, luna, *, text: str):
        enc = hashlib.sha3_384(text.encode())
        encoded = enc.hexdigest()
        await luna.send(f"{encoded}")

    @commands.command(
        name="encode_sha512",
        usage="<text>",
        description="sha512 (oneway)"
    )
    async def encode_sha512(self, luna, *, text: str):
        enc = hashlib.sha3_512(text.encode())
        encoded = enc.hexdigest()
        await luna.send(f"{encoded}")


bot.add_cog(EncodeCog(bot))


class DecodeCog(commands.Cog, name="Decode commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="decode_cea256",
        usage="<key> <text>",
        description="cea256"
    )
    async def decode_cea256(self, luna, key, *, text):

        if len(key) != 32:
            await luna.send("Invalid key, needs to be 256-bits / 32 Chars in length")
            return
        try:
            decrypted = Decryption(key).CEA256(text)
        except BaseException:
            await luna.send("Decryption failed, make sure the key is correct")
        else:
            await luna.send(f"{decrypted}")

    @commands.command(
        name="decode_base64",
        usage="<text>",
        description="base64"
    )
    async def decode_base64(self, luna, *, text: str):

        dec = base64.b64decode('{}'.format(text).encode('ascii'))
        decoded = str(dec)
        decoded = decoded[2:len(decoded) - 1]
        await luna.send(f"{decoded}")

    @commands.command(
        name="decode_leet",
        usage="<text>",
        description="leet"
    )
    async def decode_leet(self, luna, *, text: str):

        encoded = text.replace(
            '3',
            'e'
        ).replace(
            '4',
            'a'
        ).replace(
            '!',
            'i'
        ).replace(
            '|_|',
            'u'
        ).replace(
            '|_|',
            'U'
        ).replace(
            '3',
            'E'
        ).replace(
            '!',
            'I'
        ).replace(
            '4',
            'A'
        ).replace(
            '0',
            'o'
        ).replace(
            '0',
            'O'
        ).replace(
            '7',
            't'
        ).replace(
            '7',
            'T'
        ).replace(
            '1',
            'l'
        ).replace(
            '1',
            'L'
        ).replace(
            '|<',
            'k'
        ).replace(
            '|<',
            'K'
        ).replace(
            'X',
            'CK'
        ).replace(
            'x',
            'ck'
        ).replace(
            'X',
            'Ck'
        ).replace(
            'x',
            'cK'
        )
        await luna.send(f"{encoded}")


bot.add_cog(DecodeCog(bot))


class GiveawayCog(commands.Cog, name="Giveaway settings"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="giveawayjoiner",
        usage="<on/off>",
        description="Giveaway sniper"
    )
    async def giveawayjoiner(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Giveaway sniper » {mode}")
            config.giveaway.joiner(mode)
            await message_builder(luna, description=f"```\nGiveaway sniper » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="delay",
        usage="<minutes>",
        description="Delay in minutes"
    )
    async def delay(self, luna, minute: int):

        await message_builder(luna, description=f"```\nGiveaway joiner delay » {str(minute)} minute/s```")
        prints.message(f"Auto delete timer » {str(minute)}")
        config.giveaway.delay_in_minutes(f"{minute}")

    @commands.command(
        name="giveawayguild",
        usage="<on/off>",
        description="Giveaway server joiner"
    )
    async def giveawayguild(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Server joiner » {mode}")
            config.giveaway.guild_joiner(mode)
            await message_builder(luna, description=f"```\nServer joiner » {mode}```")
        else:
            await mode_error(luna, "on or off")


bot.add_cog(GiveawayCog(bot))


class CryptoCog(commands.Cog, name="Cryptocurrency commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="crypto",
        usage="<crypto>",
        description="Cryptocurrency prices"
    )
    async def crypto(self, luna, crypto: str):
        request = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={crypto}&tsyms=USD,EUR,GBP,CHF,CAD,AUD,RUB,JPY,CNY,INR,TRY,PLN'
        )
        data = request.json()
        usd = data['USD']
        eur = data['EUR']
        gbp = data['GBP']
        chf = data['CHF']
        cad = data['CAD']
        aud = data['AUD']
        rub = data['RUB']
        jpy = data['JPY']
        cny = data['CNY']
        inr = data['INR']
        pln = data['PLN']
        __try = data['TRY']
        desc = f"""```
USD: {usd}
EUR: {eur}
GBP: {gbp}
CHF: {chf}
CAD: {cad}
AUD: {aud}
RUB: {rub}
JPY: {jpy}
CNY: {cny}
INR: {inr}
TRY: {__try}
PLN: {pln}```"""
        await message_builder(luna, title=crypto, description=desc)


bot.add_cog(CryptoCog(bot))


class CustomizeCog(commands.Cog, name="Customization commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="ctitle",
        usage="<title>",
        description="Customize the title"
    )
    async def ctitle(self, luna, *, newtitle: str):

        if files.json(
                "data/config.json",
                "theme",
                documents=False
        ) == "default":
            await error_builder(
                luna,
                f"```\nYou can't change the title if you're using the default theme\n```"
                f"```\nPlease change the theme first with {get_prefix()}theme\n\n"
                f"({get_prefix()}themes to show all available themes)```"
            )
        else:
            prints.message(f"Changed title to » {color.print_gradient(f'{newtitle}')}")
            if newtitle == "None":
                config.title("")
            else:
                config.title(f"{newtitle}")
            await message_builder(luna, description=f"```\nChanged title to » {newtitle}```")

    @commands.command(
        name="cfooter",
        usage="<footer>",
        description="Customize the footer"
    )
    async def cfooter(self, luna, *, newfooter: str):

        if files.json(
                "data/config.json",
                "theme",
                documents=False
        ) == "default":
            await error_builder(
                luna,
                f"```\nYou can't change the footer if you're using the default theme\n```"
                f"```\nPlease change the theme first with {get_prefix()}theme\n\n"
                f"({get_prefix()}themes to show all available themes)```"
            )
        else:
            prints.message(
                f"Changed footer to » {color.print_gradient(f'{newfooter}')}"
            )
            if newfooter == "None":
                config.footer("")
            else:
                config.footer(f"{newfooter}")
            await message_builder(luna, description=f"```\nChanged footer to » {newfooter}```")

    @commands.command(
        name="description",
        aliases=['cdescription'],
        usage="<on/off>",
        description="Hide/Show <> | []"
    )
    async def description(self, luna, mode: str):

        if files.json(
                "data/config.json",
                "theme",
                documents=False
        ) == "default":
            await error_builder(
                luna,
                f"```\nYou can't change the description mode if you're using the default theme\n```"
                f"```\nPlease change the theme first with {get_prefix()}theme\n\n"
                f"({get_prefix()}themes to show all available themes)```"
            )
        else:
            if mode == "on":
                prints.message(
                    f"Changed description to » {color.print_gradient('on')}"
                )
                config.description(True)
                await message_builder(luna, description=f"```\nChanged description to » on```")
            elif mode == "off":
                prints.message(
                    f"Changed description to » {color.print_gradient('off')}"
                )
                config.description(False)
                await message_builder(luna, description=f"```\nChanged description to » off```")
            else:
                await mode_error(luna, "on or off")


bot.add_cog(CustomizeCog(bot))


class HScrollerCog(commands.Cog, name="HScroller commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="anime",
        usage="",
        description="High quality anime"
    )
    async def anime(self, luna):
        r = requests.post(
            "http://project-atlas.xyz:8880/api/FetchMediaContent?amount=1&NSFWEnabled=false&NSFWType=None"
        ).json()
        await message_builder(luna, large_image=str(r[0]['FileURL']))

    @commands.command(
        name="nsfw",
        usage="",
        description="High quality nsfw"
    )
    async def nsfw(self, luna):
        r = requests.post(
            "http://project-atlas.xyz:8880/api/FetchMediaContent?amount=1&NSFWEnabled=true&NSFWType=nsfw"
        ).json()
        await message_builder(luna, large_image=str(r[0]['FileURL']))

    @commands.command(
        name="yuri",
        usage="",
        description="High quality yuri"
    )
    async def yuri(self, luna):
        r = requests.post(
            "http://project-atlas.xyz:8880/api/FetchMediaContent?amount=1&NSFWEnabled=true&NSFWType=yuri"
        ).json()
        await message_builder(luna, large_image=str(r[0]['FileURL']))


bot.add_cog(HScrollerCog(bot))


class HentaiCog(commands.Cog, name="Hentai commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="hrandom",
        usage="",
        description="Random hentai"
    )
    async def hrandom(self, luna):
        r = requests.get("http://api.nekos.fun:8080/api/hentai").json()
        await message_builder(luna, large_image=str(r['image']))

    @commands.command(
        name="hass",
        usage="",
        description="Random hentai ass"
    )
    async def hass(self, luna):
        r = requests.get(
            "https://nekobot.xyz/api/image?type=hass"
        ).json()
        await message_builder(luna, large_image=str(r['message']))

    @commands.command(
        name="ass",
        usage="",
        description="Random ass"
    )
    async def ass(self, luna):
        r = requests.get(
            "http://api.nekos.fun:8080/api/ass"
        ).json()
        await message_builder(luna, large_image=str(r['image']))

    @commands.command(
        name="boobs",
        usage="",
        description="Real breasts"
    )
    async def ass(self, luna):
        r = requests.get(
            "http://api.nekos.fun:8080/api/boobs"
        ).json()
        await message_builder(luna, large_image=str(r['image']))

    @commands.command(
        name="pussy",
        usage="",
        description="Random pussy"
    )
    async def pussy(self, luna):
        r = requests.get(
            "http://api.nekos.fun:8080/api/pussy"
        ).json()
        await message_builder(luna, large_image=str(r['image']))

    @commands.command(
        name="4k",
        usage="",
        description="4k NSFW"
    )
    async def fk(self, luna):
        r = requests.get(
            "http://api.nekos.fun:8080/api/4k"
        ).json()
        await message_builder(luna, large_image=str(r['image']))

    @commands.command(
        name="cum",
        usage="",
        description="Baby gravy!"
    )
    async def cum(self, luna):
        r = requests.get(
            "http://api.nekos.fun:8080/api/cum"
        ).json()
        await message_builder(luna, large_image=str(r['image']))

    @commands.command(
        name="hblowjob",
        usage="",
        description="Self explainable"
    )
    async def blowjob(self, luna):
        r = requests.get(
            "http://api.nekos.fun:8080/api/blowjob"
        ).json()
        await message_builder(luna, large_image=str(r['image']))

    @commands.command(
        name="ahegao",
        usage="",
        description="Ahegao"
    )
    async def ahegao(self, luna):
        r = requests.get(
            "http://api.nekos.fun:8080/api/gasm"
        ).json()
        await message_builder(luna, large_image=str(r['image']))

    @commands.command(
        name="lewd",
        usage="",
        description="Lewd loli"
    )
    async def lewd(self, luna):
        r = requests.get(
            "http://api.nekos.fun:8080/api/lewd"
        ).json()
        await message_builder(luna, large_image=str(r['image']))

    @commands.command(
        name="feet",
        usage="",
        description="Random feet"
    )
    async def feet(self, luna):
        r = requests.get(
            "http://api.nekos.fun:8080/api/feet"
        ).json()
        await message_builder(luna, large_image=str(r['image']))

    @commands.command(
        name="feet",
        usage="",
        description="Random feet"
    )
    async def feet(self, luna):
        r = requests.get(
            "http://api.nekos.fun:8080/api/feet"
        ).json()
        await message_builder(luna, large_image=str(r['image']))

    @commands.command(
        name="lesbian",
        usage="",
        description="Girls rule!"
    )
    async def lesbian(self, luna):
        r = requests.get(
            "http://api.nekos.fun:8080/api/lesbian"
        ).json()
        await message_builder(luna, large_image=str(r['image']))

    @commands.command(
        name="spank",
        usage="",
        description="NSFW for butts"
    )
    async def spank(self, luna):
        r = requests.get(
            "http://api.nekos.fun:8080/api/spank"
        ).json()
        await message_builder(luna, large_image=str(r['image']))

    @commands.command(
        name="hwallpaper",
        usage="",
        description="99% SFW"
    )
    async def hwallpaper(self, luna):
        r = requests.get(
            "http://api.nekos.fun:8080/api/wallpaper"
        ).json()
        await message_builder(luna, large_image=str(r['image']))


bot.add_cog(HentaiCog(bot))


class OnMember(commands.Cog, name="on member events"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if anti_raid is True:
            guilds = files.json(
                "data/protections/config.json", "guilds", documents=False
            )
            if member.guild.id in guilds:
                try:
                    guild = member.guild
                    async for i in guild.audit_logs(limit=1, action=discord.AuditLogAction.bot_add):
                        if member.guild.id in whitelisted_users.keys(
                        ) and i.user.id in whitelisted_users[member.guild.id].keys():
                            return
                        else:
                            prints.message(
                                f"{member.name}#{member.discriminator} banned by Anti-Raid"
                            )
                            await guild.ban(member, reason="Luna Anti-Raid")
                except Exception as e:
                    print(e)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if anti_raid is True:
            guilds = files.json(
                "data/protections/config.json", "guilds", documents=False
            )
            if member.guild.id in guilds:
                try:
                    guild = member.guild
                    async for i in guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
                        if guild.id in whitelisted_users.keys() and i.user.id in whitelisted_users[
                            guild.id
                        ].keys() and i.user.id is not self.bot.user.id:
                            prints.message(
                                f"{i.user.name}#{i.user.discriminator} not banned"
                            )
                        else:
                            prints.message(
                                f"{i.user.name}#{i.user.discriminator} banned by Anti-Raid"
                            )
                            await guild.ban(i.user, reason="Luna Anti-Raid")
                except Exception as e:
                    print(e)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        if bot.user is user:
            if files.json(
                    "data/notifications/toasts.json",
                    "guildevents",
                    documents=False
            ) == "on" and files.json(
                "data/notifications/toasts.json",
                "toasts",
                documents=False
            ) == "on":
                notify.toast(
                    f"You have been banned\nServer »  {guild.name}"
                )
                print()
                prints.message("You have been banned")
                prints.message(f"Server » {guild.name}")
                print()
            if files.json(
                    "data/webhooks/webhooks.json",
                    "guildevents",
                    documents=False
            ) == "on" and files.json(
                "data/webhooks/webhooks.json",
                "webhooks",
                documents=False
            ) == "on" and not webhook.ghostpings_url() == "webhook-url-here":
                notify.webhook(
                    url=webhook.ghostpings_url(),
                    name="Ban",
                    description=f"You have been banned\nServer »  {guild.name}"
                )

    # @commands.Cog.listener()
    # async def on_guild_channel_create(self, channel):
    #     if "ticket" in channel.name.lower() and channel.permissions_for(
    #             channel.guild.me
    #     ).read_messages:
    #         if files.json(
    #                 "data/notifications/toasts.json",
    #                 "guildevents",
    #                 documents=False
    #         ) == "on" and files.json(
    #             "data/notifications/toasts.json",
    #             "toasts",
    #             documents=False
    #         ) == "on":
    #             notify.toast(
    #                 f"New Ticket\nServer » {channel.guild.name}\nChannel » {channel.name}"
    #             )
    #             print()
    #             prints.message(f"{color.print_gradient('New Ticket')}")
    #             prints.message(
    #                 f"Server  | {color.print_gradient(f'{channel.guild.name}')}"
    #             )
    #             prints.message(
    #                 f"Channel | {color.print_gradient(f'{channel.name}')}"
    #             )
    #             print()
    #         if files.json(
    #                 "data/webhooks/webhooks.json",
    #                 "guildevents",
    #                 documents=False
    #         ) == "on" and files.json(
    #             "data/webhooks/webhooks.json",
    #             "webhooks",
    #             documents=False
    #         ) == "on" and not webhook.ghostpings_url() == "webhook-url-here":
    #             notify.webhook(
    #                 url=webhook.ghostpings_url(),
    #                 name="New Ticket",
    #                 description=f"New Ticket\nServer » {channel.guild.name}\nChannel » {channel.name}"
    #             )

    @commands.Cog.listener()
    async def on_relationship_add(self, relationship):
        if isinstance(relationship.type, discord.RelationshipType.incoming_request):
            if files.json(
                    "data/notifications/toasts.json",
                    "friendevents",
                    documents=False
            ) == "on" and files.json(
                "data/notifications/toasts.json",
                "toasts",
                documents=False
            ) == "on":
                notify.toast(
                    f"Incoming Friend Request\nUser » {relationship.user}\nID » {relationship.user.id}"
                )
                print()
                prints.message("Incoming Friend Request")
                prints.message(
                    f"User    | {color.print_gradient(f'{relationship.user}')}"
                )
                prints.message(
                    f"ID      | {color.print_gradient(f'{relationship.user.id}')}"
                )
                print()
            if files.json(
                    "data/webhooks/webhooks.json",
                    "friendevents",
                    documents=False
            ) == "on" and files.json(
                "data/webhooks/webhooks.json",
                "webhooks",
                documents=False
            ) == "on" and not webhook.ghostpings_url() == "webhook-url-here":
                notify.webhook(
                    url=webhook.ghostpings_url(),
                    name="friendevents",
                    description=f"Incoming Friend Request\nUser » {relationship.user}\nID » {relationship.user.id}"
                )
        if isinstance(relationship.type, discord.RelationshipType.friend):
            if files.json(
                    "data/notifications/toasts.json",
                    "friendevents",
                    documents=False
            ) == "on" and files.json(
                "data/notifications/toasts.json",
                "toasts",
                documents=False
            ) == "on":
                notify.toast(
                    f"New Friend\nUser » {relationship.user}\nID » {relationship.user.id}"
                )
                print()
                prints.message("New Friend")
                prints.message(
                    f"User    | {color.print_gradient(f'{relationship.user}')}"
                )
                prints.message(
                    f"ID      | {color.print_gradient(f'{relationship.user.id}')}"
                )
                print()
            if files.json(
                    "data/webhooks/webhooks.json",
                    "friendevents",
                    documents=False
            ) == "on" and files.json(
                "data/webhooks/webhooks.json",
                "webhooks",
                documents=False
            ) == "on" and not webhook.ghostpings_url() == "webhook-url-here":
                notify.webhook(
                    url=webhook.ghostpings_url(),
                    name="friendevents",
                    description=f"New Friend\nUser » {relationship.user}\nID » {relationship.user.id}"
                )

    @commands.Cog.listener()
    async def on_relationship_remove(self, relationship):
        if isinstance(relationship.type, discord.RelationshipType.outgoing_request):
            if files.json(
                    "data/notifications/toasts.json",
                    "friendevents",
                    documents=False
            ) == "on" and files.json(
                "data/notifications/toasts.json",
                "toasts",
                documents=False
            ) == "on":
                notify.toast(
                    f"Outgoing Friend Request\nUser » {relationship.user}\nID » {relationship.user.id}"
                )
                print()
                prints.message("Outgoing Friend Request")
                prints.message(
                    f"User    | {color.print_gradient(f'{relationship.user}')}"
                )
                prints.message(
                    f"ID      | {color.print_gradient(f'{relationship.user.id}')}"
                )
                print()
            if files.json(
                    "data/webhooks/webhooks.json",
                    "friendevents",
                    documents=False
            ) == "on" and files.json(
                "data/webhooks/webhooks.json",
                "webhooks",
                documents=False
            ) == "on" and not webhook.ghostpings_url() == "webhook-url-here":
                notify.webhook(
                    url=webhook.ghostpings_url(),
                    name="friendevents",
                    description=f"Outgoing Friend Request\nUser » {relationship.user}\nID » {relationship.user.id}"
                )

        if isinstance(relationship.type, discord.RelationshipType.blocked):
            if files.json(
                    "data/notifications/toasts.json",
                    "friendevents",
                    documents=False
            ) == "on" and files.json(
                "data/notifications/toasts.json",
                "toasts",
                documents=False
            ) == "on":
                notify.toast(
                    f"Blocked/Removed Friend\nUser » {relationship.user}\nID » {relationship.user.id}"
                )
                print()
                prints.message("Blocked/Removed Friend")
                prints.message(
                    f"User    | {color.print_gradient(f'{relationship.user}')}"
                )
                prints.message(
                    f"ID      | {color.print_gradient(f'{relationship.user.id}')}"
                )
                print()
            if files.json(
                    "data/webhooks/webhooks.json",
                    "friendevents",
                    documents=False
            ) == "on" and files.json(
                "data/webhooks/webhooks.json",
                "webhooks",
                documents=False
            ) == "on" and not webhook.ghostpings_url() == "webhook-url-here":
                notify.webhook(
                    url=webhook.ghostpings_url(),
                    name="friendevents",
                    description=f"Blocked/Removed Friend\nUser » {relationship.user}\nID » {relationship.user.id}"
                )


bot.add_cog(OnMember(bot))


class SniperCog(commands.Cog, name="Sniper settings"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="nitrosniper",
        usage="<on/off>",
        description="Nitro sniper"
    )
    async def nitrosniper(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Nitro sniper » {mode}")
            config.nitro.sniper(mode)
            await message_builder(luna, description=f"```\nNitro sniper » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="privsniper",
        usage="<on/off>",
        description="Privnote sniper"
    )
    async def privsniper(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Privnote sniper » {mode}")
            config.privnote.sniper(mode)
            await message_builder(luna, description=f"```\nPrivnote sniper » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="snipercharge",
        usage="<on/off>",
        description="Sniper visual charge"
    )
    async def snipercharge(self, luna, mode: str):
        if mode == "on" or mode == "off":
            prints.message(f"Nitro ratelimit » {mode}")
            config._global("data/snipers/nitro.json", "charge", mode)
            await message_builder(luna, description=f"```\nNitro ratelimit » {mode}```")
            if mode == "on":
                startup_status = files.json(
                "data/config.json", "startup_status", documents=False
                )
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7',
                    'Content-Type': 'application/json',
                    'Authorization': user_token,
                }
                request = requests.Session()
                setting = {
                    'status': startup_status,
                    "custom_status": {"text": f"Ratelimit: [#####]"}
                }
                request.patch(f"https://discord.com/api/{api_version}/users/@me/settings",headers=headers, json=setting, timeout=10)
            else:
                startup_status = files.json(
                    "data/config.json", "startup_status", documents=False
                )
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7',
                    'Content-Type': 'application/json',
                    'Authorization': user_token,
                }
                request = requests.Session()
                setting = {
                    'status': startup_status,
                    "custom_status": {"text": f""}
                }
                request.patch(f"https://discord.com/api/{api_version}/users/@me/settings",headers=headers, json=setting, timeout=10)
        else:
            await mode_error(luna, "on or off")


bot.add_cog(SniperCog(bot))


class ThemeCog(commands.Cog, name="Theme command"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="theme",
        usage="<theme>",
        description="Change theme"
    )
    async def theme(self, luna, theme: str):

        theme = theme.replace('.json', '')
        if theme == "default":
            config.theme(theme)
            await message_builder(luna, description=f"```\nChanged theme to » {theme}```")
        else:
            if files.file_exist(f"data/themes/{theme}.json", documents=False):
                config.theme(theme)
                await message_builder(luna, description=f"```\nChanged theme to » {theme}```")
            else:
                await error_builder(luna, description=f"```\nThere is no theme called » {theme}```")


bot.add_cog(ThemeCog(bot))


class ThemesCog(commands.Cog, name="Theme commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="newtheme",
        usage="<name>",
        description="Create a theme"
    )
    async def newtheme(self, luna, themename: str):

        themename = themename.replace('.json', '')
        if files.file_exist(f"data/themes/{themename}.json", documents=False):
            await error_builder(luna, description=f"```\nA theme already exists with the name » {themename}```")
        else:
            prints.message(f"Created theme » {themename}")
            data = {
                "title": "Luna",
                "footer": "www.team-luna.org",
                "description": True
            }
            files.write_json(
                f"data/themes/{themename}.json", data, documents=False
            )
            config.theme(f"{themename}")
            await message_builder(luna, description=f"```\nCreated theme » {themename}```")

    @commands.command(
        name="edittheme",
        usage="<name>",
        description="Edit current theme name"
    )
    async def edittheme(self, luna, themename: str):

        themesvar = files.json("data/config.json", "theme", documents=False)
        if files.file_exist(f"data/themes/{themename}.json", documents=False):
            await error_builder(luna, description=f"```\nA theme already exists with the name » {themename}```")
        else:
            prints.message(
                f"Edited theme name to » {themename}"
            )
            os.rename(
                f"data/themes/{themesvar}",
                f"data/themes/{themename}.json"
            )
            config.theme(f"{themename}")
            await message_builder(luna, description=f"```\nEdited theme name to » {themename}```")

    @commands.command(
        name="deltheme",
        usage="<name>",
        description="Delete a theme"
    )
    async def deltheme(self, luna, themename: str):

        themename = themename.replace('.json', '')
        themesvar = files.json("data/config.json", "theme", documents=False)
        if themesvar == f"{themename}.json":
            await error_builder(luna, description="```\nYou cant delete the theme you are currently using```")
            return
        if files.file_exist(f"data/themes/{themename}.json", documents=False):
            files.remove(f"data/themes/{themename}.json", documents=False)
            prints.message(f"Deleted theme » {themename}")
            await message_builder(luna, description=f"```\nDeleted theme » {themename}```")
        else:
            await error_builder(luna, description=f"```\nThere is no theme called » {themename}```")

    @commands.command(
        name="sendtheme",
        usage="",
        description="Send the current theme file"
    )
    async def sendtheme(self, luna):

        themesvar = files.json("data/config.json", "theme", documents=False)
        await luna.send(file=discord.File(f"data/themes/{themesvar}"))

    @commands.command(
        name="cthemes",
        aliases=['communitythemes'],
        usage="",
        description="Community made themes"
    )
    async def cthemes(self, luna):

        prefix = files.json("data/config.json", "prefix", documents=False)
        await message_builder(
            luna, title="Community Themes",
            description=f"{theme.description()}"
                        f"```\n{prefix}preview <theme>  » Preview a theme\n```"
                        f"```\n{prefix}install luna     » Luna theme\n"
                        f"{prefix}install lunaanimated » Luna theme\n"
                        f"{prefix}install chill    » Chill theme\n"
                        f"{prefix}install midnight » Midnight theme\n"
                        f"{prefix}install vaporwave » Vaporwave theme\n"
                        f"{prefix}install sweetrevenge » Sweetrevenge theme\n"
                        f"{prefix}install error    » Error theme\n"
                        f"{prefix}install lunapearl » Pearl theme\n"
                        f"{prefix}install gamesense » Gamesense theme\n"
                        f"{prefix}install aimware  » Aimware theme\n"
                        f"{prefix}install guilded  » Guilded theme\n"
                        f"{prefix}install lucifer  » Lucifer selfbot theme\n"
                        f"{prefix}install nighty   » Nighty selfbot theme\n"
                        f"{prefix}install aries    » Aries selfbot theme```"
        )


bot.add_cog(ThemesCog(bot))


class CommunitythemesCog(commands.Cog, name="Community themes"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="preview",
        usage="<theme>",
        description="Preview a theme"
    )
    async def preview(self, luna, theme: str):

        prefix = files.json("data/config.json", "prefix", documents=False)
        notfound = False
        theme = theme.lower()
        if theme == "luna":
            title = "Luna"
            footer = "www.team-luna.org"
            description = True
            madeby = "Nshout"
        elif theme == "lunaanimated":
            title = "Luna"
            footer = "www.team-luna.org"
            description = True
            madeby = "Nshout"
        elif theme == "chill":
            title = "F R E E D O M"
            footer = "No one knows what it is so it exists as an illusion"
            description = True
            madeby = "$Exodus"
        elif theme == "midnight":
            title = "Midnight."
            footer = "It's Midnight."
            description = True
            madeby = "Rainy"
        elif theme == "vaporwave":
            title = "Vapor Wave"
            footer = "Ride the vapor wave."
            description = True
            madeby = "Rainy"
        elif theme == "sweetrevenge":
            title = "Sweet Revenge."
            footer = "Sweet revenge is nice."
            description = True
            madeby = "Rainy"
        elif theme == "error":
            title = "Error™"
            footer = "Error displaying footer, please contact support"
            description = True
            madeby = "$Exodus"
        elif theme == "lunapearl":
            title = "Luna"
            footer = "Team Luna"
            description = True
            madeby = "Nshout"
        elif theme == "gamesense":
            title = "gamesense"
            footer = "Get Good Get Gamesense"
            description = True
            madeby = "Dragon"
        elif theme == "aimware":
            title = "Aimware"
            footer = "Aimware | One Step Ahead Of The Game"
            description = True
            madeby = "Dragon"
        elif theme == "guilded":
            title = "Guilded"
            footer = "Guilded (Discord v2)| 2021"
            description = True
            madeby = "Exodus"
        elif theme == "lucifer":
            title = "💙 Lucifer Selfbot 💙"
            footer = "Lucifer Selfbot"
            description = True
            madeby = "Exodus"
        elif theme == "nighty":
            title = "Nighty"
            footer = "nighty.one"
            description = True
            madeby = "Exodus"
        elif theme == "aries":
            title = "Aries"
            footer = "made withu2661 by bomt and destiny"
            description = True
            madeby = "Nshout"
        else:
            notfound = True
        if notfound:
            await error_builder(luna, description=f"```\nNo theme called {theme} found```")
            return
        if not description:
            description = ""
        else:
            description = "```\n<> is required | [] is optional\n\n```"
        command_count = len(bot.commands)
        cog = bot.get_cog('Custom commands')
        custom = cog.get_commands()
        custom_command_count = 0
        for _ in custom:
            custom_command_count += 1
        embed = discord.Embed(
            title=title,
            description=f"{description}```\n\
Luna\n\nCommands          » {command_count - custom_command_count}\n\
Custom Commands   » {custom_command_count}\n``````\n\
Categories\n\n\
{prefix}help [command]   » Display all commands\n\
{prefix}chelp            » Display custom commands\n\
{prefix}admin            » Administrative commands\n\
{prefix}abusive          » Abusive commands\n\
{prefix}animated         » Animated commands\n\
{prefix}dump             » Dumping\n\
{prefix}fun              » Funny commands\n\
{prefix}game             » Game commands\n\
{prefix}image            » Image commands\n\
{prefix}hentai           » Hentai explorer\n\
{prefix}profile          » Profile settings\n\
{prefix}protection       » Protections\n\
{prefix}raiding          » Raiding tools\n\
{prefix}text             » Text commands\n\
{prefix}trolling         » Troll commands\n\
{prefix}tools            » Tools\n\
{prefix}networking       » Networking\n\
{prefix}nuking           » Account nuking\n\
{prefix}utility          » Utilities\n\
{prefix}settings         » Settings\n\
{prefix}webhook          » Webhook settings\n\
{prefix}notifications    » Toast notifications\n\
{prefix}sharing          » Share with somebody\n\
{prefix}themes           » Themes\n\
{prefix}misc             » Miscellaneous\n\
{prefix}about            » Luna information\n\
{prefix}repeat           » Repeat last used command\n\
{prefix}search <command> » Search for a command\n``````\n\
Version\n\n{version}``````\nThis is a preview of the theme {theme}\nThis theme was made by {madeby}\n```"
        )
        embed.set_footer(text=footer)
        await send(luna, embed)

    @commands.command(
        name="install",
        usage="<theme>",
        description="Install a theme"
    )
    async def install(self, luna, theme: str):

        notfound = False
        theme = theme.lower()
        if theme == "luna":
            title = "Luna"
            footer = "www.team-luna.org"
            description = True
            madeby = "Nshout"
        elif theme == "lunaanimated":
            title = "Luna"
            footer = "www.team-luna.org"
            description = True
            madeby = "Nshout"
        elif theme == "chill":
            title = "F R E E D O M"
            footer = "No one knows what it is so it exists as an illusion"
            description = True
            madeby = "$Exodus"
        elif theme == "midnight":
            title = "Midnight."
            footer = "It's Midnight."
            description = True
            madeby = "Rainy"
        elif theme == "vaporwave":
            title = "Vapor Wave"
            footer = "Ride the vapor wave."
            description = True
            madeby = "Rainy"
        elif theme == "sweetrevenge":
            title = "Sweet Revenge."
            footer = "Sweet revenge is nice."
            description = True
            madeby = "Rainy"
        elif theme == "error":
            title = "Error™"
            footer = "Error displaying footer, please contact support"
            description = True
            madeby = "$Exodus"
        elif theme == "lunapearl":
            title = "Luna"
            footer = "Team Luna"
            description = True
            madeby = "Nshout"
        elif theme == "gamesense":
            title = "gamesense"
            footer = "Get Good Get Gamesense"
            description = True
            madeby = "Dragon"
        elif theme == "aimware":
            title = "Aimware"
            footer = "Aimware | One Step Ahead Of The Game"
            description = True
            madeby = "Dragon"
        elif theme == "guilded":
            title = "Guilded"
            footer = "Guilded (Discord v2)| 2021"
            description = True
            madeby = "Exodus"
        elif theme == "lucifer":
            title = "💙 Lucifer Selfbot 💙"
            footer = "Lucifer Selfbot"
            description = True
            madeby = "Exodus"
        elif theme == "nighty":
            title = "Nighty"
            footer = "nighty.one"
            description = True
            madeby = "Exodus"
        elif theme == "aries":
            title = "Aries"
            footer = "made withu2661 by bomt and destiny"
            description = True
            madeby = "Nshout"
        else:
            notfound = True
        if notfound:
            await error_builder(luna, description=f"```\nNo theme called {theme} found```")
            return
        data = {
            "title": f"{title}",
            "footer": f"{footer}",
            "description": description
        }
        files.write_json(f"data/themes/{theme}.json", data, documents=False)
        config.theme(f"{theme}")
        await message_builder(
            luna,
            description=f"```\nInstalled theme \"{theme}\" and applied it\nThis theme was made by {madeby}```"
        )


bot.add_cog(CommunitythemesCog(bot))


class ToastCog(commands.Cog, name="Toast customization"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="toasticon",
        usage="<icon.ico>",
        description="Customize the toast icon"
    )
    async def toasticon(self, luna, *, newicon: str):

        if newicon.endswith(".ico"):
            prints.message(
                f"Changed toast icon to » {color.print_gradient(f'{newicon}')}"
            )
            config.toast.icon(f"{newicon}")
            await message_builder(luna, description=f"```\nChanged toast icon to » {newicon}```")
        else:
            await error_builder(luna, description=f"```\nNot a valid icon file (.ico)```")

    @commands.command(
        name="toasttitle",
        usage="<title>",
        description="Customize the toast title"
    )
    async def toasttitle(self, luna, *, newtitle: str):

        prints.message(
            f"Changed toast title to » {color.print_gradient(f'{newtitle}')}"
        )
        if newtitle == "None":
            config.toast.title("")
        else:
            config.toast.title(f"{newtitle}")
        await message_builder(luna, description=f"```\nChanged toast title to » {newtitle}```")


bot.add_cog(ToastCog(bot))


class ToastsCog(commands.Cog, name="Toast commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="toasts",
        usage="<on/off>",
        description="Turn toasts on or off"
    )
    async def toasts(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Toasts » {mode}")
            config.toast.toasts(mode)
            await message_builder(luna, description=f"```\nToasts » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="logintoasts",
        usage="<on/off>",
        description="Login toasts"
    )
    async def logintoasts(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Login toasts » {mode}")
            config.toast.login(mode)
            await message_builder(luna, description=f"```\nLogin toasts » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="nitrotoasts",
        usage="<on/off>",
        description="Nitro toasts"
    )
    async def nitrotoasts(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Nitro sniper toasts » {mode}")
            config.toast.nitro(mode)
            await message_builder(luna, description=f"```\nNitro sniper toasts » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="giveawaytoasts",
        usage="<on/off>",
        description="Giveaway toasts"
    )
    async def giveawaytoasts(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Giveaway toasts » {mode}")
            config.toast.giveaway(mode)
            await message_builder(luna, description=f"```\nGiveaway toasts » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="privnotetoasts",
        usage="<on/off>",
        description="Privnote toasts"
    )
    async def privnotetoasts(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Privnote toasts » {mode}")
            config.toast.privnote(mode)
            await message_builder(luna, description=f"```\nPrivnote toasts » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="selfbottoasts",
        usage="<on/off>",
        description="Selfbot toasts"
    )
    async def selfbottoasts(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Selfbot toasts » {mode}")
            config.toast.selfbot(mode)
            await message_builder(luna, description=f"```\nSelfbot toasts » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="pingtoasts",
        usage="<on/off>",
        description="Ping toasts"
    )
    async def pingtoasts(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Pings toasts » {mode}")
            config.toast.pings(mode)
            await message_builder(luna, description=f"```\nPings toasts » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="ghostpingtoasts",
        usage="<on/off>",
        description="Ghostping toasts"
    )
    async def ghostpingtoasts(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Ghostping toasts » {mode}")
            config.toast.ghostpings(mode)
            await message_builder(luna, description=f"```\nGhostping toasts » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="friendtoasts",
        usage="<on/off>",
        description="Friend event toasts"
    )
    async def friendtoasts(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Friend event toasts » {mode}")
            config.toast.friendevents(mode)
            await message_builder(luna, description=f"```\nFriend event toasts » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="guildtoasts",
        usage="<on/off>",
        description="Guild event toasts"
    )
    async def guildtoasts(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Guild event toasts » {mode}")
            config.toast.guildevents(mode)
            await message_builder(luna, description=f"```\nGuild event toasts » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="roletoasts",
        usage="<on/off>",
        description="Role update toasts"
    )
    async def roletoasts(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Role update toasts » {mode}")
            config.toast.roleupdates(mode)
            await message_builder(luna, description=f"```\nRole update toasts » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="nicktoasts",
        usage="<on/off>",
        description="Nickname update toasts"
    )
    async def nicktoasts(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(
                f"Nickname update toasts » {mode}"
            )
            config.toast.nickupdates(mode)
            await message_builder(luna, description=f"```\nNickname update toasts » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="protectiontoasts",
        usage="<on/off>",
        description="Protection toasts"
    )
    async def protectiontoasts(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Protection toasts » {mode}")
            config.toast.protection(mode)
            await message_builder(luna, description=f"```\nProtection toasts » {mode}```")
        else:
            await mode_error(luna, "on or off")


bot.add_cog(ToastsCog(bot))


class WebhookSetupCog(commands.Cog, name="Webhook setup"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="webhooksetup",
        usage="",
        description="Set up all webhooks"
    )
    async def webhooksetup(self, luna):

        try:
            prints.event("Creating webhooks...")
            await message_builder(luna, description="```\nCreating webhooks...```")
            category = await luna.guild.create_category_channel(name="Luna Webhooks")
            login = await category.create_text_channel("login")
            nitro = await category.create_text_channel("nitro")
            giveaway = await category.create_text_channel("giveaways")
            privnote = await category.create_text_channel("privnotes")
            selfbot = await category.create_text_channel("selfbots")
            pings = await category.create_text_channel("pings")
            ghostpings = await category.create_text_channel("ghostpings")
            friendevents = await category.create_text_channel("friend-events")
            guildevents = await category.create_text_channel("guild-events")
            roleupdates = await category.create_text_channel("role-updates")
            nickupdates = await category.create_text_channel("nickname-updates")
            protection = await category.create_text_channel("protections")

            wlogin = await login.create_webhook(name="Login Webhook")
            wnitro = await nitro.create_webhook(name="Nitro Webhook")
            wgiveaways = await giveaway.create_webhook(name="Giveaways Webhook")
            wprivnote = await privnote.create_webhook(name="Privnotes Webhook")
            wselfbot = await selfbot.create_webhook(name="Selfbots Webhook")
            wpings = await pings.create_webhook(name="Pings Webhook")
            wghostpings = await ghostpings.create_webhook(name="Ghostpings Webhook")
            wfriendevents = await friendevents.create_webhook(name="Friend Events Webhook")
            wguildevents = await guildevents.create_webhook(name="Guild Events Webhook")
            wroleupdates = await roleupdates.create_webhook(name="Role Updates Webhook")
            wnickupdates = await nickupdates.create_webhook(name="Nickname Updates Webhook")
            wprotection = await protection.create_webhook(name="Protections Webhook")

            config.webhook.login_url(wlogin.url)
            config.webhook.nitro_url(wnitro.url)
            config.webhook.giveaway_url(wgiveaways.url)
            config.webhook.privnote_url(wprivnote.url)
            config.webhook.selfbot_url(wselfbot.url)
            config.webhook.pings_url(wpings.url)
            config.webhook.ghostpings_url(wghostpings.url)
            config.webhook.friendevents_url(wfriendevents.url)
            config.webhook.guildevents_url(wguildevents.url)
            config.webhook.roleupdates_url(wroleupdates.url)
            config.webhook.nickupdates_url(wnickupdates.url)
            config.webhook.protection_url(wprotection.url)
            prints.message(
                "Successfully created all webhooks and stored them in the config"
            )
            await message_builder(
                luna, title="Webhooks Setup",
                description=f"```\nSuccessfully created all webhooks and stored them in the config```"
            )
        except Exception as e:
            await error_builder(luna, description=f"```{e}```")


bot.add_cog(WebhookSetupCog(bot))


class WebhooksCog(commands.Cog, name="Webhook commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="webhooks",
        usage="<on/off>",
        description="Webhooks"
    )
    async def webhooks(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Webhooks » {mode}")
            config.webhook.webhooks(mode)
            await message_builder(luna, description=f"```\nWebhooks » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="wlogin",
        usage="<on/off>",
        description="Login webhooks"
    )
    async def wlogin(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Login webhooks » {mode}")
            config.webhook.login(mode)
            await message_builder(luna, description=f"```\nLogin webhooks » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="wnitro",
        usage="<on/off>",
        description="Nitro webhooks"
    )
    async def wnitro(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Nitro webhooks » {mode}")
            config.webhook.nitro(mode)
            await message_builder(luna, description=f"```\nNitro webhooks » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="wgiveaways",
        usage="<on/off>",
        description="Giveaway webhooks"
    )
    async def wgiveaways(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Giveaway webhooks » {mode}")
            config.webhook.giveaway(mode)
            await message_builder(luna, description=f"```\nGiveaway webhooks » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="wprivnote",
        usage="<on/off>",
        description="Privnote webhooks"
    )
    async def wprivnote(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Privnote webhooks » {mode}")
            config.webhook.privnote(mode)
            await message_builder(luna, description=f"```\nPrivnote webhooks » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="wselfbot",
        usage="<on/off>",
        description="Selfbot webhooks"
    )
    async def wselfbot(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Selfbot webhooks » {mode}")
            config.webhook.selfbot(mode)
            await message_builder(luna, description=f"```\nSelfbot webhooks » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="wpings",
        usage="<on/off>",
        description="Pings webhooks"
    )
    async def wpings(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Pings webhooks » {mode}")
            config.webhook.pings(mode)
            await message_builder(luna, description=f"```\nPings webhooks » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="wghostpings",
        usage="<on/off>",
        description="Ghostpings webhooks"
    )
    async def wghostpings(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Ghostpings webhooks » {mode}")
            config.webhook.ghostpings(mode)
            await message_builder(luna, description=f"```\nGhostpings webhooks » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="wfriends",
        usage="<on/off>",
        description="Friend event webhooks"
    )
    async def wfriends(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(
                f"Friend event webhooks » {mode}"
            )
            config.webhook.friendevents(mode)
            await message_builder(luna, description=f"```\nFriend event webhooks » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="wguilds",
        usage="<on/off>",
        description="Guild event webhooks"
    )
    async def wguilds(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Guild event webhooks » {mode}")
            config.webhook.guildevents(mode)
            await message_builder(luna, description=f"```\nGuild event webhooks » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="wroles",
        usage="<on/off>",
        description="Role update webhooks"
    )
    async def wroles(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Role event webhooks » {mode}")
            config.webhook.roleupdates(mode)
            await message_builder(luna, description=f"```\nRole event webhooks » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="wnick",
        usage="<on/off>",
        description="Nickname update webhooks"
    )
    async def wnick(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(
                f"Nickname event webhooks » {mode}"
            )
            config.webhook.nickupdates(mode)
            await message_builder(luna, description=f"```\nNickname event webhooks » {mode}```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="wprotection",
        usage="<on/off>",
        description="Protection webhooks"
    )
    async def wprotection(self, luna, mode: str):

        if mode == "on" or mode == "off":
            prints.message(f"Protection webhooks » {mode}")
            config.webhook.protection(mode)
            await message_builder(luna, description=f"```\nProtection webhooks » {mode}```")
        else:
            await mode_error(luna, "on or off")


bot.add_cog(WebhooksCog(bot))


class WebhookUrlCog(commands.Cog, name="Webhook urls"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="wulogin",
        usage="<url>",
        description="Login webhook"
    )
    async def wulogin(self, luna, url: str):
        config.webhook.login_url(url)
        prints.message(
            f"Changed login webhook url to » {color.print_gradient(f'{url}')}"
        )
        await message_builder(luna, description=f"```\nChanged login webhook url to » {url}```")

    @commands.command(
        name="wunitro",
        usage="<url>",
        description="Nitro webhook"
    )
    async def wunitro(self, luna, url: str):
        config.webhook.nitro_url(url)
        prints.message(
            f"Changed nitro webhook url to » {color.print_gradient(f'{url}')}"
        )
        await message_builder(luna, description=f"```\nChanged nitro webhook url to » {url}```")

    @commands.command(
        name="wugiveaway",
        usage="<url>",
        description="Giveaways webhook"
    )
    async def wugiveaway(self, luna, url: str):
        config.webhook.giveaway_url(url)
        prints.message(
            f"Changed giveaways webhook url to » {color.print_gradient(f'{url}')}"
        )
        await message_builder(luna, description=f"```\nChanged giveaways webhook url to » {url}```")

    @commands.command(
        name="wuprivnote",
        usage="<url>",
        description="Privnotes webhook"
    )
    async def wuprivnote(self, luna, url: str):
        config.webhook.privnote_url(url)
        prints.message(
            f"Changed privnotes webhook url to » {color.print_gradient(f'{url}')}"
        )
        await message_builder(luna, description=f"```\nChanged privnotes webhook url to » {url}```")

    @commands.command(
        name="wuselfbot",
        usage="<url>",
        description="Selfbots webhook"
    )
    async def wuselfbot(self, luna, url: str):
        config.webhook.selfbot_url(url)
        prints.message(
            f"Changed selfbots webhook url to » {color.print_gradient(f'{url}')}"
        )
        await message_builder(luna, description=f"```\nChanged selfbots webhook url to » {url}```")

    @commands.command(
        name="wupings",
        usage="<url>",
        description="Pings webhook"
    )
    async def wupings(self, luna, url: str):
        config.webhook.pings_url(url)
        prints.message(
            f"Changed pings webhook url to » {color.print_gradient(f'{url}')}"
        )
        await message_builder(luna, description=f"```\nChanged pings webhook url to » {url}```")

    @commands.command(
        name="wughost",
        usage="<url>",
        description="Ghostpings webhook"
    )
    async def wughost(self, luna, url: str):
        config.webhook.ghostpings_url(url)
        prints.message(
            f"Changed ghostpings webhook url to » {color.print_gradient(f'{url}')}"
        )
        await message_builder(luna, description=f"```\nChanged ghostpings webhook url to » {url}```")

    @commands.command(
        name="wufriends",
        usage="<url>",
        description="Friend events webhook"
    )
    async def wufriends(self, luna, url: str):
        config.webhook.friendevents_url(url)
        prints.message(
            f"Changed friend events webhook url to » {color.print_gradient(f'{url}')}"
        )
        await message_builder(luna, description=f"```\nChanged friend events webhook url to » {url}```")

    @commands.command(
        name="wuguilds",
        usage="<url>",
        description="Guild events webhook"
    )
    async def wuguilds(self, luna, url: str):
        config.webhook.guildevents_url(url)
        prints.message(
            f"Changed guild events webhook url to » {color.print_gradient(f'{url}')}"
        )
        await message_builder(luna, description=f"```\nChanged guild events webhook url to » {url}```")

    @commands.command(
        name="wuroles",
        usage="<url>",
        description="Role updates webhook"
    )
    async def wuroles(self, luna, url: str):
        config.webhook.roleupdates_url(url)
        prints.message(
            f"Changed role updates webhook url to » {color.print_gradient(f'{url}')}"
        )
        await message_builder(luna, description=f"```\nChanged role updates webhook url to » {url}```")

    @commands.command(
        name="wunick",
        usage="<url>",
        description="Nick updates webhook"
    )
    async def wunick(self, luna, url: str):
        config.webhook.nickupdates_url(url)
        prints.message(
            f"Changed nick updates webhook url to » {color.print_gradient(f'{url}')}"
        )
        await message_builder(luna, description=f"```\nChanged nick updates webhook url to » {url}```")

    @commands.command(
        name="wuprotection",
        usage="<url>",
        description="Protection webhook"
    )
    async def wuprotection(self, luna, url: str):
        config.webhook.protection_url(url)
        prints.message(
            f"Changed protection webhook url to » {color.print_gradient(f'{url}')}"
        )
        await message_builder(luna, description=f"```\nChanged protection webhook url to » {url}```")


bot.add_cog(WebhookUrlCog(bot))


class WebhookCog(commands.Cog, name="Webhook customisation"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="wtitle",
        usage="<title>",
        description="Customize the webhook title"
    )
    async def wtitle(self, luna, *, newtitle: str):

        prints.message(
            f"Changed webhook title to » {color.print_gradient(f'{newtitle}')}"
        )
        if newtitle == "None":
            config.webhook.title("")
        else:
            config.webhook.title(f"{newtitle}")
        await message_builder(luna, description=f"```\nChanged webhook title to » {newtitle}```")

    @commands.command(
        name="wfooter",
        usage="<footer>",
        description="Customize the webhook footer"
    )
    async def wfooter(self, luna, *, newfooter: str):

        prints.message(
            f"Changed webhook footer to » {color.print_gradient(f'{newfooter}')}"
        )
        if newfooter == "None":
            config.webhook.footer("")
        else:
            config.webhook.footer(f"{newfooter}")
        await message_builder(luna, description=f"```\nChanged webhook footer to » {newfooter}```")

    @commands.command(
        name="wimage",
        usage="<url>",
        description="Customize the thumbnail image"
    )
    async def wimage(self, luna, newimageurl: str):

        prints.message(
            f"Changed webhook thumbnail url to » {color.print_gradient(f'{newimageurl}')}"
        )
        if newimageurl == "None":
            config.webhook.image_url("")
        else:
            config.webhook.image_url(f"{newimageurl}")
        await message_builder(luna, description=f"```\nChanged webhook thumbnail url to » {newimageurl}```")

    @commands.command(
        name="whexcolor",
        usage="<#hex>",
        description="Webhook hexadecimal color"
    )
    async def whexcolor(self, luna, newhexcolor: str):

        prints.message(
            f"Changed webhook color to » {color.print_gradient(f'{newhexcolor}')}"
        )
        if newhexcolor == "None":
            config.webhook.hex_color("")
        else:
            config.webhook.hex_color(f"{newhexcolor}")
        await message_builder(luna, description=f"```\nChanged webhook color to » {newhexcolor}```")


bot.add_cog(WebhookCog(bot))


class MiscCog(commands.Cog, name="Miscellaneous commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="uptime",
        usage="",
        description="Uptime"
    )
    async def uptime(self, luna):

        if day == 0:
            await message_builder(
                luna, title="Uptime",
                description=f"```\n{hour:02d} Hours, {minute:02d} Minutes and {second:02d} Seconds```"
            )
        else:
            await message_builder(
                luna, title="Uptime",
                description=f"```\n{day:02d} Days, {hour:02d} Hours, {minute:02d} Minutes and {second:02d} Seconds```"
            )

    @commands.command(
        name="about",
        usage="",
        description="Luna information"
    )
    async def about(self, luna):

        motd = urllib.request.urlopen('https://pastebin.com/raw/MeHTn6gZ')
        for line in motd:
            motd = line.decode().strip()
        command_count = len(bot.commands)
        cog = bot.get_cog('Custom commands')
        custom = cog.get_commands()
        custom_command_count = 0
        for _ in custom:
            custom_command_count += 1
        if platinum:
            beta_info = f"Platinum Build"
        else:
            beta_info = ""
        await message_builder(
            luna,
            description=f"```\nMOTD\n\n{motd}\n```"
                        f"```\nVersion\n\n{version}{beta_info}\n```"
                        f"```\nUptime\n\n{hour:02d} Hours, {minute:02d} Minutes and {second:02d} Seconds\n```"
                        f"```\nCommands\n\n{command_count - custom_command_count}\n```"
                        f"```\nCustom commands\n\n{custom_command_count}\n```"
                        f"```\nEnviroment\n\nDiscord.py » {discord.__version__}\n```"
                        f"```\nPublic server invite\n\nhttps://discord.gg/rnq876Kcd7\n```"
                        f"```\nCustomer only server invite\n\nhttps://discord.gg/3FGEaCnZST\n```"
                        f"```\nWebsite\n\nhttps://www.team-luna.org\n```"
        )

    @commands.command(
        name="logout",
        usage="",
        description="Logout of the bot"
    )
    async def logout(self, luna):

        prints.message(f"Logging out of the bot")
        await message_builder(luna, description=f"```\nLogging out of the bot```")
        files.remove('data/discord.luna', documents=False)
        restart_program()

    @commands.command(
        name="thelp",
        usage="",
        description="All commands in a text file"
    )
    async def thelp(self, luna):

        # ///////////////////////////////////////////////////////////////////
        try:
            helptext = ""

            cog = self.bot.get_cog('Help commands')
            helptext += "Help commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Profile commands')
            helptext += "\nProfile commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Animated statuses')
            helptext += "\nStatus commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Channel commands')
            helptext += "\nChannel commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Member commands')
            helptext += "\nMember commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Role commands')
            helptext += "\nRole commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Nickname commands')
            helptext += "\nNickname commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Invite commands')
            helptext += "\nInvite commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Administrative commands')
            helptext += "\nAdministrative commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Ignore commands')
            helptext += "\nIgnore commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Animated commands')
            helptext += "\nAnimated commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Dump commands')
            helptext += "\nDump commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Text commands')
            helptext += "\nText commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Codeblock commands')
            helptext += "\nCodeblock commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Image commands')
            helptext += "\nImage commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Troll commands')
            helptext += "\nTroll commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Fun commands')
            helptext += "\nFun commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Tools commands')
            helptext += "\nTools commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Nettool commands')
            helptext += "\nNettool commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Util commands')
            helptext += "\nUtil commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Spam commands')
            helptext += "\nSpam commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('All commands')
            helptext += "\nAll commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Mass commands')
            helptext += "\nMass commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Guild commands')
            helptext += "\nGuild commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Exploit commands')
            helptext += "\nExploit commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Abusive commands')
            helptext += "\nAbusive commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Raid commands')
            helptext += "\nRaid commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Nuking commands')
            helptext += "\nNuking commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Privacy commands')
            helptext += "\nPrivacy commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Protection Guild commands')
            helptext += "\nProtection Guild commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Protection commands')
            helptext += "\nProtection commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Backup commands')
            helptext += "\nBackup commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Whitelist commands')
            helptext += "\nWhitelist commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Settings commands')
            helptext += "\nSettings commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"
            cog = self.bot.get_cog('Share commands')
            helptext += "\nShare commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Encode commands')
            helptext += "\nEncode commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Decode commands')
            helptext += "\nDecode commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Giveaway settings')
            helptext += "\nGiveaway settings:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Cryptocurrency commands')
            helptext += "\nCryptocurrency commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Customization commands')
            helptext += "\nCustomization commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Hentai commands')
            helptext += "\nHentai commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Sniper settings')
            helptext += "\nSniper settings:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Theme commands')
            helptext += "\nTheme commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Toast customization')
            helptext += "\nToast customization:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Toast commands')
            helptext += "\nToast commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Webhook setup')
            helptext += "\nWebhook setup:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Webhook commands')
            helptext += "\nWebhook commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Webhook urls')
            helptext += "\nWebhook urls:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Webhook customisation')
            helptext += "\nWebhook customisation:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Miscellaneous commands')
            helptext += "\nMiscellaneous commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            cog = self.bot.get_cog('Game commands')
            helptext += "\nGame commands:\n"
            commands = cog.get_commands()
            for command in commands:
                helptext += f"{command.name + ' ' + command.usage:<17} » {command.description}\n"

            # ///////////////////////////////////////////////////////////////////

            commandcount = len(self.bot.commands)
            try:
                custom = cog.get_commands()
                custom_command_count = 0
                for _ in custom:
                    custom_command_count += 1
            except BaseException:
                custom_command_count = 0

            file = open("data/commands.txt", "w")
            file.write(f"{commandcount - custom_command_count} Commands\n\n<> is required | [] is optional\n\n{helptext}")
            file.close()
            await message_builder(luna, title="Text Help", description=f"```\nSaved all commands in Documents/data/commands.txt```")
        except Exception as e:
            await error_builder(luna, e)

    @commands.command(
        name="update",
        usage="",
        description="Updates Luna"
    )
    async def update(self, luna):

        r = requests.get("https://pastebin.com/raw/jBrn4WU4").json()
        version_url = r["version"]

        r = requests.get("https://pastebin.com/raw/eSGbZgms").json()
        platinum_version_url = r["version"]
        
        if platinum:
            prints.message("platinum build")
            version_url = platinum_version_url

        if developer_mode:
            await message_builder(
                luna, title="Update",
                description=f"```\nDeveloper mode active! No updates will be downloaded.```"
            )
        elif version == version_url:
            await message_builder(
                luna, title="Update",
                description=f"```\nYou are on the latest version! ({version_url})```"
            )
        else:
            if files.json(
                    "data/notifications/toasts.json",
                    "login",
                    documents=False
            ) == "on" and files.json(
                "data/notifications/toasts.json",
                "toasts",
                documents=False
            ) == "on":
                notify.toast(f"Starting update {version_url}")
            if files.json(
                    "data/webhooks/webhooks.json",
                    "login",
                    documents=False
            ) == "on" and files.json(
                "data/webhooks/webhooks.json",
                "webhooks",
                documents=False
            ) == "on" and not webhook.login_url() == "webhook-url-here":
                notify.webhook(
                    url=webhook.login_url(), name="login",
                    description=f"Starting update {version_url}"
                )
            await message_builder(luna, title="Update", description=f"```\nStarted update » {version_url}```")

            r = requests.get("https://pastebin.com/raw/jBrn4WU4").json()
            updater_url = r["updater"]

            r = requests.get("https://pastebin.com/raw/eSGbZgms").json()
            platinum_updater_url = r["updater"]

            url = updater_url
            if platinum:
                prints.message("platinum build")
                url = platinum_updater_url
            prints.event("downloading updater...")
            from clint.textui import progress
            r = requests.get(url, stream=True)
            with open('Updater.exe', 'wb') as f:
                total_length = int(r.headers.get('content-length'))
                for chunk in progress.bar(
                        r.iter_content(
                            chunk_size=1024
                        ), expected_size=(
                                                total_length / 1024) + 1
                ):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                f.close()
            time.sleep(3)
            prints.event("Starting Updater.exe...")
            os.startfile('Updater.exe')
            os._exit(0)

    @commands.command(
        name="restart",
        usage="",
        aliases=['reboot'],
        description="Restart Luna"
    )
    async def restart(self, luna):
        await luna.message.delete()
        # if configs.mode() == 2:
        #       sent = await luna.send(f"```ini\n[ Restarting ]\n\nAllow up to 5 seconds\n\n[ {theme.footer()} ]```")
        #       await asyncio.sleep(3)
        #       await sent.delete()
        # if configs.mode() == 3:
        #       sent = await luna.send(f"> **Restarting**\n>n> Allow up to 5 seconds\n>n> {theme.footer()}")
        #       await asyncio.sleep(3)
        #       await sent.delete()
        # else:
        #       embed = discord.Embed(title="Restarting", description=f"```\nAllow up to 5 seconds```")
        #
        #       embed.set_footer(text=theme.footer())
        #       embed.set_author(name=theme.author(), url=theme.author_url(), icon_url=theme.author_icon_url())
        #
        #       sent = await send(luna, embed)
        #       await asyncio.sleep(3)
        #       await sent.delete()
        restart_program()

    @commands.command(
        name="shutdown",
        usage="",
        description="Shutdown Luna"
    )
    async def shutdown(self, luna):
        await luna.message.delete()
        os._exit(0)

    @commands.command(
        name="panic",
        usage="",
        description="Quickly close Luna"
    )
    async def panic(self, luna):
        await luna.message.delete()
        os._exit(0)

    @commands.command(
        name="clear",
        aliases=['cls'],
        usage="",
        description="Clear the console"
    )
    async def clear(self, ctx):
        global command_logs
        command_logs = ""
        dpg.set_value(logs_block, "Logs cleared")

    @commands.command(
        name="covid",
        aliases=['corona'],
        usage="",
        description="Corona statistics"
    )
    async def covid(self, luna):

        request = requests.get(f'https://api.covid19api.com/summary')
        data = request.json()
        info = data['Global']
        totalconfirmed = info['TotalConfirmed']
        totalrecovered = info['TotalRecovered']
        totaldeaths = info['TotalDeaths']
        newconfirmed = info['NewConfirmed']
        newrecovered = info['NewRecovered']
        newdeaths = info['NewDeaths']
        date = info['Date']
        await message_builder(
            luna, title="Covid-19 Statistics",
            description=f"```Total Confirmed Cases\n{totalconfirmed}```"
                        f"```Total Deaths\n{totaldeaths}```"
                        f"```Total Recovered\n{totalrecovered}```"
                        f"```New Confirmed Cases\n{newconfirmed}```"
                        f"```New Deaths\n{newdeaths}```"
                        f"```New Recovered\n{newrecovered}```"
                        f"```Date\n{date}```"
        )

    typing = False

    @commands.command(
        name="typing",
        usage="<on/off>",
        description="Enable or disable typing"
    )
    async def typing(self, luna, mode: str):

        if mode == "on":
            await message_builder(luna, title="Typing", description=f"```\nTyping enabled```")
            typing = True
            while typing:
                async with luna.typing():
                    await asyncio.sleep(1)
                    if not typing:
                        break
        elif mode == "off":
            await message_builder(luna, title="Typing", description=f"```\nTyping disabled```")
        else:
            await mode_error(luna, "on or off")

    @commands.command(
        name="hwid",
        usage="",
        description="Prints your hwid"
    )
    async def hwid(self, luna):

        hwid = str(subprocess.check_output('wmic csproduct get uuid')).split(
            '\\r\\n'
        )[1].strip('\\r').strip()
        prints.message(f"Your HWID » {hwid}")

    @commands.command(
        name="edited",
        usage="<message>",
        description="Add the \"edited\" tag to the message"
    )
    async def edited(self, luna, message: str):

        magic_char = '\u202b'
        headers = {'Authorization': user_token}
        message_ = f'{magic_char} {message} {magic_char}'
        res = requests.post(
            f'https://discord.com/api/{api_version}/channels/{luna.channel.id}/messages', headers=headers,
            json={'content': message_}
        )
        if res.status_code == 200:
            message_id = res.json()['id']
            requests.patch(
                f'https://discord.com/api/{api_version}/channels/{luna.channel.id}/messages/{message_id}',
                headers=headers, json={'content': ' ' + message_}
            )


bot.add_cog(MiscCog(bot))


class GamesCog(commands.Cog, name="Game commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(
        name="fnshop",
        usage="",
        description="Fortnite shop"
    )
    async def fnshop(self, luna):
        await message_builder(luna, title="Fortnite Shop", large_image="https://api.nitestats.com/v1/shop/image")

    @commands.command(
        name="fnmap",
        usage="",
        description="Fortnite map"
    )
    async def fnmap(self, luna):
        await message_builder(
            luna, title="Fortnite Map",
            large_image="https://media.fortniteapi.io/images/map.png?showPOI=true"
        )

    @commands.command(
        name="fnnews",
        usage="",
        description="Fortnite news"
    )
    async def fnnews(self, luna):
        fortnite = requests.get("https://fortnite-api.com/v2/news/br").json()
        await message_builder(luna, title="Fortnite News", large_image=fortnite["data"]["image"])


bot.add_cog(GamesCog(bot))


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Command Functions


def convert_to_text(embed: discord.Embed):
    """[summary]

    Args:
            embed (discord.Embed): [description]

    Returns:
            [type]: [description]
    """
    if embed.image.url != "" and str(embed.image.url) != "Embed.Empty":
        return embed.image.url if embed.description == "" or str(embed.description) == "Embed.Empty" else f"{embed.description}\n{embed.image.url}"

    embed.description = embed.description.replace(
        '[', '[34m['
    ).replace(
        ']', '][0m'
    ).replace(
        '<', '[35m<'
    ).replace(
        '>', '>[0m'
    ).replace(
        '```ansi\n', '```\n'
    )
    if not embed.description.startswith("\n"):
        extra_start = "\n"
    if embed.description.startswith("```\n"):
        extra_start = ""
    if embed.description.endswith("\n```"):
        embed.description = embed.description[:-5]
    text_mode_builder = f"```ansi\n[ [34m{embed.title.replace('**', '')}[0m ]\n{extra_start}{embed.description.replace('```', '')}\n\n[ [34m{embed.footer.text}[0m ]\n```"
    if len(text_mode_builder) >= 2000:
        prints.error("INVALID, OVER 2000 CHARS. PLEASE REPORT THIS TO A DEVELOPER.")
    return text_mode_builder


def convert_to_indent(embed: discord.Embed):
    """[summary]

    Args:
            embed (discord.Embed): [description]

    Returns:
            [type]: [description]
    """
    if embed.image.url == "" or str(embed.image.url) == "Embed.Empty":
        embed.description = embed.description.replace(
            '[', '[34m['
        ).replace(
            ']', '][0m'
        ).replace(
            '<', '[35m<'
        ).replace(
            '>', '>[0m'
        ).replace(
            '```\n', '```ansi\n'
        )
        text = ""

        for line in embed.description.split("\n"):
            indent = f"> {line}"
            text += indent + "\n"

        indent_builder = f"> **{embed.title}**\n> \n{text}> {embed.footer.text}"
        if len(indent_builder) >= 2000:
            prints.error("INVALID, OVER 2000 CHARS. PLEASE REPORT THIS TO A DEVELOPER.")
    elif embed.description == "" or str(embed.description) == "Embed.Empty":
        return embed.image.url
    else:
        indent_builder = f"{embed.description}\n{embed.image.url}"
    return indent_builder


async def send(luna, embed, delete_after=None):
    """[summary]

    Args:
            luna ([type]): [description]
            embed ([type]): [description]
            delete_after ([type], optional): [description]. Defaults to None.
    """
    deletetimer = configs.delete_timer()
    if delete_after is not None:
        deletetimer = delete_after
    mode = configs.mode()
    return await luna.send(convert_to_text(embed), delete_after=deletetimer) if int(mode) == 2 else await luna.send(convert_to_indent(embed), delete_after=deletetimer)


async def mode_error(luna, modes: str):
    """
    Sends an error message to the user if the mode is not set to 2.
    param `luna` The user that sent the command.
    param `modes` The mode that the user is using.

    returns `None`
    """
    if configs.error_log() == "console":
        prints.error(f"That mode does not exist! Only {modes}")
        return None
    else:
        embed = discord.Embed(
            title="Error",
            description=f"```\nThat mode does not exist!\nOnly {modes}```"
        )
        embed.set_footer(text=theme.footer())
        return await send(luna, embed)


async def message_builder(
        luna, title: str = None, description="", large_image: str = None,
        delete_after: int = None, footer_extra: str = None, footer: str = None
):
    """
    Luna's main function for creating messages with the theme applied.\n
    Parse `data/ctx` as first argument. (Important)\n
    `title="foo"` <- Defines the title. (Optional)\n
    `description="foo"` <- Defines the description. (Optional)\n
    `large_image="url"` <- Defines the large image url. (Optional)\n
    `delete_after=30` <- Defines the auto delete time after the embed is sent. (Optional)\n
    `footer_extra="foo"` <- Defines the footer extra. (Optional)\n
    `footer="foo"` <- Defines the footer. (Optional)\n

    param `luna` The user that sent the command.
    param `title` The title of the embed.
    param `description` The description of the embed.
    param `large_image` The large image url of the embed.
    param `delete_after` The auto delete time after the embed is sent.
    param `footer_extra` The footer extra of the embed.
    param `footer` The footer of the embed.
    returns `The message that was sent.`
    """
    if large_image is None:
        large_image = ""
    if title is None:
        title = theme.title()
    if footer == "None":
        footer_extra = ""
    elif footer_extra is None:
        footer_extra = f"Enabled Protections » {active_protections} | {theme.footer()}" if files.json("data/protections/config.json", "footer", documents=False) else theme.footer()

    elif files.json(
            "data/protections/config.json",
            "footer",
            documents=False
    ):
        footer_extra = f"{footer_extra} | Enabled Protections » {active_protections} | {theme.footer()}"
    else:
        footer_extra = f"{footer_extra} | {theme.footer()}"
    embed = discord.Embed(
        title=title,
        description=description
    )
    embed.set_footer(text=footer_extra)
    embed.set_image(url=large_image)
    sent = await send(luna, embed, delete_after)
    return sent


async def error_builder(luna, description=""):
    """[summary]

    Args:
            luna ([type]): [description]
            description (str, optional): [description]. Defaults to "".
    """
    if configs.error_log() == "console":
        prints.error(description.replace('\n', ' ').replace('`', ''))
    else:
        embed = discord.Embed(
            title="Error", description=description
        )
        embed.set_footer(text=theme.footer())
        await send(luna, embed)


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Beginning of the gui

def privacy_mode(sender, app_data, user_data):

    global privacy
    global luna_user_id

    if app_data:
        privacy = True
        now = datetime.now()
        hour = now.hour
        if hour < 12:
            greeting = "Good morning"
        elif hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        dpg.set_value(luna_user, f"{greeting}, Luna")
        dpg.set_value(logged, "Logged into Luna#0000")
        dpg.set_value(luna_uid_text, "UID: Privacy Mode")
        dpg.set_value(friends_text, "0 Friends")
        dpg.set_value(guilds_text, "0 Guilds")
        prints.message("Privacy mode » on")
    else:
        privacy = False
        now = datetime.now()
        hour = now.hour
        username = f"Dev - {os.getlogin()}" if developer_mode else os.getlogin()
        if hour < 12:
            greeting = "Good morning"
        elif hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        if not developer_mode:
            if files.file_exist('data/auth.luna', documents=False):
                username = files.json(
                    "data/auth.luna", "username", documents=False
                )
                username = Decryption(
                    '5QXapyTDbrRwW4ZBnUgPGAs9CeVSdiLk'
                ).CEA256(username)
        else:
            username = "Developer"
        dpg.set_value(luna_user, f"{greeting}, {username}")
        dpg.set_value(logged, f"Logged into {bot.user}")
        dpg.set_value(luna_uid_text, f"UID: {luna_user_id}")
        dpg.set_value(friends_text, f"{len(bot.user.friends)} Friends")
        dpg.set_value(guilds_text, f"{len(bot.guilds)} Guilds")
        prints.message("Privacy mode » off")

# //////////////////////////////////////////////////////////////////////////
# Create viewport and bind font
# //////////////////////////////////////////////////////////////////////////

dpg.create_context()

# dpg.create_viewport(
#     title='Luna', width=760, height=600, resizable=False, decorated=True, clear_color=(114, 137, 218, 255), small_icon="data/resources/luna.ico", large_icon="data/resources/luna.ico"
#     )

dpg.create_viewport(
    title='Luna', width=750, height=594, resizable=False, decorated=True, clear_color=(114, 137, 218, 255), small_icon="data/resources/luna.ico", large_icon="data/resources/luna.ico"
    )


with dpg.font_registry():
    default_font = dpg.add_font("data/resources/arial.ttf", 13)

dpg.bind_font(default_font)


# //////////////////////////////////////////////////////////////////////////
# Functions
# //////////////////////////////////////////////////////////////////////////



def close_account():
    files.remove('data/auth.luna', documents=False)
    os._exit(0)


def close_token():
    files.remove('data/discord.luna', documents=False)
    os._exit(0)


def nitro_control(sender, app_data, user_data):
    if app_data:
        prints.message(f"Nitro sniper » on")
        config.nitro.sniper("on")
    else:
        prints.message(f"Nitro sniper » off")
        config.nitro.sniper("off")


def giveaway_control(sender, app_data, user_data):
    if app_data:
        prints.message(f"Giveaway sniper » on")
        config.giveaway.joiner("on")
    else:
        prints.message(f"Giveaway sniper » off")
        config.giveaway.joiner("off")


def privnote_control(sender, app_data, user_data):
    if app_data:
        prints.message(f"Privnote sniper » on")
        config.privnote.sniper("on")
    else:
        prints.message(f"Privnote sniper » off")
        config.privnote.sniper("off")


def ratelimit_control(sender, app_data, user_data):
    if app_data:
        prints.message(f"Nitro ratelimit » on")
        config._global("data/snipers/nitro.json", "charge", "on")
        startup_status = files.json(
            "data/config.json", "startup_status", documents=False
        )
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7',
            'Content-Type': 'application/json',
            'Authorization': user_token,
        }
        request = requests.Session()
        setting = {
            'status': startup_status,
            "custom_status": {"text": f"Ratelimit: [#####]"}
        }
        request.patch(f"https://discord.com/api/{api_version}/users/@me/settings",headers=headers, json=setting, timeout=10)
    else:
        prints.message(f"Nitro ratelimit » off")
        config._global("data/snipers/nitro.json", "charge", "off")
        startup_status = files.json(
            "data/config.json", "startup_status", documents=False
        )
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7',
            'Content-Type': 'application/json',
            'Authorization': user_token,
        }
        request = requests.Session()
        setting = {
            'status': startup_status,
            "custom_status": {"text": f""}
        }
        request.patch(f"https://discord.com/api/{api_version}/users/@me/settings",headers=headers, json=setting, timeout=10)


def delay_control(sender, app_data, user_data):
    minutes_value = dpg.get_value(minutes_slider)
    prints.message(f"Giveaway joiner delay » {str(minutes_value)}")
    config.giveaway.delay_in_minutes(f"{minutes_value}") 


def prefix_control(sender, app_data, user_data):
    prefix_value = dpg.get_value(gui_input_prefix)
    prints.message(f"Prefix » {str(prefix_value)}")
    bot.command_prefix = prefix_value
    config.prefix(prefix_value)
    dpg.set_value(gui_prefix, f"Prefix: {prefix_value}")


def timer_control(sender, app_data, user_data):
    timer_value = dpg.get_value(gui_delete_timer)
    config.delete_timer(f"{timer_value}")
    prints.message(f"Auto delete timer » {str(timer_value)}")


def joiner_control(sender, app_data, user_data):
    if app_data:
        prints.message(f"Server joiner » on")
        config.giveaway.guild_joiner("on")
    else:
        prints.message(f"Server joiner » off")
        config.giveaway.guild_joiner("off")


path_to_json = 'data/themes/'
themes = [pos_json.replace(".json", "") for pos_json in os.listdir(
    path_to_json
) if pos_json.endswith('.json')]
themes.insert(0, "default")
prefix = files.json("data/config.json", "prefix", documents=False)
themesvar = files.json("data/config.json", "theme", documents=False)
if themesvar == "default":
    pass
else:
    themesvar = (themesvar[:-5])


def theme_control(sender, app_data, user_data):
    if app_data == "default":
        prints.message(f"Changed theme » {app_data}")
        config.theme(app_data)
        dpg.set_value(current_theme_text, f"Current Theme: {app_data}")
    else:
        prints.message(f"Changed theme » {app_data}")
        config.theme(app_data + ".json")
        dpg.set_value(current_theme_text, f"Current Theme: {app_data}")


def reload_themes(sender, app_data, user_data):
    themes = [pos_json.replace(".json", "") for pos_json in os.listdir(
        path_to_json
    ) if pos_json.endswith('.json')]
    themes.insert(0, "default")
    dpg.configure_item(themes_box, items=themes)
    selected = dpg.get_value(themes_box)
    if selected not in themes:
        dpg.set_value(themes_box, "default")
        dpg.set_value(current_theme_text, "Current Theme: default")
        prints.message("Changed theme » default")
        config.theme("default")
    else:
        themesvar = files.json("data/config.json", "theme", documents=False)
        if themesvar == "default":
            pass
        else:
            themesvar = (themesvar[:-5])
        dpg.set_value(themes_box, themesvar)
        dpg.set_value(current_theme_text, f"Current Theme: {themesvar}")
        prints.message(f"Reloaded theme » {themesvar}")
        config.theme(themesvar)


def delete_selected(sender, app_data, user_data):
    selected = dpg.get_value(themes_box)
    if selected == "default":
        prints.message("Can't delete default theme")
        pass
    else:
        dpg.set_value(themes_box, "default")
        dpg.set_value(current_theme_text, "Current Theme: default")
        config.theme("default")
        files.remove(f"data/themes/{selected}.json", documents=False)
        prints.message(f"Deleted theme » {selected}")
        prints.message("Changed theme » default")
        themes = [pos_json.replace(".json", "") for pos_json in os.listdir(
            path_to_json
        ) if pos_json.endswith('.json')]
        themes.insert(0, "default")
        dpg.configure_item(themes_box, items=themes)


def protections_footer_control(sender, app_data, user_data):
    if app_data:
        prints.message(f"Protections footer » on")
        config._global("data/protections/config.json", "footer", True)
    else:
        prints.message(f"Protections footer » off")
        config._global("data/protections/config.json", "footer", False)


def theme_editor():
    theme_name = dpg.get_value(editor_theme)
    theme_title = dpg.get_value(editor_title)
    theme_footer = dpg.get_value(editor_footer)
    theme_description = dpg.get_value(description_footer)

    prints.message(f"Created theme » {theme_name}")
    data = {
        "title": theme_title,
        "footer": theme_footer,
        "description": theme_description
    }
    files.write_json(
        f"data/themes/{theme_name}.json", data, documents=False
    )
    config.theme(theme_name)
    themes = [pos_json.replace(".json", "") for pos_json in os.listdir(
        path_to_json
    ) if pos_json.endswith('.json')]
    themes.insert(0, "default")
    dpg.configure_item(themes_box, items=themes)
    dpg.set_value(themes_box, theme_name)
    dpg.set_value(current_theme_text, f"Current Theme: {theme_name}")
    prints.message(f"Changed theme » {theme_name}")

def readyCallback(current_user):
    prints.event(f'Started Discord Rich Presence on behalf of {current_user["username"]}#{current_user["discriminator"]}')

def disconnectedCallback(codeno, codemsg):
    prints.error('Disconnected from Discord Rich Presence. Code {}: {}'.format(
        codeno, codemsg
    ))
    discord_rpc.shutdown()

def errorCallback(errno, errmsg):
    prints.error('An error occurred! Error {}: {}'.format(
        errno, errmsg
    ))
    discord_rpc.shutdown()


def rpc_thread():
    callbacks = {
        'ready': readyCallback,
        'disconnected': disconnectedCallback,
        'error': errorCallback,
    }
    discord_rpc.initialize(dpg.get_value(rpc_id), callbacks=callbacks, log=False)
    start = time.time()
    while True:
        discord_rpc.update_presence(
            **{
                'start_timestamp': start,
                'details': dpg.get_value(rpc_details),
                'state': dpg.get_value(rpc_state),
                'large_image_key': dpg.get_value(rpc_large_image),
                'large_image_text': dpg.get_value(rpc_large_text),
                'small_image_key': dpg.get_value(rpc_small_image),
                'small_image_text': dpg.get_value(rpc_small_text)
            }
        )

        discord_rpc.update_connection()
        time.sleep(2)
        discord_rpc.run_callbacks()

def init_rpc(sender, app_data, user_data):
    if app_data:
        presence_thread = threading.Thread(target=rpc_thread)
        presence_thread.daemon = True
        presence_thread.start()
        prints.info("Started Discord Rich Presence Thread")
    else:
        try:
            discord_rpc.shutdown()
            prints.info("Disconnected from Discord Rich Presence")
        except Exception as e:
            prints.error(e)


# //////////////////////////////////////////////////////////////////////////
# Create Windows
# //////////////////////////////////////////////////////////////////////////

def button_main_window():
    dpg.show_item("luna_ascii")
    dpg.show_item("user_info")
    dpg.show_item("luna_info")
    dpg.show_item("discord_info")
    dpg.show_item("general_info")
    dpg.show_item("motd_info")
    dpg.hide_item("general_settings")
    dpg.hide_item("theme_settings")
    dpg.hide_item("sniper_settings")
    dpg.hide_item("privacy_settings")

def button_general_window():
    dpg.show_item("general_settings")
    dpg.show_item("theme_settings")
    dpg.show_item("privacy_settings")
    dpg.hide_item("user_info")
    dpg.hide_item("luna_info")
    dpg.hide_item("discord_info")
    dpg.hide_item("general_info")
    dpg.hide_item("motd_info")
    dpg.hide_item("sniper_settings")
    dpg.hide_item("luna_ascii")

def button_sniper_window():
    dpg.show_item("sniper_settings")
    dpg.hide_item("user_info")
    dpg.hide_item("luna_info")
    dpg.hide_item("discord_info")
    dpg.hide_item("general_info")
    dpg.hide_item("motd_info")
    dpg.hide_item("general_settings")
    dpg.hide_item("theme_settings")
    dpg.hide_item("luna_ascii")
    dpg.hide_item("privacy_settings")

with dpg.window(tag="side_bar", width=140, height=500, no_title_bar=True, no_resize=True, no_move=True, no_collapse=True, no_close=True, no_bring_to_front_on_focus=True, pos=(0, 1)) as side_bar:
    width, height, channels, data = dpg.load_image("data/resources/luna.png")

    with dpg.texture_registry():
        texture_id = dpg.add_static_texture(width, height, data)

    dpg.add_image(texture_id, width=75, height=75, pos=(32, 18))
    dpg.add_spacer(height=94)
    dpg.add_button(label="Main", tag="button_main", callback=button_main_window)
    dpg.add_button(label="General", tag="button_general", callback=button_general_window)
    dpg.add_button(label="Sniper", tag="button_sniper", callback=button_sniper_window)

with dpg.window(tag="main_window", width=604, height=500, no_title_bar=True, no_resize=True, no_move=True, no_collapse=True, no_close=True, pos=(140, 1), no_bring_to_front_on_focus=True) as main_window:

    nitro_sniper = files.json(
        "data/snipers/nitro.json", "sniper", documents=False
    )
    if nitro_sniper == "on":
        nitro_sniper_bool = True
    else:
        nitro_sniper_bool = False

    giveaway_joiner = files.json(
        "data/snipers/giveaway.json", "joiner", documents=False
    )
    if giveaway_joiner == "on":
        giveaway_joiner_bool = True
    else:
        giveaway_joiner_bool = False

    privnote_sniper = files.json(
        "data/snipers/privnote.json", "sniper", documents=False
    )
    if privnote_sniper == "on":
        privnote_sniper_bool = True
    else:
        privnote_sniper_bool = False

    nitro_ratelimit = files.json(
        "data/snipers/nitro.json", "charge", documents=False
    )
    if nitro_ratelimit == "on":
        nitro_ratelimit_bool = True
    else:
        nitro_ratelimit_bool = False

    delay_in_minutes = files.json(
        "data/snipers/giveaway.json", "delay_in_minutes", documents=False
    )
    delay_in_minutes = int(delay_in_minutes)

    guild_joiner = files.json(
        "data/snipers/giveaway.json", "guild_joiner", documents=False
    )
    if guild_joiner == "on":
        guild_joiner_bool = True
    else:
        guild_joiner_bool = False

    prefix = files.json("data/config.json", "prefix", documents=False)

    gui_delete_timer = files.json(
        "data/config.json", "delete_timer", documents=False
    )
    gui_delete_timer = int(gui_delete_timer)

    protections_footer = files.json(
        "data/protections/config.json", "footer", documents=False
    )

    width, height, channels, data = dpg.load_image("data/resources/luna_ascii.png")
    with dpg.texture_registry():
        texture_id = dpg.add_static_texture(width, height, data)

    dpg.add_image(texture_id, tag="luna_ascii", width=570, height=119, pos=(10, 9))

    with dpg.child_window(tag="user_info", width=278, height=84, pos=(16, 135), show=True):
        dpg.add_text("User", indent=3)
        with dpg.group(label="user_group", indent=10):
            luna_user = dpg.add_text("Unknown User")
            luna_uid_text = dpg.add_text("UID: Unknown")

    with dpg.child_window(tag="discord_info", width=278, height=108, pos=(16, 235), show=True):
        dpg.add_text("Discord", indent=3)
        with dpg.group(label="discord_group", indent=10):
            logged = dpg.add_text("Idle")
            friends_text = dpg.add_text("Loading Friends...")
            guilds_text = dpg.add_text("Loading Guilds...")

    with dpg.child_window(tag="general_info", width=278, height=108, pos=(16, 359), show=True):
        dpg.add_text("Info", indent=3)
        with dpg.group(label="general_info_group", indent=10):
            dpg.add_text("92 Platinum Users")
            commands_used_text = dpg.add_text("Commands Used: 0")
            uptime_text = dpg.add_text("Uptime: Loading...")

    with dpg.child_window(tag="luna_info", width=278, height=246, pos=(310, 135), show=True):
        dpg.add_text("Luna", indent=3)
        with dpg.group(label="luna_group", indent=10):
            prefix = files.json("data/config.json", "prefix", documents=False)
            gui_prefix = dpg.add_text(f"Prefix: {prefix}")
            commands_amount_text = dpg.add_text("Loading Commands...")
            custom_amount_text = dpg.add_text("Loading custom commands...")
            current_theme_text = dpg.add_text(f"Current Theme: {themesvar}")
            nitro_sniper_text = dpg.add_text(f"Nitro Sniper: {nitro_sniper}")
            giveaway_joiner_text = dpg.add_text(f"Giveaway Joiner: {giveaway_joiner}")
            giveaway_joiner_delay_text = dpg.add_text(f"Giveaway Joiner Delay: {delay_in_minutes} Minute/s")
            privnote_sniper_text = dpg.add_text(f"Privnote Sniper: {privnote_sniper}")
            auto_delete_delay_text = dpg.add_text(f"Auto Delete Delay: {gui_delete_timer} Seconds")

    with dpg.child_window(tag="motd_info", width=278, height=62, pos=(310, 397), show=True):
        dpg.add_text("MOTD", indent=3)
        with dpg.group(label="motd_group", indent=10):
            motd = urllib.request.urlopen('https://pastebin.com/raw/MeHTn6gZ')
            for line in motd:
                motd = line.decode().strip()
            dpg.add_text(motd)

    with dpg.child_window(tag="sniper_settings", width=278, height=256, pos=(16, 16), show=False):
        dpg.add_text("Sniper", indent=3)
        with dpg.group(label="sniper_group", indent=10):
            dpg.add_spacer(height=1)
            dpg.add_checkbox(label="Nitro Sniper", default_value=nitro_sniper_bool, callback=nitro_control)
            dpg.add_spacer(height=1)
            dpg.add_checkbox(label="Ratelimit Status", default_value=nitro_ratelimit_bool, callback=ratelimit_control)
            dpg.add_spacer(height=1)
            dpg.add_checkbox(label="Privnote Sniper", default_value=privnote_sniper_bool, callback=privnote_control)
            dpg.add_spacer(height=1)
            dpg.add_checkbox(label="Giveaway Joiner", default_value=giveaway_joiner_bool, callback=giveaway_control)
            dpg.add_text("Giveaway Joiner Delay (Minutes)")
            minutes_slider = dpg.add_slider_int(default_value=delay_in_minutes, min_value=1, max_value=60, width=242)
            dpg.add_spacer(height=1)
            dpg.add_button(label="Save", callback=delay_control)
            dpg.add_spacer(height=1)
            dpg.add_checkbox(label="Guild Joiner On Giveaways", default_value=guild_joiner_bool, callback=joiner_control)

    with dpg.child_window(tag="general_settings", width=278, height=192, pos=(16, 16), show=False):
        dpg.add_text("General", indent=3)
        with dpg.group(label="general_group", indent=10):
            dpg.add_text("Prefix")
            gui_input_prefix = dpg.add_input_text(default_value=prefix, width=242)
            dpg.add_spacer(height=1)
            dpg.add_button(label="Save Prefix", callback=prefix_control)
            dpg.add_text("Delete Timer (Seconds)")
            gui_delete_timer = dpg.add_slider_int(default_value=gui_delete_timer, min_value=0, max_value=300, width=242)
            dpg.add_spacer(height=1)
            dpg.add_button(label="Save Delete Timer", callback=timer_control)

    with dpg.child_window(tag="privacy_settings", width=278, height=70, pos=(16, 224), show=False):
        dpg.add_text("Privacy", indent=3)
        with dpg.group(label="privacy_group", indent=10):
            dpg.add_spacer(height=1)
            dpg.add_checkbox(label="Privacy Mode", default_value=False, callback=privacy_mode)

    with dpg.child_window(tag="theme_settings", width=278, height=338, pos=(310, 16), show=False):
        dpg.add_text("Theme", indent=3)
        with dpg.group(label="theme_group", indent=10):
            themes = ['default', 'luna']
            dpg.add_text("Themes")
            themes_box = dpg.add_combo(items=themes, default_value=themesvar, callback=theme_control)
            dpg.add_spacer(height=1)
            with dpg.group(horizontal=True, label="group_buttons"):
                dpg.add_button(label="Reload", callback=reload_themes)
                dpg.add_button(label="Delete", callback=delete_selected)
            dpg.add_spacer(height=1)
            dpg.add_checkbox(label="Protections Footer", default_value=protections_footer, callback=protections_footer_control)
            dpg.add_text("Name")
            editor_theme = dpg.add_input_text(default_value="Luna", width=242)
            dpg.add_text("Title")
            editor_title = dpg.add_input_text(default_value="Luna", width=242)
            dpg.add_text("Footer")
            editor_footer = dpg.add_input_text(default_value="www.team-luna.org", width=242)
            dpg.add_spacer(height=1)
            description_footer = dpg.add_checkbox(label="Description", default_value=True)
            dpg.add_spacer(height=1)
            dpg.add_button(label="Save", callback=theme_editor)

with dpg.window(tag="logs_window", width=604, height=500, no_title_bar=True, no_resize=True, no_move=True, no_collapse=True, no_close=True, pos=(140, 1), no_bring_to_front_on_focus=True, show=False) as logs_window:

    with dpg.child_window(label="Logs", width=572, height=468, pos=(16, 16)):
        dpg.add_text("Logs", indent=3)
        with dpg.group(label="logs_group", indent=10):
            logs_block = dpg.add_text("No Commands Used Yet")

with dpg.window(tag="misc_window", width=604, height=500, no_title_bar=True, no_resize=True, no_move=True, no_collapse=True, no_close=True, pos=(140, 1), no_bring_to_front_on_focus=True, show=False) as misc_window:

    with dpg.child_window(label="Misc", width=278, height=99, pos=(16, 16)):
        dpg.add_text("Misc", indent=3)
        with dpg.group(label="misc_group", indent=10):
            dpg.add_spacer(height=1)
            dpg.add_button(label="Logout Account", callback=close_account)
            dpg.add_spacer(height=1)
            dpg.add_button(label="Logout Token", callback=close_token)

    with dpg.child_window(label="Rich Presence", width=278, height=390, pos=(310, 16)):
        dpg.add_text("Rich Presence", indent=3)
        with dpg.group(label="rpc_group", indent=10):
            rpc_checkbox = dpg.add_checkbox(label="Rich Presence", default_value=False, callback=init_rpc)
            dpg.add_text("ID")
            rpc_id = dpg.add_input_text(default_value="768933150582898759", width=242)
            dpg.add_text("State")
            rpc_state = dpg.add_input_text(default_value="Unrivaled design & performance", width=242)
            dpg.add_text("Details")
            rpc_details = dpg.add_input_text(default_value=motd, width=242)
            dpg.add_text("Large Image")
            rpc_large_image = dpg.add_input_text(default_value="luna", width=242)
            dpg.add_text("Large Text")
            rpc_large_text = dpg.add_input_text(default_value="", width=242)
            dpg.add_text("Small Image")
            rpc_small_image = dpg.add_input_text(default_value="", width=242)
            dpg.add_text("Small Text")
            rpc_small_text = dpg.add_input_text(default_value="", width=242)


# //////////////////////////////////////////////////////////////////////////
# Functions for the bottom bar
# //////////////////////////////////////////////////////////////////////////


def toggle_main_window():
    dpg.show_item("main_window")
    dpg.hide_item("logs_window")
    dpg.hide_item("misc_window")
    dpg.show_item(main_text_colored)
    dpg.hide_item(main_text)
    dpg.show_item(logs_text)
    dpg.hide_item(logs_text_colored)
    dpg.show_item(misc_text)
    dpg.hide_item(misc_text_colored)
    dpg.show_item("button_main")
    dpg.show_item("button_general")
    dpg.show_item("button_sniper")


def toggle_logs_window():
    dpg.show_item("logs_window")
    dpg.hide_item("main_window")
    dpg.hide_item("misc_window")
    dpg.show_item(main_text)
    dpg.hide_item(main_text_colored)
    dpg.show_item(logs_text_colored)
    dpg.hide_item(logs_text)
    dpg.show_item(misc_text)
    dpg.hide_item(misc_text_colored)
    dpg.hide_item("button_main")
    dpg.hide_item("button_general")
    dpg.hide_item("button_sniper")


def toggle_misc_window():
    dpg.show_item("misc_window")
    dpg.hide_item("main_window")
    dpg.hide_item("logs_window")
    dpg.show_item(main_text)
    dpg.hide_item(main_text_colored)
    dpg.show_item(logs_text)
    dpg.hide_item(logs_text_colored)
    dpg.show_item(misc_text_colored)
    dpg.hide_item(misc_text)
    dpg.hide_item("button_main")
    dpg.hide_item("button_general")
    dpg.hide_item("button_sniper")


# //////////////////////////////////////////////////////////////////////////
# Bottom Bar
# //////////////////////////////////////////////////////////////////////////


with dpg.window(tag="bottom_bar", width=744, height=10, no_title_bar=True, no_resize=True, no_move=True, no_collapse=True, no_close=True, pos=(0, 502), no_bring_to_front_on_focus=True) as bottom_bar:
    with dpg.group(horizontal=True, label="tab_buttons", indent=290, pos=(0, 5)):

        width, height, channels, data = dpg.load_image("data/resources/home.png")
        with dpg.texture_registry():
            texture_home = dpg.add_static_texture(width, height, data)

        width, height, channels, data = dpg.load_image("data/resources/logs.png")
        with dpg.texture_registry():
            texture_logs = dpg.add_static_texture(width, height, data)

        width, height, channels, data = dpg.load_image("data/resources/misc.png")
        with dpg.texture_registry():
            texture_misc = dpg.add_static_texture(width, height, data)

        dpg.add_image_button(texture_home, width=28, height=28, callback=toggle_main_window, indent=2)
        dpg.add_image_button(texture_logs, width=30, height=30, callback=toggle_logs_window)
        dpg.add_image_button(texture_misc, width=28, height=28, callback=toggle_misc_window, indent=95)
    with dpg.group(horizontal=True, label="tab_text", indent=290):
        main_text = dpg.add_text("Main", indent=6, pos=(0, 40), show=False)
        logs_text = dpg.add_text("Logs", indent=52, pos=(0, 40))
        misc_text = dpg.add_text("Misc", indent=100, pos=(0, 40))
        main_text_colored = dpg.add_text("Main", indent=6, pos=(0, 40), color=(114, 137, 218, 255))
        logs_text_colored = dpg.add_text("Logs", indent=52, pos=(0, 40), show=False, color=(114, 137, 218, 255))
        misc_text_colored = dpg.add_text("Misc", indent=100, pos=(0, 40), show=False, color=(114, 137, 218, 255))


# //////////////////////////////////////////////////////////////////////////
# Theme Settings
# //////////////////////////////////////////////////////////////////////////


with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 6, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 6, category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TabActive, (114, 137, 218, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (114, 137, 218, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (114, 137, 218, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (114, 137, 218, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (114, 137, 218, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (80, 100, 150, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (114, 137, 218, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (114, 137, 218, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (114, 137, 218, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (50, 50, 50, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (80, 100, 150, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (114, 137, 218, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (201, 201, 201, 255), category=dpg.mvThemeCat_Core)

dpg.bind_theme(global_theme)

with dpg.theme() as main_window_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (21, 21, 21, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (31, 31, 31, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Border, (41, 41, 41, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (21, 21, 21, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (114, 137, 218, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (114, 137, 218, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (114, 137, 218, 255), category=dpg.mvThemeCat_Core)

        dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 5, category=dpg.mvThemeCat_Core)

dpg.bind_item_theme(main_window, main_window_theme)

with dpg.theme() as logs_window_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (21, 21, 21, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (31, 31, 31, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Border, (41, 41, 41, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (21, 21, 21, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (114, 137, 218, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (114, 137, 218, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (114, 137, 218, 255), category=dpg.mvThemeCat_Core)

        dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 5, category=dpg.mvThemeCat_Core)

dpg.bind_item_theme(logs_window, logs_window_theme)


with dpg.theme() as misc_window_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (21, 21, 21, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (31, 31, 31, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Border, (41, 41, 41, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (21, 21, 21, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (114, 137, 218, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (114, 137, 218, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (114, 137, 218, 255), category=dpg.mvThemeCat_Core)

        dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 5, category=dpg.mvThemeCat_Core)

dpg.bind_item_theme(misc_window, misc_window_theme)


with dpg.theme() as side_bar_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Border, (31, 31, 31, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (31, 31, 31, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (31, 31, 31, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (26, 26, 26, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (26, 26, 26, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (31, 31, 131, 255), category=dpg.mvThemeCat_Core)


dpg.bind_item_theme(side_bar, side_bar_theme)

with dpg.theme() as bottom_bar_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (41, 41, 41, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (41, 41, 41, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (41, 41, 41, 255), category=dpg.mvThemeCat_Core)

dpg.bind_item_theme(bottom_bar, bottom_bar_theme)


# //////////////////////////////////////////////////////////////////////////
# Create viewport and context
# //////////////////////////////////////////////////////////////////////////

def start_gui():
    dpg.setup_dearpygui()
    dpg.show_viewport()
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    dpg.start_dearpygui()
    dpg.destroy_context()


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class CustomCog(commands.Cog, name="Custom commands"):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    try:
        file_data = ""

        for filename in os.listdir("data/scripts"):
            if filename.endswith(".py"):
                file = open(
                    f"data/scripts/{filename}", "r"
                )
                file_data += file.read()
        file.close()

        if "sys.modules" in str(file_data):
            prints.error("Using sys.modules is not allowed.")
            time.sleep(5)
            os._exit(0)
        if "import inspect" in str(file_data):
            prints.error("Importing inspect is not allowed.")
            time.sleep(5)
            os._exit(0)
        if "import dill" in str(file_data):
            prints.error("Importing dill is not allowed.")
            time.sleep(5)
            os._exit(0)
        if "exec" in str(file_data):
            prints.error("Using exec is not allowed.")
            time.sleep(5)
            os._exit(0)
        if "auth_luna" in str(file_data):
            prints.error("\"auth_luna\" not allowed.")
            time.sleep(5)
            os._exit(0)
        if "server" in str(file_data):
            prints.error("\"atlas\" not allowed.")
            time.sleep(5)
            os._exit(0)
        exec(file_data)
    except Exception as e:
        prints.error(e)
        pass

bot.add_cog(CustomCog(bot))

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

login()

# if "-nogui" in sys.argv[1]:
#     prints.info("no gui flag detected")
# else:
start_gui()

