from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Simulated wallet and transaction history
wallet = {"balance": 0.0}  # Initial wallet balance
transaction_history = []  # List to store transactions

# Endpoint: Check wallet balance
@app.route('/balance', methods=['GET'])
def get_balance():
    return jsonify({"status": "success", "balance": wallet["balance"]})

# Endpoint: Send cryptocurrency
@app.route('/send', methods=['POST'])
def send_currency():
    data = request.json  # Get JSON data from frontend
    amount = float(data['amount'])
    to_address = data['to_address']
    currency = data.get('currency', 'BTC')  # Default to BTC if not provided

    if wallet["balance"] < amount:
        return jsonify({"status": "error", "message": f"Insufficient {currency} balance"})

    # Deduct from balance
    wallet["balance"] -= amount

    # Log the transaction
    transaction = {
        "type": "send",
        "currency": currency,
        "amount": amount,
        "to_address": to_address,
        "status": "success"
    }
    transaction_history.append(transaction)

    return jsonify({
        "status": "success",
        "message": f"{amount} {currency} sent to {to_address}",
        "new_balance": wallet["balance"]
    })

# Endpoint: Receive cryptocurrency
@app.route('/receive', methods=['POST'])
def receive_currency():
    data = request.json  # Get JSON data from frontend
    amount = float(data['amount'])
    currency = data.get('currency', 'BTC')  # Default to BTC if not provided

    # Add to balance
    wallet["balance"] += amount

    # Log the transaction
    transaction = {
        "type": "receive",
        "currency": currency,
        "amount": amount,
        "from_address": "Unknown",  # Can modify this if necessary
        "status": "success"
    }
    transaction_history.append(transaction)

    return jsonify({
        "status": "success",
        "message": f"{amount} {currency} received",
        "new_balance": wallet["balance"]
    })

# Endpoint: Get transaction history
@app.route('/history', methods=['GET'])
def get_transaction_history():
    return jsonify({"status": "success", "transactions": transaction_history})

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
