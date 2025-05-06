import discord
import sys
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import argparse
import os
from dotenv import load_dotenv

extDataDir = os.getcwd()
if getattr(sys, 'frozen', False):
    extDataDir = sys._MEIPASS
load_dotenv(dotenv_path=os.path.join(extDataDir, '.env'))

parser = argparse.ArgumentParser(prog="Spotify Mute", description="Mutes spotify with the help of discord")
parser.add_argument("username", help="User to mute")

TOKEN = os.getenv('DISCORD_TOKEN')
args = parser.parse_args()

intents = discord.Intents.default()
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("This bot sure has logged in, hasn't it :0")

@client.event
async def on_presence_update(before, after):
    spotify = False
    print(after.global_name)
    if (after.global_name != args.username):
        return
    print(after.activities)
    for element in after.activities:
        if element.type == discord.ActivityType.listening:
            spotify = True
    print(spotify)
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        try:
            if session.Process and session.Process.name() == "Spotify.exe":
                volume = session.SimpleAudioVolume
                if spotify:
                    volume.SetMute(0, None)
                else:
                    volume.SetMute(1, None)
        except Exception as e:
            print(f"Failed to access session info: {e}")

client.run(TOKEN)
input("Press Enter to exit...")

