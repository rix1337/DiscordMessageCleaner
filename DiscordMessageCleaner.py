# -*- coding: utf-8 -*-
# DiscordMessageCleaner
# Project by https://github.com/rix1337

import multiprocessing

import discord_message_cleaner
from discord_message_cleaner import run

if __name__ == '__main__':
    multiprocessing.freeze_support()
    discord_message_cleaner.run()
