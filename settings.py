import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ACCESS_TOKEN = os.environ.get("DISCORD_ACCESS_TOKEN")
CHANNEL_ID = os.environ.get("DISCORD_CHANNEL_ID")
