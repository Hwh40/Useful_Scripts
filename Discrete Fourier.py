import numpy as np
import matplotlib.pyplot as plt

dt = 0.1
mu = 0 
sigma = 0.1

xs = np.arange(0, 10, dt)

def signal(xs):
    ys = np.sin(2*np.pi*xs) + np.random.normal(mu, sigma, len(xs))
    return ys

def spectrum(x, fs, oversample, is_hamming):

    N = len(x)

    if is_hamming:
        w = np.hamming(N)
        g = x * w
    else:
        g = x
    
    y = np.zeros(N * oversample)
    y[0:N] = g
    Y = np.fft.rfft(y)
    f = np.fft.rfftfreq(N * oversample, 1 / fs)

    print(f'{N} Samples')
    print(f'Nyquist frequency = {fs / 2} Hz')
    print(f'Max frequency = {fs} Hz')
    print(f'Frequency resolution = {fs / (N * oversample)} Hz')
    return Y,f 

def plot(fourier, freq):
    f, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey = True)
    f.suptitle('Fourier Analysis')
    axes = [ax1, ax2, ax3]
    for ax in axes:
        ax.grid(True)
        ax.set_xlim([0,0.5/dt])
        ax.set_xlabel('Frequency [Hz]')
    ax1.set_ylabel('Magnitude')
    ax2.set_ylabel('Real')
    ax3.set_ylabel('Imaginary')
    ax1.plot(freq, abs(fourier),'r')
    ax2.plot(freq, fourier.real,'g')
    ax3.plot(freq, fourier.imag,'b')    

def main():
    ys = signal(xs)
    fourier, freq = (spectrum(ys, 1/dt, 10, is_hamming = False))
    plot(fourier,freq)
    
if __name__ == '__main__':
    main()
    plt.show()