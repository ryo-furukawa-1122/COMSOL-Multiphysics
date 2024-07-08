import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata
import pandas as pd

class Settings():
    def __init__(self):
        self.directory: str
        self.ids: list

    def read_config(self):
        """Return the path of working directory and ids of the devices"""
        f = open('config.json')
        config = json.load(f)
        self.directory = config['directory']
        self.ids = config['ids']
        return self.directory, self.ids
    
    def plot_theme(self):
        """Set the plot theme"""
        plt.rcParams['font.family'] = 'Arial'
        plt.rcParams['font.size'] = 24
        plt.rcParams['axes.linewidth'] = 1.4
    
    def read_csv(self, file:str):
        """Read csv file and return x, y, z"""
        data = pd.read_csv(file, skiprows=8, header=None, names=['x', 'y', 'value'])
        x = data['x'].values
        y = data['y'].values - 0.54
        z = data['value'].values
        return x, y, z

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

    def heatmap_parameters(self, x:list, y:list):
        """Return parameters for heatmap"""
        self.x = x
        self.y = y
        kwargs = {
            'extent': (self.x.min(), self.x.max(), self.y.min(), self.y.max()),
            'origin': 'lower',
            'cmap': 'jet',
            'vmin': 0,
            'vmax': 1,
            'aspect': 'equal',
            'interpolation': 'hanning'
        }
        return kwargs


