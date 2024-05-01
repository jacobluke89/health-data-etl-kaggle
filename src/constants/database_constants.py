from dotenv import load_dotenv
import os
load_dotenv()

# Access environment variables
SPARK_URL = os.getenv("SPARK_URL")
SPARK_DRIVER = os.getenv("SPARK_DRIVER")
SPARK_JAR_PATH = os.getenv("SPARK_JAR_PATH")
SPARK_WAREHOUSE = os.getenv("SPARK_WAREHOUSE")

os.environ['PYARROW_IGNORE_TIMEZONE'] = '1'

jdbc_url = SPARK_URL
properties = {
    "driver": SPARK_DRIVER
}
