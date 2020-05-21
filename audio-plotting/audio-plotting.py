import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile
import numpy as np
import seaborn as sns
import progressbar

fs, data = wavfile.read('data/audio/20200514-1.wav')

num_data_points = len(data)
data_len_min = len(data)/fs

print('read file with {} data points and a duration of {}s'.format(
    num_data_points, data_len_min))

window_len_seconds = 10
window_len_samples = fs * window_len_seconds


# Extract the first track
track = data.T[0]

num_frequencies = int(window_len_samples/2)
num_windows = int(num_data_points/window_len_samples)

bar = progressbar.ProgressBar(max_value=100)

print('Extracting FFTs for sample windows')
# preallocate to improve performance
fft_data = np.zeros((num_windows, num_frequencies))
for starting_frame in range(num_windows):
    window = track[starting_frame:starting_frame + window_len_samples]

    # FFT
    sample_fft = fft(window)

    # Take only the real part
    sample_fft_real = abs(sample_fft[:int(len(sample_fft)/2)])

    fft_data[starting_frame] = sample_fft_real
    bar.update(100*(starting_frame+1)/num_windows)

k = np.arange(len(sample_fft)/2)
T = window_len_samples/fs  # where fs is the sampling frequency
frqLabel = k/T

sns.heatmap(fft_data, linewidth=0.5)
#plt.plot(frqLabel, sample_fft_real)

plt.show()
