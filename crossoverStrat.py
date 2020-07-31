from math import inf

import numpy as np
import pandas
import matplotlib.pyplot as plt

"""
sma2 > sma1
Buy when a smaEntry1 is below smaEntry2 (Coz stock fell abruptly than it should have)
Sell when smaExit1 is above smaExit2 (Coz the stock has run up recently abruptly) 
"""


def calculateProfitWithPlot(smaEntry1, smaEntry2, smaExit1, smaExit2):
    commision = 15
    df = pandas.read_csv('../Data/HDFCBANK.NS _5YEAR.csv')
    smaEnter1 = str(smaEntry1) + 'SMA'
    smaEnter2 = str(smaEntry2) + 'SMA'
    smaE1 = str(smaExit1) + 'SMA'
    smaE2 = str(smaExit2) + 'SMA'

    df[smaEnter1] = df['Close'].rolling(smaEntry1).mean()
    df[smaEnter2] = df['Close'].rolling(smaEntry2).mean()
    df[smaE1] = df['Close'].rolling(smaExit1).mean()
    df[smaE2] = df['Close'].rolling(smaExit2).mean()

    buy_order_index = 0
    # Multiple Orders open

    buy_orders = []
    sell_orders = []

    """
    Buying the same day
    """
    for index, row in df.iterrows():
        if row[smaEnter1] == pandas.np.nan or row[smaEnter2] == pandas.np.nan or row[smaE1] == np.nan or row[
            smaE2] == np.nan:
            continue
        if row[smaEnter2] > row[smaEnter1] > row['Open']:
            buy_orders.append([row['Datetime'], row['Open']])
        elif row[smaE1] > row[smaE2]:
            # Close all the orders here
            for x in range(buy_order_index, len(buy_orders)):
                sell_orders.append([row['Datetime'], row['Close']])
                buy_order_index = len(buy_orders)

    print(len(buy_orders), len(sell_orders))

    # Clearing the not executed buy orders
    buy_orders = buy_orders[:buy_order_index]

    profit = []
    loss = []

    total_percentage_returns = 0

    for i in range(len(buy_orders)):
        if buy_orders[i][1] - sell_orders[i][1] <= 0:
            profitP = sell_orders[i][1] - buy_orders[i][1] - commision
            profitPer = (profitP / buy_orders[i][1]) * 100
            profit.append([profitP, profitPer])
            total_percentage_returns += profitPer

        else:
            lossL = sell_orders[i][1] - buy_orders[i][1] - commision
            lossLper = (lossL / (buy_orders[i][1]) * 100)
            total_percentage_returns += lossLper
            loss.append([lossL, lossLper])

    pandas.set_option('display.max_rows', df.shape[0] + 1)
    result = pandas.DataFrame(
        {'Buy': buy_orders,
         'Sell': sell_orders
         }
    )

    print(result)
    print("Total Trades taken : ", len(profit) + len(loss))
    print("Total Return Percentage: ", total_percentage_returns)

    print("Profit :", profit)
    print("Loss :", loss)

    overall = 0

    for i in profit:
        overall = overall + i[0]

    for i in loss:
        overall = overall + i[0]

    print("Overall :", overall, "Average Percentage Returns in 6 years: ", total_percentage_returns/len(buy_orders))

    buy_date = [buydate for buydate, buyprice in buy_orders]
    buy_price = [buyprice for buydate, buyprice in buy_orders]
    sell_date = [selldate for selldate, sellprice in sell_orders]
    sellprice = [sellprice for selldate, sellprice in sell_orders]

    plt.plot(df['Datetime'], df['Low'])
    plt.plot(df['Datetime'], df['Open'])
    plt.plot(df['Datetime'], df['Close'])
    plt.plot(buy_date, buy_price, 'g^')
    plt.plot(sell_date, sellprice, 'rv')
    plt.plot(df['Datetime'], df[smaEnter2], 'r')
    plt.plot(df['Datetime'], df[smaEnter1], 'g')
    plt.show()


