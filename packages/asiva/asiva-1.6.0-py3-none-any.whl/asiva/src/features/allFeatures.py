import numpy as np
import scipy as sp
import scipy.signal
from gatspy.periodic import LombScargleFast
from astropy.timeseries import LombScargle
import nolds
from statsmodels.tsa import stattools
import math
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def amplitude(mag):

    N = len(mag)
    sorted_mag = np.sort(mag)

    return (np.median(sorted_mag[-int(math.ceil(0.05 * N)):]) -
            np.median(sorted_mag[0:int(math.ceil(0.05 * N))])) / 2.0

def autocorr(mag):
    # return float(np.correlate(mag, mag))

    nlags = 100
    AC = stattools.acf(mag, nlags=nlags)
    k = next((index for index, value in
             enumerate(AC) if value < np.exp(-1)), None)

    while k is None:
        nlags = nlags + 100
        AC = stattools.acf(mag, nlags=nlags)
        k = next((index for index, value in
                  enumerate(AC) if value < np.exp(-1)), None)

    return k

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

def mean_abs_diff(mag):
    return np.mean(np.abs(np.diff(mag)))

def mean_diff(mag):
    return np.mean(np.diff(mag))

def median_abs_diff(mag):
    return np.median(np.abs(np.diff(mag)))

def median_diff(mag):
    return np.median(np.diff(mag))

def distance(mag):
    diff_sig = np.diff(mag).astype(float)
    return np.sum([np.sqrt(1 + diff_sig ** 2)])

def sum_abs_diff(mag):
    return np.sum(np.abs(np.diff(mag)))

def slope(mag):
    t = np.linspace(0, len(mag) - 1, len(mag))

    return np.polyfit(t, mag, 1)[0]

def pk_pk_distance(mag):
    return np.abs(np.max(mag) - np.min(mag))

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

def neighbourhood_peaks(mag, n=10):
    mag = np.array(mag)
    subsequence = mag[n:-n]
    peaks = ((subsequence > np.roll(mag, 1)[n:-n]) & (subsequence > np.roll(mag, -1)[n:-n]))
    for i in range(2, n + 1):
        peaks &= (subsequence > np.roll(mag, i)[n:-n])
        peaks &= (subsequence > np.roll(mag, -i)[n:-n])
    return np.sum(peaks)

def interq_range(mag):
    return np.percentile(mag, 75) - np.percentile(mag, 25)

def kurtosis(mag):
    return scipy.stats.kurtosis(mag)

def skewness(mag):
    return scipy.stats.skew(mag)

def calc_max(mag):
    return np.max(mag)

def calc_min(mag):
    return np.min(mag)

def calc_mean(mag):
    return np.mean(mag)

def calc_median(mag):
    return np.median(mag)

def mean_abs_deviation(mag):
    return np.mean(np.abs(mag - np.mean(mag, axis=0)), axis=0)

def median_abs_deviation(mag):
    return scipy.stats.median_absolute_deviation(mag, scale=1)

def rms(mag):
    return np.sqrt(np.sum(np.array(mag) ** 2) / len(mag))

def calc_std(mag):
    return np.std(mag)

def calc_var(mag):
    return np.var(mag)

def ecdf(mag, d=10):
    y =  np.arange(1, len(mag)+1)/len(mag)
    if len(mag) <= d:
        return tuple(y)
    else:
        return tuple(y[:d])

def lyapunov(mag):
    lyapr = nolds.lyap_r(mag)
    lyapr=lyapr.round(4)
    return lyapr

def sample_entropy(mag):
    sampe = nolds.sampen(mag)
    sampe=sampe.round(4)
    return sampe

def corr_dimension(mag,emb_dim=2):
    corrd = nolds.corr_dim(mag, emb_dim=2)
    corrd=corrd.round(4)
    return corrd

def detrended_fluctuation(mag):
    dtrfa = nolds.dfa(mag)
    dtrfa=dtrfa.round(4)
    return dtrfa

def hurst(mag):
    hurstExp = nolds.hurst_rs(mag)
    hurstExp=hurstExp.round(4)
    return hurstExp

def fractal_dimension(data,data_file_name,dim,l_range,file_index):

    if dim ==1:
        if data_file_name=='':
            l_max=data.shape[0]
            if len(data.shape)==1:
                nb_s=1
            else :    
                nb_s=data.shape[1]
        else:
            nb_s=len(data_file_name)
            l_max=np.loadtxt(data_file_name[0]).shape[0]

    n_max=int(sp.log(l_max)/sp.log(2))
    nb_ones=np.zeros((n_max+1))
    l_list=np.zeros((n_max+1))    
    for n in range(sp.int0(n_max)+1):
        l_list[n]=sp.power(2,n)
    
    if file_index == 0:  # nb_ones is computed
        if dim == 1:
            if data_file_name=='':           
                nb_ones[n_max]=sp.count_nonzero(data)/nb_s             
                for n_l in range(sp.int0(n_max-1),-1,-1):
                    nb_el=data.shape[0]
                    data=(data[0:nb_el:2,:]+data[0:nb_el+1:2,:])/2 #Upscaling of the field
                    nb_ones[n_l]=sp.count_nonzero(data)/nb_s
            else: 
                for s in range(0,nb_s):
                    data_s=np.loadtxt(data_file_name[s],delimiter=';')
                    nb_ones[n_max]=nb_ones[n_max]+sp.count_nonzero(data_s)/nb_s
                    for n_l in range(sp.int0(n_max-1),-1,-1):
                        nb_el=data_s.shape[0]                    
                        data_s=(data_s[0:nb_el:2]+data_s[1:nb_el+1:2])/2        
                        nb_ones[n_l]=nb_ones[n_l]+sp.count_nonzero(data_s)/nb_s
    
    y=sp.log(nb_ones)
    x=sp.log(l_list)

    nb_scale_reg = len(l_range) #Evaluation of the number of scaling regime    
    
    if nb_scale_reg == 0:
        a=sp.polyfit(x,y,1)   
        reg_lin=sp.poly1d(a)    
        D1=a[0]
        r2=sp.corrcoef(x,y)[0,1]**2
    else :
        print('Error in fractal_dimension_1D, l_range has wrong size')
        
    return D1



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