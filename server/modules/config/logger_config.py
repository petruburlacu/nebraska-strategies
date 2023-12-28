import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG)
logger = logging.getLogger()

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)