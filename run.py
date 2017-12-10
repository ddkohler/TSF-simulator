
import os
import numpy as np
import WrightTools as wt

import lib as l

here = os.path.dirname(__file__)

### config --------------------------------------------------------------------

axes = {
    #'w1_points'  : np.linspace(1800, 2000, 51), 
    #'w2_points'  : np.linspace(1800, 2000, 51), 
    'wIR' : np.linspace(1550, 1650, 51), # both w1 and w2 locked
    'w4'  : np.linspace(18000, 21000, 51),
    #'d1'  : np.linspace(-1e3, 1e3, 3) # 1D array of d1 scan pts [fs]
    #'d2_points'  : np.linspace(-1e3, 1e3, 3)
}

constants = {
    'pulse_width': 1000, # width of pulse [fs]
    'd2' : 0,
    'd1' : 0,
    #'w1' : 1570,
    #'w2' : 1570,
    #'w3' : 19000,
    
}

system_params = {
    # resonant frequencies [cm-1]
    'wI' : 1595,   
    'wi' : 1605,   
    'wa' : 19000,  
    'wb' : 20500,  

    # coupling/anharmonic constants [cm-1]
    #   positive number means lower frequency
    'I_anharm'    : 5,
    'i_anharm'    : 5,
    'Ii_coupling' : 5,

    # dipoles
    # --- fundamentals
    'm_gI' : 1.0,
    'm_gi' : 1.0,
    # --- electronic/vibronic
    'm_2Ia' : 0.0,
    'm_2Ib' : 1.0,
    'm_2ia' : 1.0,
    'm_2ib' : 0.0,
    'm_ca'  : 1.0,
    'm_cb'  : 1.0,
    'm_ag' : 1.0,
    'm_bg' : 1.0,
    
    # dephasing rates [fs-1]
    'G_Ig'  : 1/1000,
    'G_ig'  : 1/1000,
    'G_cg'  : 1/500,
    'G_ag'  : 1/10,
    'G_bg'  : 1/10
}

# default assumptions on some parameters

system_params['m_I2I'] = np.sqrt(2) * system_params['m_gI']
system_params['m_i2i'] = np.sqrt(2) * system_params['m_gi']
system_params['m_Ic'] = system_params['m_gi']
system_params['m_ic'] = system_params['m_gI']
# assume totally correlated
system_params['G_IIg'] = 2 * system_params['G_Ig']
system_params['G_iig'] = 2 * system_params['G_ig']

if __name__ == '__main__':
    # --- run sim--only need to run once ------------------------------------------
    if True:
        fpath = l.run(axes, constants, system_params)
    else: # use filename of already run sim
        fpath = os.path.join(l.default_sim_path, 'Sun Dec 10 03-26-55 2017')
    # --- load sim ----------------------------------------------------------------
    if True:
        dnise = l.load(fpath) # data is *intensity* scaled
        dnise.scale(kind='amplitude')
        
    # --- plot sim ----------------------------------------------------------------
    if True:
        output_folder = os.path.join(fpath, 'img')
        if not os.path.exists(output_folder): os.mkdir(output_folder)
        art = wt.artists.mpl_2D(dnise, xaxis='w12', yaxis='w4')
        art.plot(output_folder=output_folder, autosave=True) 
                 #contours=9, pixelated=False)
