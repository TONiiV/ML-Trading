import sys
import os
import random
import json as json
import gym
import numpy as np
import pandas as pd
import datetime
from copy import copy

from logic import TradingCenter


ACTION_MAP = {
    0: 'call',
    1: 'put',
    2: ('close', 'call'),
    3: ('close', 'put')
}


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
        self.set_start_date(start_date)
        self.action_space = gym.spaces.Tuple(
            (
                gym.spaces.Discrete(3),
                gym.spaces.Box(low=0, high=1, shape=(1,)),
                gym.spaces.Box(low=0, high=1, shape=(1,)),
                gym.spaces.Box(low=0, high=1, shape=(1,))
            )
        )
        self.obs_rows = obs_rows
        obs_shape = (obs_rows, len(self.df_cols)*len(self.TC.all_df_dict)+2)
        self.observation_space = gym.spaces.Box(
            low=0,
            high=np.inf, 
            shape = obs_shape, 
            dtype=np.float32
        )
        self.obs_arr = np.zeros(obs_shape)
        self.i = self.s = 0 #self.i: timestep, self.s: updated obs rows
        self.training_cycle = training_cycle #length of an episode

        self.reward_range = (float('-inf'),float('inf'))
        self.total_reward = 0


    def set_start_date(self, given_date=False):
        if given_date:
            try:
                datetime.date.fromisoformat(given_date)
            except ValueError:
                raise ValueError("Incorrect data format, should be YYYY-MM-DD")
            self.current_date = self.TC.current_date = given_date
        else:
            date_amount = len(self.TC.focus_date)
            random_idx = random.randint(0, date_amount-self.training_cycle)
            self.current_date = self.TC.current_date = self.TC.focus_date[random_idx]
           

    def reset(self):
        self.set_start_date()
        self.i = self.s = 0
        self.TC.reset_account()

        return self.obs
        

    def next_day(self):
        date = datetime.datetime.strptime(self.current_date,  "%Y-%m-%d")
        date += datetime.timedelta(days=1)
        self.i += 1
        self.current_date = date.strftime("%Y-%m-%d")
        self.TC.current_date = self.current_date

    @property
    def obs(self):
        if self.i > self.s: #in case obs gets updated every time when self.obs is called
            #self.TC.update_profolio('Open')
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
            self.obs_arr = np.vstack([self.obs_arr, obs])
            self.obs_arr = np.delete(self.obs_arr, (0), axis=0)
            self.s = copy(self.i)

        else:
            self.obs_arr = self.obs_arr

        if self.obs_rows == 1:
            self.obs_arr = self.obs_arr.flatten()

        return self.obs_arr

    @property
    def is_done(self):
        if self.i > self.training_cycle-1:
            return True, 'Max Days'
        
        elif self.TC.net_worth < 0:
            return True, 'Bankcrupt'
        
        else:
            return False, 'Trading'
    
    def get_reward(self):
        return 0
    

    def step(self, action):
        while not env.TC.check_workday():
            self.next_day()

        self.TC.update_profolio('Open')
        self.TC.check_profiloio()

        if action[0] < 2:
            self.TC.trade(ACTION_MAP[action[0]], action[action[0]+1][0])
        else: 
            self.TC.close(ACTION_MAP[action[0]][1], action[action[0]+1][0])
        
        self.TC.update_profolio('Close')
        self.TC.check_profiloio()

        reward = self.get_reward()
        obs = self.obs
        done = self.is_done[0]
        
        info = {
            'i': self.i,  
            'Result': self.is_done[1],
            'Capital': self.TC.capital,
            'Net Worth': self.TC.net_worth,
            'Profilio': self.TC.profolio 
            #'tr': self.total_reward,    
        }

        self.next_day()
        return obs, reward, done, info



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
    'obs_rows': 15,
    'training_cycle': 15
}

env = Environment(**params)
action =  env.action_space.sample()
print('Action: ',action)
epochs = 10


for e in range(epochs):
    obs = env.reset()
    Day = 0
    while True:
        print(Day)
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        Day += 1
        if done:
            print(info)
            obs = env.reset()
            break






# env.set_start_date("2015-01-19")
# while not env.TC.check_workday():
#     env.next_day()

# print('\nCall:', env.current_date)
# env.TC.update_profolio()
# print(env.TC.get_current_price())
# env.TC.trade('call', 0.5)
# print(env.TC.profolio)
# print(env.TC.capital, env.TC.net_worth)
# env.TC.check_profiloio()

# env.set_start_date('2021-03-05')
# print('\nPut:', env.TC.current_date)
# env.TC.update_profolio()
# env.TC.trade('put', 0.5)
# print(env.TC.get_current_price())
# env.TC.check_profiloio()
# print(env.TC.profolio)
# print(env.TC.capital, env.TC.net_worth)

# env.set_start_date('2021-05-05')
# print('\nPut: ', env.TC.current_date)
# env.TC.update_profolio()
# env.TC.trade('put', 0.5)
# print(env.TC.get_current_price())
# env.TC.check_profiloio()
# print(env.TC.profolio)
# print(env.TC.capital, env.TC.net_worth)


# env.set_start_date('2021-10-05')
# print('\nCheck: ', env.TC.current_date)
# env.TC.update_profolio()
# env.TC.check_profiloio()
# print(env.TC.get_current_price())
# print(env.TC.profolio)
# print(env.TC.capital, env.TC.net_worth)



# env.TC.current_date = env.current_date = '2022-11-08'
# print('\nClosed: ', env.TC.current_date)
# # env.TC.update_profolio()
# print(env.TC.get_current_price('Close'))
# env.TC.close('put', 0.6)
# print(env.TC.profolio)
# print(env.TC.capital, env.TC.net_worth)

# env.i = 1
# print(env.obs)
# env.next_day()
# env.i = 2
# print(env.obs)
# print(env.obs.shape)