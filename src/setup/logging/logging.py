import logging

# Configure the logging settings
logging.basicConfig(
    level=logging.DEBUG,  # Set the desired logging level
    format="%(asctime)s [%(levelname)s] %(message)s",  # Define the log message format
    handlers=[
        logging.StreamHandler()  # Output logs to the console
    ]
)

logging.info