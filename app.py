from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Dosewise Backend'

if __name__ == '__main__':
    app.run(debug=True, port=8080)
