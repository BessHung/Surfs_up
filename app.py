from flask import Flask

app = Flask(__name__)

# Create Flask Routes
@app.route('/') #'/' means the root of our routes.
def hello_world():
    return 'Hello world'
