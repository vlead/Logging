import requests

string = 'threadName=MainThread&name=Module&thread=47357646035584&created=1402983570.46&process=23649&processName=MainProcess&args=()&module=logging_test_client&filename=logging_test_client.py&levelno=30&exc_text=None&pathname=logging_test_client.py&lineno=19&msg=11%3A09%3A30.457934+441&exc_info=None&funcName=%3Cmodule%3E&relativeCreated=9.73606109619&levelname=WARNING&msecs=457.986116409'



r =  requests.post('http://localhost:5000/log/message/')
print r
print r.text
