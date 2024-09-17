from decouple import config
import os

URL = config("URL")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_FOLDER = os.path.join(ROOT, "downloads")
REMOTE_URL = config("REMOTE_URL") if config("REMOTE_URL") else None
OUTPUT_FOLDER = os.path.join(ROOT, "output")
