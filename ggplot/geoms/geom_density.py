from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from .geom import geom
from scipy.stats import gaussian_kde
import numpy as np


class geom_density(geom):
    VALID_AES = {'x', 'alpha', 'color', 'fill',
                 'linetype', 'size', 'weight'}
    REQUIRED_AES = {'x'}
    DEFAULT_PARAMS = {'stat': 'density', 'position': 'identity', 'label': ''}

    _groups = {'color', 'linetype', 'alpha'}
    _aes_renames = {'linetype': 'linestyle'}

    def _plot_unit(self, pinfo, ax):
        x = pinfo.pop('x')
        fill = pinfo.pop('fill', None)
        pinfo['label'] = self.params['label']

        try:
            float(x[0])
        except:
            try:
                # try to use it as a pandas.tslib.Timestamp
                x = [ts.toordinal() for ts in x]
            except:
                raise Exception("geom_density(): aesthetic x mapping needs to be convertable to float!")
        kde = gaussian_kde(x)
        bottom = np.min(x)
        top = np.max(x)
        step = (top - bottom) / 1000.0
        x = np.arange(bottom, top, step)
        y = kde.evaluate(x)
        ax.plot(x, y, **pinfo)
        if fill:
            ax.fill_between(x, y1=np.zeros(len(x)), y2=y, **pinfo)
