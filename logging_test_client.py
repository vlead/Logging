import logging
import logging.handlers # you NEED this line
from random import randint
import datetime

logger = logging.getLogger("Module")
logger.setLevel(logging.DEBUG)
socketHandler = logging.handlers.SocketHandler('localhost', 6002)
http_handler = logging.handlers.HTTPHandler('localhost:5000', '/log/message/', method='GET')

#logger.addHandler(socketHandler)
logger.addHandler(http_handler)

if randint(0, 2) == 0:
	logger.setLevel(logging.WARN)
else:
	logger.setLevel(logging.WARN)

logger.error(str(datetime.datetime.now().time()) + " " + str(randint(0, 1000)))