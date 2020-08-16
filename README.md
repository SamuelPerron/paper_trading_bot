# Trader bot
The purpose of this project is to be able to deploy an autonomous bot that would trade on the stock market.
[Kanban Board](https://www.notion.so/samperron/5a7a0284e6be4c4897bdf2c6cc11ade8?v=dc8a777fa60b42848ce5d4432a3cb693)

## Backtest framework
Test strategies with entry and exit conditions against historical data.

You can edit strategies in the file `backtest/strategies.json`. The script will output statistics in the Json format (`backtest/results.json`) and a line graph of the stock price with entry and exit points overlaid, also a line graph of the portfolio capital (`backtest/results`).

You can add historical data files in the `backtest/data` repository.

To run a backtest, edit the `backtest/run.py` file. To test a specific stock, create the `Launcher` class with the `symbol` prop `Launcher(symbol='CTC-A.TO')`. To test a specific strategy, create the class with the strategy prop `Launcher(strategy=1)`. To test everything, create the class without any props.
Finally, run the `python3 backtest/run.py` command.

## Development
**Commands**
- Run linter: `coala`

**Installation**
 1. `pipenv shell`
 2. `pip install -r requirements.txt`
 3. `cp exemple.dotenv.py dotenv.py`
 4. Fill variables in the dotenv file
