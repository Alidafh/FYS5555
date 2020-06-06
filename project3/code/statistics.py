import numpy as np
import matplotlib.pyplot as plt
import ROOT as ro


def Poisson(lamb, k):
    #return np.log(lamb) * S - np.loggamma(S + 1) - lamb
    return (lamb**k * np.exp(-lamb))/np.math.factorial(k)

def CL(lamb, nobs):
    CL_sb = 0
    for i in range(int(nobs)):
        CL_sb += Poisson(lamb, i)
    return CL_sb

def significance(s, b, n):
    Z_exp = np.nan_to_num(np.sqrt(2*(s+b)*np.log(1+(s/b)) - 2*s))
    Z_obs = np.nan_to_num(np.sqrt(2*n*np.log(n/b) - 2*(n-b)))
    return Z_exp, Z_obs

def sigFromP(pval):
    Z = np.sqrt(ro.Math.chisquared_quantile_c(pval*2,1))
    return Z

def pFromSig(sig):
    p = ro.Math.chisquared_cdf_c(pow(sig, 2), 1)/2
    return p

def test_sig(s,b):
    return s/np.sqrt(b)

if __name__ == '__main__':
    s = 425.21142578125
    b = 19732.498291015625
    nobs = 20128.0
    poisson = Poisson(s+b, nobs)
    #CL = CL(s+b, nobs)
