import sys, os, time
import json as json
import gym
import numpy as np
import pandas as pd

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
        ):
        super().__init__()
        self.wd = os.path.join(os.path.dirname(__file__),'..')
        codes = os.path.join(self.wd, 'codes.json')
        with open(codes, 'r') as f:
            self.codes = json.load(f)
        self.dtype_range = self.codes.keys()

        self.data_folder = os.path.join(self.wd, 'Data')
        self.data_time_range = f'{start_date}-to-{end_date}-{interval}'

        self.focus_type, self.foucs_name = focus_type, focus_name
        self.focus_code = self.codes[focus_type][focus_name]
        self.profolio = {focus_name: 0}

        self.capital = start_capital
        
        self.action_space = gym.spaces.Box(
            low=float(-1), 
            high=float(1), 
            shape=(1,),
            dtype=np.float32
        ) #percentage of buy and sell or keep

        self.current_date = start_date

        self._init_market()
        print(self.dfs.keys())
        print(self.dfs['US-Bond'].keys())
        print(self.dfs[focus_type][focus_name].head())
        print(len(self.all_df_list))


    def _init_market(self):
        self.dfs = {}
        self.all_df_list = []
        for k in self.dtype_range:
            k_df = {}
            for kk in self.codes[k].keys():
                file = os.path.join(self.data_folder, k, self.data_time_range, f'{kk}.csv')
                df = pd.read_csv(file, sep=',')
                k_df.update({kk: df})
                self.all_df_list.append(df)
            self.dfs.update({k: k_df})

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


