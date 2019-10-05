"""
Signal models for fitting magnetization parameters from MR Images acquired with a Gradient Echo (GRE) Ultrashort TE (UTE) pulse sequence
"""
__author__ = "Dharshan Chandramohan"

import numpy as np

def T2str_mag_simplified(K, TE, T2str, N):
    """Signal Model of T2str-weighted UTE GRE Magnitude Image
    
    S = K * [ exp(-TE/T2*) ] + N
    
    parameters:
      K :: constant (proportional to proton density)
      TE :: sequence echo time
      T2str :: relaxation due to spin-spin effects and dephasing
      N :: constant offset "noise" term
    
    @return expected (magnitude) signal
    """
    S = K * np.exp((-1.0 * TE)/T2str) + N
    return S

def t2strw_mag_resid(params, utes, obs_sig):
    """Residuals when fitting the T2str-weighted UTE GRE magnitude signal
    
    See T2str_mag_simplified(...) [above]
    Used for least-squares fitting
    
    @param params :: Parameters to be fit (e.g., current estimates)
    @param utes :: ultrashort echo times in multi-echo sequence
    
    Parameter ordering:
      params[0] = T2str
      params[1] = K
      params[2] = N
    
    @return res :: signal residuals
    """
    T2str = params[0]
    K = params[1]
    N = params[2]

    res = T2str_mag_simplified(K, utes, T2str, N) - obs_sig
    return res

def T2str_power(P_0, TE, T2str):
    """Signal Model for the "power" (square of the magnitude) of a complex signal from a T2* weighted GRE image
    
    P = M_c^2 = Re{S}^2 + Im{S}^2
    P = P_0 * [ exp(-2TE/T2*) ]
    
    M_c stands for the "noise-corrected" signal magnitude
    M_c^2 = M^2 - 2*sigma^2
    where sigma is the standard deviation in a noise region (this information is relevant to caluclating the residuals)
    
    parameters:
      P_0 :: constant (proportional to proton density)
      TE :: sequence echo time
      T2str :: relaxationn due to spin-spin effects and dephasing
    
    @return P :: predicted power of the signal
    """

    P = P_0 * np.exp((-2.0 * TE)/T2str)
    return P

def t2strw_pow_resid(params, utes, obs_power, noise_est):
    """Residuals when fitting the power of the T2str-weighted UTE GRE signal
    
    See T2str_power(...) [above]
    Used for least-squares fitting (via scipy.optimize.least_squares)
    
    @param params :: Parameters to be fit (e.g., current estimates)
    @param utes :: ultrashort echo times of the multi-echo sequence
    @param obs_signal :: should be the observed power of the complex signal (magnitude squared)
    @param noise_est :: should be the average value of the background in the squared magnitude image
    
    Parameter ordering:
      params[0] = T2str
      params[1] = P_0
    
    @return res :: power residuals
    """

    P_corr = obs_power - noise_est
    T2str = params[0]
    P_0 = params[1]

    res = T2str_power(P_0, utes, T2str) - P_corr
    return res

def T2str_cplx(K, TE, T2str, df, phi):
    """Signal Model of T2str-weighted UTE GRE Magnitude Image
    
    S = K * [ exp(-TE/T2*) ] + N
    
    parameters:
      K :: constant (proportional to proton density)
      TE :: sequence echo time
      T2str :: relaxation due to spin-spin effects and dephasing
      df :: frequency shift
      phi :: phase
    
    @return expected (magnitude) signal
    """
    S = K * np.exp((-1.0 * TE)/T2str - 1j*2*np.pi*df*TE + 1j*phi)
    return S

def t2strw_cplx_resid(params, utes, obs_sig):
    """Residuals when fitting the T2str-weighted UTE GRE magnitude signal
    
    See T2str_cplx(...) [above]
    Used for least-squares fitting
    
    @param params :: Parameters to be fit (e.g., current estimates)
    @param utes :: ultrashort echo times in multi-echo sequence
    
    Parameter ordering:
      params[0] = T2str
      params[1] = K
      params[2] = df
      params[3] = phi
    
    @return res :: signal residuals
    """
    T2str = params[0]
    K = params[1]
    df = params[2]
    phi = params[3]

    res = T2str_cplx(K, utes, T2str, df, phi) - obs_sig
    return np.array([res.real, res.imag]).T.flatten()

def spgr_mag(PD, T1, T2str, TR, TE, alph, k=1.0):
    """Spoiled Gradient Recall at Steady State (SPGR) signal equation"""
    S = k * PD * np.exp(-TE/T2str) * ((np.sin(alph) * (1 - np.exp(-TR/T1)))/(1 - (np.cos(alph) * np.exp(-TR/T1))))
    return S

def T1_mag(K, T1, TR, alph):
    """Expected signal for T1w UTE GRE 'magnitude' images"""
    S = K * ((np.sin(alph) * (1 - np.exp((-1.0 * TR)/T1))) / (1 - (np.cos(alph) * np.exp((-1.0 * TR)/T1))))
    return S

def calc_VFA_T1(S1, S2, fa1, fa2, TR):
    """Equation to calculate T1 from two T1w UTE GRE 'magnitude' images with different flip angles"""
    T1 = -1.0 * TR / np.log((S1/np.sin(fa1) - S2/np.sin(fa2)) / (S1/np.tan(fa1) - S2/np.tan(fa2)))
    return T1
