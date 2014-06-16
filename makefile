run:
	python2 logging_server.py &

client:
	python2 logging_test_client.py &

kill:
	sudo pkill python2

cat:
	cat logging/log