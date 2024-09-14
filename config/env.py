import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "SPL_USERS_BASE_URL": os.getenv("SPL_USERS_BASE_URL", "http://localhost:30001/api"),
    "SPL_USERS_TOKEN": os.getenv("SPL_USERS_TOKEN", "-"),
    "SPORTLIFE_BASE_URL": os.getenv("SPORTLIFE_BASE_URL", "https://sportnorte.com/app"),
}
