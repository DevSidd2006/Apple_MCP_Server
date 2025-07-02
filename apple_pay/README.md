# Apple Pay MCP Server

An MCP (Model Context Protocol) server that provides Apple Pay functionality including payment processing, wallet management, and transaction tracking.

## Features

- **Merchant Support Check**: Verify if merchants support Apple Pay
- **Payment Card Management**: View and add payment cards to Apple Wallet
- **Payment Simulation**: Simulate Apple Pay transactions
- **Transaction History**: Track and view payment history
- **Spending Analytics**: Get spending summaries and categorization

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd apple_pay_mcp_server
```

2. Install the required dependencies:

```bash
uv install
```

Or with pip:

```bash
pip install httpx mcp[cli]
```

## Quick Setup

For a quick MCP setup, copy the `mcp.json.template` file and modify the paths to match your system:

```bash
cp mcp.json.template mcp.json
# Edit mcp.json with your actual paths
```

## Usage

### Running the Server Directly

Run the MCP server:

```bash
python apple_pay.py
```

Or using the server script:

```bash
python server.py
```

## Available Tools

### `check_merchant_support(merchant_name: str)`
Check if a specific merchant supports Apple Pay payments.

### `get_payment_cards()`
Retrieve all payment cards stored in Apple Wallet.

### `simulate_payment(merchant: str, amount: float, card_id: str = None)`
Simulate an Apple Pay transaction with a specified merchant and amount.

### `get_transaction_history(limit: int = 10)`
Get recent Apple Pay transaction history.

### `add_payment_card(card_type: str, brand: str, last_four: str, expiry: str)`
Add a new payment card to Apple Wallet.

### `get_spending_summary()`
Get a summary of spending patterns and categories.

## Example Usage

```python
# Check if Starbucks supports Apple Pay
await check_merchant_support("Starbucks")

# View available cards
await get_payment_cards()

# Make a payment
await simulate_payment("Starbucks", 4.50)

# View transaction history
await get_transaction_history()
```

Project Structure:

```
apple_pay/
├── .gitignore
├── LICENSE
├── README.md
├── MCP_SETUP.md          # Detailed MCP setup guide
├── apple_pay.py          # Main MCP server
├── server.py             # Alternative entry point
├── main.py               # Basic entry point
├── pyproject.toml        # UV/Python project config
├── requirements.txt      # Pip requirements
└── uv.lock              # Dependency lock file
```

## Note

This is a simulation server for demonstration purposes. It uses mock data and does not connect to actual Apple Pay services or process real payments.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Disclaimer

This software is for educational and demonstration purposes only. It does not provide actual Apple Pay functionality and should not be used in production environments.
