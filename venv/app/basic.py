from flask import Flask
app = Flask(__name__)

@app.route('/loc',)
def index():
    print('Hello World')
    return "Hello World"

if __name__ == "__main__":
    print('Hello World Init')
    app.run(debug=True, port=5001)
    
