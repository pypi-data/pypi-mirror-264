import os
import matplotlib.pyplot as plt
import matplotlib
from cartopy import config
import cartopy
import cartopy.crs as ccrs
import drama.utils as drutl
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy.ma as ma
import numpy as np
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from scipy.signal import convolve2d

def guess_cmap(vmin, vmax):
    if vmax < 0:
        cmap = 'bone'
    elif vmin >= 0:
        # Coherence
        cmap = 'inferno'
    elif (vmin == (-vmax)) and (vmax < 1):
        cmap = 'RdBu'
    else:
        cmap = 'hsv'
    return cmap


def txt2txt(txt):
    if type(txt) in (list, tuple):
        #out = ""
        #for t in txt:
        #    out = out + ("%s\n" % t)
        out = "\n".join(txt)
        return out
    elif type(txt) is str:
        return txt
    else:
        return None


def rot_vect(vecd, northing_rad=-np.radians(100)):
    rot = northing_rad + np.pi/2
    rot_m = np.array([[np.cos(rot), np.sin(rot)], [-np.sin(rot), np.cos(rot)]])
    return np.einsum("km,nom->nok", rot_m, vecd)


def geoplot(xrdata, varname, basedata=None, bvarname='SST', sat='S1', pol='M', figsize=(3.25, 10),
            vmin=None, vmax=None, bmin=None, bmax=None, bcmap=None, alpha=1,
            cmap=None,  pproj=ccrs.Mercator(), #pproj=ccrs.UTM(31),
            txt=None, draw_labels=True, db=True, cblabelcolor=None, cblabeltxt='',
            lon_range=None, lat_range=None, ascending=True,
            xlabels_top=False, xlabels_bottom=True, ylabels_left=False, ylabels_right=True):
    """

    :param d:
    :param geo:
    :param figsize: ...
    :param vmin: minimum value shown
    :param vmax: idem
    :param cmap: colormap, if None it chooses soemthing
    :param pproj: map projection used
    :return:
    """

    d = xrdata[varname].values[2:-2]
    if len(d.shape) > 3:
        #print("Selecting %s", sat)
        d = xrdata[varname].sel(sat=sat, pol=pol).values[2:-2]
    if (varname in ["nrcs", "NRCS"]) and db:
        d = 10*np.log10(d)
    # d = ma.masked_invalid(d)
    #print(d.min())
    #print(d.max())
    if vmin is None:
        vmin = np.nanmin(d)
    if vmax is None:
        vmax = np.nanmax(d)
    if cmap is None:
        # guess colormap
        cmap = guess_cmap(vmin, vmax)
    txt = txt2txt(txt)
    fig = plt.figure(figsize=figsize)
    img_extent = [xrdata.longitude.values[2:-2].min(), xrdata.longitude.values[2:-2].max(), xrdata.latitude.values[2:-2].min(), xrdata.latitude.values[2:-2].max()]
    #print(img_extent)
    if lon_range is not None:
        img_extent[0] = lon_range[0]
        img_extent[1] = lon_range[1]
    if lat_range is not None:
        img_extent[2] = lat_range[0]
        img_extent[3] = lat_range[1]
    ax = plt.axes(projection=pproj)
    # ax = plt.subplot(1, 1, 1, projection=ccrs.EuroPP())
    ax.set_extent(img_extent, ccrs.PlateCarree())
    # ax.stock_img()
    gl = ax.gridlines(crs=ccrs.PlateCarree(), color='gray', draw_labels=draw_labels)
    if draw_labels:
        gl.top_labels = xlabels_top
        gl.left_labels = ylabels_left
        gl.bottom_labels = xlabels_bottom
        gl.right_labels = ylabels_right
        #gl.xlocator = mticker.FixedLocator([2.6, 3.1, 3.6, 4.1])
        #gl.ylocator = mticker.FixedLocator([41.5, 42, 42.5, 43])
        gl.xlines = True
        gl.ylines = True
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        gl.xlabel_style = {'size': 12}
        gl.ylabel_style = {'size': 12}
    land_10m = cartopy.feature.NaturalEarthFeature('physical', 'land', '10m',
                                                   edgecolor='face',
                                                   facecolor=cartopy.feature.COLORS['land'])
    sea_10m = cartopy.feature.NaturalEarthFeature('physical', 'ocean', '10m',
                                                  edgecolor='face',
                                                  facecolor=cartopy.feature.COLORS['water'])
    rivers_10m = cartopy.feature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '50m',
                                                     edgecolor='blue',
                                                     facecolor='none')
    ax.add_feature(sea_10m, zorder=1)
    ax.add_feature(land_10m, zorder=2)  # land is specified to plot above ...
    #ax.add_feature(rius_feature, zorder=10)
    if not basedata is None:
        based = basedata[bvarname]
        if bmin is None:
            bmin = np.nanmin(based)
        if bmax is None:
            bmax = np.nanmax(based)
        if bcmap is None:
            # guess colormap
            bcmap = guess_cmap(bmin, bmax)
        bim = ax.pcolormesh(basedata.longitude.values, basedata.latitude.values, based,
                            transform=ccrs.PlateCarree(), zorder=3,
                            vmin=bmin, vmax=bmax, shading='nearest')
        bim.set_cmap(bcmap)


    im = ax.pcolormesh(xrdata.longitude.values[2:-2], xrdata.latitude.values[2:-2], d,
                       transform=ccrs.PlateCarree(), zorder=4,
                       vmin=vmin, vmax=vmax,alpha=alpha, shading='nearest') #, transform=rotated_pole)
    im.set_cmap(cmap)
    #ax.add_feature(rivers_10m, zorder=5)
    #ax.coastlines(resolution='10m', zorder=4)
    if ascending:
        cbaxes = inset_axes(ax, width="7%", height="20%", loc='upper right')
    else:
        cbaxes = inset_axes(ax, width="7%", height="20%", loc='lower right')

    cb = fig.colorbar(im, cax=cbaxes, ticks=[vmin, vmax], orientation='vertical')
    #cb.set_label(cblabeltxt, rotation=0)
    cb.ax.set_xlabel(cblabeltxt, color=cblabelcolor)
    cbaxes.yaxis.tick_left()
    if not cblabelcolor is None:
        cbaxes.tick_params(labelcolor=cblabelcolor)
    # A text box for the title

    # place a text box in upper left in axes coords
    if ascending:
        if txt is not None:
            props = dict(boxstyle='round', facecolor='white', alpha=0.75)
            ax.text(0.05, 0.02, txt, transform=ax.transAxes, fontsize=14,
                    verticalalignment='bottom', bbox=props, zorder=6)
    else:
        if txt is not None:
            props = dict(boxstyle='round', facecolor='white', alpha=0.75)
            ax.text(0.05, 0.98, txt, transform=ax.transAxes, fontsize=14,
                    verticalalignment='top', bbox=props, zorder=6)

