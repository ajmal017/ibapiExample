from datetime import datetime

from ibapi.common import TickAttribLast
from samples.Python.Testbed.MyTests.BaseClass import TestApp
from samples.Python.Testbed.ContractSamples import ContractSamples
from samples.Python.Testbed.MyTests.Utils.dataFetcherStatic import dataFetcher

class LiveMarketData(TestApp):
    def __init__(self):
        TestApp.__init__(self)

    def tickByTickAllLast(self, reqId: int, tickType: int, time: int, price: float,
                          size: int, tickAttribLast: TickAttribLast, exchange: str,
                          specialConditions: str):
        super().tickByTickAllLast(reqId, tickType, time, price, size, tickAttribLast,
                                  exchange, specialConditions)
        if tickType == 1:
            print("Last. ", end='')

        print("ReqId: ", reqId,
              "Time:", datetime.datetime.fromtimestamp(time).strftime("%Y%m%d %H:%M:%S"),
              "Price:", price, "Size:", size, "Exch:", exchange,
              "Spec Cond:", specialConditions, "PastLimit:", tickAttribLast.pastLimit, "Unreported:",
              tickAttribLast.unreported)

    def tickByTickMidPoint(self, reqId: int, time: int, midPoint: float):
        # super().tickByTickMidPoint(reqId, time, midPoint)
        print("Midpoint. ReqId:", reqId,
              "Time:", datetime.fromtimestamp(time).strftime("%Y%m%d %H:%M:%S"),
              "MidPoint:", midPoint)

if __name__ == "__main__":
    datafetcher = dataFetcher()

    app = LiveMarketData()
    # app.reqTickByTickData(1, ContractSamples.UsdJpyFx(), "MidPoint", 0, True)

