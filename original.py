from utility import *
import NDE_functions as nde
import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

# parameters for simulation FMC data
# mode = '_PRISTINE'
# mode = '_POINTS'
mode = '_CRACK_TOP'
# mode = '_CRACK_MIDDLE'
# mode = '_CRACK_BOTTOM'

scan_position = 0
#SIMULATE RAW DATA
(fmc_data, time, element_positions) = nde.fn_simulate_data_weld_v5(
    mode,
    scan_position,
    no_elements,
    element_pitch,
    element_width,
    first_element_position,
    centre_frequency)

np.save('fmc/' + mode, fmc_data)
np.save('time', time)
np.save('element_pos', element_positions)
fmc_baseline = np.load('fmc/_PRISTINE_.npy')
fmc_data -= fmc_baseline

#show some raw data
(fig, (ax)) = plt.subplots(1, 1)
ax.imshow(fmc_data[:,0,:], extent=[np.min(time) * 1e6, np.max(time) * 1e6, 1, len(element_positions)], aspect = 'auto')
ax.set_title('Raw data')
ax.set_xlabel('Time ($\mu$s)')
ax.set_ylabel('Element')


# FILTER RAW DATA AND CONVERT TO ANALYTIC SIGNALS
fft_pts = len(time)
dt = time[2] - time[1]
df = 1 / (fft_pts * dt)

spectra = np.fft.fft(fmc_data, n = fft_pts)
spectra = spectra[:, :, 1:np.round(fft_pts / 2).astype(int)]
freq = np.arange(spectra.shape[2]) * df
max_freq = np.max(freq)


filter = nde.fn_hanning_band_pass(freq.shape[0], filter_rise_start / max_freq, filter_rise_end / max_freq, filter_fall_start / max_freq, filter_fall_end / max_freq)


# filter all the signals
filtered_spectra = spectra * filter

# inverse FFT
filtered_signals = np.fft.ifft(filtered_spectra, n = fft_pts) * 2
filtered_signals = filtered_signals[:,:, 0:len(time)] #make sure still same length as original signals (nesc in case calculation of fft_pts has rounded up to next even number)


#TFM IMAGING ALGORITHM
#Define output grid
x = np.arange(grid_lim_x[0], grid_lim_x[1], grid_pixel_size)
z = np.arange(grid_lim_z[0], grid_lim_z[1], grid_pixel_size)
[X, Z] = np.meshgrid(x, z)

# tic
I = 0
for T in range(filtered_signals.shape[0]):
    for R in range(filtered_signals.shape[1]):
        tau = (np.sqrt(np.square(X - element_positions[T]) + np.square(0.06-Z)) +
               np.sqrt(np.square(X - element_positions[R]) + np.square(0.06-Z))) / velocity
        I += np.interp(tau, time, filtered_signals[T, R, :], left = 0, right = 0)

directory_TFM = 'TFM/'
np.save(directory_TFM + mode, I)
# Show the image
db_val = 20 * np.log10(np.abs(I) / np.max(np.abs(I[:,:])))
(fig, (ax)) = plt.subplots(1, 1)
ax.imshow(db_val, extent=[np.min(x) * 1e3, np.max(x) * 1e3, np.max(z) * 1e3, np.min(z) * 1e3])
ax.set_title('Image' + mode)
ax.set_xlabel('x (mm)')
ax.set_ylabel('z (mm)')
ax.images[0].set_clim(-40, 0)
plt.colorbar(ax.images[0])
plt.savefig(directory_TFM + mode + '.png')
plt.show()
