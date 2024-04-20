import numpy as np
import matplotlib.pyplot as plt
from utility import *


#details for displaying image
db_range_for_output = 30

# mode = '_PRISTINE'
# mode = '_POINTS'
# mode = '_CRACK_TOP'
# mode = '_CRACK_MIDDLE'
mode = '_CRACK_BOTTOM'

intensity_TFM_abs = np.abs(np.load('TFM/' + 'TFM'+ mode + '.npy'))

# convert to dB 20*log_10(I/I_max)
I_TFM_dB = 20 * np.log10(intensity_TFM_abs
                         / np.max(np.abs(intensity_TFM_abs)))


plt.figure()
fig, ax1 = plt.subplots(ncols=1, figsize=(14,10))
ax1_plot = ax1.imshow(I_TFM_dB, vmin=-db_range_for_output, vmax=0,
           extent=[np.min(x) * 1e3, np.max(x) * 1e3, np.max(y) * 1e3, np.min(y) * 1e3],
           aspect = 'auto')
ax1.set_xlabel('x (mm)', fontsize=font_size)
ax1.set_ylabel('z (mm)', fontsize=font_size)
ax1.set_title('Imaging of TFM',fontsize=font_size)
ax1.tick_params(axis='both', which='major', labelsize=label_size)

cbar_1 = plt.colorbar(ax1_plot,ax=ax1)
cbar_1.ax.tick_params(labelsize=label_size)


directory_TFM = 'TFM/'
plt.savefig(directory_TFM + 'TFM' + mode + '.png')
plt.show()