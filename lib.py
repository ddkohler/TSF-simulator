
import NISE as n
import numpy as np
import os
import WrightTools as wt
import time

t = n.experiments.trsf
m = n.lib.measure
m.Mono.slitwidth = 120.

H = n.hamiltonians.H_TRSF
inhom = n.hamiltonians.params.inhom

here = os.path.dirname(__file__)

default_sim_path = os.path.join(here, 'sims')

def run(axes, constants, sp, output_path=None, name=None):
    
    ax = {'w1': t.w1,
          'w2': t.w2,
          'wIR': t.wIR,
          'w3': t.w3,
          'w4': t.w3,
          'd1': t.d1,
          'd2': t.d2
          }
    
    if output_path is None:
        output_path = default_sim_path
    if name is None:
        name = time.asctime(time.gmtime()).replace(':','-')
    full_path = os.path.join(output_path, name)    

    # --- parse axes ---
    w4_points = False
    
    if 'w4' in axes.keys() and 'w3' in axes.keys():
        raise ValueError('cannot scan w4 and w3 simultaneously')
    if 'wIR' in axes.keys() and ('w1' in axes.keys() or 'w2' in axes.keys()):
        raise ValueError('cannot scan wIR and w1 or w2 simultaneously')

    scan_axes = []

    for key, val in axes.items():
        if key in ax.keys():
            ax[key].points = axes[key]
            scan_axes.append(ax[key])
            if key == 'w4':
                ax[key].name = ax[key].name.replace('3','4')
                w4_points = True
        else:
            raise Warning('not able to incorporate axis {0}'.format(key))
        
    print('creating {0}-dimensional scan'.format(len(scan_axes)))

    # --- parse constants ---      
    if 'pulse_width' in constants.keys(): 
        # not sure if I should put pulsewidth in ax...keeping separate for now
        t.exp.set_coord(t.ss, constants.pop('pulse_width'))
    for key in constants.keys():
        if key in ax.keys():
            if key in axes.keys():
                raise ValueError('{0} cannot be both an axis and a constant'.format(key))
            t.exp.set_coord(ax[key], constants[key])
        else:
            raise Warning('not able to incorporate constant {0}'.format(key))
    
    # --- parse hamiltonian params ---
    Gammas = [Gi for keyi, Gi in sp.items() if 'G_' in keyi]
    pulse_widths = t.exp.positions[:,t.exp.cols['s']]

    t.exp.timestep = pulse_widths.min() / 100
    t.exp.early_buffer = 1.5 * pulse_widths.max()
    t.exp.late_buffer = max(3 * pulse_widths.max(), 4 * min(Gammas)**-1)
    
    for key in sp.keys():
        if key not in H.Omega.out_vars:
            raise ValueError('sp {0} not recognized by Hamiltonian'.format(key))

    H1 = H.Omega(**sp)

    print('--------------------------------')
    print(H1.__dict__)
    print('--------------------------------')
    print(t.exp.__dict__)
    print('--------------------------------')
    #1/0

    # --- run sim ---
    inhom_object = inhom.Inhom()    
    out = t.exp.scan(*scan_axes, H=H1, inhom_object=inhom_object)
    if w4_points:
        out.get_efield_params()
        w_ind = t.exp.cols['w']
        w2 = out.efp[...,1,w_ind]
        w1 = out.efp[...,0,w_ind]
        out.efp[...,2,w_ind] -= w2 + w1
    #return out
    out.run(autosave=False, mp=True)#, mp=False)
    out.save(full_name = full_path)
    return full_path
    
def load(p):
    out = n.lib.scan.Scan._import(p)
    m1 = m.Measure(out, m.Mono, 
                   m.SLD)
    m1.run(save=False)
    # create wt object
    channels = [wt.data.Channel(m1.pol, 'signal')]
    axes = []
    for ax in out.axis_objs:
        print(ax.name)
        if 'omega' in ax.name:
            name = 'w'
            units = 'wn'
        elif 'tau' in ax.name:
            name = 'tau'
            units = 'fs'
        #print(ax.name)
        label_seed = [s for s in ax.name if s.isdigit()]
        for l in label_seed: name += l
        axes.append(wt.data.Axis(ax.points, units, name, 
                                 label_seed=[int(i) for i in label_seed]))
    return wt.data.Data(axes, channels)
