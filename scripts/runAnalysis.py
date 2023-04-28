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

#Make plots look nice
mpl.rcParams['text.usetex'] = True
mpl.rcParams['mathtext.rm'] = 'Times New Roman'
mpl.rcParams['mathtext.it'] = 'Times New Roman:italic'
mpl.rcParams['mathtext.bf'] = 'Times New Roman:bold'

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

SiPM_ID = str(sys.argv[1])
if(len(sys.argv)>3):
    channel = int(sys.argv[3])
else:
    channel = 0
infile_name = "/home/coure/SiPMs_QA/data/SiPM_%s/SiPM_%s.dat"%(SiPM_ID,SiPM_ID)
df = CAENReader.DataFile(infile_name)
outFolder = str(sys.argv[2])

print('Processing file:', infile_name)
print('Processing channel:', channel)

wf_array = []
integ_ADC = []
samples = []

print("Calculating SPE spectrum \n")

tr = df.getNextTrigger()
while tr is not None:
    trace = tr.traces['b0tr%i'%channel].astype("float")
    array_trace = np.array(np.ones(len(trace)))
    bsl = np.mean(trace[0:20])
    for j in range(len(trace)):
        array_trace[j] = (trace[j]-bsl)
    wf_array.append(array_trace)
    integ_ADC.append(sum(array_trace[70:120]))
    samples.append(np.arange(0,300))
    tr = df.getNextTrigger()


#Fit
print("Performing fit \n")

bin_heights, bin_borders, _ = plt.hist(np.array(integ_ADC), bins=150,range=(-400,4000), density=True, );
bin_centers = bin_borders[:-1] + np.diff(bin_borders) / 2

peaks_in_interval = scipy.signal.find_peaks_cwt(bin_heights, widths=10)
number_of_peaks = len(peaks_in_interval)
amplitude = bin_heights[peaks_in_interval]
width = np.zeros(number_of_peaks) + 100
center = bin_centers[peaks_in_interval]

def make_model(num):
    pref = "f{0}_".format(num)
    model = GaussianModel(prefix = pref)
    model.set_param_hint(pref+'amplitude', value=amplitude[num], min=1E-8, max=1000*amplitude[num])
    model.set_param_hint(pref+'center', value=center[num], min=center[num]-50, max=center[num]+50)
    model.set_param_hint(pref+'sigma', value=width[num], min=10., max=800)
    return model

mod = None
for i in range(len(peaks_in_interval)):
    this_mod = make_model(i)
    if mod is None:
        mod = this_mod
    else:
        mod = mod + this_mod

mod = mod

out=mod.fit(bin_heights, x=bin_centers)

# Plot SPE spectrum

plt.figure(figsize=(7,4))
plt.hist(integ_ADC, bins = 150, histtype="step", range = (-400,4000), lw = 1.5, density=True);
plt.ylabel('Counts')
plt.xlabel('Integrated ADC')
plt.title("SPE Spectrum for SiPM_%s"%(SiPM_ID))
plt.plot(bin_centers, out.best_fit, label='best fit')
plt.legend()
plt.grid()

plt.tight_layout()
plt.savefig(outFolder+"SPE_ch%i_%s.pdf"%(channel,SiPM_ID))
del(integ_ADC)
# plt.show()

# Plot average waveform
print("Plotting average waveform \n")

wf_flat_list = [item for sublist in wf_array for item in sublist]
samples_flat_list = [item for sublist in samples for item in sublist]

plt.figure(figsize=(9,6))

plt.hist2d(np.array(samples_flat_list), wf_flat_list,range = ([0,300],[-200,1000]), bins = 200, norm=mpl.colors.LogNorm());
plt.plot(np.mean(wf_array, axis=0), c = "black", ls = "-", lw = 3, label = "Average")

plt.xlabel("Channels")
plt.ylabel("Amplitude [ADC]")
plt.colorbar()
plt.legend(fontsize = 16)
plt.grid()
plt.tight_layout()
plt.savefig(outFolder+"wform_avg_hist2D_ch%i_%s.pdf"%(channel,SiPM_ID))
del(samples, wf_flat_list, samples_flat_list)

# Perform FFT
print("Doing FFT \n")
sampling_rate = 500E6 #Smp/s
sample_length = 1/sampling_rate #s

spectrum_array = []
freq_array = []
for i in range(0,len(wf_array)):
    spectrum_array.append(abs(spectrum(wf_array[i])))
    freq_array.append(frequencies(wf_array[i],sample_length))
spectrum_array = np.array(spectrum_array)

#Plot average FFT
print("Plotting average PSD \n")
plt.figure(figsize=(7,6))
for i in range(0,100):
    plt.plot(frequencies(wf_array[i],sample_length)/1E6,abs(spectrum(wf_array[i])))
plt.plot(frequencies(wf_array[0],sample_length)/1E6,np.mean(spectrum_array, axis=0), c = "black", ls = "-", lw = 3)
plt.xlabel("Freq [MHz]")
plt.yscale('log')
plt.grid()
plt.tight_layout()

plt.savefig(outFolder+"FFT_ch%i_%s.pdf"%(channel,SiPM_ID))

#2D hist

spectrum_flat_list = [item for sublist in spectrum_array for item in sublist]
freq_flat_list = [item for sublist in freq_array for item in sublist]

plt.figure(figsize=(9,6))
plt.hist2d(np.array(freq_flat_list)/1E6, spectrum_flat_list, range = ([0,250],[0,25000]), bins = 100, norm=mpl.colors.LogNorm());
plt.plot(frequencies(wf_array[0],sample_length)/1E6,np.mean(spectrum_array, axis=0), c = "black", ls = "-", lw = 3,)
plt.xlabel("Freq [MHz]")
plt.ylabel("Amplitude [ADC/MHz]")
plt.colorbar()
plt.grid()
plt.tight_layout()

plt.savefig(outFolder+"FFT_avg_hist2D_ch%i_%s.pdf"%(channel,SiPM_ID)) 