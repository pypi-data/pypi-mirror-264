'''
Created on Feb 8, 2018

@author: rch
'''

from ibvpy.tmodel.mats2D.mats2D_eval import MATS2DEval
import numpy as np


class MATS2DElastic(MATS2DEval):
    '''Elastic material model.
    '''
    state_var_shapes = {}

    def get_corr_pred(self, eps_Es, t_n1):

        E_ = self.E # 1000# 70e+3
        nu_ = self.nu # 0 # 0.3
        D_st_ = E_ / (1 - nu_ ** 2) * np.array([[1, nu_, 0], [nu_, 1, 0], [0, 0, 0.5 * (1 - nu_)]])
        D_Est = D_st_[np.newaxis, :, :]
        sig_Es = np.einsum('st,...t->...s', D_st_, eps_Es)

        return sig_Es, D_Est
