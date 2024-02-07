from dotenv import load_dotenv
import os

class ColConstants:
    peds = "pediatric_"
    geri = "geriatric_"


load_dotenv()

# Access environment variables
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_URL = os.getenv("POSTGRES_URL")
POSTGRES_DRIVER = os.getenv("POSTGRES_DRIVER")
POSTGRES_JAR_PATH = os.getenv("POSTGRES_JAR_PATH")

jdbc_url = POSTGRES_URL
properties = {
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
    "driver": POSTGRES_DRIVER
}
