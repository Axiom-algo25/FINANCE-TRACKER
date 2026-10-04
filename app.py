from flask import Flask, request
import os

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
        
        if action == "earn":
            balance += amount
        elif action == "spend":
            balance -= amount
        
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

    return f"""
    <h1>Balance : ₹{balance}</h1>
    <form method="POST">
        <input type="number" name="amount" placeholder="Enter amount">
        <button name="action" value="earn">Earn</button>
        <button name="action" value="spend">Spend</button>
    </form>
    """

if __name__ == "__main__":
    app.run(debug=True)