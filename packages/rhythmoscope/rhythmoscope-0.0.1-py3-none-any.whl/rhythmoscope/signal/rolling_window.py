class WindowedSignal:
    """
    A generator which yield portions of a signal of length `window_size` seconds and with a hop length of 
    `hop_size` seconds

    Args:
        signal (array like): The values of the signal
        fs (int): The sampling frequency of the signal
        window_size (float, optional): The length of the output windows in seconds. Defaults to 5.
        hop_size (float, optional): The offset (in seconds) between two successives windows. 
                                  Defaults to 2
    """
    def __init__(self, sr, signal, window_size=5, hop_size=2) -> None:
        self.signal = signal
        self.fs = sr
        self.window_size = int(window_size * sr)
        self.hop_size = int(hop_size * sr)
        self.n_windows = (len(signal) - self.window_size) // self.hop_size + 1

    def __iter__(self):
        for i in range(0, len(self.signal) - self.window_size + 1, self.hop_size):
            yield i / self.fs, (i+self.window_size) / self.fs, self.signal[i: i+self.window_size]