
from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/colourize')
def colourize():
    return render_template('colourize.html')

if __name__ == "__main__":
    app.run(debug=True,port=8000)

