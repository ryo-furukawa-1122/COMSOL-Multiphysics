import json
import pandas as pd
from rich import print

class Loadings():
    def __init__(self):
        self.directory: str
        self.ids: list[str]
        self.scales: list[float]

    def read_config(self):
        """Return the path of working directory, ids, and scales of the devices"""
        f = open('config.json')
        config = json.load(f)
        self.directory = config['directory']
        self.ids = config['ids']
        self.scales = config['scales']
        return self.directory, self.ids, self.scales
    
    def read_csv(self, file:str):
        """Read csv file and return x, y, z"""
        data = pd.read_csv(file, skiprows=8, header=None, names=['x', 'y', 'value'])
        x = data['x'].values
        y = data['y'].values - 0.54
        z = data['value'].values * 1e-3  # in kPa
        return x, y, z
    
    def log(self, id:str):
        """Log message"""
        self.id = id
        print(f"[bold cyan]{id}[/bold cyan]")