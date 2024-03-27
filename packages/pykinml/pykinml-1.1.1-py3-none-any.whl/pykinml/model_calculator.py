import torch
import data
import math
import nnpes
import ddp_loop as pes
import daev as daev
from ase import Atoms
from ase.calculators.calculator import Calculator, all_changes
from ase.units import Bohr,Rydberg,kJ,kB,fs,Hartree,mol,kcal

import numpy as np
import pandas as pd
import sys
import os
from pathlib import Path
from io import StringIO



class Nn_surr(Calculator):
    implemented_properties = ['energy', 'forces']

    def __init__(self, fname, restart=None, ignore_bad_restart_file=False, label='surrogate', atoms=None, tnsr=True, device='cpu', nrho_rad=16, nrho_ang=8, nalpha=8, R_c=[5.2, 3.8], mf=False, num_species=2, 
                 **kwargs):
        Calculator.__init__(self, restart=restart, ignore_bad_restart_file=ignore_bad_restart_file, label=label,
                            atoms=atoms, tnsr=tnsr, **kwargs)
        if isinstance(fname, list) and fname.__len__() > 1:
            self.multinn = True
        else:
            self.multinn = False
        self.surrogate = Nnpes_calc(fname, self.multinn, mf=mf, device=device, num_species = num_species)
        self.tnsr = tnsr
        self.device = device
        self.nrho_rad = nrho_rad
        self.nrho_ang = nrho_ang
        self.nalpha = nalpha
        self.R_c = R_c

    def calculate(self, atoms=None, properties=['energy', 'forces'], system_changes=all_changes, args=None):
        Calculator.calculate(self, atoms, properties, system_changes)
        if 'forces' in properties:
            favail = True
        else:
            favail = False
        if atoms is None:
            atoms = self.atoms
        xyzd = [[[s for s in atoms.symbols], np.array(atoms.positions)]]
        self.surrogate.dpes.aev_from_xyz(xyzd, self.nrho_rad, self.nrho_ang, self.nalpha, self.R_c, False)
        self.surrogate.nforce = self.surrogate.dpes.full_symb_data[0].__len__() * 3

        if self.multinn:
            energy, Estd, E_hf = self.surrogate.eval()
            if favail:
                force, Fstd, force_ind = self.surrogate.eval_force()
        else:
            energy = self.surrogate.eval()[0][0]
            Estd = torch.tensor(0.)
            if favail:
                force = self.surrogate.eval_force()
                Fstd = torch.tensor(0.)

        if self.tnsr:
            self.results['energy'] = energy
            self.results['energy_std'] = Estd
            if self.multinn:
                self.results['all_energies'] = E_hf
            if favail:
                self.results['forces'] = force.view(-1, 3)
                self.results['forces_std'] = Fstd
                if self.multinn:
                    self.results['all_forces'] = force_ind
        else:
            if self.device=='cpu':
                self.results['energy'] = energy.detach().numpy()
                self.results['energy_std'] = Estd.detach().numpy()
                if self.multinn:
                    self.results['all_energies'] = E_hf.detach().numpy()
                if favail:
                    self.results['forces'] = np.reshape(force.detach().numpy(), (-1, 3))
                    self.results['forces_std'] = Fstd.detach().numpy()
                    if self.multinn:
                        self.results['all_forces'] = force_ind.detach().numpy()
            else:
                self.results['energy'] = energy.detach().cpu().numpy()
                self.results['energy_std'] = Estd.detach().cpu().numpy()
                if self.multinn:
                    self.results['all_energies'] = E_hf.detach().cpu().numpy()
                if favail:
                    self.results['forces'] = np.reshape(force.detach().cpu().numpy(), (-1, 3))
                    self.results['forces_std'] = Fstd.detach().cpu().numpy()
                    if self.multinn:
                        self.results['all_forces'] = force_ind.detach().cpu().numpy()


# ====================================================================================================

class My_args():

    def __init__(self, load_model_name, mf=False, num_species=2):
        self.load_model_name = load_model_name
        self.multi_fid = mf
        self.num_species = num_species

# ==============================================================================================
class Nnpes_calc():

    def __init__(self, fname, multinn=False, device='cpu', mf=False, num_species=2):
        self.device = device
        self.dpes = data.Data_pes(['C', 'H'])
        if multinn:
            print('MULTINET!!!')
            args_list = [My_args(fname[i], mf=mf, num_species = num_species) for i in range(len(fname))]
            #self.nmodel = fname.__len__()
            self.nn_pes = [pes.Runner(args_list[i], self.device) for i in range(len(fname))]
        else:
            args = My_args(fname, mf=mf, num_species = num_species)
            self.nmodel = 1
            self.nn_pes = pes.Runner(args, self.device)

    def eval(self, indvout=False):
        self.dpes.prep_data(device=self.device)
        self.aevs = [aev[j].requires_grad_() for j in range(self.dpes.num_nn) for aev in self.dpes.aevs]
        if self.nmodel == 1:
            self.E = self.nn_pes.eval(self.dpes.aevs)
            E_pred = self.E
            return E_pred
        else:
            self.E = torch.empty((self.dpes.ndat, self.nmodel))
            for i in range(self.nmodel):
                E = self.nn_pes[i].eval(self.dpes.aevs)
                self.E[:, i] = E.reshape(-1)
            E_pred = torch.mean(self.E)
            Estd = torch.std(self.E, 1)
            return E_pred, Estd, self.E

    def eval_force(self):
        if self.nmodel == 1:
            forces = self.nn_pes.eval_force(self.dpes.daevs)
            return forces[0][0]
        else:
            Forces = torch.empty((self.dpes.ndat, self.nmodel, self.nforce))
            for i in range(self.nmodel):
                forces = self.nn_pes[i].eval_force(self.dpes.daevs)
                Forces[:,i] = forces[0][0]
            Fmean = torch.mean(Forces, 1).reshape(-1)
            Fstd  = torch.std(Forces, 1).reshape(-1)
            return Fmean, Fstd, Forces


