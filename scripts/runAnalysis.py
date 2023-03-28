import CAENReader
import sys
from array import array
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import seaborn as sns
import pandas as pd
from scipy import fft
import scipy

#define functions
def spectrum(values):
    """The FFT complex spectrum values of the signal."""
    return scipy.fft.rfft(values)

def frequencies(values, dt):
    """The FFT frequencies of the signal."""
    return scipy.fft.rfftfreq(n=len(values), d=dt)

#Make plots look nice
mpl.rcParams['text.usetex'] = True
mpl.rcParams['mathtext.rm'] = 'Times New Roman'
mpl.rcParams['mathtext.it'] = 'Times New Roman:italic'
mpl.rcParams['mathtext.bf'] = 'Times New Roman:bold'
# mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}'] #for \text command

mpl.rc('font', family='serif', size=12)
mpl.rcParams['xtick.labelsize'] = 16
mpl.rcParams['ytick.labelsize'] = 16
mpl.rcParams['xtick.major.size'] = 5
mpl.rcParams['ytick.major.size'] = 5

mpl.rcParams['axes.titlesize'] = 18
mpl.rcParams['axes.labelsize'] = 22
# mpl.rc('font', size=16)
mpl.rc('axes', titlesize=20)

current_palette = sns.color_palette('colorblind', 10)
import warnings
warnings.filterwarnings("ignore")

infile_name = "/home/coure/SiPMs_QA/configFiles/data_underVbr.dat"
df = CAENReader.DataFile(infile_name)
print('Processing file:', infile_name)

wf_array = []
tr = df.getNextTrigger()
# for i in range(0,200):
while tr is not None:
    trace = tr.traces['b0tr0'].astype("float")
    array_trace = np.array(np.ones(len(trace)))
    bsl = np.mean(trace[0:20])
    for j in range(len(trace)):
        array_trace[j] = (trace[j]-bsl)
    wf_array.append(array_trace)
    tr = df.getNextTrigger()

# Perform FFT

sampling_rate = 500E6 #Smp/s
sample_length = 1/sampling_rate #s

spectrum_array = []
freq_array = []
for i in range(0,len(wf_array)):
    spectrum_array.append(abs(spectrum(wf_array[i])))
    freq_array.append(frequencies(wf_array[i],sample_length))
spectrum_array = np.array(spectrum_array)

#Plot average FFT
plt.figure(figsize=(7,6))
for i in range(0,100):
    plt.plot(frequencies(wf_array[i],sample_length)/1E6,abs(spectrum(wf_array[i])))
plt.plot(frequencies(wf_array[0],sample_length)/1E6,np.mean(spectrum_array, axis=0), c = "black", ls = "--", lw = 3)
plt.xlabel("Freq [MHz]")
plt.yscale('log')
plt.tight_layout()
plt.show()
# plt.savefig("./test.pdf")

