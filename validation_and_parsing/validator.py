import pandas as pd
import pandas as pd


class Validator(object):
    def check_if_valid(self, df) -> bool:
        raise NotImplementedError('Do not use abstract method')

    def validate(self, df) -> pd.DataFrame:
        raise NotImplementedError('Do not use abstract method')
