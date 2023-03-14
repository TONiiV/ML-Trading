import json as json
import pandas as pd
import os, math
from datetime import datetime

ACTION_MAP = {
    0: "call",
    1: "put",
    2: "close"
}

def normal_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    elif n - math.floor(n) == 0.5:
        return round(n, 1)
    return math.ceil(n)


class TradingCenter:

    def __init__(
            self,
            focus_type, 
            focus_name, 
            start_date,
            end_date,
            interval,
            start_capital
            
        ):
        self.wd = os.path.join(os.path.dirname(__file__),'..')
        codes = os.path.join(self.wd, 'codes.json')
        with open(codes, 'r') as f:
            self.codes = json.load(f)
        self.dtype_range = self.codes.keys()

        self.data_folder = os.path.join(self.wd, 'Data')
        self.data_time_range = f'{start_date}-to-{end_date}-{interval}'

        self.focus_type, self.foucs_name = focus_type, focus_name
        self.focus_code = self.codes[focus_type][focus_name]
    
        self.current_date = start_date
        self._init_market()
        self.focus_df = self.dfs[self.focus_type][focus_name]

        self.focus_type, self.foucs_name = focus_type, focus_name 
        self.capital = self.start_capital = start_capital

        self.reset_account()

        # print(self.dfs.keys())
        # print(self.dfs['US-Bond'].keys())
        # print(self.dfs[focus_type][focus_name].head())
        # print(len(self.all_df_dict), self.all_df_dict.keys())

    def _init_market(self):
        dtype_dict = {
            #"Date": 'int64',
            "Open": 'float',
            "High": 'float',
            "Low": 'float',
            "Close": 'float',
            "Adj Close": 'float',
            "Volume": 'float'
        }
        self.dfs = {}
        self.all_df_dict = {}
        for k in self.dtype_range:
            k_df = {}
            for kk in self.codes[k].keys():
                file = os.path.join(self.data_folder, k, self.data_time_range, f'{kk}.csv')
                df = pd.read_csv(file, sep=',')
                #df.Date = pd.to_datetime(df.Date, origin='unix')
                df = df.astype(dtype_dict)
                k_df.update({kk: df})
                self.all_df_dict.update({kk: df})
            self.dfs.update({k: k_df})
    
    def reset_account(self):
        self.capital = self.start_capital
        self.profolio = {
            'call': {"amount": 0,
                    "avg_price": 0,
                    "cost": 0,
                    "worth": 0},
            'put': {"amount": 0,
                    "avg_price": 0,
                    "cost": 0,
                    "worth": 0},
        }
        self.net_worth = self.capital

    def purchase(self, total_price):
        if total_price > self.capital:
            print("No Enough Cash to Finish Payment!")
            return False
        else:
            self.capital -= total_price
            return True

    def get_current_price(self, timing = 'Open'):
        current_price = self.focus_df.loc[self.focus_df['Date'] == self.current_date, timing].item()
        '''
        When Date does not exist in df: 
        '''
        return current_price


    def update_profolio(self, timing = 'Open'):
        current_price = self.get_current_price(timing)
        amount = self.profolio['call']['amount']
        new_worth = current_price*amount
        self.profolio['call'].update({'worth': new_worth})
        put_worth = self.profolio['put']['cost'] - self.profolio['put']['amount']*current_price
        self.profolio['put'].update({'worth': put_worth})

        self.net_worth = self.capital + self.profolio['call']['worth'] + self.profolio['put']['worth']

    def check_profiloio(self):
        '''
        If abs(type_worth) >= (type_worth + capital)*40% and type_worth < 0, all type-shares must be closed.
        '''
        
        if abs(self.profolio['put']['worth']) >= 0.4*(self.profolio['call']['worth']+self.capital) and self.profolio['put']['worth']<0:
            self.close('put', 1)

    def trade(self, type, percentage):
        bid = percentage * self.capital 
        current_price = self.get_current_price()
        print(current_price)

        amount = normal_round(bid/current_price)
        total_price = amount * current_price
        if self.purchase(total_price):
            new_amount = amount + self.profolio[type]['amount']
            new_cost = total_price + self.profolio[type]['cost']
            new_avg_price = new_cost/new_amount
            new_worth = current_price*new_amount if type == 'call' else new_cost - current_price*new_amount
            
            vals = [
                new_amount, 
                new_avg_price,
                new_cost,
                new_worth
            ]
            for i in range(len(self.profolio[type].keys())):
                self.profolio[type].update({list(self.profolio[type].keys())[i]: vals[i]})
        
        else:
            print(f"Purchase Failure! ({type})")


    def close(self, type, percentage):
        self.update_profolio()
        amount = normal_round(self.profolio[type]['amount']*percentage) 
        if self.profolio[type]['amount'] != 0:
            cash_out = self.profolio[type]['worth']*(amount/self.profolio[type]['amount'])
        else:
            cash_out = 0
        self.capital += cash_out

        new_amount = self.profolio[type]['amount']-amount
        new_cost = self.profolio[type]['avg_price']*new_amount
        new_avg_price = self.profolio[type]['avg_price'] if new_amount != 0 else 0
        new_worth = self.profolio[type]['worth'] - cash_out
        vals = [
            new_amount, 
            new_avg_price,
            new_cost,
            new_worth
        ]
        for i in range(len(self.profolio['put'].keys())):
            self.profolio[type].update({list(self.profolio['put'].keys())[i]: vals[i]})
        
        
        
        
        
        


