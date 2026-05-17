from flask import Flask, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secretkey123"

# database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bank.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# USER MODEL
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    balance = db.Column(db.Float, default=0)

with app.app_context():
    db.create_all()

# HOME PAGE
@app.route("/")
def home():
    user = session.get("user")

    if user:
        db_user = User.query.filter_by(username=user).first()
        balance = db_user.balance if db_user else 0

        return f"""
        <html>
        <body style="font-family:Arial;text-align:center;background:#0f172a;color:white;padding:20px">

            <h1>🏦 Jeffrey Bank</h1>

            <h2>Welcome {user} 👋</h2>

            <div style="background:#1e293b;padding:20px;border-radius:12px;max-width:400px;margin:auto">
                <h3>Balance</h3>
                <h2>₦{balance}</h2>

                <form action="/deposit" method="post">
                    <input name="amount" placeholder="Deposit amount" style="padding:10px;width:90%">
                    <button style="padding:10px;margin-top:10px;width:100%">Deposit</button>
                </form>

                <form action="/withdraw" method="post">
                    <input name="amount" placeholder="Withdraw amount" style="padding:10px;width:90%">
                    <button style="padding:10px;margin-top:10px;width:100%">Withdraw</button>
                </form>

                <br>
                <a href="/logout" style="color:red">Logout</a>
            </div>

        </body>
        </html>
        """

    return """
    <h2>Welcome Guest</h2>
    <a href="/login">Login</a> |
    <a href="/register">Register</a>
    """

# REGISTER
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

    return """
    <form method="post">
        <input name="username" placeholder="Username"><br>
        <input name="password" type="password" placeholder="Password"><br>
        <button>Register</button>
    </form>
    """

# LOGIN
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()

        if user and check_password_hash(user.password, request.form["password"]):
            session["user"] = user.username
            return redirect("/")

        return "Invalid login"

    return """
    <form method="post">
        <input name="username" placeholder="Username"><br>
        <input name="password" type="password" placeholder="Password"><br>
        <button>Login</button>
    </form>
    """

# DEPOSIT
@app.route("/deposit", methods=["POST"])
def deposit():
    user = User.query.filter_by(username=session["user"]).first()
    amount = float(request.form["amount"])
    user.balance += amount
    db.session.commit()
    return redirect("/")

# WITHDRAW
@app.route("/withdraw", methods=["POST"])
def withdraw():
    user = User.query.filter_by(username=session["user"]).first()
    amount = float(request.form["amount"])

    if amount <= user.balance:
        user.balance -= amount
        db.session.commit()

    return redirect("/")

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
