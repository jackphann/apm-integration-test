import logging

from flask import Flask
from flask import Flask, render_template
import elasticapm
from elasticapm.contrib.flask import ElasticAPM


app = Flask(__name__)

app.config['ELASTIC_APM'] = {
  # Set required service name. Allowed characters:
  # a-z, A-Z, 0-9, -, _, and space
  'SERVICE_NAME': 'test',

  # Use if APM Server requires a token
  'SECRET_TOKEN': '',

  # Set custom APM Server URL (default: http://localhost:8200)
  'SERVER_URL': '',

  # Allowed values: development/staging/production
  'ENVIRONMENT': 'development',

  'DISABLE_METRICS': "*.cpu.*,*.memory.*"

  # If app is in debug mode, the agent won’t send any data to the APM Server.
  # If you want to send data to APM server in debug mode, please uncomment the following line.
  # 'DEBUG': True

  # Independent from debug mode, uncomment the following line to not send and data to APM Server.
  # 'DISABLE_SEND': False

}

apm = ElasticAPM(app, logging=logging.ERROR)



@app.errorhandler(404)
def not_found_error(error):
 return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
 return render_template('500.html'), 500


@elasticapm.capture_span()
def call_me():
  return 1

@elasticapm.capture_span()
def my_func():
  call_me()

  for i in range(100000):
    continue

@app.route('/')
def index():
  my_func()
  return "Hello World!"


@app.route('/error')
def divbyzero():
    num = 2 / 0
    return "hello world - " + str(num)


app.run()