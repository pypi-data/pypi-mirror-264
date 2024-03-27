from pathlib import Path
import math
import sys
import argparse
import os
import itertools
import random
import pickle
import timeit
import time

import numpy as np
import torch
import torch.nn as nn
import torch.multiprocessing as mp
from ase.units import mol, kcal


import data
import nnpes
import daev as daev_calc
import prepper as prep
from prepper import kcpm

from torch.nn.parallel import DistributedDataParallel as DDP
from torch.distributed import init_process_group, destroy_process_group
import torch.multiprocessing as mp


os.environ['CUDA_LAUNCH_BLOCKING'] = "1"



# ====================================================================================================


def ddp_setup(rank, world_size):
    """
    Args:
        rank: Unique identifier of each process
        world_size: Total number of processes
    """
    os.environ["MASTER_ADDR"] = "localhost"
    os.environ["MASTER_PORT"] = "12334"
    init_process_group(backend="gloo", rank=rank, world_size=world_size)
    torch.cuda.set_device(rank)




# ====================================================================================================
def parse_arguments_list():
    parser = argparse.ArgumentParser(description='PES code')
    parser.add_argument('-g', '--enable-cuda', action='store_true', help='Enable CUDA -- use gpu if available')
    parser.add_argument('-c', '--num_cores', type=int, default=4,
                        help='specify number of cores to run on [4], nb. num_threads=2 x num_cores')
    parser.add_argument('-d', '--input-data-type', choices=('xyz', 'ani', 'aev', 'pca', 'sqlite'), default='sqlite',
                        help='specify input data file type [aev]')
    parser.add_argument('-f', '--input-data-fname', nargs='*', default=['/home/cjdever/mlsdb/data/C5H5/C*H*.db'],
                        help='Specify input data filename(s) [aev_db.hdf5]')
    parser.add_argument('-u', '--dont-shuffle-data', action='store_true', default=False,
                        help='do not randomly shuffle data')
    parser.add_argument('-l', '--learning-rate', type=float, default=1.e-3,
                        help='specify optimizer learning rate [1.e-3]')
    parser.add_argument('-m', '--momentum', type=float, default=0.5, help='specify optimizer momentum [0.5]')
    parser.add_argument('--weight-decay', type=float, default=0, help='specify L2-penalty for regularization')
    parser.add_argument('-e', '--epochs', type=int, default=2, help='specify number of epochs for training')
    parser.add_argument('-p', '--ntlp', type=int, default=1,
                        help='specify eval/output training error every <ntlp> epochs')
    parser.add_argument('--save_every', type=int, default=10,
                        help='specify save NN every <save_every> epochs')
    parser.add_argument('-b', '--tr_batch_size', type=int, default=10,
                        help='specify (approximate) batch size for training')
    parser.add_argument('-lmo', '--load-model', action='store_true', default=False,
                        help='specify new model, do not load exising net0.pt, net1.pt, opt.pt')
    parser.add_argument('-lm', '--load_model_name', nargs='*', default=['comp.pt'],
                        help='Specify load model file name [Comp.pt] or the path of folders which contains model parameters [net_pars/]')
    parser.add_argument('-llr', '--load-lr', action='store_true', default=False,
                        help='load saved learninig rate. Only use if loading saved model, and even then not always')
    parser.add_argument('-o', '--optimizer', nargs='*', default=['Adam'],
                        help='Specify the optimizer type [SGD or Adam or AdamW]')
    parser.add_argument('-dl', '--input-lf-data-type', choices=('xyz', 'ani', 'aev', 'pca', 'sqlite'), default=None,
                        help='specify low fidelity input data file type [aev]')
    parser.add_argument('-fl', '--input-lf-data-fname', nargs='*', default=None,
                        help='Specify low fidelity input data filename(s) [aev_db.hdf5]')
    parser.add_argument('--test-input-xid', nargs='*', default=None,
                        help='Specify test input data xyzid if the data type is sqlite [xid_tst.txt]')
    parser.add_argument('--tr-input-xid', nargs='*', default=None,
                        help='Specify training(and validation) input data xyzid if the data type is sqlite [xid_tr.txt]')
    parser.add_argument('--trtsid-name', nargs='*', default=['cut.txt'],
                        help='Specify training(and validation)/test input data xyzid with tvt mask [trid_trtst.txt]')
    parser.add_argument('--trtsid-name-lf', nargs='*', default=None,
                        help='Specify training(and validation)/test input data xyzid with tvt mask for low fidelity [trid_trtst_lf.txt]')
    parser.add_argument('-if', '--fidlevel', type=int, default=1,
                        help='Specify input fidelity level as integer [0, 1, 2, 3, 4] (SQLite db only)')
    parser.add_argument('--fidlevel-lf', type=int, default=None,
                        help='Specify input low fidelity level as integer [0, 1, 2, 3, 4] (SQLite db only)')
    parser.add_argument('-nl', '--my-neurons', nargs='+', type=int, default=None,
                        help='Specify set of the number of neurons in each layer. The last number is for the output layer (new model only)')
    parser.add_argument('-nh', '--my-neurons-hf', nargs='+', type=int, default=None,
                        help='Specify set of the number of neurons in each layer for high fidelity NN. The last number is for the output layer (new model only)')
    parser.add_argument('-al', '--my-actfn', nargs='+', default=None,
                        help='Specify set of the activation functions in each layer. [gaussian, tanh, identity, relu, silu, fsp] (new model only)')
    parser.add_argument('-sn', '--savenm', nargs='*', default='test',
                        help='Specify folder name to save the data. The optimizer and device will be appended to the name.')
    parser.add_argument('-r', '--randomseed', nargs='+', type=int, default=[0, 1], help='Specify random seed as integer')
    parser.add_argument('-nd', '--node', type=int, default=0, help='Specify gpu node as integer')
    parser.add_argument('-ls', '--lrscheduler', nargs='*', default='rop',
                        help='Specify learning rate scheduler. [exp, step, rop]')
    parser.add_argument('-dr', '--decayrate', type=float, default=0.5,
                        help='Specify learning rate scheduler decay rate. default = 0.1')
    parser.add_argument('--tvt', nargs='+', type=float, default=[0.8, 0.1, 0.1],
                        help='Specify set of the decimal fraction (0.0,1.0] or number of points for training, validation and test set. The sum should be 1 if you input decimal points')
    parser.add_argument('--tvt-lf', nargs='+', type=float, default=[0.8, 0.1, 0.1],
                        help='Specify set of the decimal fraction (0.0,1.0] or number of points for training, validation and test set for low fidelity data in multifidelity NN. The sum should be 1 if you input decimal points')
    parser.add_argument('--fw', type=float, default=0.0,
                        help='Specify the decimal fraction (0.0,1.0] for weighted loss of force. Only available when floss option is on')
    parser.add_argument('--floss', action='store_true', default=False, help='Use force in loss function')
    parser.add_argument('--write-tvtmsk', action='store_true', default=False,
                        help='write training/validation/test mask')
    parser.add_argument('--read-trid', action='store_true', default=True,
                        help='read training set xyzid list')
    parser.add_argument('--temp', type=int, default=2000,
                        help='Specify temperature that QC data was sampled. default = 20000')
    parser.add_argument('-ofw', '--optimize-force-weight', action='store_true', default=False,              #Not yet sure how this works with multi fidelity.
                        help='optimize relative weights of energy and force in loss function')
    parser.add_argument('-sae', '--sae-fit', action='store_true', default=False,                            #Not yet sure how this works with multi fidelity.
                        help='compute single atom energies and subtract them from the dataset')
    parser.add_argument('--no-biases', action='store_true', default=False,
                        help='dont include biases in NN')
    parser.add_argument('--delta', action='store_true', default=False,
                        help='delta learning to predict diference between 2 fidelity levels')
    parser.add_argument('-prs', '--pre-saved', action='store_true', default=False,
                        help='indicates that the data has already been preped and saved in the proper location')
    parser.add_argument('-bvl','--vl_batch_size', type=int,  default=10,                            #Use to avoid memory issues when doing force training.
                        help='validation set batch size')
    parser.add_argument('-bts', '--ts_batch_size', type=int,  default=10,                            #Use to avoid memory issues when doing force training.
                        help='test set batch size')
    parser.add_argument('-aev', '--aev_params', type=int, nargs='+',  default=[16, 8, 8],                            #Not yet sure how this works with multi fidelity.
                        help='parameters determining the length of the AEV')
    parser.add_argument('-R_c', '--cuttoff-radius', type=float, nargs='+',  default=[5.2, 3.8],                            #Not yet sure how this works with multi fidelity.
                        help='radial and angular cuttoff radii')
    parser.add_argument('-ns', '--nameset', nargs='+', default=None,
                        help='Specify set of the patterns of db name to generate redueced set. [w irc ...]')
    parser.add_argument('--ddp', action='store_true',  default=False,
                        help='Use pytorches Distributed Data Parallel')
    parser.add_argument('--gpus', nargs='+', type=int, default=[0],
                        help='GPU ids to use for DDP')
    parser.add_argument('--present_elements', nargs='+', default=['C', 'H'],
                        help='Specify how many chemical elements are included in the training set')
    parser.add_argument('--multi_fid', action='store_true', default=False,
                        help='Train to multiple fidelity levels')
    args = parser.parse_args()


    try:
        if args.lrscheduler[0] == 'None':
            args.lrscheduler = None
    except:
        pass
    return args


