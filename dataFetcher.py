from ibapi.common import BarData, TickerId, TagValueList
from ibapi.utils import iswrapper
from samples.Python.Testbed.MyTests.BaseClass import TestApp as ib
from ContractSamples import ContractSamples, Contract
import pandas as pd

class dataFetcher(ib):
    def __init__(self):
        ib.__init__(self)
        self.data = []
        self.contractName = ""

    @iswrapper
    def historicalData(self, reqId: int, bar: BarData):
        print("Historical Bar. ReqId: ", reqId)
        print(bar.date, 4 * '-', "Bar Open : ", bar.open, "Bar Close : ", bar.close, "Bar low : ", bar.low,
              "Bar High : ",
              bar.high, "Bar Volume: ", bar.volume)
        self.data.append([bar.date, bar.open, bar.close, bar.low, bar.high, bar.volume])

    @iswrapper
    def historicalDataEnd(self, reqId: int, start: str, end: str):
        fileName = '../Data/' + self.contractName + "6Years.csv"
        print("Historical Data Fetch Finished")
        df = pd.DataFrame(self.data, columns= ['Date', 'Open', 'Close', "Low", "High", "Volume"])
        print("Saving File to ",fileName)
        df.to_csv(fileName)

    @iswrapper
    def reqHistoricalData(self, reqId:TickerId , contract:Contract, endDateTime:str,
                          durationStr:str, barSizeSetting:str, whatToShow:str,
                          useRTH:int, formatDate:int, keepUpToDate:bool, chartOptions:TagValueList):
        self.contractName = contract.symbol
        super().reqHistoricalData(reqId, contract, endDateTime, durationStr, barSizeSetting, whatToShow, useRTH, formatDate, keepUpToDate, chartOptions)




if __name__ == "__main__":
    app = dataFetcher()
    app.reqHistoricalData(1, ContractSamples.RelianceContract(), "", "1 Y", "1 day", "TRADES", 0, 1, False, [])




