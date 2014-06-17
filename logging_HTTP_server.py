from flask import Flask
from flask import request

import socket
import pickle
import struct
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
import datetime
import time

app = Flask(__name__)


used_loggers = {}

@app.route('/log/message/', methods=['GET', 'POST'])
def log():
	
	name = request.args.get('name')
	thread = request.args.get('thread')
	created = request.args.get('created')
	process = request.args.get('process')
	processName = request.args.get('processName')
	args = request.args.get('args')
	module = request.args.get('module')
	filename = request.args.get('filename')
	levelno = request.args.get('levelno')
	exc_text = request.args.get('exc_text')
	pathname = request.args.get('pathname')
	lineno = request.args.get('lineno')
	exc_info = request.args.get('exc_info')
	funcName = request.args.get('funcName')
	relativeCreated = request.args.get('relativeCreated')
	levelname = request.args.get('levelname')
	msecs = request.args.get('msecs')
	msg = request.args.get('msg')

	print 'name ' + name
	print 'thread ' + thread
	print created 
	print process
	print processName
	print args
	print module
	print 'filename ' + filename
	print 'levelno ' + levelno
	print exc_text
	print 'pathname ' + pathname
	print 'lineno ' + lineno
	print relativeCreated
	print 'levelname ' + levelname
	print msecs
	print 'message ' + msg


	print '\n exc_info: ' + exc_info
	print '\n exc_text: ' + exc_text

 	#logging.makeLogRecord(msg)

	#get logger by the correct name
	#name = record.name


	logger = None

	if name in used_loggers:
		logger = used_loggers[name]
	else:
		logger = logging.getLogger(name)
		used_loggers[name] = logger

		formatter = logging.Formatter(
			'%(asctime)s -  %(levelname)-8s |%(pathname)s:%(lineno)-12s|%(name)s \t-> %(message)s',
			datefmt='%Y-%m-%d %I:%M:%S %p')

		timed_handler = logging.handlers.TimedRotatingFileHandler(
			"./logging/log", when='midnight', backupCount=5)
		#timed_handler.setFormatter(formatter)
		logger.addHandler(timed_handler)

		#weird bug - http://stackoverflow.com/questions/19561058/duplicate-output-in-simple-python-logging-configuration
		logger.propagate = False
		logger.has_handlers = True

	#name, lvl, fn, lno, msg, args, exc_info, func=None, extra=None


	#1st time we're creating this logger. attach formatters to it
	fmt_string = " %(levelname)-8s |%(pathname)s:%(lineno)-12s|%(name)s \t-> %(message)s"


	print "\n\n message: " + fmt_string + " | args = " + args

	my_args = {
			
			'levelname': levelname, 
			'pathname': pathname, 
			'lineno': lineno, 
			'name': name, 
			'message': msg
			}

	record = logger.makeRecord(name, levelname, funcName, lineno, "%(levelname)-8s |%(pathname)s:%(lineno)-12s|%(name)s -> %(message)s", my_args, None)
	logger.handle(record)
	return "log successful"

	#return "\n logging object: " + str(record)

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id
if __name__ == '__main__':
	#app.debug = True
	app.run(debug=True)