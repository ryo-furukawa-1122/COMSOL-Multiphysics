# %%
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from general import settings as st
from general import loadings as ld
from analysis import analysis as an

directory, ids, scales = ld.Loadings().read_config()
st.Settings().plot_theme()

data = pd.read_csv(f"{directory}/{ids[0]}/focal length/3-1-2_focal_length.csv", skiprows=8, header=None, names=['z', 'p'])

z = data['z'].values
p = data['p'].values

N:int = 10
positions:list[float] = [0 for i in range(N)]
pressures:list[float] = [0 for i in range(N)]
peak_positions:list[float] = [0 for i in range(N)]
peak_pressures:list[float] = [0 for i in range(N)]

dt = np.arange(0, 2, 0.2)

start = np.where(z == 0)[0]
for i in range(N):
    if i==N-1:
        positions[i] = z[start[i]:]
        pressures[i] = p[start[i]:]
    else:
        positions[i] = z[start[i]:start[(i+1)]]
        pressures[i] = p[start[i]:start[(i+1)]]

positions = np.array(positions)
pressures = np.array(pressures)

colors = np.arange(0, 1, 1/N)
cmap = plt.cm.get_cmap('jet')

labels = ['0.0 \u03bcs', '0.2 \u03bcs', '0.4 \u03bcs', '0.6 \u03bcs', '0.8 \u03bcs', '1.0 \u03bcs', '1.2 \u03bcs', '1.4 \u03bcs', '1.6 \u03bcs', '1.8 \u03bcs']

plt.figure(dpi=900)
for i in range(N):
    plt.plot(positions[i], pressures[i]*1e-6, color=cmap(colors[i]), label=labels[i], linewidth=2)

    maxima_x, maxima_y = an.Analysis().find_local_maxima(positions[i], pressures[i]*1e-6)
    peak_positions[i] = maxima_x

    for x, y in zip(maxima_x, maxima_y):
        plt.annotate('', xy=(x, y), xytext=(x, y + 0.1), arrowprops=dict(facecolor="None", shrink=0.05, edgecolor=cmap(colors[i]), linewidth=1.4))

plt.xlabel('z (mm)')
plt.ylabel('Acoustic pressure (MPa)')
plt.xlim([0, 7])
plt.legend(ncol=5, shadow=False, framealpha=0.0, loc='lower center', bbox_to_anchor=(0.5, 1.), fontsize=16, handlelength=1, handletextpad=0.3, columnspacing=0.4)
plt.savefig(f"{directory}/{ids[0]}/focal length/3-1-2_focal_length.png", bbox_inches='tight')
plt.close()

# %%
peak_labels = ["Primary", "Secondary"]
kwargs = {
    "color": "None",
    "markersize": 12,
    "markeredgewidth": 2,
    "marker": "o"
}
colors = ["#1C2938", "#FC5185", "#3FC1C9"]
dt_s = [dt[i] for i in range(len(dt)) if i != 5]
primary = []
secondary = []
for i in range(N):
    primary.append(peak_positions[i][0])
    if len(peak_positions[i]) != 1:
        secondary.append(peak_positions[i][1])
plt.figure(dpi=900)
plt.plot(dt, primary, markeredgecolor=colors[0], label=peak_labels[0], **kwargs)
plt.plot(dt, primary, color=colors[0], linewidth=2, linestyle="dashed")
plt.plot(dt_s, secondary, markeredgecolor=colors[1], label=peak_labels[1], **kwargs)
plt.plot(dt_s, secondary, color=colors[1], linewidth=2, linestyle="dashed")
plt.xlabel("Delay time (\u03bcs)")
plt.ylabel("Focal length (mm)")
plt.legend(shadow=False, framealpha=0.0, loc='lower center', bbox_to_anchor=(0.5, 1.), fontsize=16, ncol=2)
plt.savefig(f"{directory}/{ids[0]}/focal length/3-1-2_focal_length_peak.png", bbox_inches='tight')
plt.close()

# %%
