# %%
import general.settings as st
import general.loadings as ld
import glob
import matplotlib.pyplot as plt
import numpy as np
from rich.console import Console
from time import sleep
import analysis.analysis as an

def main():
    """Main function"""
    # Settings
    directory, ids, scales = ld.Loadings().read_config()
    st.Settings().plot_theme()
    PLOT_SHAPE = [2, 5]
    dts = np.arange(0, 2, 0.2)
    peak_pressures = np.zeros([len(ids), len(dts)])
    peak_positions = np.zeros([len(ids), len(dts)])
    console = Console()
    X_MIN, X_MAX = -7, 7
    Y_MIN, Y_MAX = 0, 10
    j = 0

    for id, scale in zip(ids, scales):
        ld.Loadings().log(id)
        # Explore csv files in the working directory
        files:list = sorted(glob.glob(f'{directory}/{id}/*.csv'))
        N:int = len(files)
        p_max:float = scale  # For nomalization

        # Create subplots
        fig, ax = plt.subplots(*PLOT_SHAPE, figsize=(24, 8), dpi=900)
        plt.subplots_adjust(hspace=0.1, wspace=0.2)
        ax_flat = ax.flatten()

        with console.status("[bold magenta]Processing...[/bold magenta]") as status:
            for i in range(N):
                sleep(1)
                # Read csv file
                x, y, z = ld.Loadings().read_csv(files[i])
                grid_z = st.Settings().generate_grid(x, y, z)

                kwargs = st.Settings().heatmap_parameters(x, y, p_max)
                # Plot heatmap
                ax_flat[i].imshow(grid_z.T, **kwargs)
                ax_flat[i].set_ylim([Y_MIN, Y_MAX])
                ax_flat[i].set_xlim([X_MIN, X_MAX])
                ax_flat[i].set_title(f'{dts[i]:.1f} \u03bcs')

                if i==5:
                    st.Settings().set_xylabels(ax_flat[i])

                peak_pressures[j, i], peak_positions[j, i] = an.Analysis().get_maximum(
                    x = x, 
                    y = y, 
                    z = z, 
                    x_min = X_MIN, 
                    x_max = X_MAX, 
                    y_min = Y_MIN, 
                    y_max = Y_MAX
                    )

                console.log(f'[magenta] Processed: {dts[i]:.1f} \u03bcs  [/magenta]')
            
            j += 1

            cbar = fig.colorbar(ax_flat[0].images[0], ax=ax_flat, orientation='vertical', pad=0.02)
            cbar.set_label('Acoustic pressure (kPa)', rotation=270, labelpad=24)
            plt.savefig(f'{directory}/{id}/{id}.png', bbox_inches='tight')
            plt.close()

    console.log(f'[bold green]Summarize[/bold green]')
    an.Analysis().plot_peak_and_dt(peak_pressures, peak_positions, dts, directory)

if __name__ == "__main__":
    main()

# %%
