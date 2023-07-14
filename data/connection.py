from dotenv import load_dotenv
import databases
import os

load_dotenv(override=True)
database = databases.Database(os.environ["MYSQL_ADDON_URI"])
