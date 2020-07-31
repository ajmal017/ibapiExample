import datetime
import threading
import time

from build.lib.ibapi.common import BarData
from ibapi import wrapper
from ibapi.account_summary_tags import AccountSummaryTags
from ibapi.client import EClient, ListOfContractDescription
from ibapi.contract import Contract, ContractDetails
from ibapi.object_implem import Object
from ibapi.utils import iswrapper
from samples.Python.Testbed.ContractSamples import ContractSamples
from samples.Python.Testbed.Indicators import *
"""
Main Logic Class which has both the wrapper to get commands from the TWS as well as send messages
to the TWS for various things
"""


def printinstance(inst: Object):
    attrs = vars(inst)
    print(', '.join("%s: %s" % item for item in attrs.items()))


def printWhenExecuting(fn):
    def fn2(self):
        print("   doing", fn.__name__)
        fn(self)
        print("   done w/", fn.__name__)

    return fn2

def message_process_loop(app):
    app.run()

class TestApp(wrapper.EWrapper, EClient):
    def __init__(self):
        wrapper.EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)

        """
        Connection to TWS
        """
        self.connect(host="127.0.0.1", port=7496, clientId=0)

        print("serverVersion:%s connectionTime:%s" % (self.serverVersion(),

                                                      self.twsConnectionTime()))
        """
        This method is used to process the queue in the infinite loop so that
        it can process it and call appropriate methods in Wrapper Class
        I will be making another thread for it to execute 
        """
        # Starting the socket in a thread
        messageQueueThread = threading.Thread(target=message_process_loop, args=(self,), daemon=True)
        messageQueueThread.start()

        # Giving the server a bit room to start everything
        time.sleep(1)

    """
    Account Details 
    """

    @iswrapper
    def managedAccounts(self, accountsList: str):
        super().managedAccounts(accountsList)
        print("Connection is ok as we get Account List")
        print("Account List : ", accountsList)

        self.account = accountsList.split(",")[0]

    """
    Information About a particular Contract
    """

    @iswrapper
    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        print(6 * '-', "Contract Details", 6 * '-')
        super().contractDetails(reqId, contractDetails)
        printinstance(contractDetails)

    @iswrapper
    def contractDetailsEnd(self, reqId: int):
        super().contractDetailsEnd(reqId)
        print(6 * "-", "ContractDetailsEnd. ReqId:", reqId)

    """
    For Matching request to a partial info about a ticker
    """

    @iswrapper
    def symbolSamples(self, reqId: int,
                      contractDescriptions: ListOfContractDescription):

        super().symbolSamples(reqId, contractDescriptions)

        print("Symbol Samples. Request Id: ", reqId)

        for contractDescription in contractDescriptions:
            derivSecTypes = ""
            for derivSecType in contractDescription.derivativeSecTypes:
                derivSecTypes += derivSecType
                derivSecTypes += " "
            print("Contract: conId:%s, symbol:%s, secType:%s primExchange:%s, ""currency:%s, derivativeSecTypes:%s" % (
                contractDescription.contract.conId,
                contractDescription.contract.symbol,
                contractDescription.contract.secType,
                contractDescription.contract.primaryExchange,
                contractDescription.contract.currency, derivSecTypes))

    """
    Earliest Data Point Receiving for a given Contract
    """

    @iswrapper
    def headTimestamp(self, reqId: int, headTimestamp: str):
        date = datetime.datetime.strptime(headTimestamp, "%Y%m%d %H:%M:%S")
        print("HeadTimeStamp. ReqId: ", reqId, "headTimeStamp: ", date)

    """
    Historical Data Returned for a Contract
    """

    @iswrapper
    def historicalData(self, reqId: int, bar: BarData):
        print("Historical Bar. ReqId: ", reqId)
        print(bar.date, 4 * '-', "Bar Open : ", bar.open, "Bar Close : ", bar.close, "Bar low : ", bar.low, "Bar High : ",
              bar.high, "Bar Volume: ", bar.volume)

    @iswrapper
    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        print("Historical Data End : ", reqId, "from", start, "to", end)

    """
    Account Summary Received
    """

    @iswrapper
    def accountSummary(self, reqId: int, account: str, tag: str, value: str,
                       currency: str):
        super().accountSummary(reqId, account, tag, value, currency)
        print("AccountSummary. ReqId:", reqId, "Account:", account,
              "Tag: ", tag, "Value:", value, "Currency:", currency)

    @iswrapper
    def accountSummaryEnd(self, reqId: int):
        super().accountSummaryEnd(reqId)
        print("Account Summary End for reqId: ", reqId)

    """
    Account Update Received
    """

    @iswrapper
    def updateAccountValue(self, key: str, val: str, currency: str,
                           accountName: str):
        super().updateAccountValue(key, val, currency, accountName)
        print("UpdateAccountValue. Key:", key, "Value:", val, "Currency:", currency, "AccountName:", accountName)

    @iswrapper
    def updatePortfolio(self, contract: Contract, position: float,
                        marketPrice: float, marketValue: float,
                        averageCost: float, unrealizedPNL: float,
                        realizedPNL: float, accountName: str):
        super().updatePortfolio(contract, position, marketPrice, marketValue,
                                averageCost, unrealizedPNL, realizedPNL, accountName)
        print("UpdatePortfolio.", "Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:",
              contract.exchange, "Position:", position, "MarketPrice:", marketPrice,
              "MarketValue:", marketValue, "AverageCost:", averageCost,
              "UnrealizedPNL:", unrealizedPNL, "RealizedPNL:", realizedPNL,
              "AccountName:", accountName)

    @iswrapper
    def updateAccountTime(self, timeStamp: str):
        super().updateAccountTime(timeStamp)
        print("UpdateAccountTime. Time:", timeStamp)

    @iswrapper
    def accountDownloadEnd(self, accountName: str):
        super().accountDownloadEnd(accountName)
        print("AccountDownloadEnd. Account:", accountName)

    """
    Receiving Position Data
    """

    @iswrapper
    def position(self, account: str, contract: Contract, position: float,
                 avgCost: float):
        super().position(account, contract, position, avgCost)
        print("Position.", "Account:", account, "Symbol:", contract.symbol, "SecType:",
              contract.secType, "Currency:", contract.currency,
              "Position:", position, "Avg cost:", avgCost)

    @iswrapper
    def positionEnd(self):
        super().positionEnd()
        print("Position End")

    @iswrapper
    def pnlSingle(self, reqId: int, pos: int, dailyPnL: float, unrealizedPnL: float, realizedPnL: float, value: float):
        super().pnlSingle(reqId, pos, dailyPnL, unrealizedPnL, realizedPnL, value)
        print("Daily PnL Single. ReqId:", reqId, "Position:", pos,
              "DailyPnL:", dailyPnL, "UnrealizedPnL:", unrealizedPnL,
              "RealizedPnL:", realizedPnL, "Value:", value)

    """
    PnL Updates for all positions
    """
    @iswrapper
    def  pnl(self, reqId: int, dailyPnL: float, unrealizedPnL: float, realizedPnL: float):
        super().pnl(reqId, dailyPnL, unrealizedPnL, realizedPnL)
        print("Daily PnL. ReqId:", reqId, "DailyPnL:", dailyPnL,
              "UnrealizedPnL:", unrealizedPnL, "RealizedPnL:", realizedPnL)


# def main():
#     try:
#         app = TestApp()

        """
        Account Summary
        """
        # app.reqAccountSummary(1, "All", AccountSummaryTags.AllTags)

        """
        Account Update
        """
        # app.reqAccountUpdates(True, app.account)

        """
        Searching for a contract Contract 
        """
        # app.reqContractDetails(1, rel)

        """ 
        Earliest Data Point for Contract 
        """
        # app.reqHeadTimeStamp(1, rel, "TRADES", 1, 1)

        """ Requesting Bar data """
        # app.reqHistoricalData(1, rel, '', "60 S", "1 secs", "TRADES", 1, 1, False, [])

        """ Requesting Position Data """
        # app.reqPositions()

        """ Requesting PnL in real Time for a single Positions"""
        # app.reqPnLSingle(1, self.account, Write the position id here)

        """ Cancel a given Position """
        # app.cancelPnLSingle(Write position Id here)

        """ PnL for all positions """
        # app.reqPnL(1, app.account, "")

#
#     except:
#         """
#         If the connection fails Ewrapper class will raise an Exception with code 502
#         """
#         raise
#
#
# if __name__ == "__main__":
#     main()