def calculateProfit(smaEntry1, smaEntry2, smaExit1, smaExit2):
    commision = 15
    df = pandas.read_csv('../Data/HDFCBANK.NS _5YEAR.csv')
    smaEnter1 = str(smaEntry1) + 'SMA'
    smaEnter2 = str(smaEntry2) + 'SMA'
    smaE1 = str(smaExit1) + 'SMA'
    smaE2 = str(smaExit2) + 'SMA'

    df[smaEnter1] = df['Close'].rolling(smaEntry1).mean()
    df[smaEnter2] = df['Close'].rolling(smaEntry2).mean()
    df[smaE1] = df['Close'].rolling(smaExit1).mean()
    df[smaE2] = df['Close'].rolling(smaExit2).mean()

    buy_order_index = 0
    # Multiple Orders open

    buy_orders = []
    sell_orders = []

    """
    Buying the same day
    """
    for index, row in df.iterrows():
        if row[smaEnter1] == pandas.np.nan or row[smaEnter2] == pandas.np.nan or row[smaE1] == np.nan or row[smaE2] == np.nan:
            continue
        if row[smaEnter2] > row[smaEnter1] > row['Open']:
            buy_orders.append([row['Datetime'], row['Open']])
        elif row[smaE1] > row[smaE2]:
            # Close all the orders here
            for x in range(buy_order_index, len(buy_orders)):
                sell_orders.append([row['Datetime'], row['Close']])
                buy_order_index = len(buy_orders)

        # print(len(buy_orders), len(sell_orders))

    # Clearing the not executed buy orders
    buy_orders = buy_orders[:buy_order_index]

    profit = []
    loss = []

    total_percentage_returns = 0

    for i in range(len(buy_orders)):
        if buy_orders[i][1] - sell_orders[i][1] <= 0:
            profitP = sell_orders[i][1] - buy_orders[i][1] - commision
            profitPer = (profitP / buy_orders[i][1]) * 100
            profit.append([profitP, profitPer])
            total_percentage_returns += profitPer

        else:
            lossL = sell_orders[i][1] - buy_orders[i][1] - commision
            lossLper = (lossL / (buy_orders[i][1]) * 100)
            total_percentage_returns += lossLper
            loss.append([lossL, lossLper])

    # pandas.set_option('display.max_rows', df.shape[0] + 1)
    # result = pandas.DataFrame(
    #     {'Buy': buy_orders,
    #      'Sell': sell_orders
    #      }
    # )

    # print(result)
    # print("Total Trades taken : ", len(profit) + len(loss))
    # print("Total Return Percentage: ", total_percentage_returns)
    #
    # print("Profit :", profit)
    # print("Loss :", loss)

    overall = 0

    for i in profit:
        overall = overall + i[0]

    for i in loss:
        overall = overall + i[0]

    avg_Total_percentage_returns = float(-inf)

    if len(buy_orders) != 0:
        avg_Total_percentage_returns = total_percentage_returns / len(buy_orders)

    print("Overall :", overall, "Average Percentage for 6 years", avg_Total_percentage_returns)

    return [overall, avg_Total_percentage_returns]
    # buy_date = [buydate for buydate, buyprice in buy_orders]
    # buy_price = [buyprice for buydate, buyprice in buy_orders]
    # sell_date = [selldate for selldate, sellprice in sell_orders]
    # sellprice = [sellprice for selldate, sellprice in sell_orders]
    #
    # plt.plot(df['Datetime'], df['Close'])
    # plt.plot(buy_date, buy_price, 'g^')
    # plt.plot(sell_date, sellprice, 'rv')
    # plt.plot(df['Datetime'], df['200SMA'], 'r')
    # plt.plot(df['Datetime'], df['50SMA'], 'g')
    # plt.show()


if __name__ == "__main__":
    bestProfit, bestsmaEntry1, bestSmaEntry2, bestsmaExit1, bestSmaexit2 = -float(inf), 0, 0, 0, 0
    bestPercentage, bestsmaEntry1P, bestSmaEntry2P, bestsmaExit1P, bestSmaexit2P = -float(inf), 0, 0, 0, 0
    for smaEntry1 in range(50, 300, 50):
        for smaEntry2 in range(smaEntry1 + 50, 300, 50):
            for smaExit1 in range(50, 300, 50):
                for smaExit2 in range(smaExit1 + 50, 300, 50):
                    currentOverall = calculateProfit(smaEntry1, smaEntry2, smaExit1, smaExit2)[0]
                    if currentOverall > bestProfit:
                        bestsmaEntry1 = smaEntry1
                        bestSmaEntry2 = smaEntry2
                        bestsmaExit1 = smaExit1
                        bestSmaexit2 = smaExit2
                        bestProfit = currentOverall
                    currentOverallP = calculateProfit(smaEntry1, smaEntry2, smaExit1, smaExit2)[1]
                    if currentOverallP > bestPercentage:
                        bestsmaEntry1P = smaEntry1
                        bestSmaEntry2P = smaEntry2
                        bestsmaExit1P = smaExit1
                        bestSmaexit2P = smaExit2
                        bestPercentage = currentOverallP

    print("Overall Profit Wise", bestProfit, bestsmaEntry1, bestSmaEntry2, bestsmaExit1, bestSmaexit2)
    print("Overall Average Profit Percentage Per Trade Wise", bestPercentage, bestsmaEntry1P, bestSmaEntry2P,
          bestsmaExit1P,
          bestSmaexit2P)

    # calculateProfitWithPlot(100, 150, 50, 250)

"""
Overall Profit Wise 11378.879893999974 50 100 50 100
Overall Average Profit Percentage Per Trade Wise 17.003855234200973 100 150 50 250
"""