# ====================================================================================================



class Trainer:
    def __init__(self, model, train_data, valid_data, test_data, keys, train_data_lf, valid_data_lf, test_data_lf, keys_lf, optimizer, lr_scheduler, sae_energies, save_every: int, fname: str, svpath:str, device, force_train=False, num_spec=2):
        random.seed(0)
        torch.manual_seed(random.randrange(200000))
        np.random.seed(random.randrange(200000))
        random.seed(random.randrange(200000))
        self.device = device
        self.model = model
        self.train_data = train_data
        self.valid_data = valid_data
        self.test_data = test_data
        self.keys = keys

        self.train_data_lf = train_data_lf
        self.valid_data_lf = valid_data_lf
        self.test_data_lf = test_data_lf
        self.keys_lf = keys_lf

        self.num_spec = num_spec
        self.save_every = save_every
        self.FT=force_train
        self.optimizer = optimizer
        self.lr_scheduler = lr_scheduler
        self.sae_energies = sae_energies
        self.fname = fname
        self.svpath = svpath
        self.openf = open(fname, "w")


    def save_ddp(self, net_fnam, epoch, optimizer):
        torch.save({'epoch': epoch,
                    'optimizer': optimizer,
                    'optimizer_state_dict': optimizer.state_dict(),
                    'lr_scheduler': self.lr_scheduler,
                    'model_state_dict': self.model.state_dict(),
                    'sae_energies': self.sae_energies,
                    'params': self.model.module.netparams
                    },
                   self.svpath + '/' + net_fnam + '-' + str(epoch).zfill(4) + ".pt")

    def save_cpu(self, net_fnam, epoch, optimizer):
        torch.save({'epoch': epoch,
                    'optimizer': optimizer,
                    'optimizer_state_dict': optimizer.state_dict(),
                    'lr_scheduler': self.lr_scheduler,
                    'model_state_dict': self.model.state_dict(),
                    'sae_energies': self.sae_energies,
                    'params': self.model.netparams
                    },
                   self.svpath + '/' + net_fnam + '-' + str(epoch).zfill(4) + ".pt")


    def cat_data(self, tocat, key, ind):
        random.seed(0)
        torch.manual_seed(random.randrange(200000))
        np.random.seed(random.randrange(200000))
        random.seed(random.randrange(200000))
        items = []
        ids = []
        nmols = []
        for batch_all in tocat:
            batch = np.array(batch_all)[:,ind]
            if key == 'aevs' or key == 'daevs':
                ss = [[[] for mol in range(len(batch))] for spec in range(self.num_spec)]
                id_spec = [[] for spec in range(self.num_spec)]
                mol_count = 0
                for mol in range(len(batch)):
                    mol_count += 1
                    for spec in range(len(batch[mol])):
                        if key == 'daevs':
                            ss[spec][mol] = batch[mol][spec].to(self.device)
                        if key == 'aevs':
                            ss[spec][mol] = batch[mol][spec].to(self.device).requires_grad_()
                            id_spec[spec] += [mol] * len(batch[mol][spec])
                ss = [torch.cat(s) for s in ss]
                bitem = ss
                if key == 'aevs':
                    id_spec = [torch.tensor(spec).to(self.device) for spec in id_spec]
                    ids.append(id_spec)
                    nmols.append(mol_count)
            
            if 'forces' in key or 'engs' in key:
                bitem = torch.cat([item for item in batch]).to(self.device)
                if 'engs' in key:
                    bitem = bitem.unsqueeze(0).T
            if 'fdims' in key:
                bitem = batch
            items.append(bitem)
        if key == 'aevs':
            return items, ids, nmols
        else:
            return items


    def _run_batch_tvs(self, tvs, aevs, ids, nmols, true_engs_lf, true_engs_hf, true_forces_lf=[], true_forces_hf=[], fdims=[], daevs=[]):

        if tvs == 'train':
            self.optimizer.zero_grad()
        pred_engs_lf, pred_engs_hf, log_sigma = self.model(aevs, ids, nmols)
        ediff_lf = prep.energy_abs_dif(pred_engs_lf, true_engs_lf)
        ediff_hf = prep.energy_abs_dif(pred_engs_hf, true_engs_hf)
        fdiff_lf=[]        #This is a placeholder for when not doing force training
        fdiff_hf=[]        #This is a placeholder for when not doing force training
        if self.FT:
            pred_forces_lf = daev_calc.cal_dEdxyz_ddp(aevs, -pred_engs_lf, daevs, ids)
            fdiff_lf = prep.force_abs_dif(pred_forces_lf, true_forces_lf, fdims)
            pred_forces_hf = daev_calc.cal_dEdxyz_ddp(aevs, -pred_engs_hf, daevs, ids)
            fdiff_hf = prep.force_abs_dif(pred_forces_hf, true_forces_hf, fdims)
        
        if tvs == 'train':
            eloss_lf, floss_lf = prep.my_loss(ediff_lf, fdiff_lf, dEsq=1., dfsq=1., p=2)
            eloss_hf, floss_hf = prep.my_loss(ediff_hf, fdiff_hf, dEsq=1., dfsq=1., p=2)
            eloss = eloss_lf + eloss_hf
            floss = floss_lf + floss_hf
            loss = self.model.mtl([eloss, floss], log_sigma)
            self.log_sigma = log_sigma
            loss.backward(retain_graph=True)
            loss.retain_grad()
            self.optimizer.step()
        return ediff_lf, fdiff_lf, ediff_hf, fdiff_hf
    


    def _run_epoch(self, epoch, data, ids, nmols, tvs, data_lf={}):
        bat_lst = list(range(len(data['engs'])))
        ediff_lf = []
        fdiff_lf = []
        ediff_hf = []
        fdiff_hf = []
        for b in bat_lst:
            if self.FT:
                bediff_lf, bfdiff_lf, bediff_hf, bfdiff_hf = self._run_batch_tvs(tvs, data['aevs'][b], ids[b], nmols[b], data_lf['engs'][b], data['engs'][b], data_lf['forces'][b], data['forces'][b], data['fdims'][b], data['daevs'][b])
                fdiff_lf += bfdiff_lf
                fdiff_hf += bfdiff_hf
            else:
                bediff_lf, bfdiff_lf, bediff_hf, bfdiff_hf = self._run_batch_tvs(tvs, data['aevs'][b], ids[b], nmols[b], data['engs'][b], data_lf['engs'][b])
            ediff_lf += bediff_lf
            ediff_hf += bediff_hf
        ediff_lf = torch.tensor(ediff_lf)
        L1_lf = torch.mean(ediff_lf)
        L2_lf = torch.sqrt(torch.mean(ediff_lf**2))
        Linf_lf = torch.max(ediff_lf)
        self.openf.write(tvs + ' L1_lf loss: ' + str(kcpm(L1_lf.item())) + '\n')
        self.openf.write(tvs + ' L2_lf loss: ' + str(kcpm(L2_lf.item())) + '\n')
        self.openf.write(tvs + ' Linf_lf loss: ' + str(kcpm(Linf_lf.item())) + '\n')
        print('device ', self.device, ' ',tvs + ' MAE_lf: ', kcpm(L1_lf.item()))
        print('device ', self.device, ' ',tvs + ' RMSE_lf: ', kcpm(L2_lf.item()))
        print('device ', self.device, ' ',tvs + ' Linf_lf: ', kcpm(Linf_lf.item()))

        ediff_hf = torch.tensor(ediff_hf)
        L1_hf = torch.mean(ediff_hf)
        L2_hf = torch.sqrt(torch.mean(ediff_hf**2))
        Linf_hf = torch.max(ediff_hf)
        self.openf.write(tvs + ' L1_hf loss: ' + str(kcpm(L1_hf.item())) + '\n')
        self.openf.write(tvs + ' L2_hf loss: ' + str(kcpm(L2_hf.item())) + '\n')
        self.openf.write(tvs + ' Linf_hf loss: ' + str(kcpm(Linf_hf.item())) + '\n')
        print('device ', self.device, ' ',tvs + ' MAE_hf: ', kcpm(L1_hf.item()))
        print('device ', self.device, ' ',tvs + ' RMSE_hf: ', kcpm(L2_hf.item()))
        print('device ', self.device, ' ',tvs + ' Linf_hf: ', kcpm(Linf_hf.item()))

        if self.FT:
            fdiff_lf = torch.cat(fdiff_lf)
            fL1_lf = torch.mean(fdiff_lf)
            fL2_lf = torch.sqrt(torch.mean(fdiff_lf**2))
            fLinf_lf = torch.max(fdiff_lf)
            self.openf.write(tvs + ' fL1_lf loss: ' + str(kcpm(fL1_lf.item())) + '\n')
            self.openf.write(tvs + ' fL2_lf loss: ' + str(kcpm(fL2_lf.item())) + '\n')
            self.openf.write(tvs + ' fLinf_lf loss: ' + str(kcpm(fLinf_lf.item())) + '\n')
            print('device ', self.device, ' ',tvs + ' FMAE_lf: ', kcpm(fL1_lf.item()))
            print('device ', self.device, ' ',tvs + ' FRMSE_lf: ', kcpm(fL2_lf.item()))
            print('device ', self.device, ' ',tvs + ' FLinf_lf: ', kcpm(fLinf_lf.item()))

            fdiff_hf = torch.cat(fdiff_hf)
            fL1_hf = torch.mean(fdiff_hf)
            fL2_hf = torch.sqrt(torch.mean(fdiff_hf**2))
            fLinf_hf = torch.max(fdiff_hf)
            self.openf.write(tvs + ' fL1_hf loss: ' + str(kcpm(fL1_hf.item())) + '\n')
            self.openf.write(tvs + ' fL2_hf loss: ' + str(kcpm(fL2_hf.item())) + '\n')
            self.openf.write(tvs + ' fLinf_hf loss: ' + str(kcpm(fLinf_hf.item())) + '\n')
            print('device ', self.device, ' ',tvs + ' FMAE_hf: ', kcpm(fL1_hf.item()))
            print('device ', self.device, ' ',tvs + ' FRMSE_hf: ', kcpm(fL2_hf.item()))
            print('device ', self.device, ' ',tvs + ' FLinf_hf: ', kcpm(fLinf_hf.item()))

            self.openf.write('log_sigma: ')
            for task in range(len(self.log_sigma)):
                self.openf.write(str(self.log_sigma[task].item())+' ')
        self.openf.write('\n')
        if tvs == 'valid':
            self.lr_scheduler.step(kcpm(L2_hf))



    def train(self, max_epochs: int):
        tr0 = time.time()
        random.seed(0)
        torch.manual_seed(random.randrange(200000))
        np.random.seed(random.randrange(200000))
        random.seed(random.randrange(200000))
        self.openf.write('Initial parameters for gpu: '+ str(self.device) + '\n')
        for name, param in self.model.named_parameters():
            if param.requires_grad:
                self.openf.write(name + ': ' + str(param.data) + '\n')
        
        train_dict = {}
        valid_dict = {}
        test_dict = {}
        print('self.keys: ', self.keys)
        print('self.keys_lf: ', self.keys_lf)
        for i in range(len(self.keys)):
            if self.keys[i] == 'aevs':
                train_dict[self.keys[i]], tr_ids, tr_nmols = self.cat_data(self.train_data, self.keys[i], i)
                valid_dict[self.keys[i]], vl_ids, vl_nmols = self.cat_data(self.valid_data, self.keys[i], i)
                test_dict[self.keys[i]], ts_ids, ts_nmols = self.cat_data(self.test_data, self.keys[i], i)
            else:
                train_dict[self.keys[i]] = self.cat_data(self.train_data, self.keys[i], i)
                valid_dict[self.keys[i]] = self.cat_data(self.valid_data, self.keys[i], i)
                test_dict[self.keys[i]] = self.cat_data(self.test_data, self.keys[i], i)
        

        train_dict_lf = {}
        valid_dict_lf = {}
        test_dict_lf = {}
        for i in range(len(self.keys_lf)):
            if self.keys_lf[i] == 'aevs':
                train_dict_lf[self.keys_lf[i]], tr_ids, tr_nmols = self.cat_data(self.train_data_lf, self.keys_lf[i], i)
                valid_dict_lf[self.keys_lf[i]], vl_ids, vl_nmols = self.cat_data(self.valid_data_lf, self.keys_lf[i], i)
                test_dict_lf[self.keys_lf[i]], ts_ids, ts_nmols = self.cat_data(self.test_data_lf, self.keys_lf[i], i)
            else:
                train_dict_lf[self.keys_lf[i]] = self.cat_data(self.train_data_lf, self.keys_lf[i], i)
                valid_dict_lf[self.keys_lf[i]] = self.cat_data(self.valid_data_lf, self.keys_lf[i], i)
                test_dict_lf[self.keys_lf[i]] = self.cat_data(self.test_data_lf, self.keys_lf[i], i)


        for epoch in range(max_epochs):
            print('\nGPU ', self.device,' epoch: ', epoch)
            self.openf.write('\nepoch: ' + str(epoch) + '\n')
            self._run_epoch(epoch, train_dict, tr_ids, tr_nmols, tvs='train', data_lf=train_dict_lf)
            self._run_epoch(epoch, valid_dict, vl_ids, vl_nmols, tvs='valid', data_lf=valid_dict_lf)
            if self.device == 0 or self.device == 'cpu':
                self._run_epoch(epoch, test_dict, ts_ids, ts_nmols, tvs='test', data_lf=test_dict_lf)
            
            if self.device == 'cpu' and (epoch % self.save_every == 0 or epoch  + 1 == max_epochs):
                self.save_cpu('ddp_model', epoch, self.optimizer)
            if self.device == 0 and (epoch % self.save_every == 0 or epoch  + 1 == max_epochs): 
                self.save_ddp('ddp_model', epoch, self.optimizer)

        print('device ', self.device, 'is DONE!!!')
        self.openf.write('Final parameters for device ' +  str(self.device) + ':\n')
        for name, param in self.model.named_parameters():
            if param.requires_grad:
                self.openf.write(name + ': ' + str(param.data) + '\n')
        
        tr1 = time.time()
        self.openf.write('Training time: ' + str(tr1-tr0))
        self.openf.close()



