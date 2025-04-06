# %%
import general.loadings as ld
import general.settings as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from rich import print
from rich.console import Console

def _mask_nan_zero(array):
    """
    Returns a masked array where NaN values are replaced with 0.
    """
    mask = np.isnan(array)
    masked_array = np.where(mask, 0, array)
    return masked_array

def idx_nearest(focal_points:float, value:float):
    """
    Returns the index of the nearest value in the array to the given value.
    """
    array = np.array(focal_points)
    valid_mask = ~np.isnan(array)
    valid_array = array[valid_mask]
    idx = (np.abs(valid_array - value)).argmin()
    # print(idx)
    return idx

def get_half_width(row):
    file_name:str = f"{directory}/PMUT3-1-2/3-1-2_{row.dt:.1f}us.csv"

    x, y, z = ld.Loadings().read_csv(file_name)
    grid_z = st.Settings().generate_grid(x, y, z).T

    M:int = grid_z.shape[0]  # x
    N:int = grid_z.shape[1]  # y
    RESOLUTION_X:float = (x.max() - x.min()) / M
    RESOLUTION_Y:float = (y.max() - y.min()) / N

    # Get the focal point
    # y_peak_id = idx_nearest(grid_z[:, int(N/2)], row.z_focus)
    y_peak_id = int(row.z_focus / RESOLUTION_Y)
    print(f"y_peak_id is {y_peak_id}")

    row_data = _mask_nan_zero(grid_z[y_peak_id, :])

    max_value = row_data[int(M/2)]
    print(f"max_value is {max_value}")
    half_max = max_value / 2
    print(f"half_max is {half_max}")

    left_idx = int(M/2)
    while row_data[left_idx] >= half_max:
        left_idx -= 1

    print(f"left_idx is {left_idx}")

    right_idx = int(M/2)
    while row_data[right_idx] >= half_max:
        right_idx += 1

    print(f"right_idx is {right_idx}")

    half_width_elements = right_idx - left_idx

    half_width_distance = half_width_elements * RESOLUTION_X

    return half_width_distance, row_data, RESOLUTION_X, left_idx, right_idx, half_max

peak_labels = ["Primary", "Secondary"]
kwargs = {
    "color": "None",
    "markersize": 12,
    "markeredgewidth": 2,
    "marker": "o"
}
colors = ["#1C2938", "#FC5185", "#3FC1C9"]

console = Console()

directory, _, _ = ld.Loadings().read_config()
st.Settings().plot_theme()

file_name_focal_primary:str = f"{directory}/PMUT3-1-2/focal length/focal_length_primary.csv"
file_name_focal_secondary:str = f"{directory}/PMUT3-1-2/focal length/focal_length_secondary.csv"

# %%
focal_primary = pd.read_csv(file_name_focal_primary, skiprows=1, header=None, names=["dt", "z_focus"])
focal_secondary = pd.read_csv(file_name_focal_secondary, skiprows=1, header=None, names=["dt", "z_focus"])

# %%
half_width_list_primary = []
print("[blue bold]Primary peak[/blue bold]")

plt.figure(dpi=900)
for row in focal_primary.itertuples():
    with console.status("[bold magenta]Processing...[/bold magenta]") as status:
        if row.dt == 0.0:
            half_width, p, res, left_idx, right_idx, half = get_half_width(row)
        else:
            half_width, _, _, _, _, _ = get_half_width(row)
        half_width_list_primary.append(half_width)

x = np.arange(0, len(p)) * res
x -= x[int(len(p)/2)]  # Center the x-axis
plt.plot(x, p, color=colors[0], linewidth=2, label=peak_labels[0])
plt.plot([x[left_idx], x[right_idx]], [half, half], color=colors[0], linewidth=2, linestyle="dotted")

half_width_list_secondary = []
print("[blue bold]Secondary peak[/blue bold]")
for row in focal_secondary.itertuples():
    with console.status("[bold magenta]Processing...[/bold magenta]") as status:
        if row.dt == 0.0:
            half_width, p, res, left_idx, right_idx, half = get_half_width(row)
        else:
            half_width, _, _, _, _, _ = get_half_width(row)
        half_width_list_secondary.append(half_width)

plt.plot(x, p, color=colors[1], linewidth=2, label=peak_labels[1])
plt.plot([x[left_idx], x[right_idx]], [half, half], color=colors[1], linewidth=2, linestyle="dotted")

plt.xlabel("x (mm)")
plt.ylabel("Acoustic pressure (kPa)")
plt.xticks(np.arange(-5, 6, 2))

plt.legend(shadow=False, framealpha=0.0, loc='lower center', bbox_to_anchor=(0.5, 1.), fontsize=16, ncol=2)

plt.savefig(f"{directory}/PMUT3-1-2/focal length/half_width_schematic.png", bbox_inches='tight')
plt.close()

# %%
plt.figure(dpi=900)

plt.plot(focal_primary["dt"], half_width_list_primary, label=peak_labels[0], markeredgecolor=colors[0], **kwargs)
plt.plot(focal_primary["dt"], half_width_list_primary, color=colors[0], linewidth=2, linestyle="dashed")

plt.plot(focal_secondary["dt"], half_width_list_secondary, label=peak_labels[1], markeredgecolor=colors[1], **kwargs)
plt.plot(focal_secondary["dt"], half_width_list_secondary, color=colors[1], linewidth=2, linestyle="dashed")

plt.xlabel("Delay time (\u03bcs)")
plt.ylabel("Half width (mm)")
plt.yticks(np.arange(2, 14, 2))

plt.legend(shadow=False, framealpha=0.0, loc='lower center', bbox_to_anchor=(0.5, 1.), fontsize=16, ncol=2)

plt.savefig(f"{directory}/PMUT3-1-2/focal length/half_width.png", bbox_inches='tight')

plt.close()
# %%
