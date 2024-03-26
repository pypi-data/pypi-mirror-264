# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 17:52:15 2014

@author: lope_fr
"""

from __future__ import absolute_import, division, print_function
import numpy as np
import matplotlib
import pandas as pd
import os
from matplotlib import pyplot as plt
from matplotlib import patches as ptch
from scipy.io.idl import readsav


def mode_dictionary():
    modes = {1: ("IWS1", True, 'darkorange'),
             2: ("IWS2", True, 'darkgreen'),
             3: ("IWS3", True, 'maroon'),
             4: ("IWS1-s", False, 'brown'),
             5: ("IWS2-s", False, 'maroon'),
             6: ("IWS3-s", False, 'aqua'),
             0: ("idle", False, 'lightgray')}
    return modes


def mode_rates():
    rates_1x4 = {"IWS1": 300.3, "IWS2": 253, "IWS3": 253,
                 "IWS1-s": 951.0, "IWS2-s": 2 * 951.0, "IWS3-s": 1963.5,
                 "E1": 410.4, "E2": 2 * 410.4, "E4": 742.8,
                 "idle": 0}
    rates_2x3 = {"IWS1": 450.3, "IWS2": 380, "IWS3": 380,
                 "IWS1-s": 951.0, "IWS2-s": 2 * 951.0, "IWS3-s": 1963.5,
                 "E1": 410.4, "E2": 2 * 410.4, "E4": 742.8,
                 "idle": 0}
    rates_2x3_opt = {"IWS1": 160.3, "IWS2": 173, "IWS3": 133,
                     "IWS1-s": 951.0, "IWS2-s": 2 * 951.0, "IWS3-s": 1963.5,
                     "E1": 410.4, "E2": 2 * 410.4, "E4": 742.8,
                     "idle": 0}
    rates_1x4_opt = {"IWS1": 105.3, "IWS2": 115, "IWS3": 88,
                     "IWS1-s": 951.0, "IWS2-s": 2 * 951.0, "IWS3-s": 1963.5,
                     "E1": 410.4, "E2": 2 * 410.4, "E4": 742.8,
                     "idle": 0}
    rates_2x4_opt = {"IWS1": 210.3, "IWS2": 231, "IWS3": 178,
                     "IWS1-s": 951.0, "IWS2-s": 2 * 951.0, "IWS3-s": 1963.5,
                     "E1": 410.4, "E2": 2 * 410.4, "E4": 742.8,
                     "idle": 0}
    # 1 channel with 4x2 bits, and the other with 3x2
    rates_2x4b_opt = {"IWS1": 210.3, "IWS2": 202, "IWS3": 178,
                      "IWS1-s": 951.0, "IWS2-s": 2 * 951.0, "IWS3-s": 1963.5,
                      "E1": 410.4, "E2": 2 * 410.4, "E4": 742.8,
                      "idle": 0}
    return rates_2x4_opt



def global_act_profile(mod_s1):
    """Takes activation profile and generates graphic report
    """
    s1_count = np.bincount(mod_s1)
    act_modes = np.nonzero(s1_count)[0]
    #s1_mod_count = zip(act_modes, s1_count[act_modes])
    s1_count = s1_count[act_modes]
    labels = []
    colors = []
    rates = []
    m_dict = mode_dictionary()
    m_rates = mode_rates()
    for mode in act_modes:
        m_tag = m_dict[mode][0]
        rate = m_rates[m_dict[mode][0]]
        if m_dict[mode][1]:
            m_tag = m_tag + " (bist)"
            rate = 2 * rate
        labels.append(m_tag)
        colors.append(m_dict[mode][2])
        rates.append(rate)
    pct_count = 100. * s1_count / np.sum(s1_count)
    rel_data_vol = s1_count * np.array(rates)
    rel_data_vol = 100 * rel_data_vol / np.sum(rel_data_vol)
    #plt.ioff()
    plt.figure()
    plt.pie(pct_count, labels=labels, shadow=True,  autopct='%1.1f%%',
            colors=colors, startangle=10)
    plt.axis('equal')
    plt.title('Mode duty cycle')
    plt.show()
    plt.figure()
    plt.pie(rel_data_vol, labels=labels, shadow=True,  autopct='%1.1f%%',
            colors=colors, startangle=10)
    plt.axis('equal')
    plt.title('Relative data volumes')
    #plt.show()
    #plt.ion()


def activation_temp_prof(Plans_, time_step_, interval, title="Duty Cycle",
                         figsize=(10, 5), trange=None, xls_export=False,
                         savepath=None, make_figures=True,
                         plan_names=(),
                         trgcolors=('purple', 'green', 'firebrick')):
    """ Function to compute duty cycles averaged over given interval
    """
    # If we are setting a savedir, make sure it exists
    if not (savepath is None):
        if not os.path.exists(savepath):
            os.makedirs(savepath)
    if type(Plans_) is tuple:
        Plans = Plans_
    else:
        Plans = (Plans_,)
    mod_ = Plans[0].mode
    if type(plan_names) is not tuple:
        plan_names = (plan_names,)
    if len(plan_names) == len(Plans):
        trig_plot = True
        actrigger_ = Plans[0].inMask * 1
    for ipl in range(1, len(Plans)):
        mod_ = np.where(mod_ == 0, Plans[ipl].mode, mod_)
        if len(plan_names) == len(Plans):
            actrigger_ = np.where(actrigger_ == 0,
                                  Plans[ipl].inMask * (1 + ipl),
                                  actrigger_)
    mod_s1 = mod_.flatten()
    if len(plan_names) == len(Plans):
        actrigger = actrigger_.flatten()

    time_step = 12 * 24 * 3600 / (mod_.shape[1] * mod_.shape[2])
    n_samp = mod_s1.size
    samp_cyc = np.int(interval / time_step)
    num_cyc = np.floor(n_samp / samp_cyc)
    t0_cyc = np.arange(num_cyc) * interval
    s0_cyc = np.round(t0_cyc / time_step)
    m_dict = mode_dictionary()
    m_rates = mode_rates()
    t_day = 24*3600
    if (trange is None):
        xlim = (0, np.max(t0_cyc/t_day))
        slim = (int(0), int(num_cyc-1))
    else:
        xlim = trange
        slim = [np.int(np.floor(trange[0] * t_day / interval)),
                np.int(np.floor(trange[1] * t_day / interval))]
    # Just to know what modes to consider
    s1_count = np.bincount(mod_s1)
    act_modes = np.nonzero(s1_count)[0]
    labels = []
    colors = []
    rates = []
    for mode in act_modes:
        m_tag = m_dict[mode][0]
        rate = m_rates[m_dict[mode][0]]
        if m_dict[mode][1]:
            # m_tag = m_tag + " (bist)"
            rate = 2 * rate
        labels.append(m_tag)
        colors.append(m_dict[mode][2])
        rates.append(rate)
    mod_profile = np.zeros((act_modes.size, num_cyc))
    if trig_plot:
        trg_profile = np.zeros((len(Plans) + 1, num_cyc))
    maxmode = np.max(act_modes) + 1
    for i_cyc in np.arange(num_cyc, dtype=np.int):
        mod_s1_now = mod_s1[s0_cyc[i_cyc]:s0_cyc[i_cyc]+samp_cyc]
        mod_profile[:, i_cyc] = (np.bincount(mod_s1_now,
                                             minlength=maxmode))[act_modes]
        if trig_plot:
            actrigger_now = actrigger[s0_cyc[i_cyc]:s0_cyc[i_cyc]+samp_cyc]
            trg_profile[:, i_cyc] = (np.bincount(actrigger_now,
                                                 minlength=len(Plans) + 1))
    norm_fact = np.sum(mod_profile, axis=0).reshape((1, num_cyc))
    mod_profile = mod_profile / norm_fact * 100
    if trig_plot:
        norm_fact = np.sum(trg_profile, axis=0).reshape((1, num_cyc))
        trg_profile = trg_profile / norm_fact * 100
    if xls_export:
        # Convert mod_profile to pandas DataFrame
        mod_prof_df = pd.DataFrame(mod_profile, index=labels)
        if (savepath is None):
            import Tkinter
            import tkFileDialog
            root = Tkinter.Tk()
            root.withdraw()
            file_opt = {}
            file_opt['defaultextension'] = '.xlsx'
            savefile = tkFileDialog.asksaveasfilename(**file_opt)
        else:
            savefile = os.path.join(savepath, 'mod_profile.xlsx')
        mod_prof_df.to_excel(savefile, sheet_name='Mode duty cycles')
    if not make_figures:
        return mod_profile

    #plt.ioff()
    plt.figure(figsize=figsize)
    t0_cyc_d = t0_cyc/t_day
    for mode in range(1, act_modes.size):
        plt.plot(t0_cyc_d[slim[0]:slim[1]], mod_profile[mode, slim[0]:slim[1]],
                 label=labels[mode], color=colors[mode])
    plt.legend(framealpha=0.66)
    plt.xlabel("Time [day]")
    plt.ylabel("Duty [%]")
    plt.title(title + " duty cycle")
    plt.xlim(xlim[0], xlim[1])
    #plt.show()
    cum_prof = np.cumsum(mod_profile[1:, :], axis=0)
    if trig_plot:
        cum_trg_prof = np.cumsum(trg_profile[1:, :], axis=0)
#    plt.figure(figsize=figsize)
#
#    for mode in range(act_modes.size-1):
#        plt.plot(t0_cyc/t_day, cum_prof[mode, :],
#                 label=labels[mode+1], color=colors[mode+1])
#    plt.legend(framealpha=0.66)
#    plt.xlabel("Time [day]")
#    plt.ylabel("Cum. Duty [%]")
#    plt.title(title + " (cumulative)")
#    plt.xlim(0, np.max(t0_cyc/t_day))
#    plt.show()
    #return mod_profile
    #Filled plot
    plt.figure(figsize=figsize)

    legrect =[]
    plt.fill_between(t0_cyc_d[slim[0]:slim[1]], cum_prof[0, slim[0]:slim[1]],
                     label=labels[1], facecolor=colors[1],
                     color=colors[1])
    legrect.append(ptch.Rectangle((0, 0), 1, 1, fc=colors[1]))
    for mode in range(1, act_modes.size-1):
        plt.fill_between(t0_cyc_d[slim[0]:slim[1]],
                         cum_prof[mode, slim[0]:slim[1]],
                         y2=cum_prof[mode - 1, slim[0]:slim[1]],
                         label=labels[mode+1],
                         facecolor=colors[mode+1], color=colors[mode+1])
        legrect.append(ptch.Rectangle((0, 0), 1, 1, fc=colors[mode+1]))
    plt.legend(legrect, labels[1:], framealpha=0.66)
    plt.xlabel("Time [day]")
    plt.ylabel("Cum. Duty [%]")
    plt.title(title + " duty cycle (cumulative)")
    plt.xlim(xlim[0], xlim[1])
    #plt.show()

    if trig_plot:
        plt.figure(figsize=figsize)
        # trgcolors = colors
        legrect =[]
        plt.fill_between(t0_cyc_d[slim[0]:slim[1]],
                         cum_trg_prof[0, slim[0]:slim[1]],
                         label=plan_names[0], facecolor=trgcolors[0],
                         color=trgcolors[0])
        legrect.append(ptch.Rectangle((0, 0), 1, 1, fc=trgcolors[0]))
        for mode in range(1, len(Plans)):
            plt.fill_between(t0_cyc_d[slim[0]:slim[1]],
                             cum_trg_prof[mode, slim[0]:slim[1]],
                             y2=cum_trg_prof[mode - 1, slim[0]:slim[1]],
                             label=plan_names[mode],
                             facecolor=trgcolors[mode], color=trgcolors[mode])
            legrect.append(ptch.Rectangle((0, 0), 1, 1, fc=trgcolors[mode]))
        plt.legend(legrect, plan_names, framealpha=0.66)
        plt.xlabel("Time [day]")
        plt.ylabel("Cum. Duty [%]")
        plt.title(title + " duty cycle (cumulative)")
        plt.xlim(xlim[0], xlim[1])
        plt.show()
    #volumes
    mod_datavol = (mod_profile[1:, :] / 100 / 1e6 * interval *
                   np.array(rates[1:]).reshape((act_modes.size -1 , 1)))
    cum_dvol = np.cumsum(mod_datavol, axis=0)
    plt.figure(figsize=figsize)
    legrect = []
    plt.fill_between(t0_cyc_d[slim[0]:slim[1]], cum_dvol[0, slim[0]:slim[1]],
                     label=labels[1], facecolor=colors[1],
                     color=colors[1])
    legrect.append(ptch.Rectangle((0, 0), 1, 1, fc=colors[1]))
    for mode in range(1, act_modes.size-1):
        plt.fill_between(t0_cyc_d[slim[0]:slim[1]],
                         cum_dvol[mode, slim[0]:slim[1]],
                         y2=cum_dvol[mode - 1, slim[0]:slim[1]],
                         label=labels[mode+1],
                         facecolor=colors[mode+1], color=colors[mode+1])
        legrect.append(ptch.Rectangle((0, 0), 1, 1, fc=colors[mode+1]))
    plt.legend(legrect, labels[1:], framealpha=0.66)
    plt.xlabel("Time [day]")
    data_vol_string = "[Tbit]"
    plt.ylabel("Cum. Data Volumes "+data_vol_string)
    plt.title(title + " data volume (cumulative)")
    plt.xlim(xlim[0], xlim[1])
    #plt.show()
    #plt.ion()
    return norm_fact

def memory_profile(mode, time_step, Torb,
                   gs_contact, gs_sel_mask, down_link_rate = 260,
                   figsize=(10,5), trange=None, title="orbit",
                   fontsize=14, fontweight='normal', memlimit=256):
    """ Compute memory profile and down-link
    """
    matplotlib.rcParams.update({'font.size': fontsize,
                                'font.weight': fontweight})
    m_dict = mode_dictionary()
    m_rates = mode_rates()
    #dbits =
    #Just to know what modes to consider
    mode_count = np.bincount(mode.flatten())
    act_modes = np.nonzero(mode_count)[0]
    labels = []
    colors = []
    rates = []
    for i_mode in act_modes:
        m_tag = m_dict[i_mode][0]
        rate = m_rates[m_dict[i_mode][0]]
        if m_dict[i_mode][1]:
            m_tag = m_tag + " (bist)"
            # rate = 2 * rate
        labels.append(m_tag)
        colors.append(m_dict[i_mode][2])
        rates.append(rate)
    rates = np.array(rates)
    dbits = rates[mode] * time_step
    # integrate orbit
    orbbits = np.sum(dbits, axis=2)
    # Now get DL capacity per orbit

    if type(gs_contact) is tuple:
        gs_cntct = gs_contact
        gs_sl_msk = gs_sel_mask
    else:
        gs_cntct = (gs_contact)
        gs_sl_msk = (gs_sel_mask)

    dl_orb_cap = np.zeros((len(gs_cntct),) + orbbits.shape)
    for i_gs in range(len(gs_cntct)):
        gs = gs_cntct[i_gs]
        gs_orb_cap_ = (np.sum(gs.contact * down_link_rate, axis=1).
                       reshape((1, orbbits.shape[1])))
        dl_orb_cap[i_gs] = gs_sl_msk[i_gs] * gs_orb_cap_
    dl_orb_cap_tot = np.sum(dl_orb_cap, axis=0)
    shp = orbbits.shape
    orbbits = orbbits.flatten()
    dl_orb_cap_tot = dl_orb_cap_tot.flatten()
    memprof = np.zeros_like(orbbits)
    dlprof = np.zeros_like(orbbits)
    for i_orb in range(1, orbbits.size):
        memprof[i_orb] = (memprof[i_orb - 1] + orbbits[i_orb - 1] -
                          dl_orb_cap_tot[i_orb])
        if memprof[i_orb] < 0:
            dlprof[i_orb] = memprof[i_orb - 1] + orbbits[i_orb - 1]
            memprof[i_orb] = 0
        else:
            dlprof[i_orb] = dl_orb_cap_tot[i_orb]

    memprof = memprof + orbbits
    # A bit of smoothing
    wmp = 7
    memprof_wm = memprof.reshape((int(memprof.size/wmp), wmp)).max(axis=1)

    #plt.ioff()
    plt.figure(figsize=figsize)
    t = np.arange(memprof.size) * Torb / 24
    plt.plot(t, dlprof/1e3, '.', label='Down-link volume / orbit',
             color='gray')
    plt.plot(t[0:-1:wmp], memprof_wm / 1e3, label='Memory usage')
    if memlimit is not None:
        memlimit_ = np.array([memlimit]).flatten()
        for meml in memlimit_:
            plt.plot(t, np.ones_like(t) * meml, 'k--', lw=2)
    plt.xlabel("Time [day]")
    plt.legend()
    data_vol_string = "[Gbit]"
    plt.ylabel("Cum. Data Volumes "+data_vol_string)
    #plt.title("Memory profile")
    plt.xlim(t[0], t[-1])
    #plt.ion()
    #plt.show()

def memory_profile_(mod_, time_step_, interval, down_link_cap=[20.],
                   figsize=(10,5), trange=None, title="orbit", logscale=True,
                   fontsize=14, fontweight='normal'):
    """ Computes the on-board memory profile

        :param mod_s1: array containing which mode is activated
        :param time_step: time interval for each sample
        :type time_step: float
        :param interval: time interval consiered, typically the orbit time
        :down_link_cap: down link capapacity in Terabit/interval
    """
    mod_s1 = mod_.flatten()
    time_step = 12 * 24 * 3600 / (mod_.shape[1] * mod_.shape[2])
    downlink_cap = np.array(down_link_cap)
    n_samp = mod_s1.size
    samp_cyc = np.int(interval / time_step)
    num_cyc = np.floor(n_samp / samp_cyc)
    t0_cyc = np.arange(num_cyc) * interval
    s0_cyc = np.round(t0_cyc / time_step)
    m_dict = mode_dictionary()
    m_rates = mode_rates()
    t_day = 24*3600
    if (trange == None):
        xlim = (0, np.max(t0_cyc/t_day))
        slim = (0, num_cyc-1)
    else:
        xlim = trange
        slim = [np.int(np.floor(trange[0] * t_day / interval)),
                np.int(np.floor(trange[1] * t_day / interval))]
    #Just to know what modes to consider
    s1_count = np.bincount(mod_s1)
    act_modes = np.nonzero(s1_count)[0]
    labels = []
    colors = []
    rates = []
    for mode in act_modes:
        m_tag = m_dict[mode][0]
        rate = m_rates[m_dict[mode][0]]
        if m_dict[mode][1]:
            m_tag = m_tag + " (bist)"
            rate = 2 * rate
        labels.append(m_tag)
        colors.append(m_dict[mode][2])
        rates.append(rate)
    mod_profile = np.zeros((act_modes.size, num_cyc))
    maxmode = np.max(act_modes) + 1
    for i_cyc in np.arange(num_cyc, dtype=np.int):
        mod_s1_now = mod_s1[s0_cyc[i_cyc]:s0_cyc[i_cyc]+samp_cyc]
        mod_profile[:, i_cyc] = (np.bincount(mod_s1_now,
                                             minlength=maxmode))[act_modes]
    norm_fact = np.sum(mod_profile, axis=0).reshape((1, num_cyc))
    mod_profile = mod_profile / norm_fact * 100
    mod_datavol = (mod_profile[1:, :] / 100 / 1e6 * interval *
                   np.array(rates[1:]).reshape((act_modes.size - 1, 1)))
    cum_dvol = np.sum(mod_datavol, axis=0)
    dlink_shape = downlink_cap.shape
    max_dvol = np.zeros((downlink_cap.shape[0], cum_dvol.size))
    # Unfortunately, a loop
    # down_link_cap_Mb = down_link_cap * 1e6
    max_dvol[:, 0] = cum_dvol[0]
    for i_intv in range(1, cum_dvol.size):
        tmp = (max_dvol[:, i_intv-1] + cum_dvol[i_intv] - downlink_cap)
        max_dvol[:, i_intv] = np.where(tmp > 0, tmp, 0)

    t0_cyc_d = t0_cyc/t_day
    plt.ioff()
    plt.figure(figsize=figsize)
    for i_dl in range(downlink_cap.shape[0]):
        lab = "%4.2d Tbit/%s" % (downlink_cap[i_dl],title)
        plt.plot(t0_cyc_d[slim[0]:slim[1]], max_dvol[i_dl, slim[0]:slim[1]],
                 label=lab) #, color=colors[mode])
    plt.xlabel("Time [day]")
    if logscale:
        plt.yscale('log')
        plt.ylim(1, np.max(max_dvol))
    plt.legend()
    data_vol_string = "[Tbit]"
    plt.ylabel("Cum. Data Volumes "+data_vol_string)
    plt.title("Memory profile (total for both spacecraft")
    plt.xlim(xlim[0], xlim[1])
    plt.show()
    plt.ion()
    return max_dvol




def activation_analysis(filename, repeat_cycle=16, revolutions=231,
                        savepath=None):
    this_savepath = None
    if not (savepath is None):
        if not os.path.exists(savepath):
            os.makedirs(savepath)
    act_sav = readsav(filename)
    time_step = act_sav.mod_profile.time_step[0]
    mod_s1 = act_sav.mod_profile.sat1[0]
    mod_s2 = act_sav.mod_profile.sat2[0]
    T_orb = 24 * 3600 * repeat_cycle / revolutions
    n_samp = mod_s1.size
    samp_orb = T_orb / time_step
    num_orb = np.floor(n_samp / samp_orb)
    t0_orb = np.arange(num_orb) * T_orb
    s0_orb = np.round(t0_orb / time_step)
    modes = mode_dictionary()
    # Global statistics
    global_act_profile(mod_s1)
    rep_samp = np.int(np.round(repeat_cycle * 24 * 3600 / time_step))
    if not (savepath is None):
        this_savepath = os.path.join(savepath, 'orbduty_d0_to_31')
    mod_profile = activation_temp_prof(mod_s1, time_step, T_orb,
                                       title="Orbit",
                                       trange=(0, 32),
                                       xls_export=True,
                                       savepath=this_savepath,
                                       make_figures=False)
    if not (savepath is None):
        this_savepath = os.path.join(savepath, 'orbduty_d64_to_95')
    mod_profile = activation_temp_prof(mod_s1, time_step, T_orb,
                                       title="Orbit",
                                       trange=(64., 96),
                                       xls_export=True,
                                       savepath=this_savepath,
                                       make_figures=False)
    if not (savepath is None):
        this_savepath = os.path.join(savepath, 'dayly_duty')
    mod_profile = activation_temp_prof(mod_s1, time_step, 3600 * 24,
                                       title="Daily",
                                       xls_export=True,
                                       savepath=this_savepath,
                                       make_figures=False)
#    mem_profile = memory_profile(mod_s1, time_step, T_orb,
#                                 down_link_cap=[8, 9, 10, 11, 12])
#    mem_profile = memory_profile(mod_s1, time_step, T_orb,
#                                 down_link_cap=[8, 9, 10, 11, 12],
#                                 trange=(0, 32))
#    mem_profile = memory_profile(mod_s1, time_step, T_orb,
#                                 down_link_cap=[8, 9, 10, 11, 12],
#                                 trange=(64, 96))
    return mod_profile



