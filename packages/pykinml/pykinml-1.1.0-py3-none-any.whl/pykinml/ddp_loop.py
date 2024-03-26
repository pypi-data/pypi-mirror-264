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
    parser.add_argument('--save_every', type=int, default=10,
                        help='specify save NN every <save_every> epochs')
    parser.add_argument('-btr', '--tr_batch_size', type=int, default=10,
                        help='specify (approximate) batch size for training')
    parser.add_argument('-lmo', '--load-model', action='store_true', default=False,
                        help='specify new model, do not load exising net0.pt, net1.pt, opt.pt')
    parser.add_argument('-lm', '--load_model_name', nargs='*', default=['comp.pt'],
                        help='Specify load model file name [Comp.pt] or the path of folders which contains model parameters [net_pars/]')
    parser.add_argument('-llr', '--load-lr', action='store_true', default=False,
                        help='load saved learninig rate. Only use if loading saved model, and even then not always')
    parser.add_argument('-o', '--optimizer', nargs='*', default=['Adam'],
                        help='Specify the optimizer type [SGD or Adam or AdamW]')
    parser.add_argument('--test-input-xid', nargs='*', default=None,
                        help='Specify test input data xyzid if the data type is sqlite [xid_tst.txt]')
    parser.add_argument('--tr-input-xid', nargs='*', default=None,
                        help='Specify training(and validation) input data xyzid if the data type is sqlite [xid_tr.txt]')
    parser.add_argument('--trtsid-name', nargs='*', default=['cut.txt'],
                        help='Specify training(and validation)/test input data xyzid with tvt mask [trid_trtst.txt]')
    parser.add_argument('-if', '--fidlevel', type=int, default=1,
                        help='Specify input fidelity level as integer [0, 1, 2, 3, 4] (SQLite db only)')
    parser.add_argument('-nl', '--my-neurons', nargs='+', type=int, default=None,
                        help='Specify set of the number of neurons in each layer. The last number is for the output layer (new model only)')
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
    parser.add_argument('--multi_fid', action='store_true', default=False,
                        help='Train to multiple fidelity levels')

    parser.add_argument('--present_elements', nargs='+', default=['C', 'H'],
                        help='Specify how many chemical elements are included in the training set')
    args = parser.parse_args()


    try:
        if args.lrscheduler[0] == 'None':
            args.lrscheduler = None
    except:
        pass
    return args


# ====================================================================================================


class Runner:
    def __init__(self, args, device, num_spec=2):
        args.num_species = num_spec
        self.model = prep.load_trained_model(args, load_opt=False)
        self.model.to(device)
        self.model.add_sae = True
        self.num_spec = num_spec
 
        self.device = device
        self.args = args


    def get_ids(self, aevs):
        ids=[[] for i in range(self.num_spec)]
        for mol in range(len(aevs)):
            for spec in range(self.num_spec):
                ids[spec] += [mol] * len(aevs[mol][spec])
        ids = [torch.tensor(ida).to(self.device) for ida in ids]
        return [ids]

    def eval_force(self, daevs):
        self.pred_forces = []
        for i in range(len(daevs)):
            force = daev_calc.cal_dEdxyz_ddp(self.aevs[i], -self.pred_engs[i], daevs[i], self.ids[i])
            self.pred_forces.append(force)
        return self.pred_forces

    def eval(self, aevs, daevs=[]):
        self.ids = self.get_ids(aevs)
        self.pred_engs = []
        self.pred_engs_lf = []
        self.aevs = aevs
        for i in range(len(aevs)):
            if self.args.multi_fid:
                eng_lf, eng = self.model(self.aevs[i], self.ids[i], 1, train=False)
                self.pred_engs_lf.append(eng_lf)
            else:
                eng = self.model(self.aevs[i], self.ids[i], 1, train=False)
            self.pred_engs.append(eng)
        return torch.cat(self.pred_engs)



