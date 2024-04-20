import numpy as np
import matplotlib.pyplot as plt
import NDT_general as NDT_gen
from utility import *

plt.close('all')


# mode = '_PRISTINE'
# mode = '_PRISTINE_NO_NOISE'
# mode = '_POINTS'
# mode = '_CRACK_TOP'
# mode = '_CRACK_MIDDLE'
mode = '_CRACK_BOTTOM'

fmc_data = np.load('fmc/' + mode + '_.npy')
fmc_baseline = np.load('fmc/_PRISTINE_.npy')
fmc_data -= fmc_baseline
time = np.load('time.npy')
element_positions = np.load('element_pos.npy')



def fft_real_signal(s, pts, f_s):
    fft_pts = len(time) + len(time) % 2
    f_step = f_s / fft_pts
    f_vector = np.arange(fft_pts/2) * f_step
    spectrum = np.fft.fft(s, n=pts)

    return f_vector, np.split(spectrum, 2, axis=-1)[0]


fft_pts = len(time) + len(time) % 2
f_s = 1/(time[1]-time[0])
f, spectra = fft_real_signal(fmc_data, fft_pts, f_s)
filter_rise_start = 0.5 * centre_freq
filter_rise_end = 0.75 * centre_freq
filter_fall_start = 1.25 * centre_freq
filter_fall_end = 1.5 * centre_freq


hann_bpf = NDT_gen.fn_hanning_band_pass(int(fft_pts/2),
                                        start_rise_fract = filter_rise_start / np.max(f),
                                        end_rise_fract = filter_rise_end / np.max(f),
                                        start_fall_fract = filter_fall_start / np.max(f),
                                        end_fall_fract= filter_fall_end / np.max(f))




plt.figure()
plt.plot(f*1e-6, np.abs(spectra[0,0,:]))
plt.plot(f*1e-6, hann_bpf*np.max(np.abs(spectra[0,0,:])))
plt.xlabel('Frequency (MHz)', fontsize=font_size)
plt.ylabel('Magnitude', fontsize=font_size)
plt.title('Hanning Bandpass filter', fontsize=font_size)
plt.savefig('fmc/'+mode+'_filtered.png')
plt.show()

spectra_filtered = np.multiply(spectra, hann_bpf)

fmc_data_filtered = np.real(np.fft.ifft(spectra_filtered, fft_pts)*2)
np.save('fmc/'+ mode +'_filtered.npy', fmc_data_filtered)


