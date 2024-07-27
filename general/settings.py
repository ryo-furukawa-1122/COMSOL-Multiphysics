import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata

class Settings():    
    def plot_theme(self):
        """Set the plot theme"""
        plt.rcParams['font.family'] = 'Arial'
        plt.rcParams['font.size'] = 24
        plt.rcParams['axes.linewidth'] = 1.4

    def generate_grid(self, x:list, y:list, z:list, partition:int = 1000):
        """Generate grid points and retuen interporated z values"""
        self.x = x
        self.y = y
        self.partition = partition
        grid_x, grid_y = np.mgrid[x.min():x.max():partition*1j, y.min():y.max():partition*1j]
        grid_z = griddata((x, y), z, (grid_x, grid_y), method='cubic')
        return grid_z
    
    def set_xylabels(self, axis:object):
        """Set labels"""
        self.axis = axis
        self.axis.set_xlabel('x (mm)')
        self.axis.set_ylabel('z (mm)')

    def heatmap_parameters(self, x:list, y:list, p_max:float):
        """Return parameters for heatmap"""
        self.x = x
        self.y = y
        self.p_max = p_max
        kwargs = {
            'extent': (self.x.min(), self.x.max(), self.y.min(), self.y.max()),
            'origin': 'lower',
            'cmap': 'jet',
            'vmin': 0,
            'vmax': p_max*1e-3,  # in kPa
            'aspect': 'equal',
            'interpolation': 'hanning'
        }
        return kwargs


