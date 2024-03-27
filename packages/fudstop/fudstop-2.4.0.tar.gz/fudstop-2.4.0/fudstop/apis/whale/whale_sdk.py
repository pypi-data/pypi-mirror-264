import httpx
import os
from dotenv import load_dotenv
load_dotenv()
from .whale_models import MarketTide, AllTide
from datetime import datetime , timedelta
today = datetime.now().strftime('%Y-%m-%d')
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')



class WhaleSDK:
    def __init__(self):
        self.key = os.environ.get('WHALES_KEY')
        self.headers = { 
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {self.key}",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }




    async def market_tide(self, date:str=yesterday, grouping_minutes:str='1'):

        endpoint = f"https://phx.unusualwhales.com/api/net-flow-ticks?date={date}&grouping_minutes={grouping_minutes}&market_day_timeframe=1"

        async with httpx.AsyncClient(headers=self.headers) as client:
            data = await client.get(endpoint)
            data = data.json()

            data = data['data']

            return MarketTide(data)



    async def all_tide(self, date:str='2024-03-26', timeframe:str='1min'): 
        endpoint = f"https://phx.unusualwhales.com/api//net_flow/second?date={date}&time_frame={timeframe}"

        async with httpx.AsyncClient(headers=self.headers) as client:
            data = await client.get(endpoint)
            data = data.json()

            data = data['data']

            return AllTide(data)
