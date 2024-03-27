import pandas as pd


class MarketTide:
    def __init__(self, data):

        self.date = [i.get('date') for i in data]
        self.net_call_premium = [i.get('net_call_premium') for i in data]
        self.net_put_premium = [i.get('net_put_premium') for i in data]
        self.net_volume = [i.get('net_volume') for i in data]
        self.timestamp = [i.get('timestamp') for i in data]



        self.data_dict = { 
            'date': self.date,
            'call_premium': self.net_call_premium,
            'put_premium': self.net_put_premium,
            'volume': self.net_volume
        }



        self.as_dataframe = pd.DataFrame(self.data_dict)