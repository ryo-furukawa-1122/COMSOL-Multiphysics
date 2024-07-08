# %%
import general.settings as st
import glob
import matplotlib.pyplot as plt
import numpy as np

def main():
    """Main function"""
    # Settings
    directory, ids = st.Settings().read_config()
    st.Settings().plot_theme()
    PLOT_SHAPE = [2, 5]
    dts = np.arange(0, 2, 0.2)
    P_MAX = 40e3

    for id in ids:
        # Explore csv files in the working directory
        files:list = sorted(glob.glob(f'{directory}/{id}/*.csv'))
        N = len(files)

        # Create subplots
        fig, ax = plt.subplots(*PLOT_SHAPE, figsize=(24, 8), dpi=900)
        plt.subplots_adjust(hspace=0.1, wspace=0.2)
        ax_flat = ax.flatten()

        for i in range(N):
            x, y, z = st.Settings().read_csv(files[i])
            grid_z = st.Settings().generate_grid(x, y, z/P_MAX)

            # Plot
            kwargs = {
                'extent': (x.min(), x.max(), y.min(), y.max()),
                'origin': 'lower',
                'cmap': 'jet',
                'vmin': 0,
                'vmax': 1,
                'aspect': 'equal',
                'interpolation': 'hanning'
            }
            ax_flat[i].imshow(grid_z.T, **kwargs)
            ax_flat[i].set_ylim([0, 10])
            ax_flat[i].set_xlim([-7, 7])
            ax_flat[i].set_title(f'{dts[i]:.1f} \u03bcs')
            if i==5:
                ax_flat[i].set_xlabel('x (mm)')
                ax_flat[i].set_ylabel('z (mm)')
                
        cbar = fig.colorbar(ax_flat[0].images[0], ax=ax_flat, orientation='vertical', pad=0.02)
        cbar.set_label('Acoustic pressure (a.u.)', rotation=270, labelpad=24)
        # plt.show()
        plt.savefig(f'{directory}/{id}/{id}.png', bbox_inches='tight')
        plt.close()


if __name__ == "__main__":
    main()

# %%
