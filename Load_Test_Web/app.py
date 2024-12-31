from flask import Flask, render_template, request
import random  # For simulating logs

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    url = request.form['url']
    total_time = request.form['total_time']
    num_requests = request.form['num_requests']
    interval_unit = request.form['interval_unit']
    
    # Simulating request logs with different types
    logs = [
        {"type": "info", "message": f"Request to {url} sent."},
        {"type": "success", "message": f"Response received for {url}. Status: 200 OK"},
        {"type": "warning", "message": f"Request took 120ms to complete."}
    ]
    
    return render_template('result.html', url=url, total_time=total_time,
                           num_requests=num_requests, interval_unit=interval_unit,
                           logs=logs)

if __name__ == '__main__':
    app.run(debug=True)
