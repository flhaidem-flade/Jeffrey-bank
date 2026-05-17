@app.route("/")
def home():
    user = session.get("user")

    return f"""
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            margin:0;
            font-family: Arial;
            background:#0f172a;
            color:white;
            text-align:center;
        }}

        .container {{
            padding:20px;
        }}

        .card {{
            background:#1e293b;
            padding:20px;
            margin:20px auto;
            border-radius:15px;
            width:90%;
            max-width:400px;
        }}

        input {{
            width:100%;
            padding:15px;
            margin-top:10px;
            border-radius:10px;
            border:none;
            font-size:16px;
        }}

        button {{
            width:100%;
            padding:15px;
            margin-top:10px;
            border-radius:10px;
            border:none;
            background:#22c55e;
            color:white;
            font-size:18px;
            font-weight:bold;
        }}

        button:active {{
            transform: scale(0.98);
        }}

        .title {{
            font-size:28px;
            margin-top:20px;
        }}

        .small {{
            opacity:0.7;
            font-size:14px;
        }}
    </style>
    </head>

    <body>

    <div class="container">

        <div class="title">🏦 Jeffrey Bank</div>
        <div class="small">Mobile Banking System</div>

        <div class="card">
            <h2>Welcome {user if user else "Guest"} 👋</h2>

            <p class="small">Secure Digital Wallet</p>

            <button onclick="location.href='/login'">Login</button>
            <button onclick="location.href='/register'">Register</button>
        </div>

    </div>

    </body>
    </html>
    """