def conv2(x, y, mode='same'):
    return np.rot90(convolve2d(np.rot90(x, 2), np.rot90(y, 2), mode=mode), 2)

def geoquiver(xrdata, field, decim=10, basedata=None, bvarname='SST', sat='S1', figsize=(3.25, 10),
              vmin=None, vmax=None, bmin=None, bmax=None, bcmap=None, alpha=1, scale=None,widths=1,
              cmap=None,  pproj=ccrs.Mercator(), #pproj=ccrs.UTM(31),
              txt=None, draw_labels=True, db=True, ascending=True, cblabeltxt='',
              lon_range=None, lat_range=None, base_is_same=False, cblabelcolor=None,
              xlabels_top=False, xlabels_bottom=True, ylabels_left=False, ylabels_right=True):
    """

    :param d:
    :param geo:
    :param figsize: ...
    :param vmin: minimum value shown
    :param vmax: idem
    :param cmap: colormap, if None it chooses soemthing
    :param pproj: map projection used
    :return:
    """
    # FIXME: override this function, it is not clear why it gives NaN's
    d = np.zeros_like(field)
    mask = np.linalg.norm(field, axis=-1) > 0
    field[:, :, 0] = np.where(mask > 0, field[:, :, 0], 0)
    field[:, :, 1] = np.where(mask > 0, field[:, :, 1], 0)
    fmask = drutl.smooth(mask, decim)
    d[:,:,0] = np.where(mask > 0, drutl.smooth(field[:,:,0], decim)/fmask,0)
    d[:,:,1] = np.where(mask > 0, drutl.smooth(field[:,:,1], decim)/fmask,0)
    #dfilt=np.ones((decim,decim))/decim**2
    #d[:, :, 0]=  conv2(field[:,:,0], dfilt)
    #d[:, :, 1] = conv2(field[:,:,1], dfilt)
    d = d[2:-2:decim,::decim, :]

    #d = ma.masked_invalid(d)
    if vmin is None:
        vmin = np.nanmin(d)
    if vmax is None:
        vmax = np.nanmax(d)
    if cmap is None:
        # guess colormap
        cmap = guess_cmap(vmin, vmax)
    txt = txt2txt(txt)
    fig = plt.figure(figsize=figsize)
    img_extent = [xrdata.longitude.values[2:-2].min(), xrdata.longitude.values[2:-2].max(), xrdata.latitude.values[2:-2].min(), xrdata.latitude.values[2:-2].max()]
    #print(img_extent)
    if lon_range is not None:
        img_extent[0] = lon_range[0]
        img_extent[1] = lon_range[1]
    if lat_range is not None:
        img_extent[2] = lat_range[0]
        img_extent[3] = lat_range[1]
    ax = plt.axes(projection=pproj)
    # ax = plt.subplot(1, 1, 1, projection=ccrs.EuroPP())
    ax.set_extent(img_extent, ccrs.PlateCarree())
    # ax.stock_img()
    gl = ax.gridlines(crs=ccrs.PlateCarree(), color='gray', draw_labels=draw_labels)
    if draw_labels:
        gl.top_labels = xlabels_top
        gl.left_labels = ylabels_left
        gl.bottom_labels = xlabels_bottom
        gl.right_labels = ylabels_right
        #gl.xlocator = mticker.FixedLocator([2.6, 3.1, 3.6, 4.1])
        #gl.ylocator = mticker.FixedLocator([41.5, 42, 42.5, 43])
        gl.xlines = True
        gl.ylines = True
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        gl.xlabel_style = {'size': 12}
        gl.ylabel_style = {'size': 12}
    land_10m = cartopy.feature.NaturalEarthFeature('physical', 'land', '10m',
                                                   edgecolor='face',
                                                   facecolor=cartopy.feature.COLORS['land'])
    sea_10m = cartopy.feature.NaturalEarthFeature('physical', 'ocean', '10m',
                                                  edgecolor='face',
                                                  facecolor=cartopy.feature.COLORS['water'])
    rivers_10m = cartopy.feature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '50m',
                                                     edgecolor='blue',
                                                     facecolor='none')
    ax.add_feature(sea_10m, zorder=1)
    ax.add_feature(land_10m, zorder=2)  # land is specified to plot above ...
    #ax.add_feature(rius_feature, zorder=10)
    if not basedata is None:
        based = basedata[bvarname]
        if bmin is None:
            bmin = np.nanmin(based)
        if bmax is None:
            bmax = np.nanmax(based)
        if bcmap is None:
            # guess colormap
            bcmap = guess_cmap(bmin, bmax)
        bim = ax.pcolormesh(basedata.longitude.values, basedata.latitude.values, based,
                            transform=ccrs.PlateCarree(), zorder=3,
                            vmin=bmin, vmax=bmax)
        bim.set_cmap(bcmap)

    cnorm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    strm_wst = ax.quiver(xrdata.longitude.values[2:-2:decim,::decim],
                         xrdata.latitude.values[2:-2:decim,::decim],
                         d[:, :, 0], d[:, :, 1],
                         np.linalg.norm(d, axis=-1),
                         transform=ccrs.PlateCarree(), zorder=4,
                         cmap=cmap, norm=cnorm, scale=scale,linewidths=widths)
    #ax.add_feature(rivers_10m, zorder=5)
    #ax.coastlines(resolution='10m', zorder=4)
    if ascending:
        cbaxes = inset_axes(ax, width="7%", height="20%", loc='upper right')
    else:
        cbaxes = inset_axes(ax, width="7%", height="20%", loc='lower right')
    if base_is_same:
        cb = fig.colorbar(bim, cax=cbaxes, ticks=[bmin, bmax], orientation='vertical')
    else:
        cb = fig.colorbar(strm_wst, cax=cbaxes, ticks=[vmin, vmax], orientation='vertical')
    if not cblabelcolor is None:
        cbaxes.tick_params(labelcolor=cblabelcolor)
    cbaxes.yaxis.tick_left()
    cb.ax.set_xlabel(cblabeltxt, color=cblabelcolor)
    # cb.set_label(cblabeltxt, rotation=0)
    # A text box for the title

    # place a text box in upper left in axes coords
    if ascending:
        if txt is not None:
            props = dict(boxstyle='round', facecolor='white', alpha=0.75)
            ax.text(0.05, 0.02, txt, transform=ax.transAxes, fontsize=14,
                    verticalalignment='bottom', bbox=props, zorder=6)
    else:
        if txt is not None:
            props = dict(boxstyle='round', facecolor='white', alpha=0.75)
            ax.text(0.05, 0.98, txt, transform=ax.transAxes, fontsize=14,
                    verticalalignment='top', bbox=props, zorder=6)

