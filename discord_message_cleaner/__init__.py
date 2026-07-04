# -*- coding: utf-8 -*-
# DiscordMessageCleaner
# Project by https://github.com/rix1337

import argparse
import asyncio
import datetime
import sys
import time
import logging

import discord
from discord.ext import commands

from discord_message_cleaner.providers import version


async def delete_old_messages(destination, cutoff):
    async for msg in destination.history(limit=None, before=cutoff):
        try:
            await msg.delete()
            print(f"[DiscordMessageCleaner] Deleted: {msg.id}")
            await asyncio.sleep(1.1)  # Small delay to avoid hitting rate limits
        except discord.Forbidden:
            print(f"[DiscordMessageCleaner] Missing permissions to delete message {msg.id}")
        except discord.HTTPException as e:
            print(f"[DiscordMessageCleaner] Rate limited or failed to delete {msg.id}: {e}")
            await asyncio.sleep(5)  # Wait longer if rate-limited


async def delete_thread_if_empty(thread):
    try:
        if not [msg async for msg in thread.history(limit=1)]:
            await thread.delete(reason="Thread is empty after message cleanup")
            print(f"[DiscordMessageCleaner] Deleted empty thread: {thread.id}")
    except discord.Forbidden:
        print(f"[DiscordMessageCleaner] Missing permissions to delete empty thread {thread.id}")
    except discord.HTTPException as e:
        print(f"[DiscordMessageCleaner] Failed to check or delete thread {thread.id}: {e}")


async def clean_threads(channel, cutoff):
    threads = {thread.id: thread for thread in channel.threads}

    try:
        async for thread in channel.archived_threads(limit=None):
            threads[thread.id] = thread
    except (discord.Forbidden, discord.HTTPException) as e:
        print(f"[DiscordMessageCleaner] Failed to list archived threads: {e}")

    if isinstance(channel, discord.TextChannel):
        try:
            async for thread in channel.archived_threads(limit=None, private=True):
                threads[thread.id] = thread
        except (discord.Forbidden, discord.HTTPException) as e:
            print(f"[DiscordMessageCleaner] Failed to list private archived threads: {e}")

    for thread in threads.values():
        await delete_old_messages(thread, cutoff)
        await delete_thread_if_empty(thread)


def run():
    print("[DiscordMessageCleaner] Version " + version.get_version() + " by rix1337")

    parser = argparse.ArgumentParser()
    parser.add_argument("--token", help="Discord Bot Token")
    parser.add_argument("--channel_id", help="Discord Channel ID with the bot already in it")
    parser.add_argument("--days", type=int, default=7, help="Number of days to keep messages (default: 7)")
    arguments = parser.parse_args()

    if not arguments.token:
        print("[DiscordMessageCleaner] Please provide a token using --token")
        sys.exit(1)
    if not arguments.channel_id:
        print("[DiscordMessageCleaner] Please provide a channel ID using --channel_id")
        sys.exit(1)

    token = arguments.token
    channel_id = int(arguments.channel_id)
    days = int(arguments.days)

    print(f"[DiscordMessageCleaner] Token: {token}")
    print(f"[DiscordMessageCleaner] Channel ID: {channel_id}")
    print(f"[DiscordMessageCleaner] Days: {days}")

    try:
        while True:
            intents = discord.Intents.default()
            intents.messages = True
            bot = commands.Bot(command_prefix='!', intents=intents)

            logging.getLogger('discord.ext.commands.bot').setLevel(logging.ERROR)
            logging.getLogger('discord.gateway').setLevel(logging.ERROR)
            logging.getLogger('discord.client').setLevel(logging.ERROR)

            @bot.event
            async def on_ready():
                print(f'[DiscordMessageCleaner] Logged in as {bot.user}')
                channel = bot.get_channel(channel_id)

                if channel:
                    cutoff = discord.utils.utcnow() - datetime.timedelta(days=days)
                    if isinstance(channel, discord.TextChannel):
                        await delete_old_messages(channel, cutoff)
                    if isinstance(channel, (discord.TextChannel, discord.ForumChannel)):
                        await clean_threads(channel, cutoff)

                await bot.close()

            bot.run(token)

            print("[DiscordMessageCleaner] Finished cleaning messages. Restarting in 1 hour...")
            time.sleep(60 * 60)

    except KeyboardInterrupt:
        sys.exit(0)

    except Exception as e:
        print(f"[DiscordMessageCleaner] An error occurred: {e}")
        pass
