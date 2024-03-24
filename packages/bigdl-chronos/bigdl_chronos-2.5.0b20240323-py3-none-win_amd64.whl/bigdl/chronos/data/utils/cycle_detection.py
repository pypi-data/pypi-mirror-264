#
# Copyright 2016 The BigDL Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from scipy.fftpack import fft, fftfreq
import numpy as np


def cycle_length_est(data, top_k=3, adjust=False):
    '''
    Detect the cycle of a time series.
    code adaptted from https://zhuanlan.zhihu.com/p/394327245

    :param data: 1 dim ndarray for time series.
    :param top_k: The freq with top top_k power after fft will be
           used to check the autocorrelation. Higher top_k might be time-consuming.
           The value is default to 3.
    :param adjust: if normalization is applied to the final result.
    '''
    from bigdl.nano.utils.common import invalidInputError
    invalidInputError((data.size//2) > abs(top_k)+1,
                      "top_k must be less than half the length of the time series,"
                      " but top_k and data length are {top_k} and {data.size} respectively.")

    fft_series = fft(data)
    power = np.abs(fft_series)
    sample_freq = fftfreq(fft_series.size)

    pos_mask = np.where(sample_freq > 0)
    freqs = sample_freq[pos_mask]
    powers = power[pos_mask]

    # top_k index
    top_k_idxs = np.argpartition(powers, -top_k)[-top_k:]
    top_k_power = powers[top_k_idxs]
    fft_periods = (1 / freqs[top_k_idxs]).astype(int)

    # Expected time period
    largest_acf_score = -float("inf")
    cycle_length_est = None

    for lag in fft_periods:
        acf_score = acf(data, lag, adjust)
        if acf_score > largest_acf_score:
            cycle_length_est = lag
            largest_acf_score = acf_score

    return cycle_length_est


def acf(x, lag, adjust):
    '''
    generate acf score as in statsmodels.tsa.stattools.acf
    code adapted from https://stackoverflow.com/questions/36038927/
    '''
    length = x.size
    y1, y2 = x[:(length-lag)], x[lag:]
    sum_product = np.sum((y1-np.mean(x))*(y2-np.mean(x)))
    if adjust:
        var = np.var(x)
        if var == 0:
            return 0
        return sum_product / ((length - lag) * var)
    else:
        return sum_product