# ====================================================================================================
def spawned_trainer(rank:int, args, world_size:int):
    random.seed(args.randomseed[1])
    torch.manual_seed(random.randrange(200000))
    np.random.seed(random.randrange(200000))
    random.seed(random.randrange(200000))
    torch.set_default_dtype(torch.float64)
    #torch.set_printoptions(precision=8)
    seeds = args.randomseed
    args.num_species = len(args.present_elements)
    print('torch.cuda.is_available(): ', torch.cuda.is_available())
    if args.ddp:
        print('setting up DDP!')
        ddp_setup(rank, world_size)
        print('DDP has been setup!')
    fname = args.savenm + '_seeds_'+str(seeds[0])+'_'+str(seeds[1])+'_device_' + str(rank) + '.log'
    print('about to load train objects!')
    save_path = args.savenm + '_seeds_'+str(seeds[0])+'_'+str(seeds[1])
    Path(save_path).mkdir(parents=True, exist_ok=True)
    torch.autograd.set_detect_anomaly(True)
    train_set, valid_set, test_set, model, optimizer, lr_scheduler, sae_energies, keys = prep.load_train_objs(args, fid=args.fidlevel, get_aevs=True)
    train_set_lf, valid_set_lf, test_set_lf, keys_lf = prep.load_train_data(args,fid=args.fidlevel_lf, get_aevs=False)
    prep.set_up_task_weights(model, args, optimizer)
    device = rank# if torch.cuda.is_available() else 'cpu'
    if args.ddp:
        model = DDP(model.to(device), device_ids=[device], find_unused_parameters=True)
        model.mtl = model.module.mtl
    else:
        model = model.to(device)
    trainer = Trainer(model, train_set, valid_set, test_set, keys, train_set_lf, valid_set_lf, test_set_lf, keys_lf, optimizer, lr_scheduler, sae_energies, args.save_every, fname, save_path, device, force_train=args.floss, num_spec = args.num_species) 
    trainer.train(args.epochs)
    if args.ddp:
        destroy_process_group()




def main(args):
    tt1 = time.time()
    torch.set_default_dtype(torch.float64)
    if args.ddp:
        args.gpus = [str(g) for g in args.gpus]
        args.gpus = ', '.join(args.gpus)
        print('GPUS: ', args.gpus)
        os.environ['CUDA_VISIBLE_DEVICES'] = args.gpus
    if not args.pre_saved:
        print('preping data')
        prep.prep_data(args)
        if args.delta:
            prep.prep_data(args)
        args.pre_saved = True
    world_size = torch.cuda.device_count()
    print('world_size: ', world_size)
    if args.ddp:
        mp.spawn(spawned_trainer, args=[args,world_size], nprocs=world_size, join=True)
    else:
        spawned_trainer('cpu', args, 0)
    tt2 = time.time()
    print('Time it took: ', tt2-tt1)




if __name__ == "__main__":
    # set default pytorch as double precision
    torch.set_default_dtype(torch.float64)

    # preamble -- handling arguments
    args = prep.parse_arguments_list()
    main(args
