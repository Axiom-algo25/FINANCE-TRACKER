from flask import Flask, request
import os
import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        amount = float(request.form["amount"])
        action = request.form["action"]

        if os.path.exists("balance.txt"):
            file = open("balance.txt", "r")
            content = file.read()
            file.close()
            balance = float(content)
        else:
            balance = 5000

        timestamp = datetime.datetime.now().strftime("%d %b %I:%M %p")

        if action == "earn":
            balance += amount
            with open("transactions.txt", "a") as f:
                f.write(f"earn,{amount},{timestamp}\n")
        elif action == "spend":
            balance -= amount
            with open("transactions.txt", "a") as f:
                f.write(f"spend,{amount},{timestamp}\n")
        elif action == "set":
            balance = amount

        file = open("balance.txt", "w")
        file.write(str(balance))
        file.close()

    if os.path.exists("balance.txt"):
        file = open("balance.txt", "r")
        content = file.read()
        file.close()
        balance = float(content)
    else:
        balance = 5000

    history = ""
    month_earned = 0
    month_spent = 0
    current_month = datetime.datetime.now().strftime("%b")

    if os.path.exists("transactions.txt"):
        file = open("transactions.txt", "r")
        lines = file.readlines()
        file.close()
        for line in lines[-20:]:
            parts = line.strip().split(",")
            if len(parts) == 3:
                if parts[0] == "earn":
                    history += f'<div class="txn earn">+ ₹{parts[1]} <span class="time">{parts[2]}</span></div>'
                else:
                    history += f'<div class="txn spend">- ₹{parts[1]} <span class="time">{parts[2]}</span></div>'

        for line in lines:
            parts = line.strip().split(",")
            if len(parts) == 3 and current_month in parts[2]:
                if parts[0] == "earn":
                    month_earned += float(parts[1])
                else:
                    month_spent += float(parts[1])

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MY FINANCES</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}
            body {{
                background: linear-gradient(135deg, #F3E5F5 0%, #E1BEE7 100%);
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                text-align: center;
                padding: 30px 20px;
                min-height: 100vh;
            }}
            .container {{
                max-width: 500px;
                margin: 0 auto;
            }}
            h1 {{
                color: #6A1B9A;
                font-size: 28px;
                margin-bottom: 20px;
                letter-spacing: 1px;
            }}
            .balance-card {{
                background: linear-gradient(135deg, #6A1B9A, #8E24AA);
                color: white;
                padding: 30px;
                border-radius: 20px;
                margin-bottom: 20px;
                box-shadow: 0 8px 20px rgba(106, 27, 154, 0.3);
            }}
            .balance-label {{
                font-size: 14px;
                opacity: 0.9;
                text-transform: uppercase;
                letter-spacing: 2px;
                margin-bottom: 10px;
            }}
            .balance-amount {{
                font-size: 42px;
                font-weight: bold;
            }}
            .form-section {{
                background: white;
                padding: 25px;
                border-radius: 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            }}
            input {{
                padding: 14px;
                border-radius: 12px;
                border: 2px solid #E1BEE7;
                width: 100%;
                font-size: 18px;
                margin-bottom: 12px;
                outline: none;
                transition: border 0.3s;
            }}
            input:focus {{
                border-color: #6A1B9A;
            }}
            .chips {{
                display: flex;
                gap: 8px;
                justify-content: center;
                margin-bottom: 12px;
                flex-wrap: wrap;
            }}
            .chip {{
                background: #F3E5F5;
                color: #6A1B9A;
                border: none;
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 14px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.2s;
            }}
            .chip:hover {{
                background: #E1BEE7;
            }}
            .buttons {{
                display: flex;
                gap: 10px;
                justify-content: center;
            }}
            button {{
                padding: 14px 30px;
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
                flex: 1;
            }}
            .earn-btn {{
                background: linear-gradient(135deg, #6A1B9A, #8E24AA);
                color: white;
            }}
            .earn-btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 15px rgba(106, 27, 154, 0.4);
            }}
            .spend-btn {{
                background: white;
                color: #6A1B9A;
                border: 2px solid #6A1B9A;
            }}
            .spend-btn:hover {{
                background: #F3E5F5;
            }}
            .set-btn {{
                background: #4A148C;
                color: white;
                border: none;
            }}
            .set-btn:hover {{
                background: #6A1B9A;
            }}
            .summary {{
                display: flex;
                gap: 12px;
                margin-bottom: 20px;
            }}
            .summary-card {{
                flex: 1;
                background: white;
                padding: 20px;
                border-radius: 16px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            }}
            .summary-label {{
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 1px;
                color: #888;
                margin-bottom: 8px;
            }}
            .summary-amount {{
                font-size: 22px;
                font-weight: bold;
            }}
            .earned {{
                color: #2E7D32;
            }}
            .spent {{
                color: #6A1B9A;
            }}
            .history-section {{
                background: white;
                padding: 20px;
                border-radius: 20px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                text-align: left;
            }}
            .history-section h3 {{
                color: #6A1B9A;
                font-size: 16px;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 15px;
                text-align: center;
            }}
            .txn {{
                padding: 12px 15px;
                border-radius: 10px;
                margin-bottom: 8px;
                font-size: 16px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            .txn.earn {{
                background: #E8F5E9;
                color: #2E7D32;
                font-weight: 600;
            }}
            .txn.spend {{
                background: #F3E5F5;
                color: #6A1B9A;
                font-weight: 600;
            }}
            .time {{
                font-size: 12px;
                opacity: 0.7;
                font-weight: normal;
            }}
            .empty {{
                text-align: center;
                color: #999;
                padding: 20px;
            }}
            .footer {{
                color: #999;
                font-size: 12px;
                margin-top: 25px;
            }}
            @media (min-width: 768px) {{
                body {{
                    padding: 60px 20px;
                }}
                .container {{
                    max-width: 600px;
                }}
                h1 {{
                    font-size: 36px;
                }}
                .balance-amount {{
                    font-size: 52px;
                }}
                .summary-card {{
                    padding: 25px;
                }}
                .summary-amount {{
                    font-size: 26px;
                }}
                button {{
                    font-size: 18px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>MY FINANCES</h1>

            <div class="balance-card">
                <div class="balance-label">Current Balance</div>
                <div class="balance-amount">₹{balance}</div>
            </div>

        <div class="form-section">
            <form method="POST">
                <input type="number" name="amount" id="amount" placeholder="Enter amount" required>
                <div class="chips">
                    <button type="button" class="chip" onclick="setAmount(100)">+₹100</button>
                    <button type="button" class="chip" onclick="setAmount(500)">+₹500</button>
                    <button type="button" class="chip" onclick="setAmount(1000)">+₹1000</button>
                </div>
                <div class="buttons">
                    <button type="submit" name="action" value="earn" class="earn-btn">Earn</button>
                    <button type="submit" name="action" value="spend" class="spend-btn">Spend</button>
                    <button type="submit" name="action" value="set" class="set-btn">Set Balance</button>
                </div>
            </form>
        </div>

            <div class="summary">
                <div class="summary-card">
                    <div class="summary-label">This Month Earned</div>
                    <div class="summary-amount earned">₹{month_earned}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-label">This Month Spent</div>
                    <div class="summary-amount spent">₹{month_spent}</div>
                </div>
            </div>

            <div class="history-section">
                <h3>Recent Transactions</h3>
                {history if history else '<div class="empty">No transactions yet.</div>'}
            </div>

            <p class="footer">Built by Mufeeth  Rahim 🫡</p>
        </div>

        <script>
            function setAmount(value) {{
                document.getElementById("amount").value = value;
            }}
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)