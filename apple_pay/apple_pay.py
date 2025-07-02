from typing import Any, Dict, List
import httpx
from mcp.server.fastmcp import FastMCP
import uuid
import datetime

# Initialize FastMCP server
mcp = FastMCP("apple_pay")

# Mock data for demonstration purposes
MOCK_MERCHANTS = {
    "amazon": {"name": "Amazon", "category": "Online Shopping", "supported": True},
    "starbucks": {"name": "Starbucks", "category": "Coffee & Food", "supported": True},
    "walmart": {"name": "Walmart", "category": "Retail", "supported": True},
    "uber": {"name": "Uber", "category": "Transportation", "supported": True},
    "mcdonalds": {"name": "McDonald's", "category": "Fast Food", "supported": True},
    "target": {"name": "Target", "category": "Retail", "supported": True},
    "gas_station": {"name": "Shell Gas Station", "category": "Gas & Fuel", "supported": False}
}

MOCK_CARDS = [
    {
        "id": "card_1",
        "type": "Credit Card",
        "brand": "Visa",
        "last_four": "1234",
        "is_default": True,
        "expires": "12/2026"
    },
    {
        "id": "card_2",
        "type": "Debit Card",
        "brand": "Mastercard",
        "last_four": "5678",
        "is_default": False,
        "expires": "08/2025"
    }
]

TRANSACTION_HISTORY = []

def generate_transaction_id() -> str:
    """Generate a unique transaction ID."""
    return f"txn_{uuid.uuid4().hex[:8]}"

def format_transaction(transaction: Dict[str, Any]) -> str:
    """Format a transaction into a readable string."""
    return f"""
Transaction ID: {transaction['id']}
Merchant: {transaction['merchant']}
Amount: ${transaction['amount']:.2f}
Date: {transaction['date']}
Status: {transaction['status']}
Card Used: {transaction['card_info']}
"""

@mcp.tool()
async def check_merchant_support(merchant_name: str) -> str:
    """Check if a merchant supports Apple Pay.

    Args:
        merchant_name: Name of the merchant to check
    """
    merchant_key = merchant_name.lower().replace(" ", "_")
    
    if merchant_key in MOCK_MERCHANTS:
        merchant = MOCK_MERCHANTS[merchant_key]
        support_status = "✅ Supported" if merchant["supported"] else "❌ Not Supported"
        return f"""
Merchant: {merchant['name']}
Category: {merchant['category']}
Apple Pay Support: {support_status}
"""
    else:
        return f"Merchant '{merchant_name}' not found in our database. Most major retailers support Apple Pay."

@mcp.tool()
async def get_payment_cards() -> str:
    """Get list of available payment cards in Apple Wallet."""
    if not MOCK_CARDS:
        return "No payment cards found in Apple Wallet."
    
    cards_info = []
    for card in MOCK_CARDS:
        default_indicator = " (Default)" if card["is_default"] else ""
        card_info = f"""
{card['brand']} {card['type']}{default_indicator}
Card ending in: ****{card['last_four']}
Expires: {card['expires']}
"""
        cards_info.append(card_info)
    
    return "Available Payment Cards:\n" + "\n---".join(cards_info)

@mcp.tool()
async def simulate_payment(merchant: str, amount: float, card_id: str = None) -> str:
    """Simulate an Apple Pay transaction.

    Args:
        merchant: Name of the merchant
        amount: Payment amount in USD
        card_id: Optional card ID to use (uses default if not specified)
    """
    if amount <= 0:
        return "❌ Payment failed: Invalid amount"
    
    # Find the card to use
    selected_card = None
    if card_id:
        selected_card = next((card for card in MOCK_CARDS if card["id"] == card_id), None)
        if not selected_card:
            return f"❌ Payment failed: Card with ID '{card_id}' not found"
    else:
        # Use default card
        selected_card = next((card for card in MOCK_CARDS if card["is_default"]), MOCK_CARDS[0] if MOCK_CARDS else None)
    
    if not selected_card:
        return "❌ Payment failed: No payment cards available"
    
    # Check if merchant supports Apple Pay
    merchant_key = merchant.lower().replace(" ", "_")
    if merchant_key in MOCK_MERCHANTS and not MOCK_MERCHANTS[merchant_key]["supported"]:
        return f"❌ Payment failed: {merchant} does not support Apple Pay"
    
    # Simulate successful payment
    transaction = {
        "id": generate_transaction_id(),
        "merchant": merchant,
        "amount": amount,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Completed",
        "card_info": f"{selected_card['brand']} ****{selected_card['last_four']}"
    }
    
    TRANSACTION_HISTORY.append(transaction)
    
    return f"""
✅ Payment Successful!

{format_transaction(transaction)}

Touch ID/Face ID authentication completed.
Receipt sent to your email.
"""

@mcp.tool()
async def get_transaction_history(limit: int = 10) -> str:
    """Get recent Apple Pay transaction history.

    Args:
        limit: Maximum number of transactions to return (default: 10)
    """
    if not TRANSACTION_HISTORY:
        return "No transaction history found."
    
    recent_transactions = TRANSACTION_HISTORY[-limit:]
    transactions_text = []
    
    for transaction in reversed(recent_transactions):
        transactions_text.append(format_transaction(transaction))
    
    return f"Recent Apple Pay Transactions:\n{'---'.join(transactions_text)}"

@mcp.tool()
async def add_payment_card(card_type: str, brand: str, last_four: str, expiry: str) -> str:
    """Add a new payment card to Apple Wallet.

    Args:
        card_type: Type of card (Credit Card, Debit Card, etc.)
        brand: Card brand (Visa, Mastercard, Amex, etc.)
        last_four: Last four digits of the card
        expiry: Expiry date in MM/YY format
    """
    new_card = {
        "id": f"card_{len(MOCK_CARDS) + 1}",
        "type": card_type,
        "brand": brand,
        "last_four": last_four,
        "is_default": len(MOCK_CARDS) == 0,  # First card becomes default
        "expires": expiry
    }
    
    MOCK_CARDS.append(new_card)
    
    default_text = " (Set as default)" if new_card["is_default"] else ""
    
    return f"""
✅ Card Added Successfully!

{brand} {card_type}{default_text}
Card ending in: ****{last_four}
Expires: {expiry}

Your card is now ready for Apple Pay transactions.
"""

@mcp.tool()
async def get_spending_summary() -> str:
    """Get spending summary from Apple Pay transactions."""
    if not TRANSACTION_HISTORY:
        return "No transactions found for spending summary."
    
    total_spent = sum(txn["amount"] for txn in TRANSACTION_HISTORY)
    transaction_count = len(TRANSACTION_HISTORY)
    
    # Calculate spending by category (based on mock merchant data)
    category_spending = {}
    for txn in TRANSACTION_HISTORY:
        merchant_key = txn["merchant"].lower().replace(" ", "_")
        if merchant_key in MOCK_MERCHANTS:
            category = MOCK_MERCHANTS[merchant_key]["category"]
            category_spending[category] = category_spending.get(category, 0) + txn["amount"]
    
    summary = f"""
Apple Pay Spending Summary:

Total Spent: ${total_spent:.2f}
Total Transactions: {transaction_count}

Spending by Category:
"""
    
    for category, amount in sorted(category_spending.items(), key=lambda x: x[1], reverse=True):
        summary += f"• {category}: ${amount:.2f}\n"
    
    return summary

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
