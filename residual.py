from utility import *
import NDE_functions as nde
import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

# parameters for simulation FMC data
# mode = '_PRISTINE'
# mode = '_POINTS'
# mode = '_CRACK_TOP'
# mode = '_CRACK_MIDDLE'
mode = 'ho21481'
scan_step = 5e-3
scan_width = 0.3
scan_positions = np.linspace(0, scan_width, int(scan_width/scan_step) +1)

for i, scan_position in enumerate(scan_positions):
    print(f'scan position: {i} / {int(scan_width/scan_step)}')
    #SIMULATE RAW DATA
    (fmc_data, time, element_positions) = nde.fn_simulate_data_weld_v5(
        mode,
        scan_position,
        no_elements,
        element_pitch,
        element_width,
        first_element_position,
        centre_frequency)

    np.save('fmc/' + mode + '_.npy', fmc_data)
    np.save('time', time)
    np.save('element_pos', element_positions)


    fmc_baseline = np.load('fmc/_PRISTINE_.npy')

    # FILTER RAW DATA AND CONVERT TO ANALYTIC SIGNALS
    fft_pts = len(time)
    dt = time[2] - time[1]
    df = 1 / (fft_pts * dt)

    spectra = np.fft.fft(fmc_data, n=fft_pts)
    spectra = spectra[:, :, 1:np.round(fft_pts / 2).astype(int)]
    freq = np.arange(spectra.shape[2]) * df
    max_freq = np.max(freq)
    filter = nde.fn_hanning_band_pass(freq.shape[0], filter_rise_start / max_freq, filter_rise_end / max_freq,
                                      filter_fall_start / max_freq, filter_fall_end / max_freq)

    # filter all the signals
    filtered_spectra = spectra * filter

    # inverse FFT
    filtered_signals = np.fft.ifft(filtered_spectra, n = fft_pts) * 2
    filtered_signals = filtered_signals[:,:, 0:len(time)] #make sure still same length as original signals (nesc in case calculation of fft_pts has rounded up to next even number)

    # tic
    I = 0
    for T in range(filtered_signals.shape[0]):
        for R in range(filtered_signals.shape[1]):
            tau = (np.sqrt(np.square(X - element_positions[T]) + np.square(0.06-Z)) +
                   np.sqrt(np.square(X - element_positions[R]) + np.square(0.06-Z))) / velocity
            I += np.interp(tau, time, filtered_signals[T, R, :], left = 0, right = 0)

    directory_TFM = 'TFM/pos/'
    np.save(directory_TFM + f'TFM_pos_{scan_position}', I)

    # Show the image
    db_val = 20 * np.log10(np.abs(I) / np.max(np.abs(I[:])))
    (fig, (ax)) = plt.subplots(1, 1)
    ax.imshow(db_val, extent=[np.min(x) * 1e3, np.max(x) * 1e3, np.max(z) * 1e3, np.min(z) * 1e3])
    ax.set_title('Image')
    ax.set_xlabel('x (mm)')
    ax.set_ylabel('z (mm)')
    ax.images[0].set_clim(-40, 0)
    plt.colorbar(ax.images[0])
    plt.savefig(directory_TFM + f'TFM_pos_{scan_position}''.png')
    plt.close('all')