#%%
if __name__ == '__main__':

    import xarray as xr

    import stereoid.sar_performance as strsarperf
    import stereoid.utils.config as st_config
    from stereoid.oceans.read_scenario_California import read_scenario_California

    paths = st_config.parse(section="Paths")
    # Unpack the paths read from user.cfg. If user.cfg is not found user_defaults.cfg is used.
    main_dir = paths["main"]
    datadir = paths["data"]
    pardir = paths["par"]
    resultsdir = paths["results"]
    scn_file = 'California/ocean_lionel.mat'
    fwddir = os.path.join(datadir, "ScatteringModels/Oceans")
    scndir = os.path.join(datadir, "Ocean/Scenarios")
    b_ati = 10
    plotdir = os.path.join(os.path.join(resultsdir, "OceanE2E"), "California")
    plotdir = os.path.join(plotdir, "%4.1f" % b_ati)

#%%
    xrL1 = xr.open_dataset(os.path.join(plotdir,"L1data.nc"))
    xrL2 = xr.open_dataset(os.path.join(plotdir,"L2data.nc"))
#%%
    cali_data, dx = read_scenario_California(os.path.join(scndir, scn_file), smp_out=1e3)
    xrInput = xr.Dataset({"U10s":(("az", "gr"), np.linalg.norm(cali_data["wnd"], axis=-1)),
                          "SST":(("az","gr"), cali_data["sst"]),
                          "lat":(("az","gr"), cali_data["lat"]),
                          "lon":(("az","gr"), cali_data["lon"])})#,
                  #coords={"gr":obsgeo_a.gr[0], "az":az, "sat": ["S1","HA","HB"]})
