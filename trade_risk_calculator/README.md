# Trade Risk Calculator (CLI)

A tiny beginner-friendly Python command-line app that calculates basic trade risk metrics.

## Project folder structure

```text
trade_risk_calculator/
├── app.py
└── README.md
```

## File-by-file explanation

- `app.py`
  - The full app logic.
  - Collects user input from the terminal.
  - Calculates risk/reward numbers.
  - Prints results in a clean format.
- `README.md`
  - Explains what the app does.
  - Shows how to run it.

## What it calculates

Given:
- ticker
- entry price
- stop loss
- profit target
- account size
- percent risk per trade

It returns:
- dollar risk per share
- dollar reward per share
- risk/reward ratio
- max dollar risk
- suggested share size based on account risk

## Step-by-step: how to run on your computer

1. Install Python 3 (if not installed)
   - Check with:
     ```bash
     python3 --version
     ```

2. Open a terminal and go to this project folder:
   ```bash
   cd trade_risk_calculator
   ```

3. Run the app:
   ```bash
   python3 app.py
   ```

4. Enter values when prompted.

### Example input

- Ticker: `AAPL`
- Entry: `100`
- Stop: `95`
- Target: `115`
- Account size: `10000`
- Percent risk: `1`

### Example output

- Dollar risk/share: `$5.00`
- Dollar reward/share: `$15.00`
- Risk/Reward: `1:3.00`
- Max dollar risk: `$100.00`
- Suggested share size: `20 shares`

## 3 ideas for the next small upgrade

1. **Add long/short mode**
   - Validate that stop/target make sense for long trades vs short trades.

2. **Round share size automatically**
   - Add choices like round down to nearest whole share or nearest 5 shares.

3. **Save trade logs to CSV**
   - After each calculation, append results to a `trades.csv` file so you can review later.
