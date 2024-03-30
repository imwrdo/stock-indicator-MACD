import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv('peo_d.csv')  

y = data['Zamkniecie'].to_numpy()
x = np.arange(1, 1001)


def exponential_moving_average(data, N):
    alpha = 2 / (N + 1)
    ema_values = []
    for i in range(len(data)):
        numerator = sum(pow(1 - alpha, j) * data[i - j] for j in range(min(N + 1, i + 1)))
        denominator = sum(pow(1 - alpha, j) for j in range(min(N + 1, i + 1)))
        ema = numerator / denominator if denominator != 0 else 0.0
        ema_values.append(ema)
    
    return ema_values


EMA_12 = exponential_moving_average(data['Zamkniecie'],12)
EMA_26 = exponential_moving_average(data['Zamkniecie'],26)


MACD = np.array(EMA_12) - np.array(EMA_26)

SIGNAL = exponential_moving_average(MACD,9)



shares_owned = 1000
money_owned_before = shares_owned*y[1]
money_owned = 0

transaction_stats = {'Date': [], 'Type': [], 'Price': [], 'Shares': [], 'Profit/Loss': []}

for i in range(1, len(MACD)):
    if MACD[i] > SIGNAL[i] and MACD[i - 1] <= SIGNAL[i - 1]:
        price = y[i]  
        shares_bought = round(money_owned/price,2)
        shares_owned += shares_bought
        transaction_stats['Date'].append(data['Data'][i])
        transaction_stats['Type'].append('Kupno')
        transaction_stats['Price'].append(price)
        transaction_stats['Shares'].append(shares_bought)
        transaction_stats['Profit/Loss'].append(0)
    elif MACD[i] < SIGNAL[i] and MACD[i - 1] >= SIGNAL[i - 1]:
        price = y[i]  
        shares_sold = shares_owned
        shares_owned -= shares_sold
        money_owned = shares_sold*price
        transaction_stats['Date'].append(data['Data'][i])
        transaction_stats['Type'].append('Sprzedaż')
        transaction_stats['Price'].append(price)
        transaction_stats['Shares'].append(shares_sold)
        transaction_stats['Profit/Loss'].append((price - y[i - 1]) * shares_sold) 

money_owned_after = money_owned 

total_profit_loss = sum(transaction_stats['Profit/Loss'])

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
transaction_df = pd.DataFrame(transaction_stats)
print("\nStatystyka transakcji:")
print(transaction_df)
print("\nCałkowity kapitał pieniężny(na samym początku):")
print(round(money_owned_before,2))
print("\nCałkowity kapitał pieniężny(po 1000 dniach):")
print(round(money_owned_after,2))
print("\nZysk/strata :")
print(round(money_owned_after-money_owned_before,3))

plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(x, y, label='Ceny zamknięcia', color='blue')
plt.title('Instrument finansowy cen zamknięcia')
plt.xlabel('Dni')
plt.ylabel('Cena')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(x, MACD, label='MACD', color='purple',zorder=1)
plt.plot(x, SIGNAL, label='SIGNAL', color='orange',zorder=1)
plt.title('MACD and SIGNAL')
plt.xlabel('Dni')
plt.ylabel('Wartość')
  
buy_signals = []
sell_signals = []

for i in range(1, len(MACD)):
    if MACD[i] > SIGNAL[i] and MACD[i - 1] <= SIGNAL[i - 1]:
        buy_signals.append(i)
    elif MACD[i] < SIGNAL[i] and MACD[i - 1] >= SIGNAL[i - 1]:
        sell_signals.append(i)
        
plt.scatter(buy_signals, MACD[buy_signals], color='green', marker='^',edgecolor='black', linewidth=1.0, label='Kupno',zorder = 2)
plt.scatter(sell_signals, MACD[sell_signals], color='red', marker='v',edgecolor='black', linewidth=1.0, label='Sprzedaż', zorder=2)

plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 4))

plt.plot(x, y, label='Ceny zamknięcia', color='blue',zorder=1)
plt.title('Instrument finansowy cen zamknięcia wraz z punktami kupna/sprzedaży')
plt.xlabel('Dni')
plt.ylabel('Cena')
plt.legend()

plt.scatter(buy_signals, y[buy_signals], color='green', marker='^', edgecolor='black', linewidth=1.0, label='Punkt kupna',zorder=2)
plt.scatter(sell_signals, y[sell_signals], color='red', marker='v', edgecolor='black', linewidth=1.0, label='Punkt sprzedaży',zorder=2)

plt.legend()
plt.grid(True)

plt.show()