class Trainer:
    def __init__(self, model, train_data, valid_data, test_data, keys, optimizer, lr_scheduler, sae_energies, save_every: int, fname: str, svpath:str, device, rank=0, force_train=False, num_spec=3):
        random.seed(0)
        torch.manual_seed(random.randrange(200000))
        np.random.seed(random.randrange(200000))
        random.seed(random.randrange(200000))
        self.device = device
        self.model = model
        self.train_data = train_data
        self.valid_data = valid_data
        self.test_data = test_data
        self.num_spec = num_spec
        self.keys = keys
        self.save_every = save_every
        self.FT=force_train
        self.optimizer = optimizer
        self.lr_scheduler = lr_scheduler
        self.sae_energies = sae_energies
        self.fname = fname
        self.svpath = svpath + '_' + 'device' + '_' + str(self.device) + '_' + str(rank)
        Path(self.svpath).mkdir(parents=True, exist_ok=True)
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
                    ss_spec = []
                    mol_count += 1
                    for spec in range(len(batch[mol])):
                        ss[spec][mol] = batch[mol][spec].to(self.device).requires_grad_()
                        if key == 'aevs':
                            id_spec[spec] += [mol] * len(batch[mol][spec])
                ss = [torch.cat(s) for s in ss]
                bitem = ss
                if key == 'aevs':
                    id_spec = [torch.tensor(spec).to(self.device) for spec in id_spec]
                    ids.append(id_spec)
                    nmols.append(mol_count)
            
            if key == 'forces' or key=='engs':
                bitem = torch.cat([item for item in batch]).to(self.device)
                if key == 'engs': 
                    bitem = bitem.unsqueeze(0).T
            if key == 'fdims':
                bitem = batch
            items.append(bitem)
        if key == 'aevs':
            return items, ids, nmols
        else:
            return items


    def _run_batch_tvs(self, tvs, aevs, ids, nmols, true_engs, true_forces=[], fdims=[], daevs=[]):

        if tvs == 'train':
            self.optimizer.zero_grad()
        pred_engs, log_sigma = self.model(aevs, ids, nmols)
        ediff = prep.energy_abs_dif(pred_engs, true_engs)
        fdiff=[]        #This is a placeholder for when not doing force training
        if self.FT:
            pred_forces = daev_calc.cal_dEdxyz_ddp(aevs, -pred_engs, daevs, ids)
            fdiff = prep.force_abs_dif(pred_forces, true_forces, fdims)
            print('HERE: ', pred_forces)
        if tvs == 'train':
            #print(fdiff)
            eloss, floss = prep.my_loss(ediff, fdiff, dEsq=1., dfsq=1., p=2)
            loss = self.model.mtl([eloss, floss], log_sigma)
            self.log_sigma = log_sigma
            loss.backward(retain_graph=True)
            loss.retain_grad()
            self.optimizer.step()
        return ediff, fdiff
    


    def _run_epoch(self, epoch, data, ids, nmols, tvs):
        bat_lst = list(range(len(data['engs'])))
        ediff = []
        fdiff = []
        for b in bat_lst:
            if self.FT:
                bediff, bfdiff = self._run_batch_tvs(tvs, data['aevs'][b], ids[b], nmols[b], data['engs'][b], data['forces'][b], data['fdims'][b], data['daevs'][b])
                fdiff += bfdiff
            else:
                bediff, bfdiff = self._run_batch_tvs(tvs, data['aevs'][b], ids[b], nmols[b], data['engs'][b])
            ediff += bediff
        ediff = torch.tensor(ediff)
        L1 = torch.mean(ediff)
        L2 = torch.sqrt(torch.mean(ediff**2))
        Linf = torch.max(ediff)
        self.openf.write(tvs + ' L1 loss: ' + str(kcpm(L1.item())) + '\n')
        self.openf.write(tvs + ' L2 loss: ' + str(kcpm(L2.item())) + '\n')
        self.openf.write(tvs + ' Linf loss: ' + str(kcpm(Linf.item())) + '\n')
        print('device ', self.device, ' ',tvs + ' MAE: ', kcpm(L1.item()))
        print('device ', self.device, ' ',tvs + ' RMSE: ', kcpm(L2.item()))
        print('device ', self.device, ' ',tvs + ' Linf: ', kcpm(Linf.item()))
        if self.FT:
            fdiff = torch.cat(fdiff)
            fL1 = torch.mean(fdiff)
            fL2 = torch.sqrt(torch.mean(fdiff**2))
            fLinf = torch.max(fdiff)
            self.openf.write(tvs + ' fL1 loss: ' + str(kcpm(fL1.item())) + '\n')
            self.openf.write(tvs + ' fL2 loss: ' + str(kcpm(fL2.item())) + '\n')
            self.openf.write(tvs + ' fLinf loss: ' + str(kcpm(fLinf.item())) + '\n')
            print('device ', self.device, ' ',tvs + ' FMAE: ', kcpm(fL1.item()))
            print('device ', self.device, ' ',tvs + ' FRMSE: ', kcpm(fL2.item()))
            print('device ', self.device, ' ',tvs + ' FLinf: ', kcpm(fLinf.item()))
            self.openf.write('log_sigma: ')
            for task in range(len(self.log_sigma)):
                self.openf.write(str(self.log_sigma[task].item())+' ')
        self.openf.write('\n')
        if tvs == 'valid':
            self.lr_scheduler.step(kcpm(L2))



    def train(self, max_epochs: int):
        tr0 = time.time()
        random.seed(0)
        torch.manual_seed(random.randrange(200000))
        np.random.seed(random.randrange(200000))
        random.seed(random.randrange(200000))
        self.openf.write('Initial parameters for device: '+ str(self.device) + '\n')
        for name, param in self.model.named_parameters():
            if param.requires_grad:
                self.openf.write(name + ': ' + str(param.data) + '\n')
        
        print('self.keys: ', self.keys)
        train_dict = {} 
        valid_dict = {}
        test_dict = {}

        for i in range(len(self.keys)):
            if self.keys[i] == 'aevs':
                train_dict[self.keys[i]], tr_ids, tr_nmols = self.cat_data(self.train_data, self.keys[i], i)
                valid_dict[self.keys[i]], vl_ids, vl_nmols = self.cat_data(self.valid_data, self.keys[i], i)
                test_dict[self.keys[i]], ts_ids, ts_nmols = self.cat_data(self.test_data, self.keys[i], i)
            else:
                train_dict[self.keys[i]] = self.cat_data(self.train_data, self.keys[i], i)
                valid_dict[self.keys[i]] = self.cat_data(self.valid_data, self.keys[i], i)
                test_dict[self.keys[i]] = self.cat_data(self.test_data, self.keys[i], i)


        for epoch in range(max_epochs):
            print('\ndevice ', self.device,' epoch: ', epoch)
            self.openf.write('\nepoch: ' + str(epoch) + '\n')
            self._run_epoch(epoch, train_dict, tr_ids, tr_nmols, tvs='train')
            self._run_epoch(epoch, valid_dict, vl_ids, vl_nmols, tvs='valid')
            if self.device == 0 or self.device == 'cpu':
                self._run_epoch(epoch, test_dict, ts_ids, ts_nmols, tvs='test')
            
            if self.device == 'cpu' and (epoch % self.save_every == 0 or epoch  + 1 == max_epochs):
                self.save_cpu('ddp_model', epoch, self.optimizer)
            if self.device == 0 and (epoch % self.save_every == 0 or epoch  + 1 == max_epochs): 
                self.save_ddp('ddp_model', epoch, self.optimizer)

        print('device Number ', self.device, 'is DONE!!!')
        self.openf.write('Final parameters for gpu: ' +  str(self.device) + '\n')
        for name, param in self.model.named_parameters():
            if param.requires_grad:
                self.openf.write(name + ': ' + str(param.data) + '\n')
        
        tr1 = time.time()
        self.openf.write('Training time: ' + str(tr1-tr0))
        self.openf.close()



# ====================================================================================================
def spawned_trainer(rank:int, args, world_size:int):
    # set default pytorch as double precision
    print('rank: ', rank)
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
    fname = args.savenm + '_gpu_' + str(rank) + '.log'
    print('about to load train objects!')
    save_path = args.savenm + '_seeds_'+str(seeds[0])+'_'+str(seeds[1])
    torch.autograd.set_detect_anomaly(True)
    train_set, valid_set, test_set, model, optimizer, lr_scheduler, sae_energies, keys = prep.load_train_objs(args, fid=args.fidlevel)
    prep.set_up_task_weights(model, args, optimizer)
    device = rank
    if args.ddp:
        model = DDP(model.to(device), device_ids=[device], find_unused_parameters=True)
        model.mtl = model.module.mtl
    else:
        model = model.to(device)
    trainer = Trainer(model, train_set, valid_set, test_set, keys, optimizer, lr_scheduler, sae_energies, args.save_every, fname, save_path, device, force_train=args.floss, num_spec = args.num_species) 
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
        print('HERE WE ARE')
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
    main(args)



