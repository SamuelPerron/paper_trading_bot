import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('data/CTC-A.TO.csv', index_col=0, parse_dates=True)
period = 14
close = df['Adj Close']
delta = close.diff()
delta = delta[1:]

# Make the positive gains (up) and negative gains (down) Series
up, down = delta.copy(), delta.copy()
up[up < 0] = 0
down[down > 0] = 0

# Calculate the EWMA
roll_up1 = up.ewm(span=period).mean()
roll_down1 = down.abs().ewm(span=period).mean()

# Calculate the RSI based on EWMA
RS1 = roll_up1 / roll_down1
RSI1 = 100.0 - (100.0 / (1.0 + RS1))


# Compare graphically
plt.figure(figsize=(8, 6))
RSI1.plot()
plt.legend(['RSI',])

print(delta)


# ctc[['Adj Close', 'rsi']].plot()
plt.savefig('testplot.png')
