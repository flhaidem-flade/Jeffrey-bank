from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "🏦 Jeffrey Bank is LIVE 🚀"

