import numpy as np
import pandas as pd


class Parser(object):
    def parse_to_df(self, input_dict: dict) -> pd.DataFrame:
        raise NotImplementedError('Do not use abstract method')

    def parse_to_array(self, input_dict: dict) -> np.ndarray:
        raise NotImplementedError('Do not use abstract method')