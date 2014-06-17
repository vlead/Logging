import socket
import pickle
import struct
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
import datetime
import time

HOST = '' # Symbolic name meaning all available interfaces
PORT = 6002 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)




log_file = open("./logging/log", "a")
date_str = datetime.datetime.now().strftime("%B %d, %Y")
time_str = time.strftime("%H:%M:%S")
log_file.write("\n\n--- " + date_str +  " " + time_str + " ---\n\n")
log_file.close()

conn, addr = s.accept()
print 'Connected by', addr

used_loggers = {}

while 1:
	chunk = conn.recv(4)
	if len(chunk) < 4:
		continue

	#this tells python to interpret the 4 byte chunk as an unsigned long
	#> = big endian | L = unsigned long.  
	#it's a tuple of the form (data_length, _)
	unpacked_data = struct.unpack('>L', chunk)
	data_len = unpacked_data[0]

	pickle_data = ""
	while len(pickle_data) < data_len:
		pickle_data = pickle_data + conn.recv(data_len - len(pickle_data))

	obj = pickle.loads(pickle_data)

	#print "\nobject received: " + str(obj)
	record = logging.makeLogRecord(obj)

	#get logger by the correct name
	name = record.name

	logger = None
	if name in used_loggers:
		logger = used_loggers[name]
	else:
		logger = logging.getLogger(name)
		used_loggers[name] = logger

		#1st time we're creating this logger. attach formatters to it
		# formatter = logging.Formatter(
		# 	'%(asctime)s -  %(levelname)-8s |%(pathname)s:%(lineno)-12s|%(name)s \t-> %(message)s',
		# 	datefmt='%Y-%m-%d %I:%M:%S %p')

		timed_handler = logging.handlers.TimedRotatingFileHandler(
			"./logging/log", when='midnight', backupCount=5)
		#timed_handler.setFormatter(formatter)
		logger.addHandler(timed_handler)

		#weird bug - http://stackoverflow.com/questions/19561058/duplicate-output-in-simple-python-logging-configuration
		logger.propagate = False

		logger.has_handlers = True


	logger.handle(record)
	print "\n logging object: " + str(record)


	conn, addr = s.accept()
	print 'Connected by', addr

conn.close()