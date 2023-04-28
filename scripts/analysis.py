import CAENReader
import sys
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import seaborn as sns
import pandas as pd
import scipy
from scipy import fft
from lmfit.models import GaussianModel, ConstantModel
import scipy.signal

#define functions
def spectrum(values):
    """The FFT complex spectrum values of the signal."""
    return scipy.fft.rfft(values)

def frequencies(values, dt):
    """The FFT frequencies of the signal."""
    return scipy.fft.rfftfreq(n=len(values), d=dt)

def make_model(num):
    """for fitting"""
    pref = "f{0}_".format(num)
    model = GaussianModel(prefix = pref)
    model.set_param_hint(pref+'amplitude', value=amplitude[num], min=0, max=1000*amplitude[num])
    model.set_param_hint(pref+'center', value=center[num], min=center[num]-50, max=center[num]+50)
    model.set_param_hint(pref+'sigma', value=width[num], min=10., max=800)
    return model