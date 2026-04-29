from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Le site de billetterie arrive !"

if __name__ == '__main__':
    app.run(debug=True)