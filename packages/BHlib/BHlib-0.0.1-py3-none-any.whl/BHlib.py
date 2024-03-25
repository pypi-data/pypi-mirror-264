import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from mpl_toolkits.axes_grid1 import host_subplot
from mpl_toolkits import axisartist

__version__ = '0.0.1'

mu0 = 1.256637e-6
staticBHcurve = {
    'amorphous_alloy': {'H': '''1e-8
1.8248175182481745
4.178832116788328
5.766423357664237
6.970802919708035
9.981751824817522
14.744525547445264
20
29.96350364963503
50''', 'B': '''1e-8
0.396273161145424
0.7983471364402022
0.9369104435710276
1.0023722627737226
1.0698729646266143
1.097101347557552
1.1070536215609208
1.1134615384615385
1.122438236945536'''},
    'pure_iron': {'H': '''75.4039500
100.5386000000
138.2406000000
165.3375200000
201.0772000000
226.2119000000
251.3465000000
263.9138000000
276.4812000000
301.6158000000
339.3178000000
439.8564000000
552.9623000000
728.9049000000
992.8186000000
1508.0790000000
2815.0810000000
5592.4590000000
5780.9700000000
5944.3450000000
6120.2870000000
6296.2300000000
6472.1730000000
6648.1150000000
6798.9230000000
7000.0000000000''', 'B': '''0.1005386000
0.2010772000
0.3016158000
0.4021544000
0.4991024000
0.5996410000
0.7001796000
0.8007081000
0.8617594000
0.9982047000
1.0987430000
1.1992820000
1.2998210000
1.3967680000
1.5008980000
1.5978460000
1.7055660000
1.8132850000
1.8204670000
1.8240570000
1.8312390000
1.8348290000
1.8420110000
1.8456010000
1.8491920000
1.8527830000'''}
}

def data(material, property, num=1024, mode='origin'):
    H_origin = np.fromstring(staticBHcurve[material]['H'], sep='\n', dtype=float)
    B_origin = np.fromstring(staticBHcurve[material]['B'], sep='\n', dtype=float)
    if mode == 'smooth':
        H = np.linspace(np.min(H_origin), np.max(H_origin), num)
        B = make_interp_spline(H_origin, B_origin)(H)
    else:
        H = H_origin
        B = B_origin

    mu = B / H
    mur = mu / mu0
    mu_diff = np.diff(B) / np.diff(H)
    mu_diff = np.append(mu_diff, mu_diff[-1])
    mur_diff = mu_diff / mu0
    sw = {'h': H,
          'b': B,
          'mu': mu,
          'mur': mur,
          'mu_diff': mu_diff,
          'mur_diff': mur_diff}
    return sw[property]

def plot(material, num=1024, mode='smooth'):
    if mode != 'smooth':
        mode = 'origin'
    H = data(material, 'h', num, mode)
    B = data(material, 'b', num, mode)
    mur = data(material, 'mur', num, mode)
    mur_diff = data(material, 'mur_diff', num, mode)
    host = host_subplot(111, axes_class=axisartist.Axes)
    plt.subplots_adjust(right=0.75)

    par1 = host.twinx()
    par2 = host.twinx()


    par2.axis["right"] = par2.new_fixed_axis(loc="right", offset=(60, 0))
    par1.axis["right"].toggle(all=True)
    par2.axis["right"].toggle(all=True)

    p1, = host.plot(H, B, label="B")
    p2, = par1.plot(H, mur, label="mur_static")
    p3, = par2.plot(H, mur_diff, label="mur_diff")

    host.set_xlabel("H")
    host.set_ylabel("B")
    par1.set_ylabel("mur_static")
    par2.set_ylabel("mur_diff")
    plt.title(f'{material} | Points:{len(H)} | Mode:{mode}\nmur_max:{int(np.max(mur))} | mur_diff_max:{int(np.max(mur_diff))}')
    host.legend()
    plt.show()