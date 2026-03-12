"""Trade Risk Calculator (CLI)

A very small command-line tool to help position sizing for a trade.
This version is intentionally beginner-friendly and heavily commented.
"""


def get_float_input(prompt_text):
    """Ask the user for a number and keep asking until they enter a valid float."""
    while True:
        raw_value = input(prompt_text).strip()
        try:
            return float(raw_value)
        except ValueError:
            print("Please enter a valid number, for example: 10 or 10.5")


def calculate_trade_risk(entry_price, stop_loss, profit_target, account_size, risk_percent):
    """Return all trade metrics as a dictionary.

    Formulas:
    - dollar_risk_per_share = abs(entry_price - stop_loss)
    - dollar_reward_per_share = abs(profit_target - entry_price)
    - risk_reward_ratio = dollar_reward_per_share / dollar_risk_per_share
    - max_dollar_risk = account_size * (risk_percent / 100)
    - suggested_share_size = max_dollar_risk / dollar_risk_per_share
    """

    # Risk and reward per share should always be positive numbers.
    dollar_risk_per_share = abs(entry_price - stop_loss)
    dollar_reward_per_share = abs(profit_target - entry_price)

    # Prevent divide-by-zero if entry and stop are the same.
    if dollar_risk_per_share == 0:
        raise ValueError("Entry price and stop loss cannot be the same.")

    risk_reward_ratio = dollar_reward_per_share / dollar_risk_per_share
    max_dollar_risk = account_size * (risk_percent / 100)
    suggested_share_size = max_dollar_risk / dollar_risk_per_share

    return {
        "dollar_risk_per_share": dollar_risk_per_share,
        "dollar_reward_per_share": dollar_reward_per_share,
        "risk_reward_ratio": risk_reward_ratio,
        "max_dollar_risk": max_dollar_risk,
        "suggested_share_size": suggested_share_size,
    }


def main():
    """Run the command-line app."""
    print("=== Trade Risk Calculator ===")

    # Collect trade inputs from the user.
    ticker = input("Ticker: ").strip().upper()
    entry_price = get_float_input("Entry price: ")
    stop_loss = get_float_input("Stop loss: ")
    profit_target = get_float_input("Profit target: ")
    account_size = get_float_input("Account size ($): ")
    risk_percent = get_float_input("Percent risk per trade (%): ")

    try:
        results = calculate_trade_risk(
            entry_price=entry_price,
            stop_loss=stop_loss,
            profit_target=profit_target,
            account_size=account_size,
            risk_percent=risk_percent,
        )
    except ValueError as error:
        print(f"\nError: {error}")
        return

    # Show results in a simple readable format.
    print("\n--- Results ---")
    print(f"Ticker: {ticker}")
    print(f"Dollar risk per share: ${results['dollar_risk_per_share']:.2f}")
    print(f"Dollar reward per share: ${results['dollar_reward_per_share']:.2f}")
    print(f"Risk/Reward ratio: 1:{results['risk_reward_ratio']:.2f}")
    print(f"Max dollar risk: ${results['max_dollar_risk']:.2f}")
    print(f"Suggested share size: {results['suggested_share_size']:.0f} shares")


if __name__ == "__main__":
    main()
