import sys, os, time
import json as json
import gym
import numpy as np
import pandas as pd

from logic import TradingCenter
class Environment(gym.Env):
    __episode = 1

    def __init__(
            self, 
            focus_type, 
            focus_name, 
            start_date,
            end_date,
            interval, #'1d', '1h'
            start_capital,
            training_cycle = 180 # days
        ):
        super().__init__()
        self.TC = TradingCenter(focus_type, focus_name, start_date, end_date, interval, start_capital)

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

        
       

    def reset(self):
        pass

    @property
    def obs(self):
        pass

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
}

env = Environment(**params)
env.TC.current_date = "2015-01-05"
print('\nPut')
env.TC.update_profolio()
print(env.TC.get_current_price())
env.TC.trade('put',0.5)
print(env.TC.profolio)
print(env.TC.capital, env.TC.net_worth)
env.TC.check_profiloio()

env.TC.current_date = '2021-03-05'
print('\nCall')
env.TC.update_profolio()
env.TC.trade('call',0.5)
print(env.TC.get_current_price())
env.TC.check_profiloio()
print(env.TC.profolio)
print(env.TC.capital, env.TC.net_worth)

env.TC.current_date = '2021-05-05'
env.TC.update_profolio()
print(env.TC.get_current_price())
env.TC.check_profiloio()
print(env.TC.profolio)
print(env.TC.capital, env.TC.net_worth)


env.TC.current_date = '2022-09-08'
env.TC.update_profolio()
env.TC.check_profiloio()
print(env.TC.get_current_price())
print(env.TC.profolio)
print(env.TC.capital, env.TC.net_worth)

print('\nClosed')

env.TC.current_date = '2022-11-08'
#env.TC.update_profolio()
print(env.TC.get_current_price())
env.TC.close('put', 0.6)
print(env.TC.profolio)
print(env.TC.capital, env.TC.net_worth)