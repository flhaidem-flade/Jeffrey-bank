from flask import Flask, request, redirect, render_template_string, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secretkey123"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bank.db"
db = SQLAlchemy(app)

# DATABASE
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(200))
    balance = db.Column(db.Float, default=0)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    if "user" in session:
        user = User.query.filter_by(username=session["user"]).first()
        return f"""
        <h1>Welcome {user.username}</h1>
        <p>Balance: ₦{user.balance}</p>
        <a href='/deposit'>Deposit</a><br>
        <a href='/withdraw'>Withdraw</a><br>
        <a href='/logout'>Logout</a>
        """
    return "<a href='/login'>Login</a> | <a href='/register'>Register</a>"

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=generate_password_hash(request.form["password"])
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return "<form method='post'>User:<input name='username'> Pass:<input name='password' type='password'><button>Register</button></form>"

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            session["user"] = user.username
            return redirect("/")
    return "<form method='post'>User:<input name='username'> Pass:<input name='password' type='password'><button>Login</button></form>"

@app.route("/deposit", methods=["GET","POST"])
def deposit():
    user = User.query.filter_by(username=session["user"]).first()
    if request.method == "POST":
        user.balance += float(request.form["amount"])
        db.session.commit()
        return redirect("/")
    return "<form method='post'>Amount:<input name='amount'><button>Deposit</button></form>"

@app.route("/withdraw", methods=["GET","POST"])
def withdraw():
    user = User.query.filter_by(username=session["user"]).first()
    if request.method == "POST":
        amt = float(request.form["amount"])
        if amt <= user.balance:
            user.balance -= amt
            db.session.commit()
        return redirect("/")
    return "<form method='post'>Amount:<input name='amount'><button>Withdraw</button></form>"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
