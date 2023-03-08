import os
import xarray as xr
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 6})
import numpy as np
from colorbar_sat import make_cmap


def path_ready(dir_path):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)    

    
def main(TCid):
    #%%-------------
    def subplot_IR(xx, yy, data, i, j):
        cf = axs[i,j].contourf(xx, yy, data,
                               levels = range(180,291,2),
                               cmap = make_cmap('clist_IR'), 
                               extend = 'both')
        axs[i,j].set_title('IR')
        fig.colorbar(cf, ax=axs[i,j], ticks=[180,190,210,230,260,290])

    def subplot_WV(xx, yy, data, i, j):
        cf = axs[i,j].contourf(xx, yy, data,
                               levels=range(180,261,2),
                               cmap='PuOr',
                               extend='both')
        axs[i,j].set_title('WV')
        fig.colorbar(cf, ax=axs[i,j], ticks=range(180,271,20))


    def subplot_PMW(xx, yy, data, i, j):
        cf = axs[i,j].contourf(xx, yy, data,
                               levels=range(160,261,2), 
                               cmap=make_cmap('clist_PMW').reversed(),
                               extend = 'min')
        axs[i,j].set_title('PMW')
        fig.colorbar(cf, ax=axs[i,j], ticks=range(160,261,20))
    #%% ------------------

    TC_ncs = sorted(os.listdir(f'/wk171/ccl/data/1_WP/{TCid}/'))
    fig_path = f'/wk171/ccl/data/1_WP/Fig/{TCid}'
    path_ready(fig_path)
    
    p0, p1 = 52, 148
    
    for TC_nc in TC_ncs:
        fig_name = f'{fig_path}/{TC_nc[8:18]}.png'
        if os.path.exists(fig_name):
            continue

        print(TC_nc[:-3])
        # load data
        fn = f'/wk171/ccl/data/1_WP/{TCid}/{TC_nc}'
        with xr.open_dataset(fn) as ds:
            IR = ds['IR'].values[p0:p1,p0:p1]
            WV = ds['WV'].values[p0:p1,p0:p1]
            PMW_f = ds['PMW85_f'].values[p0:p1,p0:p1]
            lons = ds['lon'].values[p0:p1]
            lats = ds['lat'].values[p0:p1]
            attrs = ds.attrs
        
        # plot
        xx, yy = np.meshgrid(lons,lats)
        fig, axs = plt.subplots(2,2, figsize=(5, 5), gridspec_kw={'hspace': .3, 'wspace': .3}) 
        subplot_IR(xx, yy, IR, 0,0)
        subplot_WV(xx, yy, WV, 0,1)
        subplot_PMW(xx, yy, PMW_f, 1,0)
        # text
        axs[1,1].axis('off')
        axs[1,1].axis([0, 1.2, 0, 1.2])
        axs[1,1].text(0.1, 1.0, f'TCid : {TCid}')
        t = attrs['datetime']
        axs[1,1].text(0.1, 0.8, f'time : {t[:4]}/{t[4:6]}/{t[6:8]} {t[8:]}Z')
        axs[1,1].text(0.1, 0.6, f'TC_lon : {attrs["TC_lon"]}')
        axs[1,1].text(0.1, 0.4, f'TC_lat : {attrs["TC_lat"]}')
        axs[1,1].text(0.1, 0.2, f'Vmax: {attrs["Vmax"]} (kt)')
        
        
        # all axs setting
        for i in range(2):
            for j in range(2):
                if i+j <2:
                    axs[i,j].set_aspect('equal', adjustable='box')
                    axs[i,j].axhline(y=(lats[0]+lats[-1])/2, color='gray', lw=1)
                    axs[i,j].axvline(x=(lons[0]+lons[-1])/2, color='gray', lw=1)
        plt.savefig(f'{fig_name}', dpi=200)
        plt.close()
        

if __name__ == '__main__':
    TCids = ['200410W','200505W', '200807W', '200909W','201505W','201602W','201910W','202011W']
    for TCid in TCids:
        main(TCid)
