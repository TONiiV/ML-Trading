import sys
import os
import json as json
import gym
import numpy as np
import pandas as pd
import datetime
from copy import copy

from logic import TradingCenter


class Environment(gym.Env):
    __episode = 1

    def __init__(
        self,
        focus_type,
        focus_name,
        start_date,
        end_date,
        interval,  # '1d', '1h'
        start_capital,
        training_cycle=180,
        obs_rows = 1  # days
    ):
        super().__init__()
        self.TC = TradingCenter(focus_type, focus_name,
                                start_date, end_date, interval, start_capital)
        self.df_cols = list(self.TC.focus_df.columns)
        remove_cols = ['Date', 'Adj Close']
        for ele in remove_cols:
            self.df_cols.remove(ele)
        # self.action_space = gym.spaces.Box(
        #     low=float(-1),
        #     high=float(1),
        #     shape=(1,),
        #     dtype=np.float32
        # ) #percentage of buy and sell or keep
        self.current_date = start_date
        self.action_space = gym.spaces.Tuple(
            (
                gym.spaces.Discrete(3),
                gym.spaces.Box(low=-1, high=1, shape=(1,)),
                gym.spaces.Box(low=-1, high=1, shape=(1,)),
                gym.spaces.Box(low=-1, high=1, shape=(1,))
            )
        )
        self.obs_rows = obs_rows
        obs_shape = (obs_rows, len(self.df_cols)*len(self.TC.all_df_dict)+2)
        self.observation_space = gym.spaces.Box(
            low=-1,
            high=1, 
            shape = obs_shape, 
            dtype=np.float32
        )
        self.obs_arr = np.zeros(obs_shape)
        self.s = 0
        self.i = 0
        

    def reset(self):
        pass

    def next_day(self):
        date = datetime.datetime.strptime(self.current_date,  "%Y-%m-%d")
        date += datetime.timedelta(days=1)
        self.current_date = date.strftime("%Y-%m-%d")

    @property
    def obs(self):
        self.TC.update_profolio()
        df_list = list(self.TC.all_df_dict.values())
        dlist = []
        for df in df_list:
            data = df.loc[df['Date']==self.TC.current_date, self.df_cols]
            # print(data)
            if data.empty:
                data = np.zeros((1,len(self.df_cols)))
            else:
                data = data.to_numpy()
            dlist.extend(data)
        dlist.append([self.TC.capital, self.TC.net_worth])
        obs = np.concatenate(dlist)
        print(obs.shape)
     
        if self.i > self.s:
            self.obs_arr = np.vstack([self.obs_arr, obs])
            self.obs_arr = np.delete(self.obs_arr, (0), axis=0)
            self.s = copy(self.i)
        else:
            self.obs_arr = self.obs_arr
        if self.obs_rows == 1:
            self.obs_arr = self.obs_arr.flatten()
        return self.obs_arr


    def step(self):
        pass

    def render(self):
        pass

    def close(self):
        pass


params = {
    'focus_type': 'Stocks',
    'focus_name': 'Tesla',
    'start_date': '2015-01-01',
    'end_date': '2023-03-01',
    'interval': '1d',
    'start_capital': 1000,
    'obs_rows': 2
}

env = Environment(**params)
env.current_date = env.TC.current_date = "2016-01-19"
while not env.TC.check_workday():
    env.next_day()
    env.TC.current_date = env.current_date

print('\nCall:', env.current_date)
env.TC.update_profolio()
print(env.TC.get_current_price())
env.TC.trade('call', 0.5)
print(env.TC.profolio)
print(env.TC.capital, env.TC.net_worth)
env.TC.check_profiloio()

env.TC.current_date = '2021-03-05'
print('\nPut:', env.TC.current_date)
env.TC.update_profolio()
env.TC.trade('put', 0.5)
print(env.TC.get_current_price())
env.TC.check_profiloio()
print(env.TC.profolio)
print(env.TC.capital, env.TC.net_worth)

env.TC.current_date = '2021-05-05'
print('\nPut: ', env.TC.current_date)
env.TC.update_profolio()
env.TC.trade('put', 0.5)
print(env.TC.get_current_price())
env.TC.check_profiloio()
print(env.TC.profolio)
print(env.TC.capital, env.TC.net_worth)


env.TC.current_date = '2022-09-08'
print('\nCheck: ', env.TC.current_date)
env.TC.update_profolio()
env.TC.check_profiloio()
print(env.TC.get_current_price())
print(env.TC.profolio)
print(env.TC.capital, env.TC.net_worth)



env.TC.current_date = '2022-11-08'
print('\nClosed: ', env.TC.current_date)
# env.TC.update_profolio()
print(env.TC.get_current_price('Close'))
env.TC.close('put', 0.6)
print(env.TC.profolio)
print(env.TC.capital, env.TC.net_worth)

env.i = 1
print(env.obs)
