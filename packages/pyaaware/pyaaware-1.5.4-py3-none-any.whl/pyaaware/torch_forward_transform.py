from typing import Tuple

import torch


class TorchForwardTransform:
    def __init__(self,
                 N: int = 256,
                 R: int = 64,
                 bin_start: int = 1,
                 bin_end: int = 128,
                 ttype: str = 'stft-olsa-hanns') -> None:
        from pyaaware.transform_types import Overlap
        from pyaaware.transform_types import Window
        from pyaaware.transform_types import window

        self._N = N
        self._R = R
        self._bin_start = bin_start
        self._bin_end = bin_end
        self._ttype = ttype

        if self.N % self.R:
            raise ValueError('R is not a factor of N')

        if self.bin_start >= self.N:
            raise ValueError('bin_start is greater than N')

        if self.bin_end >= self.N:
            raise ValueError('bin_end is greater than N')

        if self.bin_start >= self.bin_end:
            raise ValueError('bin_start is greater than bin_end')

        self._num_overlap = self.N // self.R
        self._overlap_indices = torch.empty((self._num_overlap, self.N), dtype=torch.int)
        for n in range(self._num_overlap):
            start = self.R * (n + 1)
            self._overlap_indices[n, :] = torch.floor(torch.tensor(range(start, start + self.N)) % self.N)

        self._bin_indices = list(range(self.bin_start, self.bin_end + 1))
        self._bins = self.bin_end - self.bin_start + 1

        self._W = None
        self._overlap_type = None
        self._xs = None
        self._overlap_count = None

        if self.ttype == 'stft-olsa-hanns':
            self._W = window(Window.NONE, self.N, self.R)
            self._W = self._W * 2 / self.N
            self._overlap_type = Overlap.OLS
        elif self.ttype == 'stft-ols':
            self._W = window(Window.NONE, self.N, self.R)
            self._W = self._W * 2 / self.N
            self._overlap_type = Overlap.OLS
        elif self.ttype == 'stft-olsa':
            self._W = window(Window.NONE, self.N, self.R)
            self._W = self._W * 2 / self.N
            self._overlap_type = Overlap.OLS
        elif self.ttype == 'stft-olsa-hann':
            self._W = window(Window.HANN, self.N, self.R)
            self._W = self._W * 2 / torch.sum(self._W)
            self._overlap_type = Overlap.OLS
        elif self.ttype == 'stft-olsa-hannd':
            self._W = window(Window.HANN, self.N, self.R)
            self._W = self._W * 2 / torch.sum(self._W)
            self._overlap_type = Overlap.OLS
        elif self.ttype == 'stft-olsa-hammd':
            self._W = window(Window.HAMM, self.N, self.R)
            self._W = self._W * 2 / torch.sum(self._W)
            self._overlap_type = Overlap.OLS
        elif self.ttype == 'stft-ola':
            self._W = window(Window.NONE, self.N, self.R)
            self._W = self._W * 2 / self.N
            self._overlap_type = Overlap.OLA
        elif self.ttype in ('tdac', 'tdac-co'):
            self._R = self.N // 2
            k = torch.arange(0, self._R + 1)
            self._W = torch.exp(-1j * 2 * torch.pi / 8 * (2 * k + 1)) * torch.exp(
                -1j * 2 * torch.pi / (2 * self.N) * k)

            if self.ttype == 'tdac':
                self._overlap_type = Overlap.TDAC
            else:
                self._overlap_type = Overlap.TDAC_CO
        else:
            raise ValueError(f"Unknown ttype: '{self.ttype}'")

        if self._overlap_type not in (Overlap.TDAC, Overlap.TDAC_CO) and len(self._W) != self.N:
            raise RuntimeError('W is not of length N')

        self.reset()

    @property
    def N(self) -> int:
        return self._N

    @property
    def R(self) -> int:
        return self._R

    @property
    def bin_start(self) -> int:
        return self._bin_start

    @property
    def bin_end(self) -> int:
        return self._bin_end

    @property
    def ttype(self) -> str:
        return self._ttype

    @property
    def bins(self) -> int:
        return self._bins

    @property
    def W(self) -> torch.Tensor:
        return self._W

    def reset(self) -> None:
        self._xs = torch.zeros(self.N, dtype=torch.float32)
        self._overlap_count = 0

    def execute_all(self, xt: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        import numpy as np

        if xt.ndim != 2 and xt.ndim != 1:
            raise ValueError('Input must have either 1 or 2 dimensions')

        has_channels = xt.ndim == 2
        samples = xt.shape[0]
        frames = int(np.ceil(samples / self.R))

        if has_channels:
            channels = xt.shape[1]
            xt_pad = torch.nn.functional.pad(input=xt,
                                             pad=(0, frames * self.R - samples, 0, 0),
                                             mode='constant',
                                             value=0)
            yf = torch.empty((self._bins, channels, frames), dtype=torch.complex64)
            energy_t = torch.empty((channels, frames), dtype=torch.float32)
        else:
            channels = 1
            xt_pad = torch.nn.functional.pad(input=xt,
                                             pad=(0, frames * self.R - samples),
                                             mode='constant',
                                             value=0)
            yf = torch.empty((self._bins, frames), dtype=torch.complex64)
            energy_t = torch.empty(frames, dtype=torch.float32)

        for channel in range(channels):
            for frame in range(frames):
                start = frame * self.R
                stop = start + self.R
                if has_channels:
                    yf[:, channel, frame], energy_t[channel, frame] = self.execute(xt_pad[start:stop, channel])
                else:
                    yf[:, frame], energy_t[frame] = self.execute(xt_pad[start:stop])
            self.reset()

        return yf, energy_t

    def execute(self, xt: torch.Tensor) -> Tuple[torch.Tensor, float]:
        import numpy as np

        from pyaaware.transform_types import Overlap

        if xt.ndim != 1 or xt.shape[0] != self.R:
            raise ValueError(f'Input shape must be a vector of length {self.R}')

        if self._overlap_type == Overlap.OLA:
            ytn = self.W * torch.concatenate((xt, torch.zeros(self.N - self.R, dtype=torch.float32)))
            energy_t = torch.mean(torch.square(xt))
            tmp = torch.fft.rfft(ytn)
        elif self._overlap_type == Overlap.OLS:
            self._xs[self._overlap_indices[self._overlap_count, (self.N - self.R):self.N]] = xt
            ytn = self._xs[self._overlap_indices[self._overlap_count, :]]
            energy_t = torch.mean(torch.square(ytn))
            ytn = self.W * ytn
            tmp = torch.fft.rfft(ytn)
            self._overlap_count = (self._overlap_count + 1) % self._num_overlap
        elif self._overlap_type in (Overlap.TDAC, Overlap.TDAC_CO):
            self._xs[self._overlap_indices[self._overlap_count, (self.N - self.R):self.N]] = xt
            ytn = self._xs[self._overlap_indices[self._overlap_count, :]]
            energy_t = torch.mean(torch.square(ytn))
            tmp = np.sqrt(1 / self.N) * torch.fft.rfft(ytn)
            tmp = 1j * self.W[0:self.R] * tmp[0:self.R] + self.W[1:self.R + 1] * tmp[1:self.R + 1]
            if self._overlap_type == Overlap.TDAC_CO:
                tmp = torch.real(tmp)
            self._overlap_count = (self._overlap_count + 1) % self._num_overlap
        else:
            raise ValueError(f"Unsupported overlap type: '{self._overlap_type}")

        xf = tmp[self._bin_indices]
        return xf, float(energy_t)
