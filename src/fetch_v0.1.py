import logging
from logging.handlers import TimedRotatingFileHandler
import time
import os
import requests

forti_logger = logging.getLogger("forti_logger")
forti_logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(
    filename="/app/logs/fortidlp_logs.log",
    when="midnight",
    interval=1,
    backupCount=7,
    encoding="utf-8"
)

formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)

forti_logger.addHandler(handler)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

forti_api_url = os.getenv('FORTI_API_URL')
forti_api_token = os.getenv('FORTI_API_TOKEN')
time_to_sleep = int(os.getenv('TIME_TO_SLEEP', '60'))

if not forti_api_url or not forti_api_token:
    raise ValueError("Missing environment variables: FORTI_API_URL and/or FORTI_API_TOKEN")

headers_str = {
    'Authorization': f'Bearer {forti_api_token}'
}

while True:
    logging.info("Polling FortiDLP")
    try:
        response = requests.request("GET", forti_api_url, headers=headers_str, data={})
        if response.ok and len(response.text) > 0:
            logging.info("Received logs successfully.")
            logging.info(response.text.strip())
            forti_logger.info(response.text.strip())
        else:
            logging.info(f"No Logs or Failed to get logs. Status code: {response.status_code} Response: {response.text.strip()}")
    except Exception as e:
        logging.error(f"Exception occurred while polling logs: {e}")
    time.sleep(time_to_sleep)