#%%
    xrL1.latitude.values.min()
    xrL1["NRCS"].sel(sat="S1")
    geoplot(xrInput, "SST", sat='HA', cmap='inferno',bvarname="U10s",vmin=8, vmax=15)
#%%
    geoplot(xrL1, "NRCS", sat='HA', vmin=-20, vmax=-8, cmap='viridis',
            basedata=xrInput, bcmap='inferno', bvarname='SST', alpha=0.5,bmin=8, bmax=15)
#%%
    geoplot(xrL1, "GDC", sat='HA', vmin=-30, vmax=30,cmap='RdBu',
            basedata=xrInput, bcmap='inferno', bvarname='SST', alpha=0.1,bmin=8, bmax=15)
#%%
    U10s = np.stack((xrL2.U10s_x.values, xrL2.estU10s_y.values), axis=-1)
    est_U10s = np.stack((xrL2.estU10s_x.values, xrL2.estU10s_y.values), axis=-1)
    est_TSC = np.stack((xrL2.estTSC_x.values, xrL2.estTSC_y.values), axis=-1)
    TSC = np.stack((xrL2.TSC_x.values, xrL2.TSC_y.values), axis=-1)


    est_U10s = rot_vect(est_U10s, northing_rad=-np.radians(100))
    est_TSC = rot_vect(est_TSC, northing_rad=-np.radians(100))
    TSC = rot_vect(TSC, northing_rad=-np.radians(100))
    U10s = rot_vect(U10s, northing_rad=-np.radians(100))
    # clean a bit TSC
    TSCerr = np.linalg.norm(est_TSC - TSC, axis=-1)
    est_TSC = est_TSC * (TSCerr < 1)[:,:,np.newaxis]
    U10serr = np.linalg.norm(est_U10s - U10s, axis=-1)
    est_U10s = est_U10s * (U10serr < 2)[:,:,np.newaxis]
    est_TSC[-2,-2]
    geoquiver(xrL2, est_TSC, decim=20, vmin=0, vmax=0.5,cmap="viridis_r",figsize=(5, 10),
              basedata=xrInput, bcmap='inferno', bvarname='SST',bmin=8, bmax=15)
    geoquiver(xrL2, TSC, decim=20, vmin=0, vmax=0.5,cmap="viridis_r",figsize=(5, 10),
              basedata=xrInput, bcmap='inferno', bvarname='SST',bmin=8, bmax=15)
#%%
    xrL1.close()
    xrL2.close()
    #%%
    est_TSC[:,:,0].min()
