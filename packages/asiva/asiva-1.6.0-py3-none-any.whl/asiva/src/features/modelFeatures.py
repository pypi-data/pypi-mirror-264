import numpy as np
import scipy.signal
from gatspy.periodic import LombScargleFast
from astropy.timeseries import LombScargle
from statsmodels.tsa import stattools
import math

def period(time,mag):
    gatspy_period = LombScargleFast()
    gatspy_period.fit(time, mag, 0.01)
    gatspy_period.optimizer.period_range=(0.1, 10)
    originalPeriod = gatspy_period.best_period
    return originalPeriod
    
def falseProbAlarm(time, mag):
        ls = LombScargle(time, mag, 1.0)
        freq, power = ls.autopower()
        return ls.false_alarm_probability(power.max())
    
def rcs(mag): 
        sigma = np.std(mag)
        N = len(mag)
        m = np.mean(mag)
        s = np.cumsum(mag - m) * 1.0 / (N * sigma)
        R = np.max(s) - np.min(s)
        return R
        
def stetsonK(mag):
        error = np.random.normal(loc=0.035, scale=0.005, size=mag.shape[0])
        
        mean_mag = (np.sum(mag/(error*error)) /
                        np.sum(1.0 / (error * error)))
        
        N = len(mag)
        sigmap = (np.sqrt(N * 1.0 / (N - 1)) *
                  (mag - mean_mag) / error)

        K = (1 / np.sqrt(N * 1.0) *
             np.sum(np.abs(sigmap)) / np.sqrt(np.sum(sigmap ** 2)))

        return K

def entropy(mag, prob='standard'):
    if prob == 'standard':
        value, counts = np.unique(mag, return_counts=True)
        p = counts / counts.sum()
    elif prob == 'kde':
        p = kde(mag)
    elif prob == 'gauss':
        p = gaussian(mag)

    if np.sum(p) == 0:
        return 0.0

    p = p[np.where(p != 0)]

    if np.log2(len(mag)) == 1:
        return 0.0
    elif np.sum(p * np.log2(p)) / np.log2(len(mag)) == 0:
        return 0.0
    else:
        return - np.sum(p * np.log2(p)) / np.log2(len(mag))

def kurtosis(mag):
    return scipy.stats.kurtosis(mag)

def skewness(mag):
    return scipy.stats.skew(mag)

def calc_mean(mag):
    return np.mean(mag)

def calc_std(mag):
    return np.std(mag)

def ecdf(mag, d=10):
    y =  np.arange(1, len(mag)+1)/len(mag)
    if len(mag) <= d:
        return tuple(y)
    else:
        return tuple(y[:d])

def psi_CS(time, mag):

    T = 1.0 / period(time,mag)
    new_time = np.mod(time, 2 * T) / (2 * T)

    folded_data = mag[np.argsort(new_time)]
    sigma = np.std(folded_data)
    N = len(folded_data)
    m = np.mean(folded_data)
    s = np.cumsum(folded_data - m) * 1.0 / (N * sigma)
    R = np.max(s) - np.min(s)

    return R