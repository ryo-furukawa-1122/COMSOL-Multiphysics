import numpy as np
import matplotlib.pyplot as plt

class Analysis():
    def get_maximum(self, x:list, y:list, z:list, x_min:float, x_max:float, y_min:float, y_max:float):
        """Return the maximum value of z"""
        self.x = x
        self.y = y
        self.z = z
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

        mask = (self.x >= self.x_min) & (self.x <= self.x_max) & (self.y >= self.y_min) & (self.y <= self.y_max)
        z_peak = np.max(self.z[mask])
        y_peak = self.y[mask][np.argmax(self.z[mask])]
        return z_peak, y_peak
    
    def find_local_maxima(self, x, y):
        """Find local maxima"""
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(y, distance=1, prominence=0.1)
        return x[peaks], y[peaks]
    
    def plot_peak_and_dt(self, peak_pressures:np.ndarray[float], peak_positions:np.ndarray[float], dts:np.ndarray[float], directory:str):
        """Plot the peak value and dt"""
        self.peak_pressures = peak_pressures
        self.peak_positions = peak_positions
        self.dts = dts
        self.directory = directory

        colors = ["#1C2938", "#FC5185", "#3FC1C9"]
        kwargs1 = {
            "linestyle": "solid",
            "linewidth": 2
        }
        kwargs2 = {
            "marker": "o",
            "color": "None",
            "markersize": 12,
            "markeredgewidth": 2
        }
        
        plt.figure(dpi=900)
        for j in range(3):
            plt.plot(self.dts, self.peak_pressures[j, :], color=colors[j], **kwargs1)
            plt.plot(self.dts, self.peak_pressures[j, :], markeredgecolor=colors[j], **kwargs2)
        plt.xlabel(" (\u03bcs)")
        plt.ylabel("Acoustic pressure (kPa)")
        plt.savefig(f"{self.directory}/peak_pressure.png", bbox_inches="tight")
        plt.close()

        plt.figure(dpi=900)
        for j in range(3):
            plt.plot(self.dts, self.peak_positions[j, :], color=colors[j], **kwargs1)
            plt.plot(self.dts, self.peak_positions[j, :], markeredgecolor=colors[j], **kwargs2)
        plt.xlabel(" (\u03bcs)")
        plt.ylabel("Focal length (mm)")
        plt.savefig(f"{self.directory}/focal_length.png", bbox_inches="tight")
        plt.close()