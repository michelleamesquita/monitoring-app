import time
import random
from flask import request
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
metrics = PrometheusMetrics(app)

@app.route('/')
def new():
    celsius = request.args.get("celsius", "")
    if celsius:
        fahrenheit = fahrenheit_from(celsius)
    else:
        fahrenheit = ""

    return (
        	"""<h2> It's a simple web app! 🦊 </h2>"""
		"""<br>"""
		"""<form action="" method="get">
                <input type="text" name="celsius">
                <input type="submit" value="Convert">
            </form>"""
        + "Fahrenheit: "
        + '<a id="fahrenheit">' +fahrenheit+ '</a>'

    )
    # return 'OK'
@app.route("/<int:celsius>")
def fahrenheit_from(celsius):
    """Convert Celsius to Fahrenheit degrees."""
    fahrenheit = float(celsius) * 9 / 5 + 32
    fahrenheit = round(fahrenheit, 3) 
    return str(fahrenheit)


@app.route('/metrics')
@metrics.do_not_track()
@metrics.histogram('http_request_duration_seconds', 'Duration of HTTP requests in seconds',buckets= [0.1, 0.3, 0.5, 0.7, 1, 3, 5, 7, 10],
         labels={'item_type': lambda: request.view_args['type']})
@metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
def metric():
    pass


@app.route('/order')
def test():
    
    time.sleep(random.random() * 0.8)
    return 'Order created successfully'

@app.route('/error')
def oops():
    return ':(', 500

@app.route('/skip')
@metrics.do_not_track()
def skip():
    pass  # default metrics are not collected


if __name__ == '__main__':
    app.run('0.0.0.0', 8080)
