from typing import List, Union
import numpy as np
import pandas as pd
from simba.utils.checks import check_valid_lst, check_valid_array


def embedding_local_outliers(data: List[np.ndarray], k: Union[int, float] = 5, contamination: float = 1e-10):
    check_valid_lst(data=data, source=embedding_local_outliers.__name__, valid_dtypes=(np.ndarray,), min_len=1)
    for i in data:
        print(i)






#
# class LOF():
#     def __init__(self):
#         pass

