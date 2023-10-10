import logging
import os



LOG_FILE = 'download.log'
logs_path = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_path, exist_ok=True)
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
	filename=LOG_FILE_PATH,
	format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
	datefmt='%m/%d/%Y %H:%M:%S',
	level=logging.INFO,

	)